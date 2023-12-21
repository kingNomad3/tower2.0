from Tour import *
from Creep import *
import time
from Chemin import *

import json


class Partie:
    ESPACE_CREEP = 1.5
    DUREE_VAGUE = 40
    NOMBRE_CREEPS_VAGUE = 20
    CHOISIR_TOUR = {"TourMitrailleuse":TourMitrailleuse, "TourEclair": TourEclair, "TourPoison": TourPoison, "TourGrenade": TourGrenade, "TourMine":TourMine, "TourCanon": TourCanon, \
        "TourRalentissement": TourRalentissement, "TourRepoussante": TourRepoussante, "TourArgent": TourArgent, "TourBoost": TourBoost }
    
    def __init__(self, parent, difficulte, joueurs, tableau=0, seed=id): #Le seed pour randomiser les Creeps de la même façon en réseau.
        self.__tableau = tableau
        self.__difficulte = difficulte
        self.__argent_base = 1250
        self.__argent_courant = self.__argent_base
        self.__modele = parent
        self.__tour_selectionne = None
        self.__vague = 0
        self.max__vague = 50 + ((difficulte - 1) * 25)
        self.score = 0
        self.__fin_partie = False
        self.__chrono = None
        self.__creeps_en_attente = []
        self.__liste_creeps = []
        self.actions_a_faire = {}        
        self.__pause = False
        self.nuages = []
        self.joueurs = {}
        self.creeps_tue_vague = 0

        for i in joueurs:
            self.joueurs[i] = Joueur(self,i)
        self.explosions = []

        self.__chemin = Chemin(self, self.__tableau)

        self.vie = 100 - ((difficulte - 1) * 25)
        self.delta_time = time.time()
        self.temps_derniere_vague = time.time()
        self.prochaine_vague()
        
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

    @chrono.setter
    def chrono(self, value):
        self.__chrono += value/1000
    
    @property
    def argent_courant(self):
        return self.__argent_courant

    @argent_courant.setter  
    def argent_courant(self, montant):
        self.__argent_courant = montant
    
    @property
    def fin_partie(self):
        return self.__fin_partie
    
    @property
    def liste_creeps(self):
        return self.__liste_creeps
    
    @property
    def liste_tours(self):
        return self.__liste_tours
    
    @property
    def tableau(self):
        return self.__tableau
    @tableau.setter
    def tableau(self, value):
        self.__tableau = value

    def creer_creeps(self):
        self.__creeps_en_attente = [Creep(self, self.__chemin.pivots[self.__tableau][0][0], self.__chemin.pivots[self.__tableau][0][1], self.__vague, self.__difficulte) for i in range(Partie.NOMBRE_CREEPS_VAGUE)]

    def creeps_apparaissent(self):
        if self.__creeps_en_attente:
            self.__liste_creeps.append(self.__creeps_en_attente.pop(0))

        
    def perte_vie(self):
        # châtelains...
        self.vie -= 1

    def prochaine_vague(self):
        # pour chaque nouvelle vague
        self.__vague += 1
        self.__chrono = 0
        self.creer_creeps()
        if self.__vague > 1:
            nom = self.__modele.controleur.nom_joueur_local
            self.__modele.controleur.agent_bd.ajouter_aux_defis(nom,  self.creeps_tue_vague)
            self.score += self.__vague * self.creeps_tue_vague + 50
            self.creeps_tue_vague = 0

    def est_game_over(self) -> bool:
        # met le bool à jour et le retourne
        self.__fin_partie = self.vie < 1
        return self.__fin_partie

    def remove_creep(self):
        for creep in self.__liste_creeps:
            if not creep.vivant:
                if creep.vie <= 0:
                    self.creeps_tue_vague += 1
                self.__liste_creeps.remove(creep)
    
     #############################################################################
    # ATTENTION : NE PAS TOUCHER
    def ajouter_actions_a_faire(self, iteration,actionsrecues):
        for i in actionsrecues:
            iteration_cle = i[0]
            if (iteration - 1) > int(iteration_cle):
                print("PEUX PASSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
            action = json.loads(i[1])
            if action:
                if iteration_cle not in self.actions_a_faire.keys():
                    self.actions_a_faire[iteration_cle] = action
                else:
                    for j in action:
                        self.actions_a_faire[iteration_cle].append(j)

    ##############################################################################

    def jouer_coup(self, iteration):
        ##################################################################
        # faire nouvelle action recu du serveur si on est au bon cadrecourant
        # ATTENTION : NE PAS TOUCHER
        if iteration in self.actions_a_faire:
            for i in self.actions_a_faire[iteration]:
                if (i[1] == "activer_partie"):
                    self.modele.controleur.vue.activer_partie_reseau()
                else:
                    self.joueurs[i[0]].actions[i[1]](i[2])

        # Gestion des creeps
        if self.__creeps_en_attente:
            start = time.time()
            if start - self.delta_time > Partie.ESPACE_CREEP:
                self.creeps_apparaissent() #TODO a comprendre
                self.delta_time = time.time()

        for creep in self.__liste_creeps:
            creep.bouger()
            creep.maj_vie()
            if creep.vie <= 0:
                creep.vivant = False
                self.__argent_courant += creep.valeur_argent

        for nom_joueur in self.joueurs: # Les tours d'attaque sont des fonctions récursives 
            for tour in self.joueurs[nom_joueur].tours:
                for projectile in tour.liste_projectiles:
                    projectile.deplacer()

        # Gestion des explosions
        for i in self.explosions:
            i.jouer_coup()

        self.remove_creep()
        
        if (maintenant := time.time()) - self.temps_derniere_vague >= Partie.DUREE_VAGUE and not self.__liste_creeps:
            self.temps_derniere_vague = maintenant
            if not self.est_game_over():
                self.prochaine_vague()

    def supprimer_explosion(self, explosion):
        if explosion in self.explosions:
            self.explosions.remove(explosion)

    def supprimer_nuage(self, nuage):
        if nuage in self.nuages:
            self.nuages.remove(nuage)
            if self.nuages ==  []:
                self.parent.supprimer_explosion(self)

class Joueur():
    def __init__(self,parent,nom):
        self.partie = parent
        self.nom_joueur = nom
        
        self.tours = []
        self.actions ={"creer_tour":self.creer_tour,
                        "ameliorer_tour": self.ameliorer_tour,
                    #    "vendre_tour":None
                    }
            
    def creer_tour(self, parametres):
        tag, x, y = parametres
        tour = Partie.CHOISIR_TOUR[tag](self, x, y)
        if self.peut_acheter_tour(tour): 
            self.tours.append(tour)
            self.partie.argent_courant = self.partie.argent_courant - tour.cout
    
    def peut_acheter_tour(self, tour) -> bool:
        return self.partie.argent_courant >= tour.cout 
    
    def peut_acheter_amelioration(self, tour) -> bool:
        return self.partie.argent_courant >= tour.cout_amelioration
    
    def ameliorer_tour(self, parametres):
        tag = parametres[0]
        for tour in self.tours:
            if tour.id == tag:
                if self.peut_acheter_amelioration(tour):
                    if tour.niveau_amelioration < 3:
                        tour.niveau_amelioration += 1
                        self.partie.argent_courant = self.partie.argent_courant - tour.cout_amelioration
        