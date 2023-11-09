import random
import time

import helper as hp

inc = 0

def nouveau_id():
    global inc
    inc += 1
    return f"id_{inc}"

class Modele:
    def __init__(self, parent):
        self.parent = parent
        self.partie = Partie(self)

    def jouer(self):
        self.partie.jouer()


class Chemin():
    def __init__(self, parent):
        self.parent = parent
        self.pivots = [[150, 0], [150, 450], [330, 450], [330, 120], [840, 120], [840, 240], [570, 240], [570, 450], [860, 450]]
        self.segments = []
        self.temp = self.pivots[0]
        self.creer_segments(self.pivots)


    def creer_segments(self, pivots):
        for i in pivots[1:]:
            self.segments.append([self.temp, i])
            self.temp = i


class Partie():
    ESPACE_CREEP = 1.5
    DUREE_VAGUE = 40
    def __init__(self, parent):
        self.parent = parent
        self.tours = []
        self.creeps = []
        self.timer = 10
        self.vague = 1
        self.aire_de_jeu = 0
        self.creeps_queue = []
        self.vie = 20
        self.chemin = Chemin(self)
        self.gameover = False
        self.argent = 10
        self.nombre_creep_vague = 20
        self.creer_creeps()
        
        self.delta_time = time.time()
        self.temps_derniere_vague = time.time()

    def creer_tour(self, x, y):
        if self.peut_acheter_tour():
            self.tours.append(Tour(x, y, self))
            self.argent -= Tour.cout

    def peut_acheter_tour(self) -> bool:
        return self.argent >= Tour.cout

    def creer_creeps(self):
        self.creeps_queue = [Creep(self.chemin.pivots[0][0], self.chemin.pivots[0][1], self) for i in range(self.nombre_creep_vague)]

    def creeps_apparaissent(self):
        if self.creeps_queue:
            self.creeps.append(self.creeps_queue.pop(0))

    def jouer(self):
        # fait apparaître les creeps progressivement
        if self.creeps_queue:
            if len(self.creeps_queue) < 20:
                start = time.time()
                if start - self.delta_time > Partie.ESPACE_CREEP:
                    self.creeps_apparaissent()
                    self.delta_time = time.time()
            else:
                self.creeps_apparaissent()

        if self.est_game_over():
            print("PERDU") # pour debogage


        for creep in self.creeps:
            creep.jouer()

        for tour in self.tours:
            tour.jouer()

        self.remove_creep()
        self.remove_obus()
        
        if (maintenant := time.time()) - self.temps_derniere_vague >= Partie.DUREE_VAGUE:
            self.temps_derniere_vague = maintenant
            self.prochaine_vague()
        
        
    def perte_vie(self):
        # châtelains...
        self.vie -= 1

    def prochaine_vague(self):
        # pour chaque nouvelle vague
        self.vague += 1
        self.creeps = []
        self.creer_creeps()

    def est_game_over(self) -> bool:
        # met le bool à jour et le retourne
        self.gameover = self.vie < 1
        return self.gameover


    def prochain_niveau(self):
        self.vague += 1
        self.creer_creeps()

    def remove_creep(self):
        for i in self.creeps:
            if not i.vivant:
                self.creeps.remove(i)

    def remove_obus(self):
        for tour in self.tours:
            for i in tour.obus:
                if not i.vivant:
                    tour.obus.remove(i)




class Tour():
    NIVEAU_MAX = 3
    cout_upgrade = 1
    rayon = 150
    largeur = 30
    cout = 10
    def __init__(self, x, y, parent):
        self.parent = parent
        self.niveau = 1
        self.x = x
        self.y = y
        self.no_id = nouveau_id()
        self.canon = [self.x, self.y + 30]
        self.rayon = Tour.rayon

        self.largeur = Tour.largeur
        self.time_dernier_tir = None
        self.obus = []

    def jouer(self):
        self.detecter()
        self.deplace_obus()

    def deplace_obus(self):
        # déplace les obus de cette tour
        if self.obus:
            for i in self.obus:
                i.deplacer()

    def update(self):
        if self.parent.argent >= Tour.cout_upgrade and self.niveau < Tour.NIVEAU_MAX:
            self.niveau += Tour.cout_upgrade
            self.parent.argent -= Tour.cout_upgrade

    def tirer(self, creep):
        self.time_dernier_tir = time.time()

        if len(self.obus) > 1:
            start = time.time()
            if self.time_dernier_tir - start > 6 - self.niveau:
                self.obus.append(Obus(self.x, self.y, creep, self))
                self.target = creep.no_id
                self.time_dernier_tir = time.time()
        elif not self.obus:
            self.obus.append(Obus(self.x, self.y, creep, self))

    def detecter(self):
        for creep in self.parent.creeps:
            distance = hp.Helper.calcDistance(creep.x, creep.y, self.x, self.y)
            if distance < self.rayon:
                self.tirer(creep)

# Retiré par manque de temps
# class TourEclair(Tour):
#     def __init__(self, x, y, parent):
#         super().__init__(x, y, parent)
#         self.rayons = []

#     def tirer(self, creep):
#         self.time_dernier_tir = time.time()

#         if len(self.rayons) > 1:
#             start = time.time()
#             if self.time_dernier_tir - start > 10: # 10 plutôt que 6 pour que ce soit plus lent entre les tirs
#                 self.obus.append(Rayon(self.x, self.y, creep, self.parent))
#                 self.target = creep.no_id
#                 self.time_dernier_tir = time.time()
#         elif not self.rayons:
#             self.rayons.append(Rayon(self.x, self.y, creep, self.parent))

# Retiré par manque de temps
# class TourPoison(Tour):
#     def __init__(self, x, y, parent):
#         super().__init__(x, y, parent)

class Obus():
    largeur = 10
    def __init__(self, x, y, cible, parent):
        self.parent = parent
        self.ox = x
        self.oy = y
        self.vivant = True
        self.x = x
        self.y = y
        self.largeur = Obus.largeur
        self.no_id = nouveau_id()
        self.vitesse = 10 + self.parent.niveau * 2
        self.dommage = 1
        self.cible = cible
        self.angle = self.deduire_angle()


    def deduire_angle(self):
        return hp.Helper.calcAngle(self.x, self.y, self.cible.x, self.cible.y)

    def deplacer(self):
        destination = hp.Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)
        self.x, self.y = destination
        distance = hp.Helper.calcDistance(self.ox, self.oy, self.x, self.y)
        if distance > Tour.rayon:
            self.vivant = False

# Retiré par manque de temps
# class Rayon(Obus):
#     def __init__(self, x, y, cible, parent):
#         super().__init__(x, y, cible, parent)

# Retiré par manque de temps
# class Poison(Obus):

#     def __init__(self, x, y, vitesse, parent):
#         super().__init__(x, y, parent)
#         self.vitesse = vitesse
#         self.dommage = 0.2


class Creep():
    largeur = 20
    valeur = 1

    def __init__(self, x, y, parent):
        self.parent = parent
        self.x = x
        self.y = y
        self.no_id = nouveau_id()
        self.max_mana = 1 + parent.vague
        self.mana = self.max_mana
        self.vitesse = 9 + 1.5 * parent.vague
        self.vivant = True
        self.segment_actuel = 0
        self.chercher_cible()

    def jouer(self):
        for tour in self.parent.tours:
            for projectile in tour.obus:
                distance = hp.Helper.calcDistance(projectile.x, projectile.y, self.x, self.y)
                if distance < Creep.largeur * 2.5:
                    tour.obus.remove(projectile)
                    self.recoit_coup(projectile.dommage)

        self.deplacer()


    def chercher_cible(self):
        x = self.parent.chemin.segments[self.segment_actuel][1][0]
        y = self.parent.chemin.segments[self.segment_actuel][1][1]

        self.angle = hp.Helper.calcAngle(self.x, self.y, x, y)
        self.cible = [x, y]

    def deplacer(self):
        self.x, self.y = hp.Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)

        dist = hp.Helper.calcDistance(self.x, self.y, self.cible[0], self.cible[1])

        if dist < self.vitesse:
            self.x = self.cible[0]
            self.y = self.cible[1]
            self.segment_actuel += 1
            if self.segment_actuel <= 7:
                self.chercher_cible()

            # arrive au chateau
            elif self.segment_actuel == 8:
                self.parent.perte_vie()
                self.vivant = False

    def recoit_coup(self, dommage):
        self.mana -= dommage
        if self.mana <= 0:
            self.vivant = False
            self.parent.argent += Creep.valeur

if __name__ == '__main__':
    # on ne veut pas pouvoir executer le modèle seul pour la remise
    pass