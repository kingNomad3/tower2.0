import helper as hp
import random
from Obus import *

numero_id = 0
def prochain_id():
    global numero_id
    numero_id += 1
    return "tour_poison" + str(numero_id)

class Tour_poison():
    def __init__(self, parent, x, y):
        self.x = x
        self.y = y
        self.parent = parent
        self.rayon = 200
        self.dommage = 1
        self.fire_rate = 1000
        self.temps_poison = 2000
        self.cible_courante = None
        self.obus = None
        self.creeps_trop_loin = True
        self.cible_possible = []
        self.niveau = 1
        self.active = True
        self.compteur_recharge = 500
        self.id = prochain_id()


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
                    self.cible_courante.empoisonne = True
                    self.parent.parent.vue.effacer_obus(self.obus)
                    self.obus = None
                    if self.cible_courante.vie <= 0 or hp.Helper.calcDistance(self.x, self.y, self.cible_courante.dimensions["x1"], self.cible_courante.dimensions["y1"]) >= self.rayon or self.creeps_trop_loin:
                        self.cible_courante = None
            else:
                if self.recharge_tir():
                    self.compteur_recharge = 0
                    self.obus = Obus(self)
            self.dommage_poison()


    def recharge_tir(self):
        self.compteur_recharge += 20
        if hp.Helper.calcDistance(self.x, self.y, self.cible_courante.dimensions["x1"],
                                  self.cible_courante.dimensions["y1"]) >= self.rayon:
            self.creeps_trop_loin = True
        return self.compteur_recharge >= self.fire_rate

    def dommage_poison(self):
        if self.cible_courante:
            if self.cible_courante.empoisonne:
                self.temps_poison -= 20
                self.cible_courante.vie -= self.dommage
                if self.cible_courante.vie <= 0:
                    self.cible_courante = None
                if self.temps_poison == 0:
                    self.cible_courante.empoisonne = False
                    self.temps_poison = 2000


    def augmenter_niveau(self):
        if self.niveau < 3:
            self.niveau += 1
            self.dommage += 3