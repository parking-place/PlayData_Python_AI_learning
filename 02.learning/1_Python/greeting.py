
def print_greeting():
    print("안녕하세요")
    
def get_greeting(name):
    return f"{name}님 안녕하세요"

class Person:
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __str__(self):
        return f"name: {self.name}, age: {self.age}"
