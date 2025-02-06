import os

from dotenv import load_dotenv

load_dotenv()

UPBIT_ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
UPBIT_SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")

SQLITE3_DATABASE = os.getenv("SQLITE3_DATABASE")

"""
Usage :
from environments.vairables import [변수이름]

Example :
from environments.vairables import ACCESS_KEY

해당 파일은 기본적으로 .env파일이 로컬에 존재한다는 가정하에 동작합니다.(그니까 꼭 세팅하고 돌리라는 이야기입니다.)
로컬 환경에서 테스팅 할떄는 ide로 수정하면 ok.
차후 CI 파이프라인이 동작하게 된다면 github action과 함께 레포지토리 설정에서 변수를 변경하면 됨.
배포할 때의 .env와 테스팅할 때의 .env는 다른 것이 정상이고, 또한 배포시의 .env는 유출하면 안됨!!! 
"""
