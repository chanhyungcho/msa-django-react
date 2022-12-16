import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import OrdinalEncoder

from sklearn.model_selection import train_test_split

OKLAHOMA_MENUS = ["종료",#0
         "spec",#1
         "Rename",#2
         "Interval",#3
         "Norminal",#4
         "Target",#5
         "Partition",#6
         "Fit",
         "Predict"]

oklahoma_meta = {
    'ACCESS' : 'ACCESS',
    'ACR' : 'ACR',
    'AGEP' : '나이',
    'BATH' : 'BATH',
    'BDSP' : '침실수',
    'BLD' : 'BLD',
    'CONP' : 'CONP',
    'COW' : 'COW',
    'ELEP' : '월전기료',
    'FESRP' : 'FESRP',
    'FKITP' : 'FKITP',
    'FPARC' : 'FPARC',
    'FSCHP' : 'FSCHP',
    'FTAXP' : 'FTAXP',
    'GASP' : '월가스비',
    'HHL' : 'HHL',
    'HHT' : 'HHT',
    'HINCP' : '가계소득',
    'ANX' : 'ANX',
    'MAR' : 'MAR',
    'MV' : 'MV',
    'NRC' : '자녀수',
    'R18' : 'R18',
    'R65' : 'R65',
    'RAC1P' : 'RAC1P',
    'RMSP' : '방수',
    'RWAT' : 'RWAT',
    'SCH' : 'SCH',
    'SCHL' : 'SCHL',
    'SEX' : 'SEX',
    'VALP' : '주택가격',
    'VALP_B1' : '주택가격중위수'
    }

oklahoma_menu = {
    "1" : lambda t: t.spec(),
    "2" : lambda t: t.rename_meta(),
    "3" : lambda t: t.interval_variables(),
    "4" : lambda t: t.nominal_variables(),
    "5" : lambda t: t.target_id(),
    "6" : lambda t: t.partition()
}


'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 21395 entries, 0 to 21394
Data columns (total 32 columns):
 #   Column   Non-Null Count  Dtype  
---  ------   --------------  -----  
 0   ACCESS   21395 non-null  float64
 1   ACR      21395 non-null  float64
 2   AGEP     21395 non-null  int64  
 3   BATH     21395 non-null  float64
 4   BDSP     21395 non-null  float64
 5   BLD      21395 non-null  float64
 6   CONP     21395 non-null  float64
 7   COW      12111 non-null  float64
 8   ELEP     21395 non-null  float64
 9   FESRP    21395 non-null  int64  
 10  FKITP    21395 non-null  float64
 11  FPARC    18744 non-null  float64
 12  FSCHP    21395 non-null  int64  
 13  FTAXP    21395 non-null  float64
 14  GASP     21395 non-null  float64
 15  HHL      21395 non-null  float64
 16  HHT      21395 non-null  float64
 17  HINCP    21395 non-null  float64
 18  LANX     20330 non-null  float64
 19  MAR      21395 non-null  int64  
 20  MV       21395 non-null  float64
 21  NRC      21395 non-null  float64
 22  R18      21395 non-null  float64
 23  R65      21395 non-null  float64
 24  RAC1P    21395 non-null  int64  
 25  RMSP     21395 non-null  float64
 26  RWAT     21395 non-null  float64
 27  SCH      20760 non-null  float64
 28  SCHL     20760 non-null  float64
 29  SEX      21395 non-null  int64  
 30  VALP     21395 non-null  float64
 31  VALP_B1  21395 non-null  float64
