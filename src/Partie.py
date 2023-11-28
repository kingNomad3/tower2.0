from Tour import *
from Creep import *
import time

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
        # self.__chateau = Chateau()
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
        


    def creer_tour(self, x, y):
        tour = TourMitrailleuse(x, y, self)
        
        if self.peut_acheter_tour(tour): 
            self.__liste_tours.append(tour)
            self.__argent_courant -= tour.cout

    def peut_acheter_tour(self, tour) -> bool:#TODO À ajuste
        if (self.__liste_tours):
            return self.__argent_courant >= tour.cout 
        else:
            return True

    def creer_creeps(self):
        self.creeps_queue = [Creep(self.chemin.pivots[0][0], self.chemin.pivots[0][1], self) for i in range(self.nombre_creep_vague)]

    def creeps_apparaissent(self):
        if self.creeps_queue:
            self.creeps.append(self.creeps_queue.pop(0))

    def jouer(self):
        # fait apparaître les creeps progressivement
        if self.creeps_queue:
            if len(self.creeps_queue) < 20:
                start = time.time()
                if start - self.delta_time > Partie.ESPACE_CREEP:
                    self.creeps_apparaissent()
                    self.delta_time = time.time()
            else:
                self.creeps_apparaissent()

        if self.est_game_over():
            print("PERDU") # pour debogage


        for creep in self.creeps:
            creep.jouer()

        for tour in self.tours:
            tour.jouer()

        self.remove_creep()
        self.remove_obus()
        
        if (maintenant := time.time()) - self.temps_derniere_vague >= Partie.DUREE_VAGUE:
            self.temps_derniere_vague = maintenant
            self.prochaine_vague()
        
        
    def perte_vie(self):
        # châtelains...
        self.vie -= 1

    def prochaine_vague(self):
        # pour chaque nouvelle vague
        self.vague += 1
        self.creeps = []
        self.creer_creeps()

    def est_game_over(self) -> bool:
        # met le bool à jour et le retourne
        self.gameover = self.vie < 1
        return self.gameover


    def prochain_niveau(self):
        self.vague += 1
        self.creer_creeps()

    def remove_creep(self):
        for i in self.creeps:
            if not i.vivant:
                self.creeps.remove(i)

    def remove_obus(self):
        for tour in self.tours:
            for i in tour.obus:
                if not i.vivant:
                    tour.obus.remove(i)