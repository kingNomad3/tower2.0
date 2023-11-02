from Projectile import *
from helper import Helper as hp

no_id = 0;

def creer_id():
    global no_id
    no_id += 1
    return "id_" + str(no_id)

class TourProjectile:

    def __init__(self, parent, pos_x, pos_y):
        self.id = creer_id()
        self.modele = parent
        self.rayon = 25
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rayon_action = self.rayon * 3.5
        self.niveau = 1
        self.cout = 80
        self.cout_upgrade = 100
        self.recharge = 5  # A revisiter
        self.target = None
        self.liste_projectiles = []
        self.est_upgrade = False


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


class TourEclair:

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


class TourPoison:

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
