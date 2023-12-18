import helper as hp
import random
from effetVisuel import *
from PIL import Image


class Creep:
    largeur = 45
    
    def __init__(self, parent, pos_x, pos_y, niveau):
        self.__id = hp.Helper.creer_id()
        self.__cible = None
        self.__angle_target = None
        self.__partie = parent
        self.__valeur_argent = 2
        self.__est_empoisone = False
        self.__est_electrocute = False
        self.__compteur_electrocute = None
        self.__dmg_poison = None
        self.__dmg_electrocute = None
        self.__vivant = True
        self.__modele = parent
        self.__vie = 10 * niveau
        self.valeur_gold = 20 * niveau
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__vitesse = 5
        self.__taille = 1
        self.__segment_actuel = 0
        self.__img_src = self.definir_img_src()
        self.definir_attribut()
        self.nouvelle_cible()
        self.__explosion = None
        
        
    def definir_attribut(self):
        attributs = ("poison", "relentissement", "electrocution")
        self.__attribut = attributs[random.randint(0,len(attributs)-1)] if random.random() < 0.05 else None

    def bouger(self):
        self.__pos_x, self.__pos_y = hp.Helper.getAngledPoint(self.__angle_target, self.__vitesse, self.__pos_x, self.__pos_y)
        
        dist = hp.Helper.calcDistance(self.__pos_x, self.__pos_y, self.__cible[0], self.__cible[1])
        # print(len(self.__partie.chemin.segments)[1])
        if dist < self.__vitesse:
            self.__pos_x = self.__cible[0]
            self.__pos_y = self.__cible[1]
            self.__segment_actuel += 1
            if self.__segment_actuel < len(self.__partie.chemin.segments):
                self.nouvelle_cible()

            # arrive au chateau
            elif self.__segment_actuel == len(self.__partie.chemin.segments):
                self.__partie.perte_vie()

                self.__vivant = False
                
    def recoit_coup(self, dommage):
        self.__vie -= dommage
        if self.__vie <= 0:
            self.__vivant = False
            self.__partie.argent_courant += self.valeur_argent
            self.__explosion = Explosion(self, self.__pos_x,self.__pos_y)


    def nouvelle_cible(self):
        x = self.__partie.chemin.segments[self.segment_actuel][1][0]
        y = self.__partie.chemin.segments[self.segment_actuel][1][1]

        self.__angle_target = hp.Helper.calcAngle(self.__pos_x, self.__pos_y, x, y)
        self.__cible = [x, y]

    def maj_vie(self):
        if self.__est_empoisone:
            if self.__cible.attribut is "poison":
                self.dmg_poison /= 2
            self.vie -= self.dmg_poison
            
        if self.__est_electrocute:
            self.__compteur_electrocute += 1
            if self.__cible.attribut is "electrocution":
                self.__compteur_electrocute +=1 
            self.__vie -= self.dmg_electrocute

        # if self.__compteur_electrocute == 3:
        #     self.est_electrocute = False
        pass
    
    def definir_img_src(self):
        random_src = random.randint(0,3)
        return f'./img/creep_{random_src}.png'
            
    @property
    def img_src(self):
        return self.__img_src
    
    @property
    def cible(self):
        return self.__cible
    
    @property
    def valeur_argent(self):
        return self.__valeur_argent
    
    @property
    def partie(self):
        return self.__partie
    
    @property
    def vivant(self):
        return self.__vivant
    
    @property
    def attribut(self):
        return self.__attribut

    @property
    def angle_target(self):
        return self.__angle_target

    @property
    def est_empoisone(self):
        return self.__est_empoisone

    @property
    def est_electrocute(self):
        return self.__est_electrocute

    @property
    def vitesse(self):
        return self.__vitesse
    @property
    def dmg_poison(self):
        return self.__dmg_poison
    @property
    def dmg_electrocute(self):
        return self.__dmg_electrocute
    @property
    def vitesse(self):
        return self.__vitesse    

    @property
    def compteur_electrocute(self):
        return self.__counter_electrocute
    @property
    def modele(self):
        return self.__modele
    @property
    def vie(self):
        return self.__vie
    @property
    def taille(self):
        return self.__taille
    @property
    def segment_actuel(self):
        return self.__segment_actuel

    @property
    def pos_x(self):
        return self.__pos_x

    @property
    def pos_y(self):
        return self.__pos_y
    
    @property
    def id(self):
        return self.__id

    @est_electrocute.setter
    def est_electrocute(self, est_electrocute):
        self.__est_electrocute = est_electrocute  # Pour les améliorations qui réduisent le coût des tours.
    
    @vie.setter
    def vie(self, vie):
        self.__vie = vie
        
    @taille.setter
    def taille(self, taille):
        self.__taille = taille
        
    @valeur_argent.setter
    def valeur_argent(self, valeur_argent):
        self.__valeur_argent = valeur_argent
    
    
    @compteur_electrocute.setter
    def compteur_electrocute(self, counter_electrocute):
        self.__counter_electrocute = counter_electrocute  # Pour les améliorations qui réduisent le coût des tours.

    @dmg_electrocute.setter
    def dmg_electrocute(self, dmg_electrocute):
        self.__dmg_electrocute = dmg_electrocute  # Pour les améliorations qui réduisent le coût des tours.

    @est_empoisone.setter
    def est_empoisone(self, est_empoisone):
        self.__est_empoisone = est_empoisone  # Pour les améliorations qui réduisent le coût des tours.

    @dmg_poison.setter
    def dmg_poison(self, dmg_poison):
        self.__dmg_poison = dmg_poison  # Pour les améliorations qui réduisent le coût des tours.




class Mini_Creep(Creep):

    def __init__(self, parent, pos_x, pos_y, niveau):
        super().__init__(self, parent, pos_x, pos_y, niveau)
        self.vie /= 2 
        self.vitesse *= 2
        
        
class Super_Creep(Creep):

    def __init__(self, parent, pos_x, pos_y, niveau):
        super().__init__(self, parent, pos_x, pos_y, niveau)
        self.vie *= 1.5
        self.vitesse /= 2
        self.taille = 2
        self.__niveau = niveau
        
    def faire_mini_creeps(self):
        for _ in range(3):
            c = Mini_Creep(self, self.pos_x, self.pos_y, self.__niveau)
            self.partie.liste_creeps.append(c)
        



# if __name__ == "__main__":
#     c = Creep(None, 20, 20, 1)
#     print(c.attribut)