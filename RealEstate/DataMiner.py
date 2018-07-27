import csv
import requests
import xml.etree.ElementTree as et
import urllib
import json
import time
import random

client_id = "5vvten7NPqtF4Bms1xPi"
client_secret = "G9jcBZw_Gx"

def extract(lawd_cd, deal_ymd):
    apt_url = '	http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade'
    apt_params = 'serviceKey=5HFe89gOZkcIZ%2FZogD9zz18ZKcqBnu9nTIvf83zgORCxMx%2BSYz5RRGguMTi%2BzwrjolzlLWS%2Fz363%2F7pyEVzUgw%3D%3D&LAWD_CD=' + lawd_cd + '&DEAL_YMD=' + deal_ymd
    apt_trade_response = requests.get(apt_url, params=apt_params)

    # print(apt_trade_response.url, end='\n')
    print(apt_trade_response.status_code)
    apt_trade_xml = et.fromstring(apt_trade_response.text)
    # et.dump(apt_trade_xml)

    return apt_trade_xml

def deal_ymd(year, month):
    if month < 10:
        return str(year) + '0' + str(month)
    elif 10 <= month < 13:
        return str(year) + str(month)

def mining():
    lawd_raw = open('Data/RealEstateData/LAWD_CD.csv', 'r')
    lawd_rd = csv.reader(lawd_raw)

    lawd = []
    for line in lawd_rd:
        lawd.append([line[0], line[1], line[2]])

    result = open('Data/RealEstateData/Result.csv', 'w', newline='')
    resultWriter = csv.writer(result)

    for year in range(2018, 2019):
        for month in range(1, 8):
            # 구로구, 영등포구, 관악구
            for i in [16, 18, 20]:
                apt_trade_list_raw = extract(lawd[i][2], deal_ymd(year, month)).find('body').find('items')
                apt_trade_list = apt_trade_list_raw.findall('item')
                for apt_trade in apt_trade_list:
                    row1 = [year, month, apt_trade.findtext('일')]
                    row2 = [apt_trade.findtext('법정동'), apt_trade.findtext('지번'), apt_trade.findtext('아파트'),
                           apt_trade.findtext('건축년도'), apt_trade.findtext('전용면적'), apt_trade.findtext('층'),
                           apt_trade.findtext('거래금액')] # todo: 모든 항목 추가
                    resultWriter.writerow(row1 + lawd[i] + row2)

                print('Writing ' + str(year) + '년 ' + str(month) + '월 ' + lawd[i][1])

# -------------------------------------------------- #

def miningTest():
    temp = extract('11545', deal_ymd(2016, 11)).find('body').find('items').findall('item')

    row1 = [2016, 11, temp[0].findtext('일')]
    row2 = [temp[0].findtext('법정동'), temp[0].findtext('지번'), temp[0].findtext('아파트'),
            temp[0].findtext('건축년도'), temp[0].findtext('전용면적'), temp[0].findtext('층'),
            temp[0].findtext('거래금액')]
    print(row1 + row2)

# ------------------------------------------------------ #

def miningPosition():
    result_raw = open('Data/RealEstateData/ADRS_LI.csv', 'r')
    result_rd = csv.reader(result_raw)

    addr_pos_raw = open('Data/RealEstateData/Address.csv', 'w', newline='')
    addr_posWriter = csv.writer(addr_pos_raw)

    for row in result_rd:
        encText = urllib.parse.quote("서울특별시 " + row[0] + ' ' + row[1])
        url = "https://openapi.naver.com/v1/map/geocode?query=" + encText  # json 결과

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        if (rescode == 200):
            raw = json.load(response)
            print("서울특별시 " + row[0] + ' ' + row[1], end=':\t\t\t')
            print(raw['result']['items'][0]['point'])
            addr_posWriter.writerow(['서울특별시'] + row + [str(raw['result']['items'][0]['point']['x']), str(raw['result']['items'][0]['point']['y'])])
        else:
            print("Error Code:" + rescode)

def miningPrecisePosition():
    rawFile = open('Data/RealEstateData/Price Raw.csv', 'r')
    dataReader = csv.reader(rawFile)

    newRaw = open('Data/RealEstateData/LocationPrice_C.csv', 'w', newline='')
    dataWriter = csv.writer(newRaw)

    buffer = set()

    count = 0
    for line in dataReader:
        count = count + 1
        if count > 100503:
            location = [-1, -1]
            address = line[3] + ' ' + line[4] + ' ' + line[6] + ' ' + line[7]

            if line[7][0] == '가' or line[7][0] == '산':
                location = [-1, -1]
            else:
                # -------------------- 지도 요청 -------------------------
                encText = urllib.parse.quote(address)
                url = "https://openapi.naver.com/v1/map/geocode?query=" + encText  # json 결과

                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urllib.request.urlopen(request)
                rescode = response.getcode()

                if (rescode == 200):
                    raw = json.load(response)
                    location = [str(raw['result']['items'][0]['point']['x']),
                                str(raw['result']['items'][0]['point']['y'])]
                else:
                    print("Error Code:" + rescode)
                # -------------------- 지도 요청 끝 ----------------------

            sleepTime = 0.15 + random.random() * 0.05
            print([count, sleepTime] + line[:9] + location + line[9:])

            dataWriter.writerow(line[:9] + location + line[9:])
            time.sleep(sleepTime)



