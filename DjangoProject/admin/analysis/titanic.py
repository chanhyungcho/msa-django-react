import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
from admin.vision.dataset import Dataset
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc

font_path = "C:/Windows/Fonts/malgunbd.ttf"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp',
#     'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked'],
#시각화를 통해 얻은 상관관계 변수(variable = feature = column)는
#Pclass
#Sex
#Age
#Fare
#Embarked
# ===null 값===
# Age            177
# Cabin          687
# Embarked         2

class TitanicModel(object):

    dataset = Dataset()

    def __init__(self):   #데이터 수집
        pass


    def __str__(self):
        b = self.new_model(self.dataset.fname) #fname이라고만 해줬는데 컴터가 게터인지 세터인지 어케 이해? 똑같은데
        return f"Train Type: {type(b)}\n" \
               f'Train columns: {b.columns}\n' \
               f'Train head: {b.head()}\n' \
               f'Train null의 갯수: {b.isnull().sum()}'
        #print(f'Train Type: {type(b)}')
        #print(f'Train columns: {b.columns}')
        #print(f'Train head: {b.head()}')
        #print(f'Train null의 갯수: {b.isnull().sum()}')

    def preprocess(self):
        pass

    def new_model(self, fname) -> object:  #이 클래스 안에서 쓰일 인스턴스
        this = self.dataset
        this.context = './data/titanic/'
        this.fname = fname
        return pd.read_csv(this.context + this.fname) #this context 쌀 pd.찧고 return 떡.


    @staticmethod
    def create_train(this) ->object:   #객체화
        return this.train.drop('Survived', axis = 1)

    @staticmethod
    def create_label(this) ->object:
        return this.train['Survived']

    @staticmethod
    def drop_features(this, *feature) -> object: # * > [ ] 자료구조의 의미
        for i in feature:
            this.train = this.train.drop(i, axis = 1)
            this.test = this.test.drop(i, axis = 1)
        return this

    #원래 pclass가 들어가지만 숫자로 되어 있어서 컴퓨터에서 알아서 가능
    @staticmethod
    def sex_nominal(this)-> object: #female > 1, male > 0
         for i in [this.train,this.test]:
             i["Gender"] = i["Sex"].map({"male" : 0, "female" : 1})#gender는 0,1 sex는 male female
         return this

    @staticmethod
    def age_ordinal(this)-> object: #연령대 10대,20대,30대
        for i in [this.train,this.test]:
            i["Age"] = i["Age"].fillna(-0.5)
        bins = [-1,0,5,12,18,24,35,68,np.inf] #bins는 자료에서 하나씩 빼는것, 구간을 나눈것. -1~0:Unknown, 0~5:Baby
        labels = ['Unknown', 'Baby', 'Child', 'Teenager', 'Student', 'Young Adult', 'Adult', 'Senior'] #영어로 먼저 설정
        age_mapping = {'Unknown': 0, 'Baby': 1, 'Child': 2, 'Teenager': 3, 'Student': 4, #매핑
                             'Young Adult': 5, 'Adult': 6, 'Senior': 7}
        for i in[this.train,this.test]:
            i["AgeGroup"] = pd.cut(i['Age'], bins=bins, labels=labels)
            i["AgeGroup"] = i["AgeGroup"].map(age_mapping)
        return this

    @staticmethod
    def fare_ordinal(this)-> object: #비싼 것, 보통, 저렴한것 #4등분 pd.qcut()사용
        for i in [this.train, this.test]:
            i['FareBand'] = pd.qcut(i['Fare'], 4, labels={1,2,3,4})
        return this

    @staticmethod
    def embarked_nominal(this)-> object: #승선항구 S,C,Q
        this.train = this.train.fillna({'Embarked': 'S'})  # 임시값을 집어넣어라 / fillna /na = not a number
        this.test = this.test.fillna({'Embarked': 'S'})  # 임시값을 집어넣어라 / fillna /na = not a number
        for i in [this.train, this.test]:
            i['Embarked'] = i['Embarked'].map({"S": 1, "C": 2, "Q": 3}) # = 어사인먼트 asignment / map 매핑
        return this

    @staticmethod
    def title_nominal(this) -> object:
        combine = [this.train, this.test]
        for i in combine:
            i['Title'] = i.Name.str.extract('([A-Za-z]+)\.', expand=False) #i가 리스트였으면 i['']
        for i in combine:
            i['Title'] = i['Title'].replace(['Countess', 'Lady', 'Sir'], 'Royal')
            i['Title'] = i['Title'].replace(['Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Jonkheer', 'Dona', 'Mme'], 'Rare')
            i['Title'] = i['Title'].replace('Mlle', 'Mr')
            i['Title'] = i['Title'].replace('Ms', 'Miss')
            i['Title'] = i['Title'].fillna(0)
            i['Title'] = i['Title'].map({
                'Mr': 1,
                'Miss': 2,
                'Mrs': 3,
                'Master': 4,
                'Royal': 5,
                'Rare': 6
            })

        return this

    @staticmethod
    def create_k_fold() -> object: #생성자
        return KFold(n_splits=10, shuffle=True, random_state=0)

    @staticmethod
    def get_accuracy(this,algo):
        score = cross_val_score(SVC(),
                                this.train,
                                this.label,
                                cv =TitanicModel.create_k_fold(),
                                n_jobs=1,
                                scoring='accuracy')
        return round(np.mean(score)*100,2)



