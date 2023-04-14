
# 현재 모듈(import_exam2.py)에서 다른패키지의 모듈을(my_package.greeting.py) 호출
# import my_package.greeting

# my_package.greeting.print_greeting()
# txt = my_package.greeting.get_greeting("홍길동")
# print("인사말:", txt)

# p = my_package.greeting.Person("이순신", 30)
# print(p)

# import my_package.greeting as gr  # 별칭을 이용해서 namespace를 간단하게 정의
# gr.print_greeting()
# p = gr.Person("유관순", 20)
# print(p)

# from my_package import greeting as gr
# gr.print_greeting()
# p = gr.Person("유관순", 40)
# print(p)

# 패키지/모듈/특정함수,클래스
# from my_package.greeting  import Person

# p = Person("강감찬", 15)
# print(p)

# my_pacakge.greeting 모듈의 모든 함수/클래스들을 import 해서 namespace 없이 호출하겠다.
from my_package.greeting  import *
print_greeting()
print(get_greeting('이름이름'))
p =  Person("이름", 20)
print(p)
