from Vue import *
from Modele import *
from Tour import *

class Controleur:

    def __init__(self):
        self.timer_counter = 0
        self.creep_counter = 0
        self.modele = Modele(self)
        self.vue = Vue(self)
        self.vue.root.after(500, self.game_loop)
        self.vue.root.mainloop()

    def game_loop(self):
        if not self.modele.gameover:
            if self.modele.timer == 0:  # va dans le modele
                self.creep_counter = 0
                self.modele.initialiser_niveau()

            if self.timer_counter % 10 == 0:
                if self.creep_counter != 20:
                    self.modele.ajouter_creep()
                    self.creep_counter += 1

            if self.timer_counter == 20:
                self.modele.game_timer()
                self.timer_counter = 0

            self.modele.bouger_creep()
            self.modele.update_vie_creep()
            self.vue.afficher_creeps()

            self.vue.canvas.delete("projectile")
            for tour in self.modele.liste_tours:
                if self.timer_counter % 15 == 0:
                    tour.attaquer()
                tour.update_position_balles()
                self.vue.afficher_projectile(tour)

            self.timer_counter += 1

            self.vue.root.after(50, self.game_loop)

    def creer_tour(self, x, y, type_tour):
        tour = self.modele.creer_tour(x, y, type_tour)

        if tour is not None:
            if isinstance(tour, TourMitrailleuse):
                self.vue.afficher_tour(tour)
            elif isinstance(tour, TourEclair):
                self.vue.afficher_tour_eclair(tour)
            elif isinstance(tour, TourPoison):
                self.vue.afficher_tour_poison(tour)

    def upgrader_tour(self):
        self.modele.upgrader_tour()

        if self.modele.tour_selectionne.est_upgrade:
            if isinstance(self.modele.tour_selectionne, TourMitrailleuse):
                self.vue.afficher_upgrade_tour(self.modele.tour_selectionne)
            elif isinstance(self.modele.tour_selectionne, TourEclair):
                self.vue.afficher_upgrade_tour_eclair(self.modele.tour_selectionne)
            elif isinstance(self.modele.tour_selectionne, TourPoison):
                self.vue.afficher_upgrade_tour_poison(self.modele.tour_selectionne)

            self.modele.tour_selectionne.est_upgrade = False
            self.modele.tour_selectionne = None