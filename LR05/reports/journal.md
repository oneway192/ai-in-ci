# Журнал выполнения ЛР05

## Фиксация до запуска

**Дата и время фиксации гипотезы:** 20.10.2026 19:30.

- Variant: 7.
- Brief: 2 — обложка подкаста о городской среде.
- Condition: `repeat` — повтор запуска в том же сеансе.
- Seed: 1007.

**Гипотеза:** при неизменной среде, одинаковом prompt, seed 1007 и свежем CPU `Generator` для каждого вызова A и B совпадут побитово.

**Допуск:**

- `identical` — побитовое равенство пикселей;
- `close` — пиксели различаются, но PSNR ≥ 40 dB;
- `different` — PSNR < 40 dB.

## Фактическая среда

- Google Colab.
- GPU: Tesla T4.
- Python: 3.13.15.
- torch: 2.11.0+cu130.
- diffusers: 0.41.0.
- transformers: 5.20.1.
- Pillow: 11.3.0.
- Platform: `Linux-6.6.122+-x86_64-with-glibc2.39`.
- CUDA available: `True`.
- Model: `stabilityai/sd-turbo`.
- Revision: `b261bac6fd2cf515557d5d0707481eafa0485ec2`.
- Parameters: steps 1, guidance scale 0.0, 512×512, `float16`, CPU `Generator`.

## Времена

- Загрузка модели: 26.77 s.
- Прогрев: 5.62 s.
- Базовая генерация: 0.36 s.
- Генерация пары A/B: 0.66 s.

## Базовый запуск

SHA-256 `artifacts/run_001/result.png`:

`96b809ceb59215db2a042f58ec1bdf68d336f5b6797a415f70790495fadb6efb`

## Основной эксперимент A/B

- SHA-256 A: `96b809ceb59215db2a042f58ec1bdf68d336f5b6797a415f70790495fadb6efb`.
- SHA-256 B: `96b809ceb59215db2a042f58ec1bdf68d336f5b6797a415f70790495fadb6efb`.
- `pixel_equal = true`.
- `max_diff = 0`.
- PSNR = `inf`.
- `verdict = identical`.
- `visual_check = true`; слои силуэта города читаются как отдельные полосы.

Гипотеза подтверждена в пределах текущей зафиксированной Colab-сессии.

## Намеренная ошибка

Description: `one shared CPU Generator object passed to two consecutive calls`.

- First SHA-256: `96b809ceb59215db2a042f58ec1bdf68d336f5b6797a415f70790495fadb6efb`.
- Second SHA-256: `2c1de397892ed86b7ae10074c54b73f745c2a5e455f918fafe13349c159b55cd`.
- `pixel_equal = false`.
- `max_diff = 255`.
- PSNR = 9.035864314461799 dB.
- Diagnosis: `Generator state advances after the first call`.
- Fix: создавать новый `torch.Generator(device="cpu").manual_seed(seed)` для каждого вызова.

Повторное использование одного объекта `Generator` изменило второй результат, потому что состояние генератора продвинулось после первого вызова.

## Итог

**PASS.** Обязательные файлы сохранены, манифесты и хеши согласованы, паспорт имеет статус `COMPLETE`.
