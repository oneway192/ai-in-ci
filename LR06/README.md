# ЛР №6. Исследование параметров text-to-image генерации

**Вариант 7:** бриф №2 — обложка подкаста о городской среде; фактор №1 — число шагов, 1 → 4; seed 101…105.

Цель работы — изменить один параметр генерации при неизменных остальных условиях, измерить отклик по четырём метрикам на серии из пяти seed и сделать вывод с учётом заранее записанного допуска.

| Параметр | Фактическое значение |
| --- | --- |
| Модель | `stabilityai/sd-turbo` @ `b261bac6fd2cf515557d5d0707481eafa0485ec2` |
| Метрика сходства | `openai/clip-vit-base-patch32` @ `3d74acf9a28c67741b2f4f2ea7635f0aaf6f0268` |
| Режимы | A: 1 шаг; B: 4 шага; оба — 512×512, `guidance_scale = 0.0`, `float16`, CPU `Generator` |
| Среда | Google Colab, Tesla T4, Python 3.13.16 |
| Библиотеки | torch 2.11.0+cu130; diffusers 0.41.0; transformers 5.20.2; Pillow 11.3.0 |
| Итог | гипотеза подтверждена частично; рост времени не окупается |

## Результат

| Метрика | A (1 шаг) | s | B (4 шага) | Δ | \|Δ\|/s | 2s | Класс по допуску |
| --- | ---: | ---: | ---: | ---: | ---: | :---: | --- |
| сходство CLIP | 34.0965 | 1.8301 | 32.6521 | −1.4444 | 0.79 | нет | ухудшение (±1.0) |
| энергия границ | 0.0417 | 0.0126 | 0.0653 | +0.0237 (+56.8 %) | 1.87 | нет | ухудшение (±10 %) |
| контраст | 0.1673 | 0.0159 | 0.2463 | +0.0790 (+47.2 %) | 4.98 | да | улучшение (±10 %) |
| время, с | 0.3290 | 0.0154 | 0.5894 | +0.2605 (+79.2 %) | 16.92 | да | ухудшение (±20 %) |

![Сравнительный лист seed 101: A слева, B справа](artifacts/comparison.png)

- Четыре шага сделали изображения площе и резче, но слои силуэта как полосы не появились (seed 101 — нет на A и B), а палитра ушла от брифа.
- Для CLIP и энергии границ критерий 2s и допуск дают разный ответ: эффект за пределами допуска, но меньше разброса между seed.
- Демонстрационный вариант 1 воспроизведён: энергия границ совпала с методичкой, CLIP и контраст — до 0.002.
- Намеренная ошибка: при `guidance_scale = 1.0` изображение совпало с `0.0` бит в бит, CFG выключен; при 3.0 CFG включён, PSNR = 10.89 дБ.

## Как повторить

1. Открыть [lab06.ipynb](lab06.ipynb) в Google Colab и выбрать среду «Графический процессор T4».
2. Выполнить ячейки сверху вниз. Первая ячейка удаляет `torchao`, несовместимый с `diffusers` в текущем образе Colab. Если `diffusers` уже импортировался в сеансе, сеанс нужно перезапустить.
3. Ноутбук сам записывает библиотеки из `src/` ячейками `%%writefile` и сверяет их SHA-256, выполняет демо-вариант и вариант 7 и сохраняет `artifacts/` и `reports/environment.txt`.
4. После просмотра изображений заполнить `VISUAL_CHECK` и выполнить ячейки до конца; последняя скачивает `lab06_results.zip`.
5. Сверить версии с [reports/environment.txt](reports/environment.txt). CLIP, энергия границ, контраст и SHA-256 изображений должны совпасть при тех же версиях; время зависит от состояния GPU.

## Что где лежит

| Файл или каталог | Содержание |
| --- | --- |
| [lab06.ipynb](lab06.ipynb) | выполненный notebook с outputs |
| [src/](src/) | `lab05_lib.py`, `lab06_lib.py`, `lab06_demo.py` из комплекта преподавателя без изменений |
| [configs/run_config.json](configs/run_config.json) | параметры варианта, допуски и направления классификации |
| [artifacts/metrics.json](artifacts/metrics.json) | таблица метрик `variant_summary` |
| [artifacts/per_seed_metrics.csv](artifacts/per_seed_metrics.csv) | значения по каждому seed и SHA-256 изображений |
| [artifacts/classification.json](artifacts/classification.json) | классификация по допуску, сравнение с 2s, чувствительность |
| [artifacts/comparison.png](artifacts/comparison.png) | сравнительный лист seed 101 |
| [artifacts/comparison_all_seeds.png](artifacts/comparison_all_seeds.png) | лист всех пяти seed |
| [artifacts/seed101_A.png](artifacts/seed101_A.png), [artifacts/seed101_B.png](artifacts/seed101_B.png) | изображения seed 101 в полном размере |
| [artifacts/intentional_error.json](artifacts/intentional_error.json) | намеренная ошибка с `guidance_scale = 1.0` |
| [artifacts/demo/demo_variant01.json](artifacts/demo/demo_variant01.json) | воспроизведение демо-варианта и сверка с методичкой |
| [artifacts/passport.json](artifacts/passport.json) | паспорт эксперимента со статусом `COMPLETE` |
| [reports/report.md](reports/report.md) | полный отчёт; [PDF](reports/report.pdf) и [DOCX](reports/report.docx) — для сдачи |
| [reports/journal.md](reports/journal.md) | журнал: гипотеза до запуска, прогоны, результаты |
| [reports/environment.txt](reports/environment.txt) | фактическая среда |
| [reports/torchao_import_error.log](reports/torchao_import_error.log) | ошибка импорта `diffusers` и её исправление |
| [reports/defense.md](reports/defense.md) | ответы на контрольные вопросы |
