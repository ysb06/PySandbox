import os
import sys
import urllib.request

client_id = "5vvten7NPqtF4Bms1xPi"
client_secret = "G9jcBZw_Gx"
encText = urllib.parse.quote("제주특별자치도 제주시 한림읍 귀덕리 1 3861-0")
url = "https://openapi.naver.com/v1/map/geocode?query=" + encText # json 결과
# url = "https://openapi.naver.com/v1/map/geocode.xml?query=" + encText # xml 결과
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)