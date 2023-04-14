# import_exam.py와 calculator.py는 동일한 경로에 위치
# calculator 모듈을 import 
# import calculator
# import calculator as calc   #import 모듈명 as 별칭(namespace이름)
# def plus(i, j):
#     print('abc')
# from calculator import plus  #calculator 모듈에서 plus함수만 import ==> import한 함수는 현재모듈의 namespace에 들어온다.

from calculator import plus, divide   # 하나의 모듈에서 여러개 함수, 클래스들 import


# calculator 모듈의 함수를 호출
# result = calculator.plus(10, 20)
# result = calc.plus(10, 20)   # 별칭을 지정한 경우 별칭으로 호출.

result = plus(100, 300)
# print(calculator.minus(1,21))
result2 = divide(10, 2)
print("덧셈결과:", result)
print('나눗셈결과', result2)
