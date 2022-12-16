from dataclasses import dataclass

@dataclass
class OOP:
    x = 30

    def foo(self):
        x = self.x
        print("OOP 출력: "+str(x))
x = 10
def foo():
    global x
    x = x + 20
    print("FP 출력: "+str(x))

def local_error():
    x=10
    def local_error_b():
        x=20

    local_error_b()
    print(x)

def funct_nonlocal():
    x = 10
    def funct_nonlocal_b():
        nonlocal x
        x=20

    funct_nonlocal_b()
    print(x)

def in_fn():
    x=10
    y=100
    def b():
        x = 20
        def c():
            nonlocal x
            nonlocal y
            x= x+30
            y = y+300
            print(x)
            print(y)
        c()
    b()
in_fn()

x=1


def gl_key():
    x = 10
    def nextkey():
        x = 20
        def quick():
            global x
            x = x + 30
            print(x)
        quick()
    nextkey()
gl_key()


def Closure():
    a=3
    b=5
    t = 0

    def mul_add(x):
        nonlocal t
        t = t + (a*x+b)
        print("클로저 1 결과:" + str(t))


    def mul_add_2(x):
        nonlocal t
        t = t + (a*x-b)
        print("클로저 2 결과:" + str(t))
    return {'1:':mul_add,'2':mul_add_2}

if __name__ == '__main__':
    f = OOP()
    f.foo()
    foo()
    local_error()
    funct_nonlocal()
    in_fn()
    print("전역출력: "+str(x))
    c = Closure()
    print("클로저1:"+ str(c['1:'](2)))
    print("클로저2:"+ str(c['2:'](2)))


'''
def closure_lambda():
    a=3
    b=5
    return lambda x: a*x+b
d = closure_lambda()
print(d(1),d(2),d(3),d(4),d(5))


def closure_nonlocal():
    a=3
    b=5
    total = 0
    def mul_ad(x):
        nonlocal total
        total = total + a * x + b
        print(total)
    return mul_ad
cn = closure_nonlocal()
cn(1)
cn(2)
cn(3)'''