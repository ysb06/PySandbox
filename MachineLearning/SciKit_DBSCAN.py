import csv
import pandas
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from mpl_toolkits.mplot3d import Axes3D

def pandas_cluster():
    # 월별로 클러스터링, 아파트 이름 기준으로 자주 클러스터링 목록에 들어간 아파트 검색, 해당 아파트가 주로 클러스터링 되는 다른 그룹이 무엇인지 검색

    for year in range(2007, 2018):
        for month in range(1, 13):
            pandas_raw = load_csv_data(year, month)

            model = DBSCAN()  # DBSCAN 기본값 사용
            labels = pandas.DataFrame(model.fit_predict(pandas_raw))
            labels.columns = ['Label']

            result = pandas.concat([pandas_raw, labels], axis=1)
            print(result.head(10))
            print('DBSCAN Result Size', end=': ')
            print(len(result), end=', Cluster: ')
            print(max(result['Label']) + 1, end=', No Cluster: ')
            print(len(result[result['Label'] == -1]))
            # draw_pandas_scatter(result)

def load_csv_data(year, month):
    raw = open('Data/RealEstateData/Location Price.csv', 'r')
    data_reader = csv.reader(raw)

    px_list = []
    py_list = []
    price_list = []
    for line in data_reader:
        contractYear = int(line[0])         # 거래 년도
        contractMonth = int(line[1])        # 거래 월
        if contractYear == year and contractMonth == month:
            # 위치, line 2, 3, 4, 5, 6, 7, 8은 문자로 나타난 주소
            px = float(line[9])             # 네이버 지도 위치 X좌표
            py = float(line[10])            # 네이버 지도 위치 Y좌표
            construction_year = line[3]      # 건설년도
            area = line[4]                  # 아파트 넓이
            height = line[5]                # 아파트 높이
            price = line[6]
            ppa = float(line[15])

            px_list.append(px)
            py_list.append(py)
            price_list.append(ppa)

    print('Raw Size', end=': ')
    print(len(price_list))
    lx = pandas.DataFrame(px_list)
    ly = pandas.DataFrame(py_list)
    values = pandas.DataFrame(price_list)
    pandas_raw = pandas.concat([lx, ly, values], axis=1)
    pandas_raw.columns=['X', 'Y', 'PPA']

    return pandas_raw

# pandas 읽어들이기
def draw_pandas_scatter(pandas_result):
    fig = plt.figure()
    ax = Axes3D(fig)
    # ax.set_xlim3d(left=126.79, right=126.99)
    # ax.set_ylim3d(bottom=37.45, top=37.55)

    ax.scatter(pandas_result['X'], pandas_result['Y'], pandas_result['PPA'], c=pandas_result['Label'])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('PPA')

    plt.legend()
    plt.show()