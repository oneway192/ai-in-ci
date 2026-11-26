# ЛР №11. Базовая GAN

**Вариант 7** — синтетические сцены «диск и прямоугольник» (`disc_rect`). В режимах A и B меняется размерность шума с 32 до 8. Для обоих режимов используются одни и те же обучающие и тестовые данные, пять seed и 1500 шагов.

Основная серия выполнена в Google Colab на CPU с Python 3.13.18 и PyTorch 2.14.1+cpu. Смена размерности дала +0,0028 дБ по nn_psnr, −0,0012 по coverage и +0,0045 по diversity. Все изменения в пределах практических допусков, критерий 2s не сработал. Средние по качеству согласуются с контрольными числами Engee в пределах 2s.

[Выполненный ноутбук Colab](https://colab.research.google.com/drive/1ZH67calfZqfAlxTfbBTGIPoqfkmo-YbR) содержит листы и график. В отдельном сеансе все три метрики качества совпали по каждому seed и режиму с сохранённой точностью. [Ноутбук повторения](https://colab.research.google.com/drive/10lnT8sTzH8ta6fUyEaY5nq13s38d1IUb) · [ZIP](artifacts/lr11_repeat.zip) · [Сверка](artifacts/repeat_session/repeat_check.json).

## Как повторить

1. Открыть [lab11.ipynb](lab11.ipynb) в Google Colab со стандартной средой CPU и выполнить все ячейки. Сохранённые выходы в локальной копии восстановлены из проверенного ZIP. При выполнении ноутбук сам записывает и проверяет библиотеки. Используются предустановленные PyTorch, NumPy, Pillow и Matplotlib. Версии сопоставляются с указанными в методичке в отчёте.
2. Проверить на выходных листах динамику обучения, форму и положение объектов, заметность прямоугольника и повторы. Вписать наблюдения в `VISUAL_CHECK` и повторить две последние ячейки для итогового архива.
3. Для отдельной проверки воспроизводимости в новом сеансе задать `OUT = WORK / "repeat_session"` в первой ячейке и `RUN_DEMO = False` в ячейке обучения. Сравнить средние, разброс и классификацию по допускам. Время сравнивается между A и B внутри одного сеанса.

| Материал | Где находится |
| --- | --- |
| Контрольные значения Engee | [Конфигурация](configs/run_config.json) и [сверка](artifacts/engee_comparison.json) |
| Учебные библиотеки и протокол | [src/](src/), [configs/run_config.json](configs/run_config.json) |
| Гипотеза, допуски и план | [reports/journal.md](reports/journal.md) |
| Результаты собственного прогона | [По seed](artifacts/per_seed_metrics.csv), [сводка](artifacts/metrics.json), [сверка с Engee](artifacts/engee_comparison.json), [визуальная проверка](artifacts/visual_check.json), [метрики снимков](artifacts/checkpoint_metrics.csv) |
| Материалы повтора | [Полный ZIP](artifacts/lr11_repeat.zip), [паспорт](artifacts/repeat_session/passport.json), [сверка](artifacts/repeat_session/repeat_check.json), [график](artifacts/repeat_session/training_curves.png) |
| Отчёт и защита | [PDF](reports/report.pdf), [DOCX](reports/report.docx), [Markdown](reports/report.md), [фактическая среда](reports/environment.txt), [вопросы к защите](reports/defense.md) |

Демонстрационный вариант 1 воспроизводится на seed 101 для сверки динамики обучения. Вариант 7 выполняется на всех пяти seed. Метрики качества сверяются с контрольным прогоном Engee с учётом разброса.
