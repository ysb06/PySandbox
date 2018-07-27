import csv
import pandas
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from mpl_toolkits.mplot3d import Axes3D

def pandas_cluster():
    raw = open('Data/RealEstateData/Location Price.csv', 'r')
    data_reader = csv.reader(raw)

    px_list = []
    py_list = []
    price_list = []
    xyprice_list = []
    for line in data_reader:
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


    print('Raw Size', end=': ')
    print(len(price_list))
    lx = pandas.DataFrame(px_list)
    ly = pandas.DataFrame(py_list)
    values = pandas.DataFrame(price_list)
    pandas_raw = pandas.concat([lx, ly, values], axis=1)
    pandas_raw.columns=['X', 'Y', 'PPA']

    model = DBSCAN(eps=0.033)
    labels = pandas.DataFrame(model.fit_predict(pandas_raw))
    labels.columns = ['Label']

    result = pandas.concat([pandas_raw, labels], axis=1)
    print(result.head(10))
    print('DBSCAN Result Size', end=': ')
    print(len(result), end=', Cluster: ')
    print(max(result['Label']) + 1, end=', No Cluster: ')
    print(len(result[result['Label'] == -1]))
    draw_pandas_scatter(result)

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