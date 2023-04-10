# %%writefile 파일경로  -> cell의 내용을 파일로 저장.

# 모듈 버전을 저장하는 변수
__version__ = 1.0

def plus(num1, num2):
    return num1 + num2

def minus(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    if num2 != 0:
        return num1 / num2
    else:
        print("num2는 0이외의 숫자를 넣으세요.")

