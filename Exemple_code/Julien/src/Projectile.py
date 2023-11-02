from helper import Helper as hp


class Balle:

    def __init__(self, parent, niveau_tour, target, x, y):
        self.tour = parent
        self.rayon = 4
        self.pos_x = x
        self.pos_y = y
        self.vitesse = 12
        self.target = target
        self.dommage = 5

        if niveau_tour == 3:
            self.dommage = 10

    def update_position(self):
        angle_attaque = self.get_angle_attaque()
        self.pos_x, self.pos_y = hp.getAngledPoint(angle_attaque, self.vitesse, self.pos_x, self.pos_y)
        dist = hp.calcDistance(self.target.pos_x * 25, self.target.pos_y * 25, self.pos_x, self.pos_y)

        if dist < self.vitesse:
            self.tour.modele.supprimer_creep()
            self.target.vie -= self.dommage
            self.tour.liste_projectiles.remove(self)

    def get_angle_attaque(self):
        return hp.calcAngle(self.pos_x, self.pos_y, self.target.pos_x * 25, self.target.pos_y * 25)


class Eclair:

    def __init__(self, parent, niveau_tour, target, x, y):
        self.tour = parent
        self.angle_target = None
        self.rayon = 4
        self.pos_x = x
        self.pos_y = y
        self.vitesse = 18
        self.target = target
        self.dommage = 5
        self.niveau = niveau_tour
        if niveau_tour == 2:
            self.dommage = 10
        elif niveau_tour == 3:
            self.dommage = 15

    def update_position(self):
        angle_attaque = self.get_angle_attaque()
        self.pos_x, self.pos_y = hp.getAngledPoint(angle_attaque, self.vitesse, self.pos_x, self.pos_y)
        dist = hp.calcDistance(self.target.pos_x * 25, self.target.pos_y * 25, self.pos_x, self.pos_y)

        if dist < self.vitesse:
            self.target.est_electrocute = True
            self.target.counter_electrocute = 0
            self.target.dmg_electrocute = self.dommage
            self.tour.liste_projectiles.remove(self)

    def get_angle_attaque(self):
        return hp.calcAngle(self.pos_x, self.pos_y, self.target.pos_x * 25, self.target.pos_y * 25)


class Poison:

    def __init__(self, parent, niveau_tour, target, x, y):
        self.tour = parent
        self.angle_target = None
        self.rayon = 4
        self.pos_x = x
        self.pos_y = y
        self.vitesse = 8
        self.target = target
        self.dommage = 0.03125
        if niveau_tour == 3:
            self.dommage = 1.5

    def update_position(self):
        angle_attaque = self.get_angle_attaque()
        self.pos_x, self.pos_y = hp.getAngledPoint(angle_attaque, self.vitesse, self.pos_x, self.pos_y)
        dist = hp.calcDistance(self.target.pos_x * 25, self.target.pos_y * 25, self.pos_x, self.pos_y)

        if dist < self.vitesse:
            self.target.est_empoisone = True
            self.target.dmg_poison = self.dommage
            self.tour.liste_projectiles.remove(self)

    def get_angle_attaque(self):
        return hp.calcAngle(self.pos_x, self.pos_y, self.target.pos_x * 25, self.target.pos_y * 25)
