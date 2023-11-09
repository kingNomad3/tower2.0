import math

numero_id = 0


def prochain_id():
    global numero_id
    numero_id += 1
    return "tour_" + str(numero_id)


class Obus():
    def __init__(self, parent):
        self.parent = parent
        self.x = parent.x
        self.y = parent.y
        self.alive = True
        self.collision = False
        self.id = "obus_" + prochain_id()
        self.id_tkinter = None
        self.vitesse = 40
        self.dx = 0
        self.dy = 0


    def voyage_cible(self):
        cible_x = self.parent.cible_courante.dimensions["x1"] + 38
        cible_y = self.parent.cible_courante.dimensions["y1"] + 40
        angle = math.atan2(cible_y - self.y, cible_x - self.x)
        self.dx = self.vitesse * math.cos(angle)
        self.dy = self.vitesse * math.sin(angle)

        self.x += self.dx
        self.y += self.dy

        if abs(cible_y - self.y) <= 20 and abs(cible_x - self.x) <= 20:
           self.collision = True


        return self.collision

