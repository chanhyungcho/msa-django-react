import numpy as np
import pandas as pd
import random
import string
from sqlalchemy import create_engine

class B_userService(object):
    def __init__(self):
        pass

    def create_users(self):

        number_of_strings = 99
        length_of_string = 8
        for x in range(number_of_strings):
            result =(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string)))


            # 1과 100  사이의 random 한 값 생성하기
            email = f'{result}@gmail.com'
            nickname = result
            password = random.randint(1, 100)
            # DataFrame에 특정 정보를 이용하여 data 채우기
            df = df.append(pd.DataFrame([email,nickname,password], columns=['email','nickname','password']), ignore_index=True)

        print(df)
        return df

    def conn_db(self):
        df = self.create_users()
        #jdbc:mysql://localhost:3306/mydb
        engine = create_engine(
            "mysql+pymysql://root:root@localhost:3306/mydb",
            encoding='utf-8')
        df.to_sql(name='b_users',
                  if_exists='append',
                  con=engine,
                  index=False)

        # email_list = b_users.objects.values_list("email", flat=True)
        # if b_users.objects.filter(email=data["email"]).exists():
        #     return ~~


stroke_menu = ["Exit",  # 0
               "create_users",# 1
               "show_csv" #2
               ]
stroke_lambda = {
    "1": lambda x: x.create_users(),
    "2": lambda x: x.conn_db(),

}
if __name__ == '__main__':
    stroke = B_userService()
    while True:
        [print(f"{i}. {j}") for i, j in enumerate(stroke_menu)]
        menu = input('메뉴선택: ')
        if menu == '0':
            print("종료")
            break
        else:
            try:
                stroke_lambda[menu](stroke)
            except KeyError as e:
                if 'some error message' in str(e):
                    print('Caught error message')
                else:
                    print("Didn't catch error message")




