from Tour import *
from Creep import *
import time
from Chemin import *

# Fonction qui génère un id pour chaque partie qui pourra être envoyé en réseau.
def creer_id():
    pass
    #random.randint(0, 10000)


class Partie:
    ESPACE_CREEP = 1.5
    DUREE_VAGUE = 40
    NOMBRE_CREEPS_VAGUE = 20
    CHOISIR_TOUR = {"TourMitrailleuse":TourMitrailleuse, "TourEclair": TourEclair, "TourPoison": TourPoison, "TourGrenade": TourGrenade, "TourMine":TourMine, "TourCanon": TourCanon, \
        "TourRalentissement": TourRalentissement, "TourRepoussante": TourRepoussante, "TourArgent": TourArgent, "TourBoost": TourBoost }
    
    def __init__(self, parent, tableau, difficulte, seed=id): #Le seed pour randomiser les Creeps de la même façon en réseau.
        self.__tableau = tableau
        self.__difficulte = difficulte
        self.__argent_base = 2000 #TODO a determiner
        self.__argent_courant = self.__argent_base
        self.__modele = parent
        self.__tour_selectionne = None
        self.__vague = 1
        # self.__chateau = Chateau()
        # self.__aire_de_jeu = AireDeJeu() utile?
        self.__fin_partie = False
        self.__chrono = 0
        self.__liste_tours = []
        self.__creeps_en_attente = []
        self.__liste_creeps = []
        self.__pause = False
        self.__creeps_tues = 0      
        #self.liste_creeps_full = False
        #Appartient au modele ou classe Tableau
        self.__chemin = Chemin(self)
        
        self.vie = 20
        self.delta_time = time.time()
        self.temps_derniere_vague = time.time()
        self.creer_creeps()
        
    @property
    def chemin(self):
        return self.__chemin

    @property
    def modele(self):
        return self.__modele
    
    @property
    def vague(self):
        return self.__vague
    
    @property
    def chrono(self):
        return self.__chrono
    
    @property
    def argent_courant(self):
        return self.__argent_courant
    
    @property
    def fin_partie(self):
        return self.__fin_partie
    
    @property
    def liste_creeps(self):
        return self.__liste_creeps
    
    @property
    def liste_tours(self):
        return self.__liste_tours
        

    def creer_tour(self, x, y, tag):
        tour = Partie.CHOISIR_TOUR[tag](self, x, y)
        if self.peut_acheter_tour(tour): 
            self.__liste_tours.append(tour)
            self.__argent_courant -= tour.cout

    def peut_acheter_tour(self, tour) -> bool:
        return self.__argent_courant >= tour.cout 

    def creer_creeps(self):
        self.__creeps_en_attente = [Creep(self, self.__chemin.pivots[0][0], self.__chemin.pivots[0][1],self.__vague) for i in range(Partie.NOMBRE_CREEPS_VAGUE)]

    def creeps_apparaissent(self):
        if self.__creeps_en_attente:
            self.__liste_creeps.append(self.__creeps_en_attente.pop(0))

    def jouer(self):
        # fait apparaître les creeps progressivement
        if self.__creeps_en_attente:
            if len(self.__creeps_en_attente) < 20:
                start = time.time()
                if start - self.delta_time > Partie.ESPACE_CREEP:
                    self.creeps_apparaissent() #TODO a comprendre 
                    self.delta_time = time.time()
            else:
                self.creeps_apparaissent()

        if self.est_game_over():
            print("PERDU") # pour debogage


        for creep in self.__liste_creeps:
            creep.bouger()

        for tour in self.__liste_tours: # Les tours d'attaque sont des fonctions récursives 
            for projectile in tour.liste_projectiles:
                projectile.deplacer()

        self.remove_creep()
        # self.remove_obus()
        
        if (maintenant := time.time()) - self.temps_derniere_vague >= Partie.DUREE_VAGUE:
            self.temps_derniere_vague = maintenant
            self.prochaine_vague()
            
        
        
    def perte_vie(self):
        # châtelains...
        self.vie -= 1
        print(self.vie)

    def prochaine_vague(self):
        # pour chaque nouvelle vague
        self.__vague += 1
       
        self.creer_creeps()

    def est_game_over(self) -> bool:
        # met le bool à jour et le retourne
        self.__fin_partie = self.vie < 1
        return self.__fin_partie

    def remove_creep(self):
        for creep in self.__liste_creeps:
            if not creep.vivant:
                self.__liste_creeps.remove(creep)

    # def remove_obus(self):
    #     for tour in self.tours:
    #         for i in tour.obus:
    #             if not i.vivant:
    #                 tour.obus.remove(i)