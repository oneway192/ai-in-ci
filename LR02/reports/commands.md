# Команды ЛР02

Все команды выполняются из каталога `D:\dev\ai-in-ci\LR02` с интерпретатором среды ЛР01 `..\LR01\.venv\Scripts\python.exe`.

Основные stdout-логи сохранены в UTF-8. Логи первоначальных запусков, которые Windows создала в Windows-1251, после выполнения были механически перекодированы в UTF-8 без изменения текста. Повреждённый диагностический stdout первой попытки повторной генерации карточки сохранён отдельно и не используется как основной результат.

## Проверка среды

```powershell
..\LR01\.venv\Scripts\python.exe --version
```

Код возврата: `0`. Stdout: `reports\logs\python_version.stdout.txt`. Stderr: `reports\logs\python_version.stderr.txt`.

## Создание варианта

```powershell
..\LR01\.venv\Scripts\python.exe src\lab02_make_variant.py --variant 7 --out artifacts\v07
```

Код возврата: `0`. Stdout: `reports\logs\make_variant.stdout.txt`. Stderr: `reports\logs\make_variant.stderr.txt`.

## Аудит

```powershell
..\LR01\.venv\Scripts\python.exe src\lab02_audit.py --manifest artifacts\v07\manifest.csv --policy artifacts\v07\policy.json --out artifacts\v07
```

Код возврата: `0`. Stdout: `reports\logs\audit.stdout.txt`. Stderr: `reports\logs\audit.stderr.txt`.

## Первоначальная генерация карточки модели

```powershell
..\LR01\.venv\Scripts\python.exe src\lab02_model_card.py --passport ..\LR01\artifacts\v07\passport.json --out artifacts\model_card.md
```

Код возврата: `0`. Stdout: `reports\logs\model_card.stdout.txt`. Stderr: `reports\logs\model_card.stderr.txt`.

При этом запуске исходный паспорт ЛР01 не содержал лицензию кода и ответственного, поэтому в карточке были отмечены пробелы.

## Повторная генерация карточки после назначения лицензии и ответственного

```powershell
$env:PYTHONUTF8 = "1"
..\LR01\.venv\Scripts\python.exe src\lab02_model_card.py --passport ..\LR01\artifacts\v07\passport.json --out artifacts\model_card.md --code-license MIT --owner "Провков Иван Александрович"
```

Код возврата: `0`. Stdout: `reports\logs\model_card_assigned.stdout.txt`. Stderr: `reports\logs\model_card_assigned.stderr.txt`.

Перед финальным логированием та же команда один раз завершилась с кодом `0`, но перенаправление PowerShell заменило кириллицу stdout символами замены. Диагностический лог сохранён как `reports\logs\model_card_assigned.first_attempt.stdout.txt`, stderr — как `reports\logs\model_card_assigned.first_attempt.stderr.txt`. Затем команда повторена с `PYTHONUTF8=1`; основной stdout сохранён в корректной UTF-8 кодировке.

## Шаблон реестра рисков

```powershell
..\LR01\.venv\Scripts\python.exe src\lab02_risks.py --template artifacts\risk_register.csv
```

Код возврата: `0`. Stdout: `reports\logs\risk_template.stdout.txt`. Stderr: `reports\logs\risk_template.stderr.txt`.

## Проверка и ранжирование реестра

```powershell
..\LR01\.venv\Scripts\python.exe src\lab02_risks.py --csv artifacts\risk_register.csv --out artifacts\risk_ranking.md
```

Код возврата: `0`. Stdout: `reports\logs\risk_check.stdout.txt`. Stderr: `reports\logs\risk_check.stderr.txt`. Фактический итог: `RESULT: PASS`.
