import random
import helper as hp


def rgb_to_hex( r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

class Explosion():
    def __init__(self,parent,x,y):
        self.parent = parent
        self.x = x
        self.y = y
        self.nuages = []
        self.creer_nuages()

    def creer_nuages(self):
        n = random.randrange(12,20)
        for i in range(n):
            nuage = Nuage(self,self.x,self.y)
            self.nuages.append(nuage)

    def jouer_coup(self):
        for i in self.nuages:
            i.jouer_coup()

    def supprimer_nuage(self,nuage):
        if nuage in self.nuages:
            self.nuages.remove(nuage)
            if self.nuages ==  []:
                self.parent.supprimer_explosion(self)

class Nuage():
    def __init__(self,parent,x,y):
        self.id = hp.Helper.creer_id()
        self.parent = parent
        self.vitesse = random.randrange(3)+1
        nl = 20
        nl2 = int(nl / 2)
        self.x = x+random.randrange(nl)-nl2
        self.y = y+random.randrange(nl)-nl2
        self.largemax = random.randrange(10,45)
        self.img_src = f'./img/polygone_{random.randint(1,3)}.png'
        self.large = 2
        self.x1 = self.x - self.large
        self.x2 = self.x + self.large
        self.y1 = self.y - self.large
        self.y2 = self.y + self.large

    def jouer_coup(self):
        self.x1 = self.x - self.large
        self.x2 = self.x + self.large
        self.y1 = self.y - self.large
        self.y2 = self.y + self.large
        self.large += self.vitesse
        if self.large > self.largemax:
            self.parent.supprimer_nuage(self)