import os


def database_url() -> str:
    return os.environ.get('PKG_SERVER_DATABASE', "./test.db")

