from person import person

class Adult(person):
    def __init__(self, name, age, weight, height,):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


    def smd(self):
        if self.age >= 18:
            print("your age is greater than 18")
        else:
            print("your age is lower than 18")

    def smw(self):
        if self.weight <= 60:
            print("your are avarage weight")
        elif 60 < self.weight < 100:
            print("you are a little fat")
        else:
            print("your Obese")








