class Animal:

    def sound(selfself,):
        print("sound of the animal")

class Dog(Animal):

    def sound(self):
        print("woof!")

class Cat(Animal):

    def sound(self):
        print("Meow!")

animal1 = Animal()
animal1.sound()


animal2 = Dog()
animal2.sound()

animal3 = Cat()
animal3.sound()