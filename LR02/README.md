# ЛР02 — вариант 7

Сценарий: обложки подкастов с публикацией в сети и монетизацией. Профиль дефектов: материалы с условием NonCommercial.

## Основные материалы

- [Основной отчёт](reports/report.md)
- [Команды и коды возврата](reports/commands.md)
- [Журнал выполнения](reports/journal.md)
- [Отчёт аудита](artifacts/v07/audit_report.md)
- [JSON с фактическими находками](artifacts/v07/audit_report.json)
- [Паспорт набора данных](artifacts/v07/data_card_draft.md)
- [Карточка модели](artifacts/model_card.md)
- [Реестр рисков](artifacts/risk_register.csv)
- [Ранжирование рисков](artifacts/risk_ranking.md)

## Минимальная последовательность воспроизведения

Команды выполняются из `D:\dev\ai-in-ci\LR02` в свежей копии рабочей папки. Повторный аудит перезаписывает автоматически создаваемые Markdown-файлы, поэтому заполненные версии нужно предварительно сохранить или выполнять проверку в копии.

```powershell
..\LR01\.venv\Scripts\python.exe --version
..\LR01\.venv\Scripts\python.exe src\lab02_make_variant.py --variant 7 --out artifacts\v07
..\LR01\.venv\Scripts\python.exe src\lab02_audit.py --manifest artifacts\v07\manifest.csv --policy artifacts\v07\policy.json --out artifacts\v07
..\LR01\.venv\Scripts\python.exe src\lab02_model_card.py --passport ..\LR01\artifacts\v07\passport.json --out artifacts\model_card.md --code-license MIT --owner "Провков Иван Александрович"
..\LR01\.venv\Scripts\python.exe src\lab02_risks.py --csv artifacts\risk_register.csv --out artifacts\risk_ranking.md
```

Ожидаемые фактические результаты текущего выполнения зафиксированы в `reports/logs/`: Python 3.12.0; аудит — 12 объектов, 4 ошибки и 1 предупреждение; проверка реестра — `RESULT: PASS`. Эти значения не следует переносить в другое выполнение без проверки его stdout.

Шаблон реестра уже сохранён отдельно как `artifacts/risk_register.template.csv`. Команду `--template` не следует запускать поверх заполненного `artifacts/risk_register.csv`.
