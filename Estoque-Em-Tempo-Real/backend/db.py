import pyodbc
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover - fallback for Python <3.11
    import tomli as tomllib

SECRETS_PATH = Path(__file__).resolve().parent / "secrets.toml"


def load_secrets():
    if not SECRETS_PATH.exists():
        raise FileNotFoundError(f"Arquivo de credenciais nao encontrado em {SECRETS_PATH}")
    with SECRETS_PATH.open("rb") as f:
        return tomllib.load(f)


def build_connection_string(secrets=None):
    if secrets is None:
        secrets = load_secrets()
    sql = secrets["sql_server"]
    encrypt = sql.get("encrypt", "no")
    trust_cert = sql.get("trust_server_certificate", "no")
    return (
        f"DRIVER={{{sql['driver']}}};"
        f"SERVER={sql['server']};"
        f"DATABASE={sql['database']};"
        f"UID={sql['username']};"
        f"PWD={sql['password']};"
        f"Encrypt={encrypt};"
        f"TrustServerCertificate={trust_cert}"
    )


def connect(connection_string):
    return pyodbc.connect(connection_string)
