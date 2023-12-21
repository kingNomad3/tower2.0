from Partie import *


class Modele:
    def __init__(self, parent):
        self.controleur = parent
        self.partie = None
        
    def terminer_partie(self):
        self.partie = None

    def jouer(self):
        self.partie.jouer()
        
    def lancer_partie(self, joueurs, tableau):
        self.partie = Partie(self, 1, joueurs, tableau)

