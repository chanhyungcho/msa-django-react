from dataclasses import dataclass

import googlemaps
import numpy as np
import openpyxl
import pandas as pd
from scipy import stats
from sklearn import preprocessing
from sklearn.preprocessing import OrdinalEncoder
import folium

import json

from sklearn.model_selection import train_test_split

CRIME_MENUS = ["종료",#0
         "show spec",#1
         "save_police_pos",#2.여러개의 데이터프레임을 하나로 통합
         "save_cctv_pos",#3
         "save_police_nominalize",#4
         "save_us_unemployment_map",#5
         "save_seoul_crime_map",#6
         "create_folium_data" #7
         "Fit",
         "Predict"]



crime_menu = {
    "1" : lambda t: t.spec(),
    "2" : lambda t: t.save_police_pop(),
    "3" : lambda t: t.save_cctv_pop(),
    "4" : lambda t: t.save_police_normalize(),
    "5" : lambda t: t.save_us_unemployment_map(),
    "6" : lambda t: t.save_seoul_crime_map()
}

@dataclass
class MyChoroplethVO:
    geo_data = "",
    data = object,
    name = "",
    columns = [],
    key_on = "",
    fill_color = "",
    fill_opacity = 0.0,
    line_opacity = 0.0,
    legend_name = "",
    bins = None,
    location = [],
    zoom_start = 0,
    save_path = ''

def MyChoroplethService(vo):
    map = folium.Map(location=vo.location, zoom_start=vo.zoom_start)
    folium.Choropleth(
        geo_data=vo.geo_data,
        data=vo.data,
        name=vo.name,
        columns=vo.columns,
        key_on=vo.key_on,
        fill_color=vo.fill_color,
        fill_opacity=vo.fill_opacity,
        line_opacity=vo.line_opacity,
        legend_name=vo.legend_name
    ).add_to(map)
    map.save(vo.save_path)




