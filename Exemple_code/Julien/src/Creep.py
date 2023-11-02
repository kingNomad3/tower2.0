from helper import Helper as hp


class Creep:

    def __init__(self, pos_x, pos_y, niveau, parent):
        self.target = None
        self.angle_target = None

        self.est_empoisone = False
        self.est_electrocute = False
        self.counter_electrocute = None

        self.dmg_poison = None
        self.dmg_electrocute = None

        self.modele = parent
        self.vie = 10 * niveau
        self.valeur_gold = 20 * niveau
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vitesse = 0.15
        self.taille = 0.5
        self.pivot_courrant = -1
        self.nouvelle_target()

    def bouger(self):
        self.pos_x, self.pos_y = hp.getAngledPoint(self.angle_target, self.vitesse, self.pos_x, self.pos_y)
        dist = hp.calcDistance(self.pos_x, self.pos_y, self.target[0], self.target[1])

        if dist < self.vitesse:
            self.nouvelle_target()

    def nouvelle_target(self):
        if self.pivot_courrant != 7:
            self.pivot_courrant += 1
            self.target = self.modele.liste_pivots[self.pivot_courrant]
            self.angle_target = hp.calcAngle(self.pos_x, self.pos_y, self.target[0], self.target[1])
        else:
            self.pivot_courrant = 8

    def update_vie(self):
        if self.est_empoisone:
            self.vie -= self.dmg_poison

        if self.est_electrocute:
            self.counter_electrocute += 1
            self.vie -= self.dmg_electrocute

        if self.counter_electrocute == 3:
            self.est_electrocute = False
