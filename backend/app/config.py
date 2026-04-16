import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")


def _build_sqlalchemy_uri():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "1433")
    database = os.getenv("DB_NAME", "access_system")
    user = os.getenv("DB_USER", "sa")
    password = os.getenv("DB_PASSWORD", "")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
    trust_cert = os.getenv("DB_TRUST_CERT", "yes")

    user_quoted = quote_plus(user)
    password_quoted = quote_plus(password)
    driver_quoted = quote_plus(driver)

    return (
        f"mssql+pyodbc://{user_quoted}:{password_quoted}@{host}:{port}/{database}"
        f"?driver={driver_quoted}&TrustServerCertificate={trust_cert}"
    )


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
    SQLALCHEMY_DATABASE_URI = _build_sqlalchemy_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv("FRONTEND_ORIGIN", "http://127.0.0.1:5500").split(",")
        if origin.strip()
    ]
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin@123456")
