from Chemin import *
from Creep import *
from Tour_laser import *
from Tour_poison import Tour_poison
from Tour_projectile import Tour_projectile


class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.creeps = []
        self.chemin = Chemin()
        self.tours = []
        self.temps = self.parent.temps
        self.compteur = 0
        self.x = None
        self.y= None
        self.tour_a_creer = -1
        self.tour_a_upgrade = -1

    def creer_creeps(self):
        creep = Creep(self)
        self.creeps.append(creep)

    def creer_tour(self):
        tour = None
        self.tour_a_upgrade = 1
        if self.x and self.y:
            if self.tour_a_creer == 0:
                tour = Tour_laser(self, self.x, self.y)
            elif self.tour_a_creer == 1:
                tour = Tour_projectile(self, self.x, self.y)
            elif self.tour_a_creer == 2:
                tour = Tour_poison(self, self.x, self.y)
        if tour:
            self.tours.append(tour)
            self.tour_a_creer = -1
            self.x = None
            self.y = None

    def tour_a_upgrade(self):
        pass

    def travailler(self):
        if self.parent.temps % 500 == 0 and self.compteur < 20:
            self.creer_creeps()
            self.compteur += 1
        for i in self.creeps:
            i.mouvement_creep()
            i.am_i_alive()
            if not i.is_alive:
                self.creeps.remove(i)
                if not i.a_tue:
                    self.parent.argent += 5
                if i.a_tue:
                    self.parent.vies -= 1