class CrimeService:
    def __init__(self):
        self.crime = pd.read_csv(r'C:\Users\AIA\djangoProject\admin\data\crime\cctv_in_seoul.csv')
        cols = ['절도 발생', '절도 검거', '폭력 발생', '폭력 검거']
        self.crime[cols] = self.crime[cols].replace(',','',regex=True).astype(int)
        self.cctv = pd.read_csv('../data/crime/cctv_in_seoul.csv')
        self.pop = pd.read_excel('./data/crime/pop_in_seoul.xls', usecols=[1, 3, 6, 9, 13], skiprows=[0,2])
        self.ls = [self.crime,self.cctv,self.pop]
        self.crime_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        self.crime_columns = ['살인', '강도', '강간', '절도', '폭력']
        self.arrest_columns = ['살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거']
        self.us_states = pd.read_json('../data/ml/us-states.json')
        self.us_unemployment = pd.read_csv('../data/crime/us_unemployment.csv')
        self.kr_states = './data/crime/kr-state.json'






    '''
    1.스펙보기
    '''
    def spec(self):
        print("클로저테스트")
        #__init__ 이 아님. 속성값을 만들지 않음(메모리를 점유하지 않음). s는 지역변수?로 기능을 가짐.(주소만 가짐. 실행만 하고 사라짐).

        [(lambda x: print(f"--- 1.Shape ---\n{x.shape}\n"
                               f"--- 2.Features ---\n{x.columns}\n"
                               f"--- 3.Info ---\n{x.info}\n"
                               f"--- 4.Case Top1 ---\n{x.head(1)}\n"
                               f"--- 5.Case Bottom1 ---\n{x.tail(3)}\n"
                               f"--- 6.Describe ---\n{x.describe()}\n"
                               f"--- 7.Describe All ---\n{x.describe(include='all')}"))
        (i) for i in self.ls]


    '''
    2
    '''
    def save_police_pop(self):
        crime = self.crime
        station_names =[]
        for name in crime['관서명']:
            print(f"지역이름: {name}")
            station_names.append(f'서울{str(name[:-1])}경찰서')
        print(f"서울시내 경찰서는 총 {len(station_names)}개 이다.")
        [print(f"{str(i)}") for i in station_names]
        gmaps = (lambda x: googlemaps.Client(key=x))("AIzaSyAN7pBYLDJ7MERqNphuWaqp4LWeFpLKpz0")
        print(gmaps.geocode("서울중부경찰서", language='ko'))
        print("API에서 주소 추출 시작")
        station_addrs=[]
        station_lats=[]
        station_lngs=[]
        for i,name in enumerate(station_names):
            _ = gmaps.geocode(name, language='ko')
            print(f'name {i} = {_[0].get("formatted_address")}')
            station_addrs.append(_[0].get('formatted_address'))
            _loc = _[0].get('geometry')
            station_lats.append(_loc['location']['lat'])
            station_lngs.append(_loc['location']['lng'])
        gu_names = []
        for name in station_addrs:
            _ = name.split()
            gu_name = [gu for gu in _ if gu[-1] == '구'][0]
            gu_names.append(gu_name)
        crime['구별'] = gu_names
        # 구와 경찰서의 위치가 다른 경우 수작업
        crime.loc[crime['관서명'] == '혜화서', ['구별']] = '종로구'
        crime.loc[crime['관서명'] == '서부서', ['구별']] = '은평구'
        crime.loc[crime['관서명'] == '종암서', ['구별']] = '성북구'
        crime.loc[crime['관서명'] == '방배서', ['구별']] = '서초구'
        crime.loc[crime['관서명'] == '수서서', ['구별']] = '강남구'
        crime.to_pickle('./save/police_pos.pkl')
        print(pd.read_pickle('../save/crime/police_pos.pkl'))


    '''
    3
    '''
    def save_cctv_pop(self): #ratio로 판단하고 nominal로 결과값
        cctv = self.cctv
        pop = self.pop
        cctv.rename(columns={cctv.columns[0]: '구별'}, inplace = True)
        pop.rename(columns={
            pop.columns[0]: '구별',
            pop.columns[1]: '인구수',
            pop.columns[2]: '한국인',
            pop.columns[3]: '외국인',
            pop.columns[4]: '고령자'
        },inplace=True)
        print('*'*100)
        pop.drop(index=26, inplace=True)
        pop['외국인비율'] = pop['외국인'].astype(int) / pop['인구수'].astype(int) *100 #인구 중 외국인이나 고령자가 있는 것에 상관관계가 있는지 확인하는것. ratio(*100)
        pop['고령자비율'] = pop['고령자'].astype(int) / pop['인구수'].astype(int) *100

        cctv.drop(["2013년도 이전","2014년","2015년","2016년"],axis=1,inplace=True) #axis =1
        cctv_pop = pd.merge(cctv, pop, on="구별")
        cor1 = np.corrcoef(cctv_pop['고령자비율'], cctv_pop['소계'])
        cor2 = np.corrcoef(cctv_pop['외국인비율'], cctv_pop['소계'])
        print(f'고령자비율과 CCTV의 상관계수 {str(cor1)} \n'
              f'외국인비율과 CCTV의 상관계수 {str(cor2)} ')
        cctv_pop.to_pickle('./save/cctv_pop.pkl')
        print(pd.read_pickle('.save/crime/cctv_pop.pkl'))
        """
         고령자비율과 CCTV 의 상관계수 [[ 1.         -0.28078554]
                                     [-0.28078554  1.        ]] 
         외국인비율과 CCTV 의 상관계수 [[ 1.         -0.13607433]
                                     [-0.13607433  1.        ]]
        r이 -1.0과 -0.7 사이이면, 강한 음적 선형관계,
        r이 -0.7과 -0.3 사이이면, 뚜렷한 음적 선형관계,
        r이 -0.3과 -0.1 사이이면, 약한 음적 선형관계,
        r이 -0.1과 +0.1 사이이면, 거의 무시될 수 있는 선형관계,
        r이 +0.1과 +0.3 사이이면, 약한 양적 선형관계,
        r이 +0.3과 +0.7 사이이면, 뚜렷한 양적 선형관계,
        r이 +0.7과 +1.0 사이이면, 강한 양적 선형관계
        고령자비율 과 CCTV 상관계수 [[ 1.         -0.28078554] 약한 음적 선형관계
                                    [-0.28078554  1.        ]]
        외국인비율 과 CCTV 상관계수 [[ 1.         -0.13607433] 거의 무시될 수 있는
                                    [-0.13607433  1.        ]]                        
         """



    '''
    4
    '''
    def save_police_normalize(self): #정규화
        police_pos = pd.read_pickle('../../../../static/save/dam/ml/police_pos.pkl')
        police = pd.pivot_table(police_pos,index="구별",aggfunc=np.sum) #pivot 내가 원하는 컬럼을 인덱스로 치환
        police['살인검거율'] = (police['살인 검거'].astype(int) / police['살인 발생'].astype(int)) * 100
        police['강도검거율'] = (police['강도 검거'].astype(int) / police['강도 발생'].astype(int)) * 100
        police['강간검거율'] = (police['강간 검거'].astype(int) / police['강간 발생'].astype(int)) * 100
        police['절도검거율'] = (police['절도 검거'].astype(int) / police['절도 발생'].astype(int)) * 100
        police['폭력검거율'] = (police['폭력 검거'].astype(int) / police['폭력 발생'].astype(int)) * 100
        police.drop(columns={'살인 검거','강도 검거','강간 검거','절도 검거','폭력 검거'}, axis=1, inplace=True)
        for i in self.crime_rate_columns:
            police.loc[police[i] > 100,1] = 100  # 데이터값의 기간 오류로 100을 넘으면 100으로 계산
        police.rename(columns={
            '살인 발생': '살인',
            '강도 발생': '강도',
            '강간 발생': '강간',
            '절도 발생': '절도',
            '폭력 발생': '폭력'
        }, inplace=True)
        x = police[self.crime_rate_columns].values
        min_max_scalar = preprocessing.MinMaxScaler() # 연속화
        """
        스케일링은 선형변환을 적용하여
        전체 자료의 분포를 평균 0, 분산 1이 되도록 만드는 과정
        """
        x_scaled = min_max_scalar.fit_transform(x.astype(float))
        """
        정규화 normalization
        많은 양의 데이터를 처리함에 있어 데이터의 범위(도메인)를 일치시키거나
        분포(스케일)를 유사하게 만드는 작업
        """
        police_norm = pd.DataFrame(x_scaled, columns=self.crime_columns, index=police.index)
        police_norm[self.crime_rate_columns] = police[self.crime_rate_columns]
        police_norm['범죄'] = np.sum(police_norm[self.crime_rate_columns], axis=1)
        police_norm['검거'] = np.sum(police_norm[self.crime_columns], axis=1)
        # police_norm.reset_index(drop=False, inplace=True) # pickle 저장직전 인덱스 해제
        police_norm.to_pickle('./save/police_norm.pkl')
        print(pd.read_pickle('../../../../static/save/dam/ml/police_norm.pkl'))

    def save_us_unemployment_map(self):  # 5
        mc = MyChoroplethVO()
        mc.geo_data = self.us_states
        mc.data = self.us_unemployment
        mc.name = "choropleth"
        mc.columns = ["State", "Unemployment"]
        mc.key_on = "feature.id"
        mc.fill_color = "YlGn"
        mc.fill_opacity = 0.7
        mc.line_opacity = 0.5
        mc.legend_name = "Unemployment Rate (%)"
        mc.bins = list(mc.data["Unemployment"].quantile([0, 0.25, 0.5, 0.75, 1]))
        mc.location = [48, -102]
        mc.zoom_start = 5
        mc.save_path = "../../../../static/save/dam/ml/unemployment.html"
        MyChoroplethService(mc)

    def save_seoul_crime_map(self):  # 6
        mc = MyChoroplethVO()
        mc.geo_data = self.kr_states
        mc.data = self.get_seoul_crime_data()
        mc.name = "choropleth"
        mc.columns = ["State", "Crime Rate"]
        mc.key_on = "feature.id"
        mc.fill_color = "PuRd"
        mc.fill_opacity = 0.7
        mc.line_opacity = 0.2
        mc.legend_name = "Crime Rate (%)"
        mc.location = [37.5502, 126.982]
        mc.zoom_start = 12
        mc.save_path = "./save/seoul_crime_rate.html"
        MyChoroplethService(mc)

    def get_seoul_crime_data(self):
        police_norm = pd.read_pickle('../../../../static/save/dam/ml/police_norm.pkl')
        return tuple(zip(police_norm.index, police_norm['범죄']))
        # police_norm.index 는 '구별'


def set_json_from_df(fname):  # 미국 주가 콜롬비아, 푸에르토-리코(준주) 포함시
    df = pd.read_json(fname)
    df.drop(df.index[[8,51]], inplace=True)
    df.to_json("./save/us-states.json", orient='index')


if __name__ == '__main__':
    set_json_from_df(fname='./data/ml/us-states.json')
    x = pd.read_json("../data/ml/us-states.json")
    print(x.tail(1))
    # 콜롬비아('id': '11'-> 인덱스 8),
    # 푸에르토리코('id': '72' -> 인덱스 51)는 준주라서 제거해야함


def my_menu(ls):
    for i, j in enumerate(ls):
        print(f"{i}. {j}")
    return input('메뉴선택: ')

if __name__ == '__main__':
    t = CrimeService()
    while True:
        menu = my_menu(CRIME_MENUS)
        if menu == '0':
            print("종료")
            break
        else:
            crime_menu[menu](t)
            '''
               try:
                   stroke_menu[menu](t)
               except KeyError:
                   print(" ### Error ### ")
               '''

crime_menu = {
    "1" : lambda t: t.spec(),
    "2" : lambda t: t.save_police_pop(),
    "3" : lambda t: t.save_cctv_pop(),
    "4" : lambda t: t.save_police_normalize(),
    "5" : lambda t: t.save_us_unemployment_map(),
    "6" : lambda t: t.save_seoul_crime_map()
}

