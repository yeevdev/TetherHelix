import os

import pytest

from database.client.implementation.mysql import MySQLClient
from database.client.implementation.sqlite3 import SQLite3Client
from database.client.manager import SQLManager
from database.model.transaction import TransactionManager


def pytest_addoption(parser):
    parser.addoption("--db", action="store", default="sqlite", help="Choose database: sqlite or mysql")

# ✅ 테스트용 DB 연결 정보
TEST_MYSQL_DB_CONFIG = {
    "mysql_host": "127.0.0.1",
    "mysql_user": "tester",
    "mysql_password": "Tester!!P80$",
    "mysql_database": "test_db",  # 테스트용 DB를 별도로 만들면 안전함
}

@pytest.fixture(scope="module")
def dao(request):
    """DAO 객체를 생성하고 테스트 후 닫기"""
    db_type = request.config.getoption("--db")
    if db_type == "mysql":
        client = MySQLClient(**TEST_MYSQL_DB_CONFIG)
    elif db_type == "sqlite":
        client = SQLite3Client("tetherhelix.db")
    else:
        raise ValueError(f"Unknown database type : {db_type}")
    os.environ["SQL_MODE"] = "TEST"
    SQLManager(client_override=client)
    dao_instance = TransactionManager()
    return dao_instance  # 테스트가 끝나면 dao_instance 반환