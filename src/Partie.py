from Tour import *
from Creep import *

# Fonction qui génère un id pour chaque partie qui pourra être envoyé en réseau.
def creer_id():
    pass
    #random.randint(0, 10000)


class Partie:

    def __init__(self, tableau, difficulte, parent, seed=id): #Le seed pour randomiser les Creeps de la même façon en réseau.
        self.__tableau = tableau
        self.__difficulte = difficulte
        self.__argent_base = 2000 #TODO a determiner
        self.__argent_courant = None
        self.__modele = parent
        self.__tour_selectionne = None
        self.__vague = 1
        self.__chateau = Chateau()
        # self.__aire_de_jeu = AireDeJeu() utile?
        self.__fin_partie = False
        self.__chrono = 0
        self.__liste_tours = []
        self.__liste_creeps = []
        self.__pause = False
        self.__creeps_tues = 0      
        #self.liste_creeps_full = False
        #Appartient au modele ou classe Tableau
        self.liste_pivots = [[5, 17], [11, 17], [11, 4], [26, 4], [26, 9], [19, 9], [19, 17], [27, 17]]
        

# Modèle va avoir ses actions dans sa liste et appelera sur la partie quoi faire.

#     def game_timer(self):
#         self.__chrono -= 1

#         if self.__chrono == 0:
#             self.__vague += 1
#             self.__modele.vue.afficher_niveau()

#         self.__modele.vue.afficher_timer()

#     def initialiser_niveau(self):
#         self.__chrono = 38
#         self.liste_creeps_full = False
#         self.__liste_creeps = []

#     def ajouter_creep(self):
#         self.__liste_creeps.append(Creep(5, -2, self.__vague, self))

#     def bouger_creep(self):
#         for creep in self.__liste_creeps:
#             creep.bouger()
#             if creep.pivot_courrant == 8:
#                 self.retirer_vie(creep)

#     def retirer_vie(self, creep):
#         self.__liste_creeps.remove(creep)
#         self.__chateau.chatelains -= 1

#         if self.__chateau.chatelains == 0:
#             self.__fin_partie = True

#         self.__modele.vue.afficher_vie()

#     def creer_tour(self, x, y, type_tour):

#         nouvelle_tour = None

#         if type_tour == "tour_projectile":
#             nouvelle_tour = TourProjectile(self, x, y)
#         elif type_tour == "tour_eclair":
#             nouvelle_tour = TourEclair(self, x, y)
#         elif type_tour == "tour_poison":
#             nouvelle_tour = TourPoison(self, x, y)

#         if self.verifCoutTour(nouvelle_tour):
#             self.__liste_tours.append(nouvelle_tour)
#             self.__argent_courant -= nouvelle_tour.cout
#             self.__modele.vue.afficher_argent()
#         else:
#             nouvelle_tour = None

#         return nouvelle_tour

#     def supprimer_creep(self):
#         for creep in self.__liste_creeps:
#             if creep.vie <= 0:
#                 self.__argent_courant += creep.valeur_gold
#                 self.__modele.vue.afficher_argent()
#                 self.__liste_creeps.remove(creep)

#     def verifCoutTour(self, tour):
#         if self.__argent_courant - tour.cout >= 0:
#             return True
#         else:
#             return False

#     def update_vie_creep(self):
#         for creep in self.__liste_creeps:
#             self.supprimer_creep()
#             creep.update_vie()

#     def tour_courante(self, id_tour):
#         for tour in self.__liste_tours:
#             if tour.id == id_tour:
#                 return tour

#     def upgrader_tour(self):
#         self.__tour_selectionne.upgrade_tour()
#         self.__argent_courant -= self.__tour_selectionne.cout_upgrade



# class Segment:

#     def __init__(self, x_1, y_1, x_2, y_2):
#         self.depart = {"x": x_1, "y": y_1}
#         self.arrive = {"x": x_2, "y": y_2}


# class Chateau:

#     def __init__(self):
#         self.chatelains = 20
#         self.pos_x = None
#         self.pos_y = None


# class AireDeJeu:

#     def __init__(self):
#         self.largeur = 800
#         self.hauteur = 600
#         self.colonne = 32
#         self.ligne = 24
