from Projectile import *
from helper import Helper as hp

class Tour:
    largeur = 20
    
    def __init__(self, parent, rayon, pos_x, pos_y, niveau_amelioration, cout):
        self.__id = hp.creer_id()
        self.__joueur = parent
        self.__rayon = rayon
        self.__champ_action = self.__rayon * 3.5 #TODO Taille exacte du champ d'action à décider. On pourrait se passer en paramètre le multiplicateur au besoin.
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__niveau_amelioration = 1
        self.__cout = cout
        self.__cout_amelioration = self.__cout * self.__niveau_amelioration #TODO Manière de calculer à déterminer. Permettrait de faire en sorte que les améliorations en jeu coûtent moins cher si on réduit son coût.
        self.__cible = None # Contient un Creep, a chaque fois qu'on attaque, on verifie si la cible existe encore/est encore dans le range, sinon on trouve une nouvelle cible. Permet de passer la cible aux projectiles.
        self.__combine = None
        self.__img_src = "./img/pacman.png"
        #self.__vie = vie Si on peut faire perdre de la vie à nos tours
        self.__base = 20 #TODO a verifier avec la VUE
        self.__colonne = 16 #TODO a verifier avec la VUE
        self.ameloriation_permanente()

    @property
    def id(self):
        return self.__id
  
    @property
    def img_src(self):
        return self.__img_src
    
    @property #TODO À voir si on a besoin
    def joueur(self):
        return self.__joueur
    
    @property
    def rayon(self):
        return self.__rayon
    
    @rayon.setter #TODO Pour les améliorations, si les tours deviennent plus grosses
    def rayon(self, rayon):
        self.__rayon = rayon
    
    @property
    def champ_action(self):
        return self.__champ_action
    
    @champ_action.setter #TODO Pour les améliorations, si les champs d'actions deviennent plus larges
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

    @property
    def cout(self):
        return self.__cout
    
    @cout.setter #TODO Pour les améliorations qui réduisent le coût des tours.
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

    @base.setter #TODO voir avec vue si besoin de setter
    def base(self,valeur):
        self.__base = valeur

    @property
    def colonne(self):
        return self.__colonne

    @colonne.setter #TODO voir avec vue si besoin de setter
    def colonne(self,valeur):
        self.__colonne = valeur

    def ameliorer_tour(self):
        if self.verifcation_cout_amelioration():
            self.__niveau_amelioration += 1

    def verifcation_cout_amelioration(self):
        return self.__joueur.partie.argent_courant - self.__cout_amelioration >= 0

    def ameloriation_permanente(self): #TODO dans le modele self.amelioration_perm
        pass

    def verif_tour_voisine(self):
        pass

    # def verif_cible_active(self, cible): # verification si la cible existe encore
    #     if cible:
    #         dist = hp.calcDistance(cible.pos_x, cible.pos_y, self.__pos_x, self.__pos_y)
    #         if dist > self.__champ_action or self.cible.vie == 0 or len(self.__joueur.partie.liste_creeps) == 0:
    #             self.definir_cible()
    #     else:
    #         self.definir_cible()
        

    def activer_combinaison_tour(self):
        pass

    def verif_champ_action(self):
        pass

    def definir_cible(self):
        self.cible = None
        for creep in self.__joueur.partie.liste_creeps:
            dist = hp.calcDistance(creep.pos_x, creep.pos_y, self.__pos_x, self.__pos_y)
            if dist < self.__champ_action:
                self.__cible = creep
                break


class TourAttaque(Tour):
    def __init__(self, parent, rayon, pos_x, pos_y, niveau_amelioration, cout):
        super().__init__(parent, rayon, pos_x, pos_y, niveau_amelioration, cout)
        self.__liste_projectiles = []

        self.__temps_recharge = 1/self.niveau_amelioration * 250 #TODO reviser car toutes les tours ont le meme temps de recharge
        self.__canon = 6 #TODO a verifier avec la VUE
        self.__longueur_canon = 5 #TODO a verifier avec la VUE
        self.__gueule_canon =  (self.pos_x+self.__longueur_canon,self.pos_y) #TODO a verifier avec la VUE
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

    @canon.setter #TODO a voir avec la VUE
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

    def attaque_boost(self):
        pass
        

class TourMitrailleuse(TourAttaque):
    def __init__(self, parent, pos_x, pos_y):
        # p1 : parent, p2 : rayon (le même pour toutes les tours de ce type), p3 et p4 : positions, p5 : niveau 1 en partant (amélioration générale possible??)
        # p6 : coût (amélioration générale possible??), éventuel p7 : vie (si on fait perdre de la vie à nos tours)
        super().__init__(parent, 35, pos_x, pos_y, 1, 300) #TODO a confirmer le rayon et le cout
        self.background_src = "./img/tour_mitrailleuse.png"

    def attaquer(self):
        self.definir_cible()
        if self.cible:
            balle = Balle(self, self.pos_x, self.pos_y,self.cible,self.niveau_amelioration)#TODO verifier si les bonnes variables sont passes
            self.liste_projectiles.append(balle)
        self.joueur.partie.modele.controleur.vue.root.after(int(self.temps_recharge), self.attaquer)


class TourEclair(TourAttaque):
    def __init__(self, parent, pos_x, pos_y):
       super().__init__(parent, 40, pos_x, pos_y, 1, 80)#TODO a confirmer le rayon et le cout
       self.background_src = "./img/tour_eclaire.png"

    def attaquer(self):
        self.definir_cible()
        if self.cible:
            eclair = Eclair(self, self.pos_x, self.pos_y, self.cible,self.niveau_amelioration)#TODO verifier si les bonnes variables sont passes
            self.liste_projectiles.append(eclair)
        self.joueur.partie.modele.controleur.vue.root.after(int(self.temps_recharge), self.attaquer)


class TourPoison(TourAttaque):
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 45, pos_x, pos_y, 1, 80)#TODO a confirmer le rayon et le cout
        self.background_src = "./img/tour_poison.png"

    def attaquer(self):
        self.definir_cible()
        if self.cible:
            poison = Poison(self, self.pos_x,self.pos_y,self.cible,self.niveau_amelioration)  # TODO verifier si les bonnes variables sont passes
            self.liste_projectiles.append(poison)
        self.joueur.partie.modele.controleur.vue.root.after(int(self.temps_recharge) * 5, self.attaquer)

class TourGrenade(TourAttaque):
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 30, pos_x, pos_y, 1, 160) #TODO a confirmer le rayon et le cout
        self.background_src = "./img/tour_grenade.png"

    def attaquer(self):
        self.definir_cible()
        if self.cible:
            grenade = Grenade(self,  self.pos_x,self.pos_y, self.cible, self.niveau_amelioration)  # TODO verifier si les bonnes variables sont passes
            self.liste_projectiles.append(grenade)
        self.joueur.partie.modele.controleur.vue.root.after(int(self.temps_recharge), self.attaquer)


class TourMine(TourAttaque):
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 42, pos_x, pos_y, 1, 100)#TODO a confirmer le rayon et le cout
        self.background_src = "./img/tour_mine.png"

    def attaquer(self):
        self.definir_cible()
        if self.cible:
            mine = Mine(self, self.pos_x,self.pos_y,self.cible,self.niveau_amelioration)  # TODO verifier si les bonnes variables sont passes
            self.liste_projectiles.append(mine)
        self.joueur.partie.modele.controleur.vue.root.after(int(self.temps_recharge), self.attaquer)


class TourCanon(TourAttaque):
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 25, pos_x, pos_y, 1, 150) #TODO a confirmer le rayon et le cout
        self.background_src = "./img/tour_canon.png"

    def attaquer(self):
        self.definir_cible()
        if self.cible:
            obus = Obus(self, self.pos_x,self.pos_y,self.cible,self.niveau_amelioration)  # TODO verifier si les bonnes variables sont passes
            self.liste_projectiles.append(obus)
        self.joueur.partie.modele.controleur.vue.root.after(int(self.temps_recharge), self.attaquer)


class TourArgent(Tour):
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 35, pos_x, pos_y, 1, 160)  # TODO a confirmer le rayon et le cout


class TourRalentissement(Tour):
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 35, pos_x, pos_y, 1, 160)  # TODO a confirmer le rayon et le cout


class TourBoost(Tour):
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 35, pos_x, pos_y, 1, 160)  # TODO a confirmer le rayon et le cout


class TourRepoussante(Tour):
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 35, pos_x, pos_y, 1, 160)  # TODO a confirmer le rayon et le cout