"""
    def save_us_folium(self):
        self.us_states = pd.read_json('./titanic/us-states.json').dr
        self.us_unemployment = pd.read_csv('./titanic/us_unemployment.csv')

        geo_data=self.us_states
        titanic = self.us_unemployment
        bins = list(self.us_unemployment["Unemployment"].quantile([0,0.25,0.5,0.75,1]))
        map = folium.Map(location=[48, -102], zoom_start=5)
        folium.Choropleth(
            geo_data=geo_data, #us_states
            titanic=titanic, #us_unemployment
            name="choropleth",
            columns=["State","Unemployment"],
            key_on="feature.id",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=0.5,
            legend_name='Unemployment Rate (%)',
            bins=bins,
        ).add_to(map)
        map.save('./save/unemployment.html')

    def save_seoul_folium(self):

        geo_data = self.kr_states
        titanic = self.create_folium_data()

        map = folium.Map(location=[37.5502, 126.982], zoom_start=12)
        folium.Choropleth(
            geo_data=geo_data,  # us_states
            titanic=titanic,  # us_unemployment
            name="choropleth",
            columns=["State", "Crime Rate"],
            key_on="feature.id",
            fill_color="PuRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Crime Rate (%)'
        ).add_to(map)
        map.save('./save/CrimeRate.html')


    def create_folium_data(self):
        crime = self.crime
        police_pos = pd.read_pickle('./save/police_pos.pkl')
        police_norm =pd.read_pickle('./save/police_norm.pkl')
        print(police_pos)
        print(police_norm)
        station_names = []
        for name in crime['관서명']:
            station_names.append('서울' + str(name[:-1] + '경찰서'))
        station_addrs = []
        station_lats = []
        station_lngs = []
        gmaps = (lambda x: googlemaps.Client(key=x))("AIzaSyAN7pBYLDJ7MERqNphuWaqp4LWeFpLKpz0")
        for name in station_names:
            t = gmaps.geocode(name, language='ko')
            station_addrs.append(t[0].get('formatted_address')) # 'formatted_address'고정
            t_loc = t[0].get('geometry') # 'geometry'고정
            station_lats.append(t_loc['location']['lat'])
            station_lngs.append(t_loc['location']['lng'])
        police_pos['lat'] = station_lats # 'lat'고정
        police_pos['lng'] = station_lngs # 'lng'고정
        temp = police_pos[self.arrest_columns] / police_pos[self.arrest_columns].max()
        police_pos['검거'] = np.sum(temp, axis=1)
        return tuple(zip(police_norm.index,police_norm['범죄']))

    def ordinal(self): # 순서가 있는
        pass

    '''
        5. 타깃변수(=종속변수 dependent, Y값) 설정
        입력변수(=설명변수, 확률변수, X값)
        타깃변수명: stroke (=뇌졸중)
        타깃변수값: 과거에 한번이라도 뇌졸중이 발병했으면 1, 아니면 0
    '''




    '''
    6.파티션
    '''

    def partition(self):
        pass

"""