dtypes: float64(26), int64(6)
memory usage: 5.2 MB
None
'''




class OklahomaService:
    def __init__(self):
        self.target = None
        self.data = None
        self.my_oklahoma = None
        self.oklahoma = pd.read_csv('../data/ml/comb32.csv')

    '''
       1.스펙보기
       '''

    def spec(self):
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        print(" --- 1.Shape ---")
        print(self.oklahoma.shape)
        print(" --- 2.Features ---")
        print(self.oklahoma.columns)
        print(" --- 3.Info ---")
        print(self.oklahoma.info())
        print(" --- 4.Case Top1 ---")
        print(self.oklahoma.head(1))
        print(" --- 5.Case Bottom1 ---")
        print(self.oklahoma.tail(3))
        print(" --- 6.Describe ---")
        print(self.oklahoma.describe())
        print(" --- 7.Describe All ---")
        print(self.oklahoma.describe(include='all'))


    '''
    2.한글 메타데이터
    '''

    def rename_meta(self):
        self.my_oklahoma = self.oklahoma.rename(columns=oklahoma_meta)
        print(" --- 2.Features ---")
        print(self.my_oklahoma.columns)


    '''
    'AGEP' : '나이',
     'BDSP' : '침실수',
     'ELEP' : '월전기료',
    'GASP' : '월가스비',
    'HINCP' : '가계소득',
    'NRC' : '자녀수',
    'RMSP' : '방수',
    'VALP' : '주택가격',
    'VALP_B1' : '주택가격중위수'
    '''



    def interval_variables(self): #숫자 자체. 구간변수.
        self.rename_meta()
        df = self.my_oklahoma
        cols = ['나이','침실수','CONP','월전기료','월가스비','가계소득','자녀수','방수','주택가격']
        print(f'범주형 변수 데이터타입\n {df[cols].dtypes}')
        print(f'범주형 변수 결측값\n {df[cols].isnull().sum()}')
        print(f'범주형 변수 데이터타입\n {df[cols].isna().any()[lambda x:x]}')
        self.spec()
        print("##finish preprocess")
        self.oklahoma.to_csv("./save/oklahoma.csv")


    def ratio_variables(self): # 비율
        pass

    '''4.범주형 = ['성별','심장병','기혼여부','근무형태',
                   '주거형태','흡연여부','고혈압',]'''

    def nominal_variables(self): #순서가 없는
        o = self.my_oklahoma
        cols = ['COW', 'FPARC', 'LANX', 'SCH', 'SCHL']
        o[cols] = o[cols].fillna(0).astype(np.int64)
        o_with_VALP_B1 = o.drop(['주택가격'], axis=1)
        o_with_VALP_B1.to_csv('./save/2017DC1.csv', index=False)

    def ordinal_variables(self): # 순서가 있는
        pass

    '''
        5. 타깃변수(=종속변수 dependent, Y값) 설정
        입력변수(=설명변수, 확률변수, X값)
        타깃변수명: stroke (=뇌졸중)
        타깃변수값: 과거에 한번이라도 뇌졸중이 발병했으면 1, 아니면 0
    '''

    def target_id(self):
        df = pd.read_csv('../data/ml/2017DC1.csv')
        self.data = df.drop(['주택가격중위수'], axis=1)
        self.target = df['주택가격중위수']
        print(self.data.shape)
        print(self.target.shape)

    '''
    6.파티션
    '''

    def partition(self):
        self.target_id()
        X_train, X_test, y_train, y_test = train_test_split(self.data, self.target, test_size=0.5,
                                                            random_state=42)
        print('X_train shape:', X_train.shape)
        print('X_test shape:', X_test.shape)
        print('y_train shape:', y_train.shape)
        print('y_test shape:', y_test.shape)
        return X_train

def my_menu(ls):
    for i, j in enumerate(ls):
        print(f"{i}. {j}")
    return input('메뉴선택: ')

if __name__ == '__main__':
    t = OklahomaService()
    while True:
        menu = my_menu(OKLAHOMA_MENUS)
        if menu == '0':
            print("종료")
            break
        else:
            oklahoma_menu[menu](t)
            '''
               try:
                   stroke_menu[menu](t)
               except KeyError:
                   print(" ### Error ### ")
               '''


"""
    '''
        7.핏
        '''

    def fit(self):
        rf = RandomForestClassifier(n_estimators=100, random_state=0)
        X_train, X_test, y_train, y_test = self.partition()
        self.model = rf.fit(X_train, y_train)

    '''
    8.예측
    '''

    def predicate(self):
        model = self.model
        X_train, X_test, y_train, y_test = self.partition()
        self.pred = model.predict(X_test)
        print(f'Accuracy on training set: {model.score(X_train, y_train):.5f}')
        print(f'Accuracy on training set: {model.score(y_test, self.pred):.5f}')"""