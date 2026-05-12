class Student:
    def __init__(self,name,age):
        self.__name=name
        self.__age=age

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @name.setter
    def name(self,name):
        self.__name=name

    @age.setter
    def name(self,age):
        self.__age=age


studenti = Student("Edeni",17)

print(studenti.name)
print(studenti.age)

studenti.name = "666"


print(studenti.name)
print(studenti.age)