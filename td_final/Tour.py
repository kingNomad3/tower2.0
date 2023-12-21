from Projectile import *
from helper import Helper as hp
import random

class Tour:
    largeur = 20
    
    def __init__(self, parent, rayon, pos_x, pos_y, niveau_amelioration, cout):
        self.__id = hp.creer_id()
        self.__joueur = parent
        self.__rayon = rayon
        self.__niveau_amelioration = 1
        self.__champ_action = self.__rayon * 3.5
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__cout = cout
        self.__cout_amelioration = self.__cout * self.__niveau_amelioration 
        self.__cible = None # Contient un Creep, a chaque fois qu'on attaque, on verifie si la cible existe encore/est encore dans le range, sinon on trouve une nouvelle cible. Permet de passer la cible aux projectiles.
        self.__combine = None
        self.__img_src = f'./img/pacman_{self.__niveau_amelioration}.png'

    @property
    def id(self):
        return self.__id
  
    @property
    def img_src(self):
        return self.__img_src
    
    @property 
    def joueur(self):
        return self.__joueur
    
    @property
    def rayon(self):
        return self.__rayon
    
    @rayon.setter 
    def rayon(self, rayon):
        self.__rayon = rayon
    
    @property
    def champ_action(self):
        return self.__champ_action
    
    @champ_action.setter 
    def champ_action(self, champ_action):
        self.__champ_action = champ_action
    
    @property
    def pos_x(self):
        return self.__pos_x
    
    @property
    def pos_y(self):
        return self.__pos_y
    
    @property
    def niveau_amelioration(self):
        return self.__niveau_amelioration
    
    @niveau_amelioration.setter
    def niveau_amelioration(self, niveau_amelioration):
        self.__niveau_amelioration = niveau_amelioration
        self.__champ_action = self.__rayon * 3.5 * 1.15
        self.__img_src = f'./img/pacman_{self.__niveau_amelioration}.png'

    @property
    def cout(self):
        return self.__cout
    
    @cout.setter 
    def cout(self, cout):
        self.__cout = cout
        
    @property
    def cout_amelioration(self):
        return self.__cout_amelioration
    
    @property
    def cible(self):
        return self.__cible
    
    @cible.setter
    def cible(self, cible):
        self.__cible = cible
        
    @property
    def combine(self):
        return self.__combine
    
    @combine.setter
    def combine(self, combine):
        self.__combine = combine

    @property
    def base(self):
        return self.__base

    @base.setter 
    def base(self,valeur):
        self.__base = valeur

    @property
    def colonne(self):
        return self.__colonne

    @colonne.setter 
    def colonne(self,valeur):
        self.__colonne = valeur


    def verifcation_cout_amelioration(self):
        return self.__joueur.partie.argent_courant - self.__cout_amelioration >= 0

    def definir_cible(self):
        self.cible = None
        for creep in self.__joueur.partie.liste_creeps:
            dist = hp.calcDistance(creep.pos_x, creep.pos_y, self.__pos_x, self.__pos_y)
            if dist < self.__champ_action:
                self.__cible = creep
                break


class TourAttaque(Tour):
    def __init__(self, parent, rayon, pos_x, pos_y, temps_recharge, niveau_amelioration, cout):
        super().__init__(parent, rayon, pos_x, pos_y, niveau_amelioration, cout)
        self.__liste_projectiles = []

        self.__temps_recharge = temps_recharge/self.niveau_amelioration * 250 
        self.__canon = 6 
        self.__longueur_canon = 5 
        self.__gueule_canon =  (self.pos_x+self.__longueur_canon,self.pos_y) 
        self.attaquer()

    @property
    def liste_projectiles(self):
        return self.__liste_projectiles
    
    @liste_projectiles.setter
    def liste_projectiles(self, liste): # Passer dans la liste en 1er élément quel projectile on veut puis en 2e élément si on veut ajouter ou retirer.
        try:
            element, action = liste
            if action == "ajouter":
                self.__liste_projectiles.append(element)
            else:
                self.__liste_projectiles.remove(element)
        except:
            raise Exception('La liste doit avoir 2 paramètres : le projectile et l\'action à réaliser.')
    
    @property 
    def temps_recharge(self):
        return self.__temps_recharge
    
    @temps_recharge.setter
    def temps_recharge(self, temps):
        self.__temps_recharge = temps

    @property
    def canon(self):
        return self.__canon

    @canon.setter 
    def canon(self,valeur):
        self.__canon = valeur

    @property
    def longueur_canon(self):
        return self.__longueur_canon

    @longueur_canon.setter
    def longueur_canon(self,valeur):
        self.__longueur_canon = valeur\

    @property
    def gueule_canon(self):
        return self.__gueule_canon

    @gueule_canon.setter
    def gueule_canon(self,valeur):
        self.__gueule_canon = valeur


class TourMitrailleuse(TourAttaque):
    COUT = 600
    def __init__(self, parent, pos_x, pos_y):
        # p1 : parent, p2 : rayon (le même pour toutes les tours de ce type), p3 et p4 : positions, p5 : niveau 1 en partant (amélioration générale possible??)
        # p6 : coût (amélioration générale possible??), éventuel p7 : vie (si on fait perdre de la vie à nos tours)
        super().__init__(parent, 35, pos_x, pos_y, 1, 1, 600) 
        self.background_src = "./img/tour_mitrailleuse.png"

    def attaquer(self):
        self.definir_cible()
        if self.cible:
            balle = Balle(self, self.pos_x, self.pos_y,self.cible,self.niveau_amelioration)
            self.liste_projectiles.append(balle)
        self.joueur.partie.modele.controleur.vue.root.after(int(self.temps_recharge), self.attaquer)


class TourEclair(TourAttaque):
    COUT = 1000
    def __init__(self, parent, pos_x, pos_y):
       super().__init__(parent, 40, pos_x, pos_y, 7, 1, 1000)
       self.background_src = "./img/tour_eclair.png"

    def attaquer(self):
        self.definir_cible()
        if self.cible:
            eclair = Eclair(self, self.pos_x, self.pos_y, self.cible,self.niveau_amelioration)
            self.liste_projectiles.append(eclair)
        self.joueur.partie.modele.controleur.vue.root.after(int(self.temps_recharge), self.attaquer)


class TourPoison(TourAttaque):
    COUT = 800
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 50, pos_x, pos_y, 5, 1, 800)
        self.background_src = "./img/tour_poison.png"

    def attaquer(self):
        self.definir_cible()
        if self.cible:
            poison = Poison(self, self.pos_x,self.pos_y,self.cible,self.niveau_amelioration)  
            self.liste_projectiles.append(poison)
        self.joueur.partie.modele.controleur.vue.root.after(int(self.temps_recharge) * 2, self.attaquer)


class TourGrenade(TourAttaque):
    COUT = 2000
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 50, pos_x, pos_y, 10, 1, 2000) 
        self.background_src = "./img/tour_grenade.png"

    def attaquer(self):
        self.definir_cible()
        if self.cible:
            grenade = Grenade(self,  self.pos_x,self.pos_y, self.cible, self.niveau_amelioration)  
            self.liste_projectiles.append(grenade)
        self.joueur.partie.modele.controleur.vue.root.after(int(self.temps_recharge), self.attaquer)


class TourMine(TourAttaque):
    COUT = 1800
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 40, pos_x, pos_y, 12, 1, 1800)
        self.background_src = "./img/tour_mine.png"

    def attaquer(self):
        pos_x = random.randint(self.pos_x - self.champ_action, self.pos_x + self.champ_action)
        pos_y = random.randint(self.pos_y - self.champ_action, self.pos_y + self.champ_action)
        canvas = self.joueur.partie.modele.controleur.vue.canvas
        largeur = Projectile.largeur - 10

        temp = canvas.find_overlapping(pos_x - largeur,
                                            pos_y - largeur,
                                            pos_x + largeur,
                                            pos_y + largeur)

        chemins = canvas.find_withtag("chemin")


        while not any(i in temp for i in chemins):
            pos_x = random.randint(self.pos_x - self.champ_action, self.pos_x + self.champ_action)
            pos_y = random.randint(self.pos_y - self.champ_action, self.pos_y + self.champ_action)

            temp = canvas.find_overlapping(pos_x - Projectile.largeur, pos_y - Projectile.largeur, pos_x + Projectile.largeur,
                                    pos_y + Projectile.largeur)

        mine = Mine(self, pos_x, pos_y, self.cible, self.niveau_amelioration)
        self.liste_projectiles.append(mine)
        self.joueur.partie.modele.controleur.vue.root.after(int(self.temps_recharge), self.attaquer)


class TourCanon(TourAttaque):
    COUT = 3000
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 60, pos_x, pos_y, 15, 1, 3000) 
        self.background_src = "./img/tour_canon.png"

    def attaquer(self):
        self.definir_cible()
        if self.cible:
            obus = Obus(self, self.pos_x,self.pos_y,self.cible,self.niveau_amelioration) 
            self.liste_projectiles.append(obus)
        self.joueur.partie.modele.controleur.vue.root.after(int(self.temps_recharge), self.attaquer)


class TourArgent(Tour):
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 35, pos_x, pos_y, 1, 160)  


class TourRalentissement(Tour):
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 35, pos_x, pos_y, 1, 160)  


class TourBoost(Tour):
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 35, pos_x, pos_y, 1, 160) 


class TourRepoussante(Tour):
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 35, pos_x, pos_y, 1, 160) 