class Plot(object):
    dataset = Dataset()
    model = TitanicModel()
    def __init__(self, fname):
        self.entry = self.model.new_model(fname)

    def __str__(self):
        return f""

    def draw_survived(self):
        this = self.entry
        f, ax = plt.subplots(1, 2, figsize=(18, 8)) #한 화면에 두 개의 그래프를 그릴 때는 복수형 subplots을 취한다.
        this['Survived'].value_counts().plot.pie(explode=[0, 0.1], autopct='%1.1f%%', ax=ax[0], shadow=True)
        ax[0].set_title('0.사망자 vs 1.생존자')
        ax[0].set_ylabel('')
        ax[1].set_title('0. 사망자 vs 1.생존자')
        sns.countplot('Survived', data=this, ax=ax[1])
        plt.show()

    def draw_pclass(self):
        this = self.entry
        this["생존결과"] = this["Survived"].replace(0, "사망자").replace(1, "생존자")
        this["좌석등급"] = this["Pclass"].replace(1, "1등석").replace(2, "2등석").replace(3, "3등석")
        sns.countplot(data=this, x="좌석등급", hue="생존결과")
        plt.show()

    def draw_sex(self):
        this = self.entry
        f, ax = plt.subplots(1, 2, figsize=(18, 8))
        this['Survived'][this['Sex'] == "male"].value_counts().plot.pie(explode=[0, 0.1], autopct='%1.1f%%', ax=ax[0], shadow=True) #조건 룹. 연산 [ ], for문이 없으면 if 생략가능
        this['Survived'][this['Sex'] == "female"].value_counts().plot.pie(explode=[0, 0.1], autopct='%1.1f%%', ax=ax[1], shadow=True)
        ax[0].set_title('남성의 생존비율 [0.사망자 vs 1.생존자]')
        ax[1].set_title('여성의 생존비율 [0.사망자 vs 1.생존자]')
        plt.show()

    def draw_embarked(self):
        this = self.entry
        this["생존결과"] = this["Survived"].replace(0, "사망자").replace(1, "생존자") #replace = 0을 사망자로 바꿔 보여줄것
        this["승선항구"] = this["Embarked"].replace("C", "쉘버그").replace("S", "사우스헴튼").replace("Q", "퀸즈타운")
        sns.countplot(data=this, x="승선항구", hue="생존결과")
        plt.show()

class TitanicController(object):

    model = TitanicModel()
    def __init__(self):
        pass

    def __str__(self):
        return f""

    dataset = Dataset()
    model = TitanicModel()

    def mining(self):
        pass

    def preprocess(self,train,test) -> object: #전처리
        model = self.model
        this = self.dataset
        this.train = model.new_model(train)
        this.test = model.new_model(test)
        this.td = this.test['PassengerId']
        #columns 편집과정'
        #this = model.pclass_ordinal(this) 데이터 자체가 이미 ordinal이라 손댈 필요가 없음.
        this = model.sex_nominal(this) #this는 자료구조라서 이렇게 가능. 변수였으면 이렇게 불가. 사람 != 홍길동, 홍길동 == 사람
        this = model.age_ordinal(this)
        this = model.fare_ordinal(this)
        this = model.embarked_nominal(this)
        this = model.title_nominal(this)
        this = model.drop_features(this,
                                   'PassengerId','Name', 'Sex', 'Age',
                                   'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin')
        return this


    def postprcess(self): #원래 필요
        pass

    def modeling(self,train,test) -> object: #모델생성
        model = self.model
        this = self.preprocess(train, test)
        this.label = model.create_label(this)
        this.train = model.create_train(this)
        return this

    def learning(self,train, test, algo): #기계학습
        this = self.modeling(train, test)
        accuracy = self.model.get_accuracy(this,algo)
        print(f'서포트벡터머신 정확도: {accuracy}%')

    def submit(self): #배포
        pass


if __name__ == "__main__":  #스테틱 같은 공간 # main이라 self가 아님
    t = TitanicModel()
    this = Dataset()
    this.train = t.new_model('train.csv')
    this.test = t.new_model('test.csv')
    this = TitanicModel.title_nominal(this) #
    print(this.train.columns)
    print(this.train.head()) #위에서 부터 몇 개 볼지 tail()은 아래서 몇개볼지


    from admin.vision.common import Common
    import warnings

    warnings.simplefilter(action='ignore', category=FutureWarning)

    if __name__ == '__main__':
        api = TitanicController()
        while True:
            menu = Common.menu(["종료", "시각화", "모델링", "머신러닝", "배포"])
            if menu == "0":
                print("## 종료 ##")
                break
            elif menu == "1":
                print("### 시각화 ###")
                plot = Plot("train.csv")
                plot.draw_survived()
                plot.draw_pclass()
                plot.draw_sex()
                plot.draw_embarked()
            elif menu == "2":
                print("### 모델링 ###")
                this = api.modeling('train.csv', 'test.csv')
                print(this.train.head())
                print(this.train.columns)
            elif menu == "3":
                print("### 머신러닝 ###")
                df = api.learning('train.csv', 'test.csv', '서포트벡터머신')
                # 랜덤포레스트분류기: 82.61%
                # 결정트리분류기: 81.82%
                # 로지스틱회귀: 77.89%
                # 서포트벡터머신: 80.7%
            elif menu == "4":
                print("### 배포 ###")
                df = api.submit('train.csv', 'test.csv')
            else:
                print("해당 메뉴 없음")