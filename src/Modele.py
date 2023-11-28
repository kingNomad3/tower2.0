from Partie import *


class Modele:
    def __init__(self, parent):
        self.controleur = parent
        self.partie = Partie(self, 1, 1) # Mettre à none quand on aura des tableaux et difficultés.
        
    # def creer_partie(self,  parent): # Passer tableau et difficulte
    #     self.partie = Partie(self, 1, 1, parent) # Mettre tableau et difficulte en temps et lieu.
        
    def terminer_partie(self):
        self.partie = None

    def jouer(self):
        self.partie.jouer()

