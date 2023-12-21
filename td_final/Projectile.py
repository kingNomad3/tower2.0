import helper as hp

class Projectile:
    largeur = 3
    
    def __init__(self, parent, pos_x, pos_y, creep, niveau_tour):
        self.__tour = parent
        self.__id = hp.Helper.creer_id()
        self.__cible = creep  # Contient un Creep, a chaque fois qu'on attaque, on verifie si la cible existe encore/est encore dans le range, sinon on trouve une nouvelle cible. Permet de passer la cible aux projectiles.
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__niveau = niveau_tour
        self.__rayon_attaque = 4
        self.__vitesse = None
        self.__dommage = None
    
    def deplacer(self):
        if isinstance(self, Mine):
            for creep in self.tour.joueur.partie.liste_creeps:
                dist = hp.Helper.calcDistance(creep.pos_x, creep.pos_y, self.__pos_x, self.__pos_y)
                if dist < self.champ_action:
                    self.attaque_special()
                    creep.recoit_coup(self.__dommage)
                    self.__tour.liste_projectiles.remove(self)
        else:

            self.__angle = hp.Helper.calcAngle(self.__pos_x, self.__pos_y, self.__cible.pos_x, self.__cible.pos_y)
            dist = hp.Helper.calcDistance(self.__pos_x, self.__pos_y, self.__cible.pos_x, self.__cible.pos_y)
            if self.__vitesse < dist:
                self.__pos_x, self.__pos_y = hp.Helper.getAngledPoint(self.__angle, self.__vitesse, self.__pos_x, self.__pos_y)
            else:
                # frappe le creep vise
                self.attaque_special()
                if isinstance(self, Poison):
                    self.__cible.est_empoisone = True
                self.__cible.recoit_coup(self.__dommage)
                self.__tour.liste_projectiles.remove(self)
            
    def attaque_special(self):
        #niveau_tour affectera les effets
        if isinstance(self, Eclair):
            self.__cible.est_electrocute = True
            self.__cible.counter_electrocute = 0
            self.__cible.dmg_electrocute = self.__dommage
        elif isinstance(self, Poison):
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
    
    @property
    def id(self):
        return self.__id

    @dommage.setter
    def dommage(self, dommage):
        self.__dommage = dommage  # Pour les améliorations qui réduisent le coût des tours.

    @vitesse.setter
    def vitesse(self, vitesse):
        self.__vitesse = vitesse  # Pour les améliorations qui réduisent le coût des tours.


class Obus(Projectile):

    def __init__(self, parent, pos_x, pos_y, cible, niveau_tour):
        super().__init__(parent, pos_x, pos_y, cible, niveau_tour)
        self.vitesse = 6
        self.dommage = 10 * niveau_tour


class Eclair(Projectile):

    def __init__(self, parent, pos_x, pos_y, cible, niveau_tour ):
        super().__init__(parent, pos_x, pos_y, cible, niveau_tour)
        self.vitesse = 15
        self.dommage = 0.25 * niveau_tour
        # niveau 3 a determiner
            
class Poison(Projectile):
 def __init__(self, parent, pos_x, pos_y, cible, niveau_tour ):
        super().__init__(parent, pos_x, pos_y, cible, niveau_tour)
        self.vitesse = 8  
        self.dommage = 0.05 * niveau_tour
        
class Balle(Projectile):
 def __init__(self, parent, pos_x, pos_y, cible, niveau_tour ):
        super().__init__(parent, pos_x, pos_y, cible, niveau_tour)
        self.vitesse = 10
        self.dommage = 1 * niveau_tour
        
class Grenade(Projectile):
 def __init__(self, parent, pos_x, pos_y, cible, niveau_tour ):
        super().__init__(parent, pos_x, pos_y, cible, niveau_tour)
        self.vitesse = 7 
        self.dommage = 8 * niveau_tour
        
class Mine(Projectile):
 def __init__(self, parent, pos_x, pos_y, cible, niveau_tour ):
        super().__init__(parent, pos_x, pos_y, cible, niveau_tour)
        self.dommage = 6 * niveau_tour
        self.champ_action = 35
        self.img_src = "./img/cerise.png"        




