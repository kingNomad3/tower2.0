from helper import Helper as hp


class Creep:

    def __init__(self, parent, pos_x, pos_y, niveau):
        self.__cible = None
        self.__angle_target = None

        self.__est_empoisone = False
        self.__est_electrocute = False
        self.__counter_electrocute = None

        self.__dmg_poison = None
        self.__dmg_electrocute = None

        self.__modele = parent
        self.__vie = 10 * niveau
        self.valeur_gold = 20 * niveau
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__vitesse = 0.15
        self.__taille = 0.5
        self.__segment_actuel = 0
        self.nouvelle_target()

    def bouger(self):
        self.x, self.y = hp.Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)

        dist = hp.Helper.calcDistance(self.__pos_x, self.__pos_y, self.__cible[0], self.__cible[1])

        if dist < self.vitesse:
            self.__pos_x = self.__cible[0]
            self.__pos_y = self.__cible[1]
            self.segment_actuel += 1
            if self.segment_actuel <= 7:
                self.chercher_cible()

            # arrive au chateau
            elif self.segment_actuel == 8:
                self.parent.perte_vie()
                self.vivant = False

    def nouvelle_target(self):
        x = self.parent.chemin.segments[self.segment_actuel][1][0]
        y = self.parent.chemin.segments[self.segment_actuel][1][1]

        self.angle = hp.Helper.calcAngle(self.x, self.y, x, y)
        self.cible = [x, y]

    def update_vie(self):
        if self.est_empoisone:
            self.vie -= self.dmg_poison

        if self.est_electrocute:
            self.counter_electrocute += 1
            self.vie -= self.dmg_electrocute

        if self.counter_electrocute == 3:
            self.est_electrocute = False
            
    @property
    def target(self):
        return self.cible

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
    def counter_electrocute(self):
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
    def pivot_courrant(self):
        return self.__pivot_courrant

    @property
    def pos_x(self):
        return self.__pos_x

    @property
    def pos_y(self):
        return self.__pos_y

    @est_electrocute.setter
    def vitesse(self, est_electrocute):
        self.__est_electrocute = est_electrocute  # Pour les améliorations qui réduisent le coût des tours.
    
    @counter_electrocute.setter
    def counter_electrocute(self, counter_electrocute):
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
