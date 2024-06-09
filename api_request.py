from dotenv import load_dotenv
from os import environ
import requests

load_dotenv()  # API 키 보관 환경 변수 로드

url = "http://openapi.seoul.go.kr:8088/"\
      + f"{environ.get('API_KEY')}"\
      + "/xml/citydata/1/5/광화문·덕수궁"
        
response = requests.get(url)
print(response.content)
