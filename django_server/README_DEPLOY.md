# Deploy no Render

## O que subir para o GitHub

Suba a pasta `django_server` e o arquivo `render.yaml` da raiz do projeto.

Nao suba:

- `django_server/.env`
- `work/`
- `.venv/`

Esses itens ja estao no `.gitignore`.

## Variaveis no Render

No painel do Render, confira ou crie estas variaveis:

- `GOOGLE_SHEETS_API_KEY`
- `LEC_CURRENT_SHEET_ID`
- `DASHBOARD_USERNAME`
- `DASHBOARD_PASSWORD`
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=0`
- `DJANGO_ALLOWED_HOSTS=.onrender.com`

## Comandos

Build Command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

Start Command:

```bash
gunicorn lec_dashboard.wsgi:application
```

## Teste local

```bash
python manage.py runserver
```

Depois acesse:

```text
http://127.0.0.1:8000
```
