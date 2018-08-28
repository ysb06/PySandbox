import pandas
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import matplotlib
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import numpy



def load_raw_csv():
    raw = open('Data/RealEstateData/Location Price.csv', 'r')
    pandas_raw = pandas.read_csv(raw)
    pandas_raw.columns=['Year', 'Month', 'Date', 'City', 'Gu', 'Location Code', 'Dong', 'Location Number', 'Apartment', 'X', 'Y', 'Construction_Year', 'Area', 'Floor', 'Price', 'PPA']

    print(pandas_raw.head(), end='\n\n')
    return pandas_raw

def simple_correlation_print(data):
    for year in range(2007, 2018):
        for month in range(1, 13):
            file_name = 'Data/RealEstateData/Result/Corr_' + str(year) + '_' + str(month) + '.csv'
            file = open(file_name, 'w')
            target = data[(data['Year'] == year) & (data['Month'] == month)]
            target = target.drop(['Year', 'Month', 'X', 'Y'], axis=1)
            target.corr().to_csv(file)

def simple_correlation(data):
    target_all = data.drop(['Location Code', 'Year', 'Month', 'X', 'Y'], axis=1)
    print('--- Correlation Table ---')
    print(target_all.corr().head(), end='\n\n')
    print('Correlation > 0.5 --->')

    for year in range(2007, 2018):
        for month in range(1, 13):
            target = data[(data['Year'] == year) & (data['Month'] == month)]
            target = target.drop(['Location Code', 'Year', 'Month', 'X', 'Y'], axis=1)
            correlation = target.corr()
            cor_list = correlation.values.tolist()

            count = 0
            for line in cor_list:
                for val in line:
                    if val > 0.5 or val < -0.5:
                        count += 1
            if count > 4:
                print(str(year) + '년 ' + str(month) + '월: ' + str(count))

def anova(data):
    print('----------------------------- ANOVA(three-way) ----------------------------- ')
    print('All -----> ')
    target_all = data.drop(['Location Code', 'Year', 'Month', 'X', 'Y'], axis=1)

    model = ols('PPA ~ Construction_Year + Area + Floor + Area:Construction_Year + Floor:Construction_Year + Area:Floor + Area:Construction_Year:Floor', target_all).fit()
    model_anova = anova_lm(model)
    print('Size: ' + str(len(model_anova)))
    print(model_anova, end='\n\n')


    print('Monthly -----> ')
    for year in range(2007, 2018):
        for month in range(1, 13):
            table_m = data[(data['Year'] == year) & (data['Month'] == month)]
            model = ols('PPA ~ Construction_Year + Area + Floor + Area:Construction_Year + Floor:Construction_Year + Area:Floor + Area:Construction_Year:Floor', table_m).fit()
            print(str(year) + '년 ' + str(month) + '월(Size: ' + str(len(model_anova)) + '): ')
            print(anova_lm(model), end='\n\n')


