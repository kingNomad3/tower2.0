import helper as hp

class Projectile:

    def __init__(self, parent, pos_x, pos_y, creep, niveau_tour):
        self.__id = hp.creer_id
        self.__tour = parent
        self.__cible = creep  # Contient un Creep, a chaque fois qu'on attaque, on verifie si la cible existe encore/est encore dans le range, sinon on trouve une nouvelle cible. Permet de passer la cible aux projectiles.
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__niveau = niveau_tour
        self.__rayon_attaque = 4
        self.__vitesse = None
        self.__dommage = None
        self.__angle = hp.calcAngle(self.__pos_x, self.__pos_y, self.__cible.pos_x, self.__cible.pos_y)

    def deplacer(self):
        dist = hp.calcDistance(self.__pos_x, self.__pos_y, self.__cible.pos_x, self.__cible.pos_y)
        if self.__vitesse < dist:
            self.__pos_x, self.__pos_y = hp.getAngledPoint(self.__angle, self.__vitesse, self.__pos_x, self.__pos_y)
        else:
            # frappe le creep vise
            self.attaque_special()
            self.__cible.recoit_coup(self.__dommage)
            self.__tour.liste_projectiles.remove(self)
            
    def attaque_special(self):
        #niveau_tour affectera les effets
        if isinstance(self, Eclair):
            self.__cible.est_electrocute = True
            self.__cible.counter_electrocute = 0
            self.__cible.dmg_electrocute = self.__dommage
        elif isinstance(self, Poison):            
            self.__cible.est_empoisone = True
            self.__cible.dmg_poison = self.__dommage
        elif isinstance(self, Grenade):
            pass

    @property
    def niveau(self):
        return self.__niveau

    @property
    def tour(self):
        return self.__tour

    @property
    def cible(self):
        return self.__cible

    @property
    def dommage(self):
        return self.__dommage

    @property
    def vitesse(self):
        return self.__vitesse

    @property
    def rayon_attaque(self):
        return self.__rayon_attaque

    @rayon_attaque.setter  # Pour les améliorations, si les tours deviennent plus grosses
    def rayon(self, rayon):
        self.__rayon = rayon

    @property
    def pos_x(self):
        return self.__pos_x

    @property
    def pos_y(self):
        return self.__pos_y

    @dommage.setter
    def dommage(self, dommage):
        self.__dommage = dommage  # Pour les améliorations qui réduisent le coût des tours.

    @vitesse.setter
    def vitesse(self, vitesse):
        self.__vitesse = vitesse  # Pour les améliorations qui réduisent le coût des tours.


class Obus(Projectile):

    def __init__(self, parent, pos_x, pos_y, cible, niveau_tour):
        super().__init__(parent, pos_x, pos_y, cible, niveau_tour)
        self.vitesse = 10
        self.dommage = 4 * niveau_tour


class Eclair(Projectile):

    def __init__(self, parent, pos_x, pos_y, cible, niveau_tour ):
        super().__init__(parent, pos_x, pos_y, cible, niveau_tour)
        self.vitesse = 18
        self.dommage = 5 * niveau_tour
        # niveau 3 a determiner
            
class Poison(Projectile):
 def __init__(self, parent, pos_x, pos_y, cible, niveau_tour ):
        super().__init__(parent, pos_x, pos_y, cible, niveau_tour)
        self.vitesse = 8  
        self.dommage = 0.3 * niveau_tour
        
class Balle(Projectile):
 def __init__(self, parent, pos_x, pos_y, cible, niveau_tour ):
        super().__init__(parent, pos_x, pos_y, cible, niveau_tour)
        self.vitesse = 15
        self.dommage = 2 
        
class Grenade(Projectile):
 def __init__(self, parent, pos_x, pos_y, cible, niveau_tour ):
        super().__init__(parent, pos_x, pos_y, cible, niveau_tour)
        self.vitesse = 7 
        self.dommage = 8
        
class Mine(Projectile):
 def __init__(self, parent, pos_x, pos_y, cible, niveau_tour ):
        super().__init__(parent, pos_x, pos_y, cible, niveau_tour)
        self.vitesse = 5 
        self.dommage = 8
        
        
 



#if __name__ == "__main__":



