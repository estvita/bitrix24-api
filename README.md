# bitrix24-api
Парсер документации по API битрикс24 для генерации swagger.yaml


## Запуск

```
git clone https://github.com/estvita/bitrix24-api.git
cd bitrix24-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
<!-- Склонировать в жту же папку репозиторий б24 -->
git clone https://github.com/bitrix-tools/b24-rest-docs.git
<!-- заупустить парсер -->
python parser.py
```