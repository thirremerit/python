from Kerri import Kerri


class KerriElektrik(Kerri):

    def __init__(self,emri,viti,modeli,bateria):
        super(),__init__(emri,viti,modeli)
        self.bateria=bateria

        def mbusheBaterin(self):
            print("mbushe Baterin")