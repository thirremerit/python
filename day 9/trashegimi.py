class Kurrizore:
    def __init__(self, ka_kurriz=True):
        self.ka_kurriz = ka_kurriz

        def info_Kurrizor(self):
            print("kan kurriz")

class ujore:
    def __init__(self, habitat="uje"):
        self.habitat = habitat

        def info_ujrore(self):
            print("jetojn ne uje")


class Peshku (Kurrizore,ujore):
    def __init__(self, looji, habitat="uje" , ka_kurriz=True):
        super().__init__(ka_kurriz=ka_kurriz)
        self.habitat = habitat
        self.looji =looji


        def info(self):
            print(f" {self.looji}jetojn ne uje{self.habitat}")

        def noton(self):
            print("peshku noton")

peshku = Peshku("peshku i arte")

print(peshku,ka_kurriz)
print(peshku.habitat)

peshku.info_peshku()
peshku.info_ujrore
peshku.noton()
peshku.info_kurrizor()