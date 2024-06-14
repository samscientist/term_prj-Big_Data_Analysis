from dotenv import load_dotenv
from os import environ
import requests
import json

load_dotenv()  # API 키 보관 환경 변수 로드

url = "http://openapi.seoul.go.kr:8088/"\
      + f"{environ.get('API_KEY')}"\
      + "/json/citydata/17/17/"
        

async def fetch_data(area='광화문·덕수궁'):
    response = requests.get(url+area)#type(response) -> <class 'requests.models.Response'>
    # Ensure the response is valid JSON
    try:
        response_json:dict = response.json()
    except ValueError:
        print("Response content is not valid JSON")
    else:
        with open('data_cache.json', 'w', encoding='utf-8') as f:
            json.dump(response_json, f, ensure_ascii=False, indent=4)
        return response_json
    