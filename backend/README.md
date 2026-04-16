# Backend Setup

## 1) Configure env

`backend/.env` already exists for local development. Adjust values if needed.

## 2) Install dependencies

Use a Python distribution that supports binary wheels for `pyodbc` and `bcrypt`.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 3) Run migrations

```bash
flask --app run.py db upgrade
```

## 4) Seed admin user

```bash
flask --app run.py seed-admin --username admin --password "Admin@123456"
```

## 5) Start API

```bash
python run.py
```

API base URL: `http://127.0.0.1:5000`
