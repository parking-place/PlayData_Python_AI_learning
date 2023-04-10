def print_hello():
    print("Hello, Python!")

def print_hi():
    print("Hi, Python!")
    
class Person :
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def print_info(self):
        print("이름 : ", self.name)
        print("나이 : ", self.age)