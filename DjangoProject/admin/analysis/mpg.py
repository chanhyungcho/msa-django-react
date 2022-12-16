import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os
'''Data columns (total 12 columns):
 #   Column        Non-Null Count  Dtype  
---  ------        --------------  -----  
 0   Unnamed: 0    234 non-null    int64  
 1   manufacturer : 회사  234 non-null    object 
 2   model : 모델         234 non-null    object 
 3   displ : 배기량         234 non-null    float64
 4   year : 연식          234 non-null    int64  
 5   cyl : 실린더           234 non-null    int64  
 6   trans : 차축         234 non-null    object 
 7   drv : 오토           234 non-null    object 
 8   cty : 시내연비           234 non-null    int64  
 9   hwy : 시외연비           234 non-null    int64  
 10  fl : 연료            234 non-null    object 
 11  class : 차종         234 non-null    object
 dtypes: float64(1), int64(5), object(6)'''


my_meta = {
    "manufacturer": "회사",
    "model": "모델",
    "displ": "배기량",
    "year": "연식",
    "cyl": "실린더",
    "trans": "차축",
    "drv": "오토",
    "cty": "시내연비",
    "hwy": "시외연비",
    "fl": "연료",
    "class": "차종"
}

MPG_MENUS = ["종료",
        "mpg 앞부분 확인",
        "mpg 뒷부분 확인",
        "행,열 출력",
        "데이터 속성 확인",
        "요약 통계량 출력",
        "문자 변수 요약 통계량 함께 출력",
        "manufacturer를 company로 변경",
        "test 변수 생성",
        #cty와 hwy 변수를 머지(merge)하여 total
        #변수 생성하고 20이상이면 pass 미만이면 fail 저장
        "test 빈도표 만들기",
        "test 빈도 막대 그래프 만들기",
         # mpg 144페이지 문제
         "displ(배기량)이 4이하와 5이상 자동차의 hwy(고속도로 연비) 비교",
         "아우디와 토요타 중 도시연비(cty) 평균이 높은 회사 검색",
         "쉐보레, 포드, 혼다 데이터 출력과 hwy 전체 평균",
         # mpg 150페이지 문제
         # 메타데이터가 category, cty 데이터는 해당 raw 데이터인 객체생성
         # 후 다음 문제 풀이
         "suv / 컴팩 자동차 중 어떤 자동차의 도시연비 평균이 더 높은가?",
         # mpg 153페이지 문제
         "아우디차에서 고속도로 연비 1~5위 출력하시오",
         # mpg 158페이지 문제
         "평균연비가 가장 높은 자동차 1~3위 출력하시오"
         ]

def my_menu(ls):
    print(f'type is {type(ls)}')
    for i, j in enumerate(ls):
        print(f"{i} {j}")
    return input("메뉴 선택: ")





