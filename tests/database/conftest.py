import pytest

from database.model.transaction import TransactionManager
from database.mysql import MySQLClient

# ✅ 테스트용 DB 연결 정보
DB_CONFIG = {
    "mysql_host": "127.0.0.1",
    "mysql_user": "tester",
    "mysql_password": "Tester!!P80$",
    "mysql_database": "test_db",  # 테스트용 DB를 별도로 만들면 안전함
}

@pytest.fixture(scope="package")
def dao():
    client = MySQLClient(**DB_CONFIG)
    """DAO 객체를 생성하고 테스트 후 닫기"""
    dao_instance = TransactionManager(client=client)
    return dao_instance  # 테스트가 끝나면 dao_instance 반환
    #dao_instance.close() # nothing to close here...