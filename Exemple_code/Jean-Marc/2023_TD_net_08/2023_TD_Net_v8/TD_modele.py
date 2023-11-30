
import random
from helper import Helper as hp
import json

# fonction pour generer des id uniques pour les objets
# sert a lier les dessins du canevas aux objets qui sont dans le modele
def creer_id():
    if not hasattr(creer_id,'no_id'):
        creer_id.no_id = 0
    creer_id.no_id += 1
    return "id_"+str(creer_id.no_id)

# fonction pour creer des couleurs RGB en faisant varier les nombres
# utiliser dans la fonction de creation ds entites constituant un nuage
# qui est le resultat d'une explosion lorsqu'un projectile atteint sa cible
def rgb_to_hex( r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

class Joueur():
    def __init__(self,parent,nom):
        self.parent = parent
        self.nom_joueur = nom
        self.tours = {"tour":[],
                      "poison":[]
                      }
        self.actions ={"ajouter_tour":self.ajouter_tour,
                       "ajouter_poison":self.ajouter_poison,
                       "ameliorer_tour":None,
                       "vendre_tour":None}

    def ajouter_poison(self,params):
        print("PAS IMPLANTE")
        self.parent.parent.afficher_message("PAS IMPLANTE")

    def ajouter_tour(self,param):
        x,y = param
        tour = Tour(self,x,y)
        self.tours["tour"].append(tour)
        self.parent.parent.dessiner_tour(tour)

    def jouer_coup(self):
        for val in self.tours["tour"]:
            val.jouer_coup()

class Tour():
    base = 20
    colonne = 16
    canon = 6
    def __init__(self,parent,x,y):
        self.parent = parent
        self.mon_id = creer_id()
        self.x = x
        self.y = y
        self.force = 3
        self.long_canon = 16
        self.gueule_canon = (x+self.long_canon,self.y)
        self.etendu = 100
        self.delai_tir_max = 4
        self.delai_tir = 0
        self.cible = None
        self.mes_obus = []

    def get_cible(self):
        liste_pos = []
        for i in self.parent.parent.creeps_actifs:
            dist = hp.calcDistance(self.x,self.y,i.x,i.y)
            if dist <= self.etendu:
                liste_pos.append(i)
        if liste_pos:
            cible_choisie= random.choice(liste_pos)
            angle_cible = hp.calcAngle(self.x,self.y,cible_choisie.x,cible_choisie.y)
            self.gueule_canon = hp.getAngledPoint(angle_cible, self.long_canon, self.x, self.y)
        else:
            cible_choisie = None
        return cible_choisie

    def jouer_coup(self): # attaquer
        if not self.cible:
            self.cible = self.get_cible()
        if self.cible:
            dist = hp.calcDistance(self.x,self.y,self.cible.x,self.cible.y)
            if dist >= self.etendu:
                self.cible = None
            elif self.cible and self.delai_tir <= 0 : # pcq si on a pas de cible on decremente quand meme
                o = Obus(self,self.cible)
                self.mes_obus.append(o)
                self.delai_tir = self.delai_tir_max
                self.cible = None
            else:
                self.delai_tir -= 1
        for i in self.mes_obus:
            i.jouer_coup()

class Obus():
    taille = 3
    def __init__(self,parent: Tour, cible):
        self.parent = parent
        self.cible = cible
        self.x = self.parent.gueule_canon[0]
        self.y = self.parent.gueule_canon[1]
        self.x_cible = self.cible.x
        self.y_cible = self.cible.y
        self.angle = hp.calcAngle(self.x,self.y,self.x_cible,self.y_cible)
        self.vitesse = 12

    def jouer_coup(self):
        dist = hp.calcDistance(self.x, self.y, self.x_cible, self.y_cible)
        if self.vitesse < dist :
            self.x, self.y = hp.getAngledPoint(self.angle, self.vitesse, self.x, self.y)
        else:
            # frappe le creep vise
            self.cible.recoit_coup(self.parent.force)
            self.parent.mes_obus.remove(self)

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
        self.parent = parent
        self.vitesse = random.randrange(3)+1
        nl = 20
        nl2 = int(nl / 2)
        self.x = x+random.randrange(nl)-nl2
        self.y = y+random.randrange(nl)-nl2
        self.largemax = random.randrange(10,30)
        self.couleur = rgb_to_hex(random.randrange(220,240), random.randrange(5,220), 3)
        #return '#{:02x}{:02x}{:02x}'.format(r, g, b)
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

class TourPoison():
    base = 20
    colonne = 16
    canon = 6
    def __init__(self,x,y):
        self.partie = partie
        self.mon_id = creer_id()
        self.x = x
        self.y = y
        self.force = 3
        self.long_canon = 16
        self.gueule_canon = (x+self.long_canon,self.y)
        self.etendu = 100
        self.delai_tir_max = 4
        self.delai_tir = 0
        self.cible = None
        self.mes_poisons = [] # liste de pouchePoison projete

    def get_cible(self):
        liste_pos = []
        for i in self.partie.creeps_actifs:
            dist = hp.calcDistance(self.x,self.y,i.x,i.y)
            if dist <= self.etendu:
                liste_pos.append(i)
        if liste_pos:
            cible_choisie= random.choice(liste_pos)
            angle_cible = hp.calcAngle(self.x,self.y,cible_choisie.x,cible_choisie.y)
            self.gueule_canon = hp.getAngledPoint(angle_cible, self.long_canon, self.x, self.y)
        else:
            cible_choisie = None
        return cible_choisie

    def jouer_coup(self): # attaquer
        if not self.cible:
            self.cible = self.get_cible()
        if self.cible:
            dist = hp.calcDistance(self.x,self.y,self.cible.x,self.cible.y)
            if dist >= self.etendu:
                self.cible = None
            elif self.cible and self.delai_tir <= 0 : # pcq si on a pas de cible on decremente quand meme
                o = PouchePoison(self,self.cible)
                self.mes_poisons.append(o)
                self.delai_tir = self.delai_tir_max
                self.cible = None
            else:
                self.delai_tir -= 1
        for i in self.mes_poisons:
            i.jouer_coup()

class PouchePoison(): # projectile poison, comme un jet
    taille = 3
    def __init__(self,parent: Tour, cible):
        self.parent = parent
        self.cible = cible
        self.x = self.parent.gueule_canon[0]
        self.y = self.parent.gueule_canon[1]
        self.x_cible = self.cible.x
        self.y_cible = self.cible.y
        self.angle = hp.calcAngle(self.x,self.y,self.x_cible,self.y_cible)
        self.vitesse = 12
        self.force = 1

    def jouer_coup(self):
        dist = hp.calcDistance(self.x, self.y, self.x_cible, self.y_cible)
        if self.vitesse < dist :
            self.x, self.y = hp.getAngledPoint(self.angle, self.vitesse, self.x, self.y)
        else:
            # frappe le creep vise
            self.cible.recoit_poison(self.parent.force)
            self.parent.mes_poisons.remove(self)

class Creep():
    taille = 10 # attribut de classe
    mana = 4
    def __init__(self, parent):
        self.parent = parent
        self.no_segment_courant = 0
        self.segment_courant = self.parent.chemin.segments[0]
        self.vitesse = 4
        self.empoisonne = 0
        self.mana = Creep.mana + self.parent.niveau
        self.x = self.segment_courant[0][0]
        self.y = self.segment_courant[0][1]
        self.x_cible = self.segment_courant[1][0]
        self.y_cible = self.segment_courant[1][1]
        self.angle = hp.calcAngle(self.x, self.y, self.x_cible, self.y_cible)

    def jouer_coup(self):
        self.x,self.y = hp.getAngledPoint(self.angle,self.vitesse, self.x, self.y)
        dist = hp.calcDistance(self.x, self.y, self.x_cible, self.y_cible)

        if int(dist) <= self.vitesse:
            self.no_segment_courant+=1
            if self.no_segment_courant<len(self.parent.chemin.segments):
                self.segment_courant=self.parent.chemin.segments[self.no_segment_courant]
                self.x_cible = self.segment_courant[1][0]
                self.y_cible = self.segment_courant[1][1]
                self.angle = hp.calcAngle(self.x, self.y, self.x_cible, self.y_cible)
            else:
                print("un creep rendu)")
                self.parent.vie -= 1
                if self.parent.vie < 1:
                    self.parent.terminer_partie()
                    return
                self.parent.supprimer_creep(self)

    def recoit_coup(self,force):
        self.mana -= force
        if self.mana < 1 :
            self.parent.supprimer_creep(self)

    def recoit_poison(self,force):
        self.empoisonne -= force
        if self.empoisonne < 1 :
            self.parent.supprimer_creep(self)

class Germe(Creep):
    taille = 2
    def __init__(self,parent):
        nl =24
        nl2 = int(nl/2)
        Creep.__init__(self, parent)
        self.vitesse = random.randrange(5)+9
        self.x = self.segment_courant[0][0] +random.randrange(nl)-nl2
        self.y = self.segment_courant[0][1] +random.randrange(nl)-nl2
        self.x_cible = self.segment_courant[1][0] +random.randrange(nl)-nl2
        self.y_cible = self.segment_courant[1][1] +random.randrange(nl)-nl2
        self.angle = hp.calcAngle(self.x, self.y, self.x_cible, self.y_cible)

    def jouer_coup(self):
        self.x,self.y = hp.getAngledPoint(self.angle,self.vitesse, self.x, self.y)
        dist = hp.calcDistance(self.x, self.y, self.x_cible, self.y_cible)

        if int(dist) <= self.vitesse:
            self.no_segment_courant+=1
            if self.no_segment_courant<len(self.parent.chemin.segments):
                self.segment_courant=self.parent.chemin.segments[self.no_segment_courant]
                nl = 24
                nl2 = int(nl / 2)
                self.x_cible = self.segment_courant[1][0]+random.randrange(nl)-nl2
                self.y_cible = self.segment_courant[1][1]+random.randrange(nl)-nl2
                self.angle = hp.calcAngle(self.x, self.y, self.x_cible, self.y_cible)
            else:
                self.parent.supprimer_germe(self)

class Chemin():
    def __init__(self,parent):
        self.parent = parent
        self.pivots = [[0,200],
                         [300,200],
                         [300,100],
                         [600,100],
                         [600,500],
                         [700,500],
                         [700,100],
                         [200,400],
                         [900,400]]
        self.segments = []
        self.creer_segments(self.pivots)

    def creer_segments(self,pivots):
        self.segments=[]
        deb=pivots[0]
        for i in pivots[1:]:
            self.segments.append([deb,i])
            deb=i

class Partie():
    def __init__(self, parent, joueurs):
        self.parent = parent
        self.largeur = 900
        self.hauteur = 600
        self.chemin = Chemin(self)
        self.actions_a_faire = {}
        self.parent.joueurs = joueurs
        self.vie = 100000
        self.pointage = 0
        self.niveau = 0
        self.creeps_en_attente = []
        self.creeps_actifs = []
        self.germes = []
        self.joueurs = {}
        for i in joueurs:
            self.joueurs[i] = Joueur(self,i)
        self.poisons = []
        self.explosions = []
        self.delai_lancement_max = 3
        self.delai_lancement = 0
        self.creer_prochain_niveau()

    def terminer_partie(self):
        self.parent.terminer_partie()

    def supprimer_explosion(self, explosion):
        if explosion in self.explosions:
            self.explosions.remove(explosion)

    def supprimer_germe(self, germe):
        if germe in self.germes:
            self.germes.remove(germe)

    def supprimer_creep(self, creep):
        if creep in self.creeps_actifs:
            explo = Explosion(self, creep.x, creep.y)
            self.explosions.append(explo)
            self.creeps_actifs.remove(creep)
            self.pointage += 1
            if len(self.creeps_en_attente) == 0 and len(self.creeps_actifs) == 0:
                self.creer_prochain_niveau()

    def creer_prochain_niveau(self):
        self.niveau += 1
        for i in range(20, 50):
            self.creeps_en_attente.append(Creep(self))

    def jouer_coup(self, iteration):
        ##################################################################
        # faire nouvelle action recu du serveur si on est au bon cadrecourant
        # ATTENTION : NE PAS TOUCHER
        if iteration in self.actions_a_faire:
            for i in self.actions_a_faire[iteration]:
                self.joueurs[i[0]].actions[i[1]](i[2])
        ##################################################################
        # Gestion des creeps
        for i in self.creeps_actifs:
            i.jouer_coup()

        if self.creeps_en_attente and self.delai_lancement < 1:
            creep = self.creeps_en_attente.pop(0)
            self.creeps_actifs.append(creep)
            self.delai_lancement = self.delai_lancement_max
        else:
            self.delai_lancement -= 1

        # Gestion des germes
        for i in self.germes:
            i.jouer_coup()
        chance = random.randrange(3)
        if chance == 0:
            nb_germe = random.randrange(0, 2)
            for i in range(nb_germe):
                self.germes.append(Germe(self))

        # Gestion des explosions
        for i in self.explosions:
            i.jouer_coup()

        for i in self.joueurs:
            self.joueurs[i].jouer_coup()

    def terminer_partie(self):
        self.parent.pause = 1
        # self.parent.afficher_fin()

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

class Modele():
    def __init__(self, parent):
        self.parent = parent

    def lancer_partie(self,joueurs):
        return Partie(self.parent,joueurs)

