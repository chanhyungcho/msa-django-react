import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

MENUS = ["종료",
         "메타데이터 출력",
         "poptotal/popasian 변수를 total/asian로 이름변경",
         "전체 인구 대비 아시아 인구 백분율 변수 추가",
         "아시아 인구 백분율 전체 평균을 large/small 로 분류",
         "large/small 빈도표와 빈도막대그래프 작성"]

my_meta_data = {
    "county" : "자치 정부 소재지",
    "state" : "국가",
    "area" : "지역 ",
    "poptotal" : "총인구",
    "popdensity" : "밀집도",
    "popwhite" : "백인",
    "popblack" : "흑인",
    "popamerindian": "인디언",
    "popasian" : "아시안",
    "popother" : "기타",
    "percwhite" : "백인 비율",
    "percblack" : "흑인 비율"
}

class Midwest:
    def __init__(self):
        self.midwest_test = None
        self.midwest = pd.read_csv('../data/midwest.csv')
        self.my_midwest = None

    def print_meta(self):
        print(self.midwest.head(3))
        print(self.midwest.columns)
        print(self.midwest.shape)
        print(self.midwest.info())
        print(self.midwest.describe())
    def change_name(self):
        self.midwest_test = self.midwest.rename(columns=my_meta_data)
        print(self.midwest_test)

    def add_hundred_part(self):
        self.change_name()
        self.midwest_test['전체 인구 대비 아시아 인구 백분율'] = self.midwest_test['아시안'] / self.midwest_test['총인구'] *100
        self.midwest_test['전체 인구 대비 아시아 인구 백분율'].div(10)
        print(self.midwest_test.head(3))

    def class_avg(self):
        self.add_hundred_part()
        self.midwest_test['평균이상'] = np.where(self.midwest_test['전체 인구 대비 아시아 인구 백분율'].mean() >=48, 'large','small')
        print(self.midwest_test)

    def draw_plot(self):
        self.change_name()
        self.add_hundred_part()
        self.class_avg()
        count_test = self.midwest_test['평균이상'].value_counts()
        count_test.plot.bar(rot = 0)
        plt.show()

def keys(ls):
        for i,j in enumerate(ls):
            print(f"{i} {j}")
        return input(f"메뉴: ")



if __name__ == '__main__':
    md = Midwest()
    while True:
        key = keys(MENUS)
        if key == "0":
            print("종료")
        elif key == "1":
            print("메타데이터 출력")
            md.print_meta()
        elif key == "2":
            print("poptotal/popasian 변수를 total/asian로 이름변경")
            md.change_name()
        elif key == "3":
            print("전체 인구 대비 아시아 인구 백분율 변수 추가")
            md.add_hundred_part()
        elif key == "4":
            print("아시아 인구 백분율 전체 평균을 large/small 로 분류")
            md.class_avg()
        elif key == "5":
            print("large/small 빈도표와 빈도막대그래프 작성")
            md.draw_plot()