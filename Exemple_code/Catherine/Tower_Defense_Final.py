#Henrick Baril, Catherine Gilbert, Catherine Lavoie, Frédéric Roy

from tkinter import *
import helper as hp
import math


class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = Tk()
        self.aire_jeu()
        self.interface_usager_default()
        self.chateau()
        self.canevas.bind("<Button-1>", self.position_clic)

    def aire_jeu(self):
        # Fond vert
        self.canevas = Canvas(self.root, width=1200, height=700, bg="green")
        self.canevas.grid(row=0, column=0, sticky="EW")

        # Sentier
        for i in range(self.parent.modele.sentier.__len__() - 1):
            self.canevas.create_rectangle(self.parent.modele.sentier[i][0] - self.parent.modele.largeur / 32,
                                          self.parent.modele.sentier[i][1] - self.parent.modele.hauteur / 24,
                                          self.parent.modele.sentier[i + 1][0] + self.parent.modele.largeur / 32,
                                          self.parent.modele.sentier[i + 1][1] + self.parent.modele.hauteur / 24,
                                          fill="#9b5d35", tags=("statique","sentier",), outline="#9b5d35")

    def chateau(self):
        # Extérieur du chateau
        self.canevas.create_rectangle(self.parent.modele.sentier[8][0] - 30, self.parent.modele.sentier[8][1] + 65,
                                      self.parent.modele.sentier[8][0] + 100, self.parent.modele.sentier[8][1] - 65,
                                      fill="#947575", tags="chateau")

        # Intérieur du chateau
        self.canevas.create_rectangle(self.parent.modele.sentier[8][0] - 15, self.parent.modele.sentier[8][1] + 50,
                                      self.parent.modele.sentier[8][0] + 85, self.parent.modele.sentier[8][1] - 50,
                                      fill="#b69e9e", tags="chateau")

        # Tour bas gauche
        self.canevas.create_oval(self.parent.modele.sentier[8][0] - 60, self.parent.modele.sentier[8][1] + 95,
                                 self.parent.modele.sentier[8][0], self.parent.modele.sentier[8][1] + 35,
                                 fill="#654f4f", tags="chateau")

        # Tour haut gauche
        self.canevas.create_oval(self.parent.modele.sentier[8][0] - 60, self.parent.modele.sentier[8][1] - 35,
                                 self.parent.modele.sentier[8][0], self.parent.modele.sentier[8][1] - 95,
                                 fill="#654f4f", tags="chateau")

        # Tour haut droite
        self.canevas.create_oval(self.parent.modele.sentier[8][0] + 60, self.parent.modele.sentier[8][1] - 35,
                                 self.parent.modele.sentier[8][0] + 120, self.parent.modele.sentier[8][1] - 95,
                                 fill="#654f4f", tags="chateau")

        # Tour bas droite
        self.canevas.create_oval(self.parent.modele.sentier[8][0] + 60, self.parent.modele.sentier[8][1] + 95,
                                 self.parent.modele.sentier[8][0] + 120, self.parent.modele.sentier[8][1] + 35,
                                 fill="#654f4f", tags="chateau")

    def interface_usager_default(self):
        # Rectangle "Chronos"
        self.canevas.create_rectangle(30, 575, 150, 625, fill="light grey", tags="chronos")
        self.canevas.create_text(90 - 3, 600, text="Chrono :", tags="textChronos")
        self.afficherTimer()

        # Rectangle "Vague(s)"
        self.canevas.create_rectangle(30, 625, 150, 675, fill="light grey", tags="vague")
        self.canevas.create_text(90 - 3, 650, text="Vague(s) :", tags="textVagues")
        self.drawVague()

        # Rectangle "Choix de tours"
        self.canevas.create_rectangle(200, 575, 600, 675, fill="light grey", tags="choixTours")
        self.canevas.create_text(245, 587, text="Choix de tours", tags="texteChoixT")

        # Bouton Tour Mitraillete
        self.canevas.create_rectangle(240, 610, 310, 660, fill="light blue", tags="tourM")
        self.canevas.create_text(275, 630, text="Tour", tags="Tour")
        self.canevas.create_text(275, 640, text="Mitraillete", tags="typeTour")

        # Rectangle nombre de vie
        self.canevas.create_rectangle(800, 575, 980, 625, fill="light grey", tags="vie")
        self.canevas.create_text(860, 600, text="Nombre de vies :", tags="textVie")
        self.affichage_vie_joueur()

    def affichageFinJeu(self):
        self.canevas.create_rectangle(200, 50, 1000, 650, fill="#FFB6C1", tags="finPartie")
        self.canevas.create_text(600, 340, text="Vous avez perdu...", tags="messageFin", font=('', '25', ''))

    def affichage_vie_joueur(self):
        self.canevas.create_text(920, 600, text=str(self.parent.modele.joueur.vie), tags=("nbrVie", "dynamique",))

    def position_clic(self, evt):
        x = evt.x
        y = evt.y
        x1 = x - 20
        y1 = y - 20
        x2 = x + 20
        y2 = y + 20
        temp = self.canevas.find_overlapping(x1, y1, x2, y2)
        if len(temp) == 0:
            self.parent.creer_tour(evt.x, evt.y)

    def afficherTimer(self):
        self.canevas.create_text(125, 600, text=str(self.parent.modele.temps), tags=("nbrChronos", "dynamique",))

    def drawTourMit(self, position_x, position_y, type, niveau, cible_angle, scale, range):

        base = self.canevas.create_rectangle(position_x + 0.5 * scale, position_y + 0.5 * scale,
                                             position_x - 0.5 * scale, position_y - 0.5 * scale,
                                             fill="grey",
                                             tags=("dynamique", "id_test", "obj_type", "type",))
        tower = self.canevas.create_oval(position_x + 0.4 * scale, position_y + 0.4 * scale,
                                         position_x - 0.4 * scale, position_y - 0.4 * scale,
                                         fill="black",
                                         tags=("dynamique", "id_test", "obj_type", "type",))
        canon = self.canevas.create_line(position_x, position_y,
                                         position_x + 0.8 * scale * round(math.cos(math.radians(cible_angle)), 2),
                                         position_y + 0.8 * scale * round(math.sin(math.radians(cible_angle)), 2),
                                         width=8,
                                         tags=("dynamique", "id_test", "obj_type", "type",))

        self.canevas.create_oval(position_x - range, position_y - range,
                                         position_x + range, position_y + range,
                                         tags=("dynamique", "id_test", "obj_type", "type",))

    def redraw(self):
        self.canevas.delete("dynamique")
        self.drawCreeps()
        self.drawTours()
        self.drawProjectiles()
        self.affichage_vie_joueur()
        self.afficherTimer()
        self.drawVague()

    def drawCreeps(self):
        for i in self.parent.modele.creeps:
            # Points pour la jambe de gauche
            pointsR1 = [i.position[0] + i.largeur - 35, i.position[1] + i.largeur - 15,
                        i.position[0] + i.largeur - 25,
                        i.position[1] + i.largeur + 30, i.position[0] + i.largeur - 20,
                        i.position[1] + i.largeur - 15]

            # Points pour la jambe de droite
            pointsR2 = [i.position[0] + i.largeur - 15, i.position[1] + i.largeur - 15,
                        i.position[0] + i.largeur - 10,
                        i.position[1] + i.largeur + 30, i.position[0] + i.largeur - 2,
                        i.position[1] + i.largeur - 15]

            # Points pour l'oeil
            pointsR3 = [i.position[0] + i.largeur - 25, i.position[1] + i.largeur - 22,
                        i.position[0] + i.largeur - 18,
                        i.position[1] + i.largeur - 17, i.position[0] + i.largeur - 10,
                        i.position[1] + i.largeur - 22]

            # Corps
            self.canevas.create_oval(i.position[0] + i.largeur, i.position[1] + i.largeur,
                                     i.position[0] - i.largeur, i.position[1] - i.largeur,
                                     fill="#22c8a8", tags=("dynamique", "creeps",), outline="#22c8a8")

            # Jambes
            self.canevas.create_polygon(pointsR1, fill="#22c8a8", tags=("dynamique", "creeps",))
            self.canevas.create_polygon(pointsR2, fill="#22c8a8", tags=("dynamique", "creeps",))

            # Oeil
            self.canevas.create_polygon(pointsR3, fill="#ff0000", tags=("dynamique", "creeps",))
            self.canevas.tag_lower("creeps")
            self.canevas.tag_lower("sentier")

    def drawTours(self):
        for i in self.parent.modele.tours:
            self.drawTourMit(i.position[0], i.position[1], i.type, i.niveau, i.cible_angle, i.scale, i.rayon)

    def drawProjectiles(self):
        for i in self.parent.modele.projectiles:
            self.canevas.create_oval(i.position[0] - i.taille, i.position[1] - i.taille,
                                     i.position[0] + i.taille, i.position[1] + i.taille,
                                     fill="black", tags=("dynamique", "projectiles",))

    def drawVague(self):
        self.canevas.create_text(125, 650, text=str(self.parent.modele.vague), tags=("nbrVague", "dynamique",))


