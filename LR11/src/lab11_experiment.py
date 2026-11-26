"""Протокол ЛР11 поверх исходных библиотек из учебного комплекта."""
import csv
import hashlib
import json
import math
import os
import platform
import time
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
import numpy as np
import PIL
import torch
from PIL import Image, ImageDraw

import lab11_lib as L


def write_json(path, data):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def save_sheet(path, images, labels, columns=8):
    tile = 64
    label_height = 22
    rows = math.ceil(len(images) / columns)
    sheet = Image.new("RGB", (columns * tile, rows * (tile + label_height)), "white")
    draw = ImageDraw.Draw(sheet)
    for i, (pixels, label) in enumerate(zip(images, labels, strict=True)):
        row, column = divmod(i, columns)
        x, y = column * tile, row * (tile + label_height)
        image = Image.fromarray(pixels).resize((tile, tile), Image.Resampling.NEAREST)
        sheet.paste(image, (x, y))
        draw.text((x + 4, y + tile + 2), label, fill="#17202a")
    sheet.save(path)


def loss_plot(path, records):
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(11, 6), sharex=True)
    for axis, key, title in zip(
        axes.flat, ("lg", "ld", "d_real", "d_fake"),
        ("Потеря G", "Потеря D", "D на реальных", "D на сгенерированных"), strict=True,
    ):
        for mode, record in records.items():
            values = record["history"][key]
            axis.plot(range(1, record["config"]["steps"] + 1, 10), values, label=mode)
        axis.set_title(title)
        axis.set_xlabel("Шаг обучения")
        axis.grid(alpha=0.25)
        axis.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=135)
    plt.close(fig)


def fit(kind, config, seed, folder, mode, settings, snapshots=()):
    path = folder / f"{mode}_{seed}.json"
    if path.exists():
        return json.loads(path.read_text())
    train, _, _, _ = L.L.dataset(kind)
    started_at = datetime.now(timezone.utc).isoformat()
    saved = {}
    callback_seconds = 0.0

    def snapshot(step, generator):
        nonlocal callback_seconds
        started = time.perf_counter()
        saved[step] = deepcopy(generator)
        callback_seconds += time.perf_counter() - started

    started = time.perf_counter()
    generator, history = L.train_gan(train[:config["n_train"]], config, seed, snapshots, snapshot)
    seconds = time.perf_counter() - started - callback_seconds
    metrics = L.metrics(deepcopy(generator), kind, seed)
    metrics["seconds"] = seconds
    checkpoints = {}
    for step, model in saved.items():
        checkpoints[str(step)] = L.metrics(deepcopy(model), kind, seed)
        images = L.sample(model, settings["samples_per_mode"], settings["sample_seed"])
        images = images.mul(255).round().byte().permute(0, 2, 3, 1).numpy()
        save_sheet(folder / f"{mode}_{seed}_step_{step:04}.png", images,
                   [f"{mode} {i + 1:02d}" for i in range(len(images))])
    record = dict(mode=mode, seed=seed, config=config, started_at=started_at,
                  metrics=metrics, checkpoints=checkpoints, history=history)
    write_json(path, record)
    print(f"{folder.name} {mode} seed {seed}: {seconds:.1f} с", flush=True)
    return record


