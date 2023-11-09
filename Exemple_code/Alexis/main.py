from Vue import *
from Modele import *

class Controleur:
    def __init__(self):
        self.modele = Modele(self)
        self.timer = 0
        self.vue = Vue(self, self.modele)
        self.vue.root.after(300, self.boucler_jeu)
        self.vue.root.mainloop()

    def boucler_jeu(self):
        if not self.modele.partie.gameover:
            self.incrementer_timer()
            
            self.modele.jouer()
            self.vue.dessiner_jeu()
            self.vue.root.after(50, self.boucler_jeu)
        else:
           self.traiter_gameover()


    # pour du visuel et le modèle (en cas de besoin)
    def incrementer_timer(self):
        self.timer += 0.5

    def get_timer_str(self):
        return f"{int(self.timer//10)}s"

    # Lié à l'intéraction usager...
    def traiter_gameover(self):
        self.vue.root.destroy()

    def creer_tour(self, x, y):
        self.modele.partie.creer_tour(x, y)

if __name__ == "__main__":
    c = Controleur()







