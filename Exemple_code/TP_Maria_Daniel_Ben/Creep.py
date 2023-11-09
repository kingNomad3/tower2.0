numero_id = 0

def prochain_id():
    global numero_id
    numero_id += 1
    return "creep_" + str(numero_id)

class Creep:
    def __init__(self, parent):
        self.parent = parent
        self.pivot = 1
        self.vitesse = 15
        self.vie = 20
        self.vie_courante = self.vie
        self.id_tkinter = None
        self.id = prochain_id()
        self.couleur = "red"
        self.dimensions = {
            "x1": 164,
            "y1": 0,
            "x2": 240,
            "y2": 80
        }
        self.is_alive = True
        self.a_tue = False
        self.empoisonne = False


    def mouvement_creep(self):
        pivot_actuel = self.parent.chemin.pivots[self.pivot]
        monter = 1
        a_droite = 1
        if pivot_actuel[0] + 5 >= self.dimensions["x1"] >= pivot_actuel[0] - 5 and self.dimensions["y2"] == pivot_actuel[1] + 40:
            self.pivot = self.pivot + 1
        pivot_actuel = self.parent.chemin.pivots[self.pivot]

        if pivot_actuel[0] + 5 >= self.dimensions["x1"] >= pivot_actuel[0] - 5:
            if self.dimensions["y2"] - pivot_actuel[1] - 40 > 0:
                monter = monter * -1
            self.dimensions["y1"] = self.dimensions["y1"] + self.vitesse * monter
            self.dimensions["y2"] = self.dimensions["y2"] + self.vitesse * monter

        elif pivot_actuel[1] + 40 >= self.dimensions["y2"] >= pivot_actuel[1] - 40:
            if self.dimensions["x1"] - pivot_actuel[0] > 5:
                a_droite = a_droite * -1
            self.dimensions["x1"] = self.dimensions["x1"] + self.vitesse * a_droite
            self.dimensions["x2"] = self.dimensions["x2"] + self.vitesse * a_droite

        if self.dimensions["x2"] >= 1180 and self.dimensions["y2"] >= 600:
            self.is_alive = False
            self.a_tue = True

    def am_i_alive(self):
        if self.vie <= 0:
            self.is_alive = False



