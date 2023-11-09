import random

import helper as hp
from Obus import *

numero_id = 0
def prochain_id():
    global numero_id
    numero_id += 1
    return "tour_projectile" + str(numero_id)

class Tour_projectile():
    def __init__(self, parent, x, y):
        self.x = x
        self.y = y
        self.parent = parent
        self.rayon = 200
        self.dommage = 20
        self.fire_rate = 500
        self.cible_courante = None
        self.obus = None
        self.creeps_trop_loin = True
        self.cible_possible = []
        self.niveau = 1
        self.active = True
        self.compteur_recharge = 500
        self.id= prochain_id()


    def chercher_cible(self, temps):
         self.cible_courante = None
         for i in self.parent.creeps:
            distance = hp.Helper.calcDistance(self.x, self.y, i.dimensions["x1"], i.dimensions["y1"])
            if distance <= self.rayon:
                self.cible_possible.append(i)
                self.creeps_trop_loin = False
         if len(self.cible_possible) == 0:
             return False
         else:
            self.cible_courante = random.choice(self.cible_possible)
            self.cible_possible = []
            return True

    def attaquer_cible(self):
            if self.obus:
                collision = self.obus.voyage_cible()
                if collision:
                    self.cible_courante.vie -= self.dommage
                    self.parent.parent.vue.effacer_obus(self.obus)
                    self.obus = None
                    if self.cible_courante.vie <= 0 or hp.Helper.calcDistance(self.x, self.y, self.cible_courante.dimensions["x1"], self.cible_courante.dimensions["y1"]) >= self.rayon or self.creeps_trop_loin:
                        self.cible_courante = None
            else:
                if self.recharge_tir():
                    self.compteur_recharge = 0
                    self.obus = Obus(self)


    def recharge_tir(self):
        self.compteur_recharge += 20
        if hp.Helper.calcDistance(self.x, self.y, self.cible_courante.dimensions["x1"],
                                  self.cible_courante.dimensions["y1"]) >= self.rayon:
            self.creeps_trop_loin = True
        return self.compteur_recharge >= self.fire_rate


    def augmenter_niveau(self):
        if self.niveau < 3:
            self.niveau += 1
            self.dommage += 2