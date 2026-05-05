class Personi:

    def __init__(self, emri,vitlindjes, gjinia):
        self.emri=emri
        self.vitlindjes = vitlindjes
        self.gjinia = gjinia


     def prezantimi(self):
         print(f"un jam {self.emri},")

    def sayHi(self):
        print(f"hello from {self.emri},")
