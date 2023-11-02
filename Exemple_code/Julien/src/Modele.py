from Tour import *
from Creep import *


class Modele:

    def __init__(self, parent):
        self.tour_selectionne = None
        self.liste_creeps_full = False
        self.controleur = parent
        self.niveau = 1
        self.chateau = Chateau()
        self.aire_de_jeu = AireDeJeu()
        self.qte_gold = 120
        self.gameover = False
        self.timer = 0
        self.liste_tours = []
        self.liste_creeps = []
        self.liste_segments = [Segment(4, 0, 6, 18), Segment(6, 16, 10, 18), Segment(10, 3, 12, 18),
                               Segment(12, 3, 27, 5), Segment(25, 5, 27, 10), Segment(18, 8, 27, 10),
                               Segment(18, 10, 20, 18), Segment(20, 16, 26, 18)]
        self.liste_pivots = [[5, 17], [11, 17], [11, 4], [26, 4], [26, 9], [19, 9], [19, 17], [27, 17]]

    def game_timer(self):
        self.timer -= 1

        if self.timer == 0:
            self.niveau += 1
            self.controleur.vue.afficher_niveau()

        self.controleur.vue.afficher_timer()

    def initialiser_niveau(self):
        self.timer = 38
        self.liste_creeps_full = False
        self.liste_creeps = []

    def ajouter_creep(self):
        self.liste_creeps.append(Creep(5, -2, self.niveau, self))

    def bouger_creep(self):
        for creep in self.liste_creeps:
            creep.bouger()
            if creep.pivot_courrant == 8:
                self.retirer_vie(creep)

    def retirer_vie(self, creep):
        self.liste_creeps.remove(creep)
        self.chateau.chatelains -= 1

        if self.chateau.chatelains == 0:
            self.gameover = True

        self.controleur.vue.afficher_vie()

    def creer_tour(self, x, y, type_tour):

        nouvelle_tour = None

        if type_tour == "tour_projectile":
            nouvelle_tour = TourProjectile(self, x, y)
        elif type_tour == "tour_eclair":
            nouvelle_tour = TourEclair(self, x, y)
        elif type_tour == "tour_poison":
            nouvelle_tour = TourPoison(self, x, y)

        if self.verifCoutTour(nouvelle_tour):
            self.liste_tours.append(nouvelle_tour)
            self.qte_gold -= nouvelle_tour.cout
            self.controleur.vue.afficher_argent()
        else:
            nouvelle_tour = None

        return nouvelle_tour

    def supprimer_creep(self):
        for creep in self.liste_creeps:
            if creep.vie <= 0:
                self.qte_gold += creep.valeur_gold
                self.controleur.vue.afficher_argent()
                self.liste_creeps.remove(creep)

    def verifCoutTour(self, tour):
        if self.qte_gold - tour.cout >= 0:
            return True
        else:
            return False

    def update_vie_creep(self):
        for creep in self.liste_creeps:
            self.supprimer_creep()
            creep.update_vie()

    def tour_courante(self, id_tour):
        for tour in self.liste_tours:
            if tour.id == id_tour:
                return tour

    def upgrader_tour(self):
        self.tour_selectionne.upgrade_tour()
        self.qte_gold -= self.tour_selectionne.cout_upgrade



class Segment:

    def __init__(self, x_1, y_1, x_2, y_2):
        self.depart = {"x": x_1, "y": y_1}
        self.arrive = {"x": x_2, "y": y_2}


class Chateau:

    def __init__(self):
        self.chatelains = 20
        self.pos_x = None
        self.pos_y = None


class AireDeJeu:

    def __init__(self):
        self.largeur = 800
        self.hauteur = 600
        self.colonne = 32
        self.ligne = 24
