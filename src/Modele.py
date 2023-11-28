import Partie


class Modele:
    def __init__(self, parent):
        self.parent = parent
        self.partie = Partie(self)

    def jouer(self):
        self.partie.jouer()

