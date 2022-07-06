class Menu():
    def __init__(self):
        self.name = ['ビール', '唐揚げ', '枝豆']
        self.price = ['500', '600', '300']
        
    def getName(self, id):
        return self.name[id]
    
    def getPrice(self, id):
        return self.price[id]