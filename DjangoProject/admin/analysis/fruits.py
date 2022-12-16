import numpy as np
import pandas as pd
from string import ascii_lowercase

MENUS = ["종료","출력"]
def new_fruits_df():
    dc = {}

    #df = pd.DataFrame(dc)
    ls1 = ['제품','가격','판매량'] #스키마 , 키, (상수, 아래는 변수)
    ls2 = ['사과', '딸기','수박'] # 제품 , 벨류
    ls3 = [1800, 1500, 3000] # 가격, 벨류
    ls4 = [24, 38, 13] # 판매량, 벨류
    ls5 = [ls2,ls3,ls4]


   # for i,j in enumerate(ls1): #중요
    #    dc[j]= ls5[i]
        #dc의 리스트의 0번째 벨류는 ls5의 0번째 인덱스


    df = pd.DataFrame.from_dict({j : ls5[i] for i,j in enumerate(ls1)})
    print(df)
    print('가격평균:' + str(df['가격'].mean()))
    print('판매량평균:' + str(df['판매량'].mean()))

al = list(ascii_lowercase)
def new_number():
    df = pd.DataFrame(np.array([list(range(1,11)),
                                list(range(11,21)),
                                list(range(21,31))]), columns=[al[:10]])
    print(df)

def choice_menu(ls):
    for i,j in enumerate(ls):
        print(f"{i} {j}")
    return input('메뉴: ')

if __name__ == '__main__':
    while True:
        key = choice_menu(MENUS)
        if key == "0":
            break
        elif key == "1":
            new_number()




