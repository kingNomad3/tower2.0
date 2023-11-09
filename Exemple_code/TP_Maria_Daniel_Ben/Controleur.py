from Vue import *
from Modele import *

class Controleur:
    def __init__(self):
        self.temps = 0
        self.vague = 1
        self.vies = 20
        self.argent = 50
        self.modele = Modele(self)
        self.vue = Vue(self, self.modele)
        self.vue.root.after(500, self.boucler_travail)
        self.vue.root.mainloop()


    def boucler_travail(self):
        if self.vies:
            self.modele.travailler()
            self.vue.afficher_modele()
            self.vue.root.after(50, self.boucler_travail)
            self.temps += 50
            if self.argent >= 25:
                if self.modele.tour_a_creer != -1 and self.modele.x and self.modele.y:
                    self.modele.creer_tour()
                    self.argent -= 25
            self.nouvelle_partie()
            self.vue.afficher_tours()
            self.vue.afficher_obus()
            self.vue.afficher_laser()
            for i in self.modele.tours:
                if i.cible_courante:
                    i.attaquer_cible()
                else:
                    i.chercher_cible(self.temps)


    def nouvelle_partie(self):
        if len(self.modele.creeps) == 0:
            pass
        if self.temps % 30000 == 0:
            self.modele.compteur = 0
            self.temps = 0
            self.vague += 1