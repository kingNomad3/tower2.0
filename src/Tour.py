

from Exemple_code.Julien.src.Projectile import Poison
from Projectile import *
from helper import Helper as hp

no_id = 0

def creer_id():
    global no_id
    no_id += 1
    return "id_" + str(no_id)

class Tour():

    def __init__(self, parent, rayon, pos_x, pos_y, niveau_amelioration, cout):
        self.__id = creer_id()
        self.__partie = parent
        self.__rayon = rayon
        self.__champ_action = self.__rayon * 3.5 # Taille exacte du champ d'action à décider. On pourrait se passer paramètre le multiplicateur au besoin.
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__niveau_amelioration = niveau_amelioration
        self.__cout = cout
        self.__cout_amelioration = self.__cout * self.__niveau_amelioration # Manière de calculer à déterminer. Permettrait de faire en sorte que les améliorations en jeu coûtent moins cher si on réduit son coût.
        self.__cible = None # Contient un Creep, a chaque fois qu'on attaque, on verifie si la cible existe encore/est encore dans le range, sinon on trouve une nouvelle cible. Permet de passer la cible aux projectiles.
        self.__combine = None
        #self.__vie = vie Si on peut faire perdre de la vie à nos tours
        self.__base = 20 #TODO a verifier avec la VUE
        self.__colonne = 16 #TODO a verifier avec la VUE

    
    @property
    def id(self):
        return self.__id
    
    @property # À voir si on a besoin
    def partie(self):
        return self.__partie
    
    @property
    def rayon(self):
        return self.__rayon
    
    @rayon.setter() # Pour les améliorations, si les tours deviennent plus grosses
    def rayon(self, rayon):
        self.__rayon = rayon
    
    @property
    def champ_action(self):
        return self.__champ_action
    
    @champ_action.setter # Pour les améliorations, si les champs d'actions deviennent plus larges
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
    def niveau_amelioration(self, niveau):
        self.__niveau_amelioration = niveau # Au cas où avec une amélioration, on pourrait améliorer plus d'un niveau
        
    @property
    def cout(self):
        return self.__cout
    
    @cout.setter
    def cout(self, cout):
        self.__cout = cout # Pour les améliorations qui réduisent le coût des tours.
        
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





   
    # def ameliorer_tour(self):
    #     if self.__cout_amelioration():
    #         self.__niveau_amelioration += 1
    #
    #         # self.est_upgrade = True
    #
    # def ameloriation_permanente(self):
    #     pass
    #
    # def verif_tour_voisine(self):
    #     pass
    #
    # def verif_cible_active(self, cible): # verification si la cible existe encore
    #     dist = hp.calcDistance(cible.pos_x, cible.pos_y, self.__pos_x, self.__pos_y)
    #     if dist > self.__champ_action or self.cible.vie == 0 or len(self.__partie.liste_creeps) == 0:
    #         self.__cible = None
    #
    # def activer_combinaison_tour(self):
    #     pass
    #
    # def definir_cible(self):
    #     for creep in self.__partie.liste_creeps:
    #         dist = hp.calcDistance(creep.pos_x, creep.pos_y, self.__pos_x, self.__pos_y)
    #         if dist < self.__champ_action:
    #             self.__cible = creep
    #
            


class TourAttaque(Tour):
    def __init__(self, parent, rayon, pos_x, pos_y, niveau_amelioration, cout,dommage):
        super().__init__(parent, rayon, pos_x, pos_y, niveau_amelioration, cout)
        self.__liste_projectiles = []
        self.__temps_recharge = 1/self.__niveau_amelioration * 100 #TODO reviser car toutes les tours ont le meme temps de recharge
        self.__dommage = dommage

        self.__canon = 6 #TODO a verifier avec la VUE
        self.__longueur_canon = 5 #TODO a verifier avec la VUE
        self.__gueule_canon =  (self.__pos_x+self.__longueur_canon,self.__pos_y) #TODO a verifier avec la VUE



        # self.attaquer()

    
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
    def dommage(self):
        return self.__dommage

    @dommage.setter
    def dommage(self,valeur):
        self.__dommage = valeur

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
        
        
    # def attaquer(self):
    #     if self.__cible is None:
    #         self.definir_cible()
    #     elif self.__cible:
    #         balle = Balle(self, self.__cible, self.__pos_x, self.__pos_y)
    #         self.__liste_projectiles.append(balle)
    #
    #     if self.__cible:
    #         self.update_target(self.__cible)
    #
    #
    #     self.__partie.modele.controleur.vue.root.after(self.__temps_recharge, self.attaquer) # Confirmer la chaine d'appel vers le root.
    #
    # def attaque_boost(self):
    #     pass
        
        
    

class TourMitrailleuse(TourAttaque):
    def __init__(self, parent, pos_x, pos_y):
        # p1 : parent, p2 : rayon (le même pour toutes les tours de ce type), p3 et p4 : positions, p5 : niveau 1 en partant (amélioration générale possible??)
        # p6 : coût (amélioration générale possible??), éventuel p7 : vie (si on fait perdre de la vie à nos tours)
        super().__init__(parent, 25, pos_x, pos_y, 1, 300, 15) #TODO a confirmer le rayon et le cout, dommage


    



  

    # def augmenter_niveau(self):
    #     self.niveau += 1
    #
    # def update_position_balles(self):
    #     for projectile in self.liste_projectiles:
    #         projectile.update_position()
    #
    #
    #
    #
    # def verifCoutUpgrade(self):
    #     if self.modele.qte_gold - self.cout_upgrade >= 0:
    #         return True
    #     else:
    #         return False


class TourEclair(TourAttaque):
    def __init__(self, parent, pos_x, pos_y):
       super().__init__(parent, 25, pos_x, pos_y, 1, 80,10)#TODO a confirmer le rayon et le cout, dommage



    # def attaquer(self):
    #     if self.target is None:
    #         self.definir_cible()
    #     elif not self.target.est_electrocute:
    #         eclair = Eclair(self, self.niveau, self.target, self.pos_x, self.pos_y)
    #         self.liste_projectiles.append(eclair)
    #
    #     if self.target:
    #         self.update_target(self.target)
    #
    # def definir_cible(self):
    #     for creep in self.modele.liste_creeps:
    #         dist = hp.calcDistance(creep.pos_x * 25, creep.pos_y * 25, self.pos_x, self.pos_y)
    #         if dist < self.rayon_action:
    #             self.target = creep
    #
    # def update_target(self, target):
    #     dist = hp.calcDistance(target.pos_x * 25, target.pos_y * 25, self.pos_x, self.pos_y)
    #     if dist > self.rayon_action or self.target.vie == 0 or len(self.modele.liste_creeps) == 0:
    #         self.target = None
    #
    # def augmenter_niveau(self):
    #     self.niveau += 1
    #
    # def update_position_balles(self):
    #     for projectile in self.liste_projectiles:
    #         projectile.update_position()
    #
    # def upgrade_tour(self):
    #     if self.verifCoutUpgrade():
    #         self.augmenter_niveau()
    #
    #         self.recharge = 0  # si le niveau est 2 ou 3, laser continu
    #         self.est_upgrade = True
    #
    # def verifCoutUpgrade(self):
    #     if self.modele.qte_gold - self.cout_upgrade >= 0:
    #         return True
    #     else:
    #         return False


class TourPoison(TourAttaque):
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 25, pos_x, pos_y, 1, 80,80)#TODO a confirmer le rayon et le cout, dommage


    # def attaquer(self):
    #     if self.target is None:
    #         self.definir_cible()
    #     elif not self.target.est_empoisone:
    #         poison = Poison(self, self.niveau, self.target, self.pos_x, self.pos_y)
    #         self.liste_projectiles.append(poison)
    #
    #     if self.target:
    #         self.update_target(self.target)
    #
    # def definir_cible(self):
    #     for creep in self.modele.liste_creeps:
    #         dist = hp.calcDistance(creep.pos_x * 25, creep.pos_y * 25, self.pos_x, self.pos_y)
    #         if dist < self.rayon_action:
    #             self.target = creep
    #
    # def update_target(self, target):
    #     dist = hp.calcDistance(target.pos_x * 25, target.pos_y * 25, self.pos_x, self.pos_y)
    #     if dist > self.rayon_action or self.target.vie == 0 or len(self.modele.liste_creeps) == 0:
    #         self.target = None
    #
    # def augmenter_niveau(self):
    #     self.niveau += 1
    #
    # def update_position_balles(self):
    #     for projectile in self.liste_projectiles:
    #         projectile.update_position()
    #
    # def upgrade_tour(self):
    #     if self.verifCoutUpgrade():
    #         self.augmenter_niveau()
    #
    #         if self.niveau == 2:
    #             self.recharge = self.recharge / 1.5  # temps de recharge plus rapide dans niveaux 2 et 3
    #
    #         self.est_upgrade = True
    #
    #
    #
    # def verifCoutUpgrade(self):
    #     if self.modele.qte_gold - self.cout_upgrade >= 0:
    #         return True
    #     else:
    #         return False

class TourGrenade(TourAttaque):
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 35, pos_x, pos_y, 1, 160,80) #TODO a confirmer le rayon et le cout, dommage

class TourMine(TourAttaque):
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 42, pos_x, pos_y, 1, 100,100)#TODO a confirmer le rayon et le cout, dommage


class TourCanon(TourAttaque):
    def __init__(self, parent, pos_x, pos_y):
        super().__init__(parent, 100, pos_x, pos_y, 1, 150,800)#TODO a confirmer le rayon et le cout, dommage


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



