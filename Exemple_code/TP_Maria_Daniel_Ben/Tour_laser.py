import helper as hp

numero_id = 0
def prochain_id():
    global numero_id
    numero_id += 1
    return "tour_laser" + str(numero_id)

class Tour_laser():
    def __init__(self, parent, x, y):
        self.id = prochain_id()
        self.x = x
        self.y = y
        self.parent = parent
        self.rayon = 150
        self.dommage = 5
        self.cible_courante = None
        self.niveau = 1
        self.obus = None
        self.dimensions = {
            "x1": x,
            "y1": y,
            "x2": x,
            "y2": y
        }

    def chercher_cible(self, temps):
        if not self.cible_courante:
            for i in self.parent.creeps:
                distance = hp.Helper.calcDistance(self.x, self.y, i.dimensions["x1"], i.dimensions["y1"])
                if distance <= self.rayon:
                    self.cible_courante = i
        else:
            if self.cible_courante > self.rayon:
                self.cible_courante = None

    def attaquer_cible(self):
        if hp.Helper.calcDistance(self.x, self.y, self.cible_courante.dimensions["x1"],
                                  self.cible_courante.dimensions["y1"]) <= self.rayon:
            self.dimensions["x2"] = self.cible_courante.dimensions["x1"] +38
            self.dimensions["y2"] = self.cible_courante.dimensions["y1"] +40
            self.cible_courante.vie -= self.dommage

            if self.cible_courante.vie < 1:
                self.cible_courante = None
                self.dimensions["x2"] = self.x
                self.dimensions["y2"] = self.y

        else:
            self.cible_courante = None
            self.dimensions["x2"] = self.x
            self.dimensions["y2"] = self.y


    def augmenter_niveau(self):
        if self.niveau < 3:
            self.niveau += 1
            self.dommage += 2