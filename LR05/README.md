# ЛР №5. Запуск открытой модели text-to-image

**Вариант 7:** бриф №2 — обложка подкаста о городской среде; условие `repeat`; seed 1007.

Цель работы — запустить закреплённую ревизию открытой модели, сохранить результат и проверить повторяемость двух запусков в пределах одной Google Colab-сессии.

| Параметр | Фактическое значение |
| --- | --- |
| Модель | `stabilityai/sd-turbo` |
| Ревизия | `b261bac6fd2cf515557d5d0707481eafa0485ec2` |
| Генерация | 1 шаг, `guidance_scale = 0.0`, 512×512, `float16` |
| Генератор | свежий CPU `Generator` для каждого запуска |
| Среда | Google Colab, Tesla T4, Python 3.13.15 |
| Библиотеки | torch 2.11.0+cu130; diffusers 0.41.0; transformers 5.20.1; Pillow 11.3.0 |
| Результат A/B | `identical`, PSNR = `inf` |

## Результат

![Результат варианта 7](artifacts/run_001/result.png)

- SHA-256 A и B одинаков: `96b809ceb59215db2a042f58ec1bdf68d336f5b6797a415f70790495fadb6efb`.
- `pixel_equal = true`, `max_diff = 0`, `visual_check = true`.
- При намеренном повторном использовании общего `Generator` изображения различились: PSNR = 9.035864314461799 dB (≈ 9.04 dB).
- Вывод о побитовом совпадении относится только к зафиксированной Colab-сессии.

## Как повторить

1. Открыть [lab05.ipynb](lab05.ipynb) в Google Colab.
2. Выбрать GPU-среду выполнения (для фактического запуска использована Tesla T4).
3. Выполнить ячейки сверху вниз. Notebook сам записывает точную библиотеку `lab05_lib.py`, загружает и прогревает модель, создаёт изображения и сохраняет артефакты.
4. После выполнения сохранить notebook с outputs и созданные каталоги `artifacts/` и `reports/`.
5. Сверить фактические версии с [reports/environment.txt](reports/environment.txt); при новом запуске заново зафиксировать среду, времена и хеши.

## Что где лежит

| Файл или каталог | Содержание |
| --- | --- |
| [lab05.ipynb](lab05.ipynb) | выполненный notebook с outputs |
| [src/lab05_lib.py](src/lab05_lib.py) | неизменённая библиотека из комплекта преподавателя |
| [configs/run_config.json](configs/run_config.json) | параметры варианта |
| [artifacts/run_001/](artifacts/run_001/) | baseline PNG и manifest |
| [artifacts/pair_A/](artifacts/pair_A/) | изображение A и manifest |
| [artifacts/pair_B/](artifacts/pair_B/) | изображение B и manifest |
| [artifacts/comparison.json](artifacts/comparison.json) | сравнение A/B |
| [artifacts/intentional_error.json](artifacts/intentional_error.json) | результат намеренной ошибки |
| [artifacts/passport.json](artifacts/passport.json) | паспорт эксперимента со статусом `COMPLETE` |
| [reports/report.md](reports/report.md) | полный отчёт |
| [reports/journal.md](reports/journal.md) | журнал выполнения |
| [reports/environment.txt](reports/environment.txt) | фактическая среда |
| [reports/defense.md](reports/defense.md) | ответы для защиты |
