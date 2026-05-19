class person:
    def __init__(self,name,age,weight,height):
        self.name=name
        self.age=age
        self.weight = weight
        self.height = height


def smd(self):
    if self.age >= 18:
        print("your age is greater than 18")
    else:
        print("your age is lower than 18")