def run(out, settings, source_dir, *, demo=True):
    out.mkdir(parents=True, exist_ok=True)
    assert L.DEVICE == "cpu", "Выберите CPU в настройках среды Colab."
    kind, a, b = L.variant_settings(settings["variant"])
    assert {key for key in a if a[key] != b[key]} == {"z"}
    assert list(L.SEEDS) == settings["seeds"] and a["steps"] == settings["snapshots"][-1]
    environment = {
        "runtime": "Google Colab CPU" if "COLAB_RELEASE_TAG" in os.environ else "CPU",
        "colab_release_tag": os.environ.get("COLAB_RELEASE_TAG"),
        "python": platform.python_version(), "platform": platform.platform(),
        "torch": str(torch.__version__), "torch_cuda_build": torch.version.cuda,
        "numpy": np.__version__, "pillow": PIL.__version__,
        "matplotlib": matplotlib.__version__, "device": L.DEVICE,
        "available_cpus": len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else os.cpu_count(),
        "torch_threads": torch.get_num_threads(), "torch_interop_threads": torch.get_num_interop_threads(),
        "sources_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in sorted(source_dir.glob("*.py"))},
    }
    protocol = dict(settings=settings, kind=kind, configs={"A": a, "B": b}, environment=environment,
                    demo=demo, dataset_seed=7, n_eval=L.N_EVAL, coverage_k=L.K_COVER)
    protocol_path = out / "protocol.json"
    if protocol_path.exists() and json.loads(protocol_path.read_text()) != protocol:
        raise ValueError("Среда или протокол изменились. Выберите новый каталог запуска.")
    write_json(protocol_path, protocol)
    print(json.dumps(environment, ensure_ascii=False, indent=2), flush=True)

    folder = out / "variant07"
    folder.mkdir(exist_ok=True)
    records = []
    for seed in settings["seeds"]:
        for mode, cfg in (("A", a), ("B", b)):
            snapshots = settings["snapshots"] if seed == 101 else ()
            records.append(fit(kind, cfg, seed, folder, mode, settings, snapshots))

    samples = {r["mode"]: r for r in records if r["seed"] == 101}
    loss_plot(out / "training_curves.png", samples)
    _, test, _, _ = L.L.dataset(kind)
    real = test[:32].mul(255).round().byte().permute(0, 2, 3, 1).numpy()
    save_sheet(out / "real_test.png", real, [f"Real {i + 1:02d}" for i in range(len(real))])

    values = {
        mode: {key: [r["metrics"][key] for r in records if r["mode"] == mode] for key in L.METRICS}
        for mode in ("A", "B")
    }
    with (out / "per_seed_metrics.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["seed", "mode", *L.METRICS])
        writer.writeheader()
        for record in records:
            writer.writerow(dict(seed=record["seed"], mode=record["mode"], **record["metrics"]))
    rows = []
    reference = {}
    for key, mean_a, spread, mean_b, delta, ratio, exceeds_2s in L.summarize(values["A"], values["B"]):
        tolerance = settings["tolerances"].get(key)
        rows.append(dict(metric=key, A=mean_a, s_A=spread, B=mean_b, delta=delta,
                         abs_delta_over_s=ratio if math.isfinite(ratio) else None, exceeds_2s=exceeds_2s,
                         tolerance=tolerance, exceeds_tolerance=abs(delta) > tolerance if tolerance is not None else None))
        if key in settings["engee_reference"]:
            ref = settings["engee_reference"][key]
            reference[key] = {mode: dict(delta=mean - ref[mode], within_2s=abs(mean - ref[mode]) <= 2 * ref["s_A"])
                              for mode, mean in (("A", mean_a), ("B", mean_b))}
    write_json(out / "metrics.json", rows)
    write_json(out / "engee_comparison.json", reference)

    errors = {
        "one_seed": {"seed101_delta": {key: values["B"][key][0] - values["A"][key][0] for key in L.METRICS},
                     "five_seed_delta": {row["metric"]: row["delta"] for row in rows}},
        "loss_as_quality": {mode: dict(mean_last_10_lg=float(np.mean(r["history"]["lg"][-10:])),
                                       final_metrics=r["metrics"]) for mode, r in samples.items()},
        "unequal_steps": {mode: {step: r["checkpoints"][step] for step in ("700", "1500")}
                          for mode, r in samples.items()},
    }
    write_json(out / "intentional_errors.json", errors)

    if demo:
        folder = out / "demo01"
        folder.mkdir(exist_ok=True)
        demo_kind, demo_a, demo_b = L.variant_settings(settings["demo_variant"])
        for mode, cfg in (("A", demo_a), ("B", demo_b)):
            fit(demo_kind, cfg, 101, folder, mode, settings, settings["snapshots"])

    write_json(out / "passport.json", dict(**protocol, finished_at=datetime.now(timezone.utc).isoformat(),
                                          trainings_variant=len(records), trainings_demo=2 if demo else 0,
                                          status="AWAITING_VISUAL_REVIEW"))
    return rows
