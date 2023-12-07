from Partie import *


class Modele:
    def __init__(self, parent):
        self.controleur = parent
        self.partie = None
        
    # def creer_partie(self,  parent): # Passer tableau et difficulte
    #     self.partie = Partie(self, 1, 1, parent) # Mettre tableau et difficulte en temps et lieu.
        
    def terminer_partie(self):
        self.partie = None

    def jouer(self):
        self.partie.jouer()
        
    def lancer_partie(self,joueurs, tableau):
        self.partie = Partie(self,1,joueurs, tableau)