class MpgService:
    def __init__(self): #변수로 쓸 것이 중복될 경우 클래스 생성자로 넣어주는게 좋음.
        self.mpg_add_test = None
        self.mpg = pd.read_csv(os.path.join('../data/data', 'mpg.csv'))
        self.my_mpg = None

    def head(self):
        print(self.mpg.head(3))

    def tail(self):
        print(self.mpg.tail(3))

    def shape(self):
        print(self.mpg.shape)

    def info(self):
        print(self.mpg.info())

    def describe(self):
        print(self.mpg.describe())

    def describe_include(self):
        print(self.mpg.describe(include = 'all'))

    def change_meta(self):
        self.my_mpg = self.mpg.rename(columns=my_meta)


    def change_manufacturer_to_company(self):
        self.mpg_add_test = self.mpg.rename(columns=self.my_mpg)
        print(self.mpg_add_test)

    def create_test_variable(self):
        self.change_meta()
        self.change_manufacturer_to_company()
        self.mpg['총연비'] = (self.mpg['시내연비'] + self.mpg['시외여비'])/2
        self.mpg['연비테스트'] = np.where(self.mpg['총연비'] >= 20, 'pass', 'fail')
        print(self.my_mpg.columns)
        print(self.my_mpg.head())
        #print(self.mpg['test'])

    def create_test_frequency(self):
        self.mpg = pd.read_csv('../data/ml/mpg.csv')
        self.mpg['total'] = ( self.mpg['cty'] +  self.mpg['hwy']) / 2
        self.mpg['test'] = np.where( self.mpg['total'] >= 20, 'pass', 'fail')
        self.mpg.to_csv('./titanic/test.csv', header=False, index=False)
        print( self.mpg['test'].value_counts())


    def draw_freq_bar_graph(self):
        self.mpg = pd.read_csv('../data/ml/mpg.csv')
        self.mpg['total'] = (self.mpg['cty'] + self.mpg['hwy']) / 2
        self.mpg['test'] = np.where(self.mpg['total'] >= 20, 'pass', 'fail')
        count_test = self.mpg['test'].value_counts()
        count_test.plot.bar(rot = 0)
        plt.show()
        #plt.savefig('./save/test.png')

    def compare_displ_and_hwy(self):
        print("배기량이 4 이하인 자동차의 시외연비:", self.mpg.query('displ <= 4')["hwy"].mean())
        print("배기량이 5 이상인 자동차의 시외연비:", self.mpg.query('displ >= 5')["hwy"].mean())


    def search_higher_cty(self):
        print("아우디의 평균 도시연비:", self.mpg.query('manufacturer == "audi"')['cty'].mean())
        print("토요타의 평균 도시연비:", self.mpg.query('manufacturer == "toyota"')['cty'].mean())

    def find_hwy_average(self):
        all_avg=self.mpg.query('manufacturer in ["chevrolet","ford","honda"]')
        print(all_avg)
        print("세 회사의 평균 도시연비:", all_avg['hwy'].mean())

        # 메타데이터가 category, cty 데이터는 해당 raw 데이터인 객체생성
        # 후 다음 문제 풀이

    def which_higher_between_suv_compact(self):
        print("suv 자동차의 도시연비:",self.mpg.query("clazz == 'suv'")['cty'].mean()) #clazz가 suv인 행만 추출한 다음 cty 호출 후 그 객체의 평균구함
        print("compact 자동차의 도시연비:",self.mpg.query("clazz == 'compact'")['cty'].mean())

    def search_hwy_in_audi_top5(self):
        a = self.mpg.query("manufacturer == 'audi'")
        b= a.sort_values(['hwy'], ascending=False).head()
        print(b)


    def search_average_mileage_top3(self):
        pass


if __name__ == '__main__':
    t = MpgService()
    while True:
        key = my_menu(MPG_MENUS)
        if key == "0":
            print("종료")
            break
        elif key == "1":
            print("mpg 앞부분 확인")
            t.head()
        elif key == "2":
            print("mpg 뒷부분 확인")
            t.tail()
        elif key == "3":
            print("행,열 출력")
            t.shape()
        elif key == "4":
            print("데이터 속성 확인")
            t.info()
        elif key == "5":
            print("요약 통계량 출력")
            t.describe()
        elif key == "6":
            print("문자 변수 요약 통계량 함께 출력")
            t.describe_include()
        elif key == "7":
            print("manufacturer를 company로 변경")
            t.change_manufacturer_to_company()
        elif key == "8":
            print("test 변수 생성")
            t.create_test_variable()
        elif key == "9":
            print("test 빈도표 만들기")
            t.create_test_frequency()
        elif key == "10":
            print("test 빈도 막대 그래프 만들기")
            t.draw_freq_bar_graph()
        elif key == "11":
            print('displ(배기량)이 4이하와 5이상 자동차의 hwy(시외연비) 비교')
            t.compare_displ_and_hwy()
        elif key == "12":
            print("아우디와 토요타 중 도시연비(cty) 평균이 높은 회사 검색")
            t.search_higher_cty()
        elif key == "13":
            print("쉐보레, 포드, 혼다 데이터 출력과 hwy 전체 평균")
            t.find_hwy_average()
        elif key == "14":
            print("suv / 컴팩 자동차 중 어떤 자동차의 도시연비 평균이 더 높은가?")
            t.which_higher_between_suv_compact()
        elif key == "15":
            print("아우디차에서 고속도로 연비 1~5위 출력하시오")
            t.search_hwy_in_audi_top5()
        elif key == "16":
            print("평균연비가 가장 높은 자동차 1~3위 출력하시오")
            t.search_average_mileage_top3()
            
            
        else:
            print("다시 선택하십시오")
