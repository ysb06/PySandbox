import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib._color_data as mcd
import random
from sklearn.cluster import DBSCAN
import pandas


def cluster():
    raw = open('Data/RealEstateData/Location Price.csv', 'r')
    data_reader = csv.reader(raw)

    data = []
    for line in data_reader:
        data.append(line)

    px_list = []
    py_list = []
    price_list = []
    xyprice_list = []

    for line in data:
        contractYear = int(line[0])
        contractMonth = int(line[1])
        if contractYear == 2008 and contractMonth == 1:
            # 위치
            px = float(line[9])
            py = float(line[10])
            constructed_year = line[3]
            area = line[4]
            height = line[5]
            price = line[6]
            ppa = float(line[15])

            px_list.append(px)
            py_list.append(py)
            price_list.append(ppa)
            xyprice_list.append([px, py, ppa])


    # ----- 여기까지 데이터 정리 -----#
    # ---- Clustering ---- #

    dbscan = DBSCAN(eps=0.033)
    clusters = dbscan.fit_predict(xyprice_list)



    # ----- 그래프 그리기 ------ #
    colors = []
    for color in mcd.CSS4_COLORS:
        colors.append(color)
    colors[0] = 'violet'
    color_codes = [0] + random.sample(range(1, len(colors)), max(clusters) + 2)

    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure()
    ax = Axes3D(fig)
    # ax.set_xlim3d(left=126.79, right=126.99)
    # ax.set_ylim3d(bottom=37.45, top=37.55)

    for i in range(-1, max(clusters) + 1):
        sx = []
        sy = []
        sv = []
        for cursor in range(0, len(clusters)):
            if clusters[cursor] == i:
                sx.append(px_list[cursor])
                sy.append(py_list[cursor])
                sv.append(price_list[cursor])
        ax.scatter(sx, sy, sv, color=colors[color_codes[i + 1]])
        print(i,end=': ')
        print(colors[color_codes[i + 1]], end='\t--> ')
        print(len(sv))

    plt.legend()
    plt.show()


# x, y, price 에 따른 클러스터링 실시
# 년월 시기 별로 실시
# 잘 되지 않을 경우 년 단위로 실시
# 모두 잘 안 되면 discrete하게 분포 되어 있을 것인데.....동 별로 비슷하게 묶일 가능성이 커서 가능성은 거의 없다고 보임
# 차라리 클러스터가 시기 별로 유지 되지 않을 경우가 많음.
# 특정 시기에만 클러스터가 유지될 경우 요인을 예상하는 정도에서 마무리

def showPlotResult(x, y, value, title='Result'):
    fig = plt.figure()
    ax = Axes3D(fig)

def dbscanTest():
    from sklearn.datasets import load_iris
    iris = load_iris()

    labels = pandas.DataFrame(iris.target)
    labels.columns = ['labels']
    data = pandas.DataFrame(iris.data)
    data.columns = ['Sepal length', 'Sepal width', 'Petal length', 'Petal width']
    # data = pandas.concat([data, labels], axis=1)

    print(labels.head(), end='\n-------------------\n')
    print(data.head(), end='\n-------------------\n')

    data = pandas.concat([data, labels], axis=1)
    print(data.head(), end='\n-------------------\n')

    feature = data[['Sepal length', 'Sepal width', 'Petal length', 'Petal width']]
    print(feature.head(), end='\n-------------------\n')

    model = DBSCAN(min_samples=6)
    predict = pandas.DataFrame(model.fit_predict(feature))
    predict.columns = ['predict']

    print(predict.head())

    r = pandas.concat([feature, predict], axis=1)
    print(r.head())

    fig = plt.figure(figsize=(6, 6))
    ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
    ax.scatter(r['Sepal length'], r['Sepal width'], r['Petal length'], c=r['predict'], alpha=0.5)
    ax.set_xlabel('Sepal lenth')
    ax.set_ylabel('Sepal width')
    ax.set_zlabel('Petal length')
    plt.show()

