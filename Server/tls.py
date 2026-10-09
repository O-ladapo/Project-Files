import os
import ssl
import sys
from functools import lru_cache
from pathlib import Path


SERVER_CERT_ENV = "GAME_TLS_CERTFILE"
LOCAL_ENV_FILE_NAME = ".env"


def _configured_certificate():
    certfile = os.environ.get(SERVER_CERT_ENV)
    if certfile:
        return certfile

    runtime_dir = Path(
        getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent)
    )
    env_file = runtime_dir / LOCAL_ENV_FILE_NAME
    if not env_file.is_file():
        return None

    for line_number, raw_line in enumerate(
        env_file.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        if key != SERVER_CERT_ENV:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        if not value:
            raise ValueError(
                f"{SERVER_CERT_ENV} is empty in {env_file} on line {line_number}"
            )
        return value
    return None


def create_client_context():
    return _create_client_context(_configured_certificate())


@lru_cache(maxsize=8)
def _create_client_context(certfile):
    context = ssl.create_default_context()
    if certfile:
        certificate_path = Path(certfile)
        if not certificate_path.is_absolute():
            runtime_dir = Path(
                getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent)
            )
            certificate_path = runtime_dir / certificate_path
        context.load_verify_locations(cafile=str(certificate_path))
    return context