def regresssion():
    print('----------------------------- Regression ----------------------------- ')
    # 로드 되는 csv는 Location Price에서 각 구의 월별 평균 PPA 데이터
    # 엑셀 사용
    monthly_ppa = open('Data/RealEstateData/PPA_Mean.csv', 'r')
    pandas_ppa = pandas.read_csv(monthly_ppa)
    pandas_ppa.columns= ['Time', 'Gwanak', 'Guro', 'Yeongdeungpo']

    monthly_ppa_2018 = open('Data/RealEstateData/PPA_Mean_2018.csv', 'r')
    pandas_ppa_verification = pandas.read_csv(monthly_ppa_2018)
    pandas_ppa_verification.columns = ['Time', 'Gwanak', 'Guro', 'Yeongdeungpo']

    # 변수 초기화
    x_ = numpy.array(pandas_ppa['Time'])[:, numpy.newaxis]
    y_gw = numpy.array(pandas_ppa['Gwanak'])
    y_gu = numpy.array(pandas_ppa['Guro'])
    y_ye = numpy.array(pandas_ppa['Yeongdeungpo'])

    # -- Scatter 그래프 그리기 --
    plt.figure()
    plt.title('서울시 아파트 거래가격 월별 산점도')
    plt.scatter(x_, y_gw, label='관악구')
    plt.scatter(x_, y_gu, label='구로구')
    plt.scatter(x_, y_ye, label='영등포구')

    plt.legend()
    plt.show()

    print('다항 회귀(Polynomial Regression) 3차식', end='\n\n')
    reg_gw = LinearRegression()
    reg_gu = LinearRegression()
    reg_ye = LinearRegression()

    quad = PolynomialFeatures(degree=3)
    x_quad = quad.fit_transform(x_)

    reg_gw.fit(x_quad, y_gw)
    reg_gu.fit(x_quad, y_gu)
    reg_ye.fit(x_quad, y_ye)

    y_gw_fit = reg_gw.predict(quad.fit_transform(x_))
    y_gu_fit = reg_gu.predict(quad.fit_transform(x_))
    y_ye_fit = reg_ye.predict(quad.fit_transform(x_))

    print('-- 관악구 --')
    print('3차식 계수 목록: ', end='')
    print(quad.get_feature_names())
    print('예측된 계수 목록')
    for line in reg_gw.coef_:
        print(line, end=', ')
    print('\n')

    print('-- 구로구 --')
    print('3차식 계수 목록: ', end='')
    print(quad.get_feature_names())
    print('예측된 계수 목록')
    for line in reg_gu.coef_:
        print(line, end=', ')
    print('\n')

    print('-- 영등포구 --')
    print('3차식 계수 목록: ', end='')
    print(quad.get_feature_names())
    print('예측된 계수 목록')
    for line in reg_ye.coef_:
        print(line, end=', ')
    print('\n')

    # 검증
    y_gw_quad_predict = reg_gw.predict(x_quad)
    y_gu_quad_predict = reg_gu.predict(x_quad)
    y_ye_quad_predict = reg_ye.predict(x_quad)

    # -- Mean Square Error
    mse_gw = mean_squared_error(y_gw, y_gw_quad_predict)
    mse_gu = mean_squared_error(y_gu, y_gu_quad_predict)
    mse_ye = mean_squared_error(y_ye, y_ye_quad_predict)
    list_mse = [mse_gw, mse_gu, mse_ye]

    # -- R Square
    r2_gw = r2_score(y_gw, y_gw_quad_predict)
    r2_gu = r2_score(y_gu, y_gu_quad_predict)
    r2_ye = r2_score(y_ye, y_ye_quad_predict)
    list_r2 = [r2_gw, r2_gu, r2_ye]

    reg_result = pandas.concat([pandas.DataFrame(['관악구', '구로구', '영등포구']), pandas.DataFrame(list_mse), pandas.DataFrame(list_r2)], axis=1)
    reg_result.columns = ['지역', 'MSE', 'R2']
    print(reg_result, end='\n\n')
    # -- 그래프 그리기 --
    plt.figure()
    plt.title('서울시 아파트 거래가격 추세')
    plt.scatter(x_, y_gw, label='관악구')
    plt.scatter(x_, y_gu, label='구로구')
    plt.scatter(x_, y_ye, label='영등포구')

    plt.plot(x_, y_gw_fit, label='관악구 추세선')
    plt.plot(x_, y_gu_fit, label='구로구 추세선')
    plt.plot(x_, y_ye_fit, label='영등포구 추세선')

    plt.legend()
    plt.show()
    # 다항 회귀 3차식....4차 및 5차도 고려할 필요가 있음...그러나 넘어감

    # 여기까지가 회귀 모형 결과
    print('모형 검증 --> 2018년도 값 대입')
    # 직관적 예측 ---> 맞는 것 같다
    sample_x = numpy.array(pandas_ppa_verification['Time'])[:, numpy.newaxis]
    sample_y_gw = numpy.array(pandas_ppa_verification['Gwanak'])
    sample_y_gu = numpy.array(pandas_ppa_verification['Guro'])
    sample_y_ye = numpy.array(pandas_ppa_verification['Yeongdeungpo'])

    comp_x = numpy.concatenate((x_, sample_x,))
    comp_y_gw = numpy.concatenate((y_gw, sample_y_gw,))
    comp_y_gu = numpy.concatenate((y_gu, sample_y_gu,))
    comp_y_ye = numpy.concatenate((y_ye, sample_y_ye,))

    plt.figure()
    plt.title('서울시 아파트 거래가격 추세')
    plt.scatter(comp_x, comp_y_gw, label='관악구')
    plt.scatter(comp_x, comp_y_gu, label='구로구')
    plt.scatter(comp_x, comp_y_ye, label='영등포구')

    plt.plot(x_, y_gw_fit, label='관악구 추세선')
    plt.plot(x_, y_gu_fit, label='구로구 추세선')
    plt.plot(x_, y_ye_fit, label='영등포구 추세선')

    plt.legend()
    plt.show()
    # 예측 값 재계산
    comp_y_gw_fit = reg_gw.predict(quad.fit_transform(comp_x))
    comp_y_gu_fit = reg_gu.predict(quad.fit_transform(comp_x))
    comp_y_ye_fit = reg_ye.predict(quad.fit_transform(comp_x))

    # 예측 값을 재검증
    comp_x_quad = quad.fit_transform(comp_x)

    comp_y_gw_quad_predict = reg_gw.predict(comp_x_quad)
    comp_y_gu_quad_predict = reg_gu.predict(comp_x_quad)
    comp_y_ye_quad_predict = reg_ye.predict(comp_x_quad)

    # -- Mean Square Error
    comp_mse_gw = mean_squared_error(comp_y_gw, comp_y_gw_quad_predict)
    comp_mse_gu = mean_squared_error(comp_y_gu, comp_y_gu_quad_predict)
    comp_mse_ye = mean_squared_error(comp_y_ye, comp_y_ye_quad_predict)
    comp_list_mse = [comp_mse_gw, comp_mse_gu, comp_mse_ye]

    # -- R Square
    comp_r2_gw = r2_score(comp_y_gw, comp_y_gw_quad_predict)
    comp_r2_gu = r2_score(comp_y_gu, comp_y_gu_quad_predict)
    comp_r2_ye = r2_score(comp_y_ye, comp_y_ye_quad_predict)
    comp_list_r2 = [comp_r2_gw, comp_r2_gu, comp_r2_ye]

    comp_reg_result = pandas.concat([pandas.DataFrame(['관악구', '구로구', '영등포구']), pandas.DataFrame(comp_list_mse), pandas.DataFrame(comp_list_r2)], axis=1)
    comp_reg_result.columns = ['지역', 'MSE', 'R2']
    print(comp_reg_result)

    plt.figure()
    plt.title('서울시 아파트 거래가격 추세')
    plt.scatter(comp_x, comp_y_gw, label='관악구')
    plt.scatter(comp_x, comp_y_gu, label='구로구')
    plt.scatter(comp_x, comp_y_ye, label='영등포구')

    plt.plot(comp_x, comp_y_gw_fit, label='관악구 추세선')
    plt.plot(comp_x, comp_y_gu_fit, label='구로구 추세선')
    plt.plot(comp_x, comp_y_ye_fit, label='영등포구 추세선')

    plt.legend()
    plt.show()

    plt.figure()
    plt.title('서울시 아파트 거래가격 추세 (2018)')
    plt.xlim([43000,43300])
    plt.scatter(comp_x, comp_y_gw, label='관악구')
    plt.scatter(comp_x, comp_y_gu, label='구로구')
    plt.scatter(comp_x, comp_y_ye, label='영등포구')

    plt.plot(comp_x, comp_y_gw_fit, label='관악구 추세선')
    plt.plot(comp_x, comp_y_gu_fit, label='구로구 추세선')
    plt.plot(comp_x, comp_y_ye_fit, label='영등포구 추세선')

    plt.legend()
    plt.show()








data_raw = load_raw_csv()
pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)
pandas.set_option('display.width', 320)

font = {'family': 'NanumGothic', 'size': 16}
matplotlib.rc('font', **font)

# Pandas 피어슨 상관계수
simple_correlation(data_raw)

# 분산 분석
anova(data_raw)

# 회귀 분석
regresssion()


'''
분석 방법
회귀 분석 --> 상관 분석 --> 분산 분석

결과
각 변수(년식, 넓이, 층수) 에 대해 -->

상관계수의 경우 1차원적 변수 비교로는 크게 의미가 없다.
일부 상관 계수가 0.5를 넘는 것도 있지만 예외적인 상황으로 보인다.
실제로 분산 분석 결과로도 PPA와 각각의 변수는 독립적이라고 나옴

그러나 3-way 분산 분석 결과 변수의 조합으로 이루어 졌을 때 관련성을 보이는 경우가 많이 보인다.
이러한 점으로 미루어 봤을 때 이것은 3개의 변수가 종합적으로 가격에 영향을 준다는 것을 의미한다.

사후 검정이 필요하지만....아흐흑
'''