class Modele:
    def __init__(self, parent):
        self.parent = parent
        self.creeps = []
        self.tours = []
        self.vague = 0
        self.temps = 30
        self.timeStop = True
        self.joueur = Joueur(self)
        self.projectiles = []
        self.largeur = 1200
        self.hauteur = 700
        self.sentier = [[5 * self.largeur/32, 0],
                        [5 * self.largeur/32, 15 * self.hauteur/24],
                        [11 * self.largeur/32, 15 * self.hauteur/24],
                        [11 * self.largeur/32, 4 * self.hauteur/24],
                        [28 * self.largeur/32, 4 * self.hauteur/24],
                        [28 * self.largeur/32, 9 * self.hauteur/24],
                        [19 * self.largeur/32, 9 * self.hauteur/24],
                        [19 * self.largeur/32, 15 * self.hauteur/24],
                        [29 * self.largeur/32, 15 * self.hauteur/24]]
        self.initialiser_creeps()

    def creer_tour(self, x, y):
        tour = TourProjectile(self, x, y)
        self.tours.append(tour)
        tour.chercherCible()

    def creer_projectiles(self, cible, position):
        projectile = Projectile(cible, position)
        self.projectiles.append(projectile)

    def initialiser_creeps(self):
        for i in range(20):
            creep = Creep(self, self.sentier[0][0], self.sentier[0][1] - self.hauteur / 24)
            self.creeps.append(creep)
        self.vague += 1
        self.resetTimer()

    def deplacement_creep(self):
        for i in self.creeps:
            if i.enDeplacement:
                try:
                    angle = hp.Helper.calcAngle(i.position[0], i.position[1], self.sentier[i.cible_actuelle][0], self.sentier[i.cible_actuelle][1])
                    i.position[0], i.position[1] = hp.Helper.getAngledPoint(angle, i.vitesse, i.position[0], i.position[1])
                    distance = hp.Helper.calcDistance(i.position[0], i.position[1], self.sentier[i.cible_actuelle][0], self.sentier[i.cible_actuelle][1])
                    if distance < i.vitesse:
                        i.cible_actuelle += 1
                except:
                    self.creeps.remove(i)
                    self.joueur.reduireVie()
            if i in self.creeps and i.vie <= 0:
                self.creeps.remove(i)
            if len(self.creeps) == 0:
                self.parent.vue.root.after(10000, self.initialiser_creeps)

    def decrementerTimer(self):
        if self.temps > 0:
            self.temps -= 1
        self.parent.vue.root.after(1000, self.decrementerTimer)

    def resetTimer(self):
        self.temps = 30


