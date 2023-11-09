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
        self.__modele = parent
        self.__rayon = rayon
        self.__champ_action = self.__rayon * 3.5 # Taille exacte du champ d'action à décider. On pourrait se passer paramètre le multiplicateur au besoin.
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__niveau_amelioration = niveau_amelioration
        self.__cout = cout
        self.__cout_amelioration = self.__cout * self.__niveau_amelioration # Manière de calculer à déterminer. Permettrait de faire en sorte que les améliorations en jeu coûtent moins cher si on réduit son coût.
        self.__cible = None
        self.__combine = None
        #self.__vie = vie Si on peut faire perdre de la vie à nos tours
    
    @property
    def id(self):
        return self.__id
    
    @property # À voir si on a besoin
    def modele(self):
        return self.__modele
    
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


class TourAttaque(Tour):
    def __init__(self, parent, rayon, pos_x, pos_y, niveau_amelioration, cout, temps_recharge):
        super().__init__(parent, rayon, pos_x, pos_y, niveau_amelioration, cout)
        self.__liste_projectiles = []
        self.__temps_recharge = temps_recharge
    
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
    

class TourProjectile(TourAttaque):

    def __init__(self, parent, pos_x, pos_y):
        # p1 : parent, p2 : rayon (le même pour toutes les tours de ce type), p3 et p4 : positions, p5 : niveau 1 en partant (amélioration générale possible??)
        # p6 : coût (amélioration générale possible??), p7 : temps de recharge, éventuel p8 : vie (si on fait perdre de la vie à nos tours)
        super().__init__(parent, 25, pos_x, pos_y, 1, 300, 5)























    def attaquer(self):
        if self.target is None:
            self.definir_cible()
        elif self.target:
            balle = Balle(self, self.niveau, self.target, self.pos_x, self.pos_y)
            self.liste_projectiles.append(balle)

        if self.target:
            self.update_target(self.target)

    def definir_cible(self):
        for creep in self.modele.liste_creeps:
            dist = hp.calcDistance(creep.pos_x * 25, creep.pos_y * 25, self.pos_x, self.pos_y)
            if dist < self.rayon_action:
                self.target = creep

    def update_target(self, target):
        dist = hp.calcDistance(target.pos_x * 25, target.pos_y * 25, self.pos_x, self.pos_y)
        if dist > self.rayon_action or self.target.vie == 0 or len(self.modele.liste_creeps) == 0:
            self.target = None

    def augmenter_niveau(self):
        self.niveau += 1

    def update_position_balles(self):
        for projectile in self.liste_projectiles:
            projectile.update_position()

    def upgrade_tour(self):
        if self.verifCoutUpgrade():
            self.augmenter_niveau()
            #self.cout_upgrade = self.cout_upgrade * self.niveau

            if self.niveau == 2:
                self.recharge = 2.5

            if self.niveau == 3:
                self.recharge = 10

            self.est_upgrade = True


    def verifCoutUpgrade(self):
        if self.modele.qte_gold - self.cout_upgrade >= 0:
            return True
        else:
            return False


class TourEclair(Tour):

    def __init__(self, parent, pos_x, pos_y):
        self.id = creer_id()
        self.cout_upgrade = 250
        self.target = None
        self.modele = parent
        self.rayon = 25
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rayon_action = self.rayon * 3
        self.niveau = 1
        self.cout = 80  # A revisiter
        self.recharge = 5  # A revisiter
        self.liste_projectiles = []
        self.est_upgrade = False


    def attaquer(self):
        if self.target is None:
            self.definir_cible()
        elif not self.target.est_electrocute:
            eclair = Eclair(self, self.niveau, self.target, self.pos_x, self.pos_y)
            self.liste_projectiles.append(eclair)

        if self.target:
            self.update_target(self.target)

    def definir_cible(self):
        for creep in self.modele.liste_creeps:
            dist = hp.calcDistance(creep.pos_x * 25, creep.pos_y * 25, self.pos_x, self.pos_y)
            if dist < self.rayon_action:
                self.target = creep

    def update_target(self, target):
        dist = hp.calcDistance(target.pos_x * 25, target.pos_y * 25, self.pos_x, self.pos_y)
        if dist > self.rayon_action or self.target.vie == 0 or len(self.modele.liste_creeps) == 0:
            self.target = None

    def augmenter_niveau(self):
        self.niveau += 1

    def update_position_balles(self):
        for projectile in self.liste_projectiles:
            projectile.update_position()

    def upgrade_tour(self):
        if self.verifCoutUpgrade():
            self.augmenter_niveau()

            self.recharge = 0  # si le niveau est 2 ou 3, laser continu
            self.est_upgrade = True

    def verifCoutUpgrade(self):
        if self.modele.qte_gold - self.cout_upgrade >= 0:
            return True
        else:
            return False


class TourPoison(Tour):

    def __init__(self, parent, pos_x, pos_y):
        self.id = creer_id()
        self.cout_upgrade = 200
        self.target = None
        self.modele = parent
        self.rayon = 25
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rayon_action = self.rayon * 3
        self.niveau = 1
        self.cout = 80  # A revisiter
        self.recharge = 10  # A revisiter
        self.liste_projectiles = []
        self.est_upgrade = False


    def attaquer(self):
        if self.target is None:
            self.definir_cible()
        elif not self.target.est_empoisone:
            poison = Poison(self, self.niveau, self.target, self.pos_x, self.pos_y)
            self.liste_projectiles.append(poison)

        if self.target:
            self.update_target(self.target)

    def definir_cible(self):
        for creep in self.modele.liste_creeps:
            dist = hp.calcDistance(creep.pos_x * 25, creep.pos_y * 25, self.pos_x, self.pos_y)
            if dist < self.rayon_action:
                self.target = creep

    def update_target(self, target):
        dist = hp.calcDistance(target.pos_x * 25, target.pos_y * 25, self.pos_x, self.pos_y)
        if dist > self.rayon_action or self.target.vie == 0 or len(self.modele.liste_creeps) == 0:
            self.target = None

    def augmenter_niveau(self):
        self.niveau += 1

    def update_position_balles(self):
        for projectile in self.liste_projectiles:
            projectile.update_position()

    def upgrade_tour(self):
        if self.verifCoutUpgrade():
            self.augmenter_niveau()

            if self.niveau == 2:
                self.recharge = self.recharge / 1.5  # temps de recharge plus rapide dans niveaux 2 et 3

            self.est_upgrade = True



    def verifCoutUpgrade(self):
        if self.modele.qte_gold - self.cout_upgrade >= 0:
            return True
        else:
            return False