class TourProjectile:
    def __init__(self, parent, posX, posY):
        self.parent = parent
        self.position = [posX, posY]
        self.type = "mit"
        self.niveau = 1
        self.cible_angle = 90
        self.scale = 40
        self.rayon = 200
        self.cible = False
        self.projectiles = []

    def chercherCible(self):
        if not self.cible:
            for i in self.parent.creeps:
                if i.position[0] > self.position[0] - self.rayon and i.position[0] < self.position[0] + self.rayon and i.position[1] > self.position[1] - self.rayon and i.position[1] < self.position[1] + self.rayon:
                    projectile = Projectile(i, self.position)
                    self.parent.projectiles.append(projectile)
                    self.cible = True
                    self.parent.parent.vue.root.after(1000, self.libererCible)
                    break
        self.parent.parent.vue.root.after(500, self.chercherCible)

    def libererCible(self):
        self.cible = False

class Creep:
    def __init__(self, parent, posX, posY):
        self.parent = parent
        self.position = [posX, posY]
        self.cible_actuelle = 1
        self.enDeplacement = False
        self.vitesse = 8
        self.largeur = self.parent.largeur / 32 / 2
        self.vie = 3

    def mettreEnDeplacement(self):
        self.enDeplacement = True


class Projectile():
    def __init__(self, cible, position):
        self.taille = 4
        self.cible = cible
        self.position = position
        self.cibleAtteinte = False
        self.vitesse = 30
        self.tags = ("dynamique", "projectile",)
        self.degat = 1

    def deplacerProjectile(self):
        distance = hp.Helper.calcDistance(self.position[0], self.position[1], self.cible.position[0], self.cible.position[1])
        if distance > self.vitesse:
            angle = hp.Helper.calcAngle(self.position[0], self.position[1], self.cible.position[0], self.cible.position[1])
            self.position = hp.Helper.getAngledPoint(angle, self.vitesse, self.position[0], self.position[1])
        else:
            self.position = self.cible.position
            self.cibleAtteinte = True

    def verifierProjectile(self):
        return self.cibleAtteinte


class Joueur:
    def __init__(self, parent):
        self.parent = parent
        self.vie = 20

    def reduireVie(self):
        self.vie -= 1


class Controleur:
    def __init__(self):
        self.modele = Modele(self)
        self.vue = Vue(self)
        self.vue.root.after(500, self.gameloop)
        self.vue.root.mainloop()

    def gameloop(self):
        # modele
        # self.update positions, etc..
        if(self.modele.timeStop):
            self.vue.root.after(1000, self.decrementerTimer)
            self.modele.timeStop = False

        self.deplacement_creep()
        self.deplacement_projectile()

        # vue
        self.vue.redraw()

        # controleur
        if self.modele.joueur.vie > 0:
            self.vue.root.after(40, self.gameloop)
        else:
            self.vue.affichageFinJeu()

    def deplacement_creep(self):
        timer = 50
        for i in self.modele.creeps:
            self.vue.root.after(timer, i.mettreEnDeplacement)
            timer += 489
        self.modele.deplacement_creep()

    def deplacement_projectile(self):
        for i in self.modele.projectiles:
            i.deplacerProjectile()
            if(i.cibleAtteinte):
                i.cible.vie -= 1
                self.modele.projectiles.remove(i)

    def creer_tour(self, x, y):
        self.modele.creer_tour(x, y)

    def decrementerTimer(self):
        self.modele.decrementerTimer()


if __name__ == "__main__":
    c = Controleur()