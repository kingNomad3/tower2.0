from tkinter import *
from Projectile import *


class Vue:

    def __init__(self, parent):
        self.tag_bouton_choisi = None
        self.nb_pixel_hauteur = None
        self.nb_pixel_largeur = None
        self.rect_tour = None
        self.root = Tk()
        self.root.geometry("800x600")

        self.controleur = parent

        self.creer_fenetre()
        self.afficher_segments()
        self.afficher_chateau()
        self.afficher_interface()

    def creer_fenetre(self):
        self.nb_pixel_largeur = self.controleur.modele.aire_de_jeu.largeur / self.controleur.modele.aire_de_jeu.colonne
        self.nb_pixel_hauteur = 400 / 18  # nouvelle largeur de aire de jeu / nouvelle ligne aire de jeu

        self.canvas_largeur = self.controleur.modele.aire_de_jeu.colonne * self.nb_pixel_largeur
        self.canvas_hauteur = 18 * self.nb_pixel_hauteur

        # canvas pour jeu
        self.canvas = Canvas(self.root, width=self.canvas_largeur, height=self.canvas_hauteur, bg="grey")
        self.canvas.pack()

        # canvas pour interface
        self.canvas_interface = Canvas(self.root, width=self.canvas_largeur, height=14 * self.nb_pixel_hauteur,
                                       bg="green")
        self.canvas_interface.pack()

    def afficher_segments(self):
        for i in self.controleur.modele.liste_segments:
            self.canvas.create_rectangle(i.depart.get("x") * self.nb_pixel_largeur,
                                         i.depart.get("y") * self.nb_pixel_hauteur,
                                         i.arrive.get("x") * self.nb_pixel_largeur,
                                         i.arrive.get("y") * self.nb_pixel_hauteur, fill="brown", outline="")

    def afficher_chateau(self):
        self.canvas.create_rectangle(26 * self.nb_pixel_largeur, 15 * self.nb_pixel_hauteur,
                                     28 * self.nb_pixel_largeur, 18 * self.nb_pixel_hauteur, fill="blue")
        self.canvas.create_rectangle(25 * self.nb_pixel_largeur, 14 * self.nb_pixel_hauteur,
                                     26 * self.nb_pixel_largeur, 15 * self.nb_pixel_hauteur, fill="blue")
        self.canvas.create_rectangle(28 * 25, 14 * self.nb_pixel_hauteur, 29 * 25, 15 * self.nb_pixel_hauteur,
                                     fill="blue")

    def afficher_creeps(self):
        self.canvas.delete("creep")
        for i in self.controleur.modele.liste_creeps:
            self.canvas.create_oval((i.pos_x - i.taille) * self.nb_pixel_largeur,
                                    (i.pos_y - i.taille) * self.nb_pixel_hauteur,
                                    (i.pos_x + i.taille) * self.nb_pixel_largeur,
                                    (i.pos_y + i.taille) * self.nb_pixel_hauteur, fill="green", tags=("creep",))

    def afficher_tour(self, tour):
        self.canvas.create_oval((tour.pos_x - tour.rayon),
                                (tour.pos_y - tour.rayon),
                                (tour.pos_x + tour.rayon),
                                (tour.pos_y + tour.rayon), fill="white", tags=(tour.id, "tour_projectile",))

        self.canvas.create_oval((tour.pos_x - tour.rayon_action),
                                (tour.pos_y - tour.rayon_action),
                                (tour.pos_x + tour.rayon_action),
                                (tour.pos_y + tour.rayon_action), outline="green", width=2, dash=(5, 4))
        self.canvas.tag_bind("tour_projectile", "<Button-1>", self.afficher_menu_upgrade)

    def afficher_tour_eclair(self, tour):
        self.canvas.create_oval((tour.pos_x - tour.rayon),
                                                   (tour.pos_y - tour.rayon),
                                                   (tour.pos_x + tour.rayon),
                                                   (tour.pos_y + tour.rayon), fill="pink",
                                                   tags=(tour.id, "tour_eclair"))
        self.canvas.create_oval((tour.pos_x - tour.rayon_action),
                                (tour.pos_y - tour.rayon_action),
                                (tour.pos_x + tour.rayon_action),
                                (tour.pos_y + tour.rayon_action), outline="green", width=2, dash=(5, 4))
        self.canvas.tag_bind("tour_eclair", "<Button-1>", self.afficher_menu_upgrade)

    def afficher_tour_poison(self, tour):
        self.canvas.create_oval((tour.pos_x - tour.rayon),
                                                   (tour.pos_y - tour.rayon),
                                                   (tour.pos_x + tour.rayon),
                                                   (tour.pos_y + tour.rayon), fill="orange", tags=(tour.id))
        self.canvas.create_oval((tour.pos_x - tour.rayon_action),
                                (tour.pos_y - tour.rayon_action),
                                (tour.pos_x + tour.rayon_action),
                                (tour.pos_y + tour.rayon_action), outline="green", width=2, dash=(5, 4))
        self.canvas.tag_bind("tour_poison", "<Button-1>", self.afficher_menu_upgrade)

    def afficher_projectile(self, tour):
        for projectile in tour.liste_projectiles:
            if isinstance(projectile, Balle):
                self.canvas.create_oval((projectile.pos_x - projectile.rayon),
                                        (projectile.pos_y - projectile.rayon),
                                        (projectile.pos_x + projectile.rayon),
                                        (projectile.pos_y + projectile.rayon), fill="pink", tags=("projectile",))
            elif isinstance(projectile, Eclair):
                if projectile.niveau == 1:
                    self.canvas.create_line(projectile.pos_x,
                                            projectile.pos_y,
                                            projectile.target.pos_x * 25,
                                            projectile.target.pos_y * 25, fill="lightblue", width=1,
                                            tags=("projectile",))
                elif projectile.niveau == 2:
                    self.canvas.create_line(projectile.pos_x,
                                            projectile.pos_y,
                                            projectile.target.pos_x * 25,
                                            projectile.target.pos_y * 25, fill="lightblue", width=3,
                                            tags=("projectile",))
                elif projectile.niveau == 3:
                    self.canvas.create_line(projectile.pos_x,
                                            projectile.pos_y,
                                            projectile.target.pos_x * 25,
                                            projectile.target.pos_y * 25, fill="blue", width=5,
                                            tags=("projectile",))
            elif isinstance(projectile, Poison):
                self.canvas.create_oval((projectile.pos_x - projectile.rayon),
                                        (projectile.pos_y - projectile.rayon),
                                        (projectile.pos_x + projectile.rayon),
                                        (projectile.pos_y + projectile.rayon), fill="green", tags=("projectile",))

    def afficher_interface(self):
        # affichage rectangle pour chrono
        self.canvas_interface.create_rectangle(1 * self.nb_pixel_largeur, 1 * self.nb_pixel_hauteur,
                                               5 * self.nb_pixel_largeur, 3 * self.nb_pixel_hauteur, fill="white",
                                               tags=("chrono",))
        self.canvas_interface.create_text(3 * self.nb_pixel_largeur, 1.5 * self.nb_pixel_hauteur, text="Chronomètre")
        self.afficher_timer()

        # affichage rectangle pour niveau/vague
        self.canvas_interface.create_rectangle(1 * self.nb_pixel_largeur, 3 * self.nb_pixel_hauteur,
                                               5 * self.nb_pixel_largeur, 5 * self.nb_pixel_hauteur, fill="white",
                                               tags=("vague",))
        self.canvas_interface.create_text(3 * self.nb_pixel_largeur, 3.5 * self.nb_pixel_hauteur, text="Vague")
        self.afficher_niveau()

        # affichage rectangle pour choix tours
        self.canvas_interface.create_rectangle(6 * self.nb_pixel_largeur, 1 * self.nb_pixel_hauteur,
                                               18 * self.nb_pixel_largeur, 5 * self.nb_pixel_hauteur, fill="white",
                                               tags=("frame_upgrade",))

        self.canvas_interface.create_text(8 * self.nb_pixel_largeur, 1.5 * self.nb_pixel_hauteur, text="Projectile")
        self.rect_tour = self.canvas_interface.create_rectangle(7 * self.nb_pixel_largeur, 2 * self.nb_pixel_hauteur,
                                                                9 * self.nb_pixel_largeur, 4 * self.nb_pixel_hauteur,
                                                                fill="blue",
                                                                tags=("tour_projectile", "interface_tour",))

        self.canvas_interface.create_text(11 * self.nb_pixel_largeur, 1.5 * self.nb_pixel_hauteur, text="Éclair")
        self.rect_tour_eclair = self.canvas_interface.create_rectangle(10 * self.nb_pixel_largeur,
                                                                       2 * self.nb_pixel_hauteur,
                                                                       12 * self.nb_pixel_largeur,
                                                                       4 * self.nb_pixel_hauteur, fill="pink",
                                                                       tags=("tour_eclair", "interface_tour",))

        self.canvas_interface.create_text(14 * self.nb_pixel_largeur, 1.5 * self.nb_pixel_hauteur, text="Poison")
        self.rect_tour_poison = self.canvas_interface.create_rectangle(13 * self.nb_pixel_largeur,
                                                                       2 * self.nb_pixel_hauteur,
                                                                       15 * self.nb_pixel_largeur,
                                                                       4 * self.nb_pixel_hauteur, fill="orange",
                                                                       tags=("tour_poison", "interface_tour",))

        # affichage rect vie
        self.canvas_interface.create_rectangle(24 * self.nb_pixel_largeur, 1 * self.nb_pixel_hauteur,
                                               29 * self.nb_pixel_largeur, 3 * self.nb_pixel_hauteur, fill="white")
        self.canvas_interface.create_text(26.5 * self.nb_pixel_largeur, 1.5 * self.nb_pixel_hauteur, text="Nbr vies")
        self.afficher_vie()

        # affichage rectangle argent/gold
        self.canvas_interface.create_rectangle(24 * self.nb_pixel_largeur, 3 * self.nb_pixel_hauteur,
                                               29 * self.nb_pixel_largeur, 5 * self.nb_pixel_hauteur, fill="white")
        self.canvas_interface.create_text(26.5 * self.nb_pixel_largeur, 3.5 * self.nb_pixel_hauteur, text="Argent")
        self.afficher_argent()

        self.canvas_interface.tag_bind(self.rect_tour, "<Button-1>", self.bind_canvas)
        self.canvas_interface.tag_bind(self.rect_tour_eclair, "<Button-1>", self.bind_canvas)
        self.canvas_interface.tag_bind(self.rect_tour_poison, "<Button-1>", self.bind_canvas)

    def bind_canvas(self, evt):
        self.tag_bouton_choisi = self.canvas_interface.itemcget(evt.widget.find_withtag("current")[0], "tags").split()[0]

        self.canvas.bind("<Button-1>", self.creer_tour)

    def afficher_timer(self):
        self.canvas_interface.delete("timer")
        texte = str(self.controleur.modele.timer)
        self.canvas_interface.create_text(3 * self.nb_pixel_largeur, 2.5 * self.nb_pixel_hauteur,
                                          text=texte, tags=("timer",))

    def afficher_niveau(self):
        self.canvas_interface.delete("niveau")
        texte = str(self.controleur.modele.niveau)
        self.canvas_interface.create_text(3 * self.nb_pixel_largeur, 4.5 * self.nb_pixel_hauteur,
                                          text=texte, tags=("niveau",))

    def afficher_vie(self):
        self.canvas_interface.delete("vies")
        texte = str(self.controleur.modele.chateau.chatelains)
        self.canvas_interface.create_text(26.5 * self.nb_pixel_largeur, 2.5 * self.nb_pixel_hauteur,
                                          text=texte, tags=("vies",))

    def afficher_argent(self):
        self.canvas_interface.delete("gold")
        texte = str(self.controleur.modele.qte_gold)
        self.canvas_interface.create_text(26.5 * self.nb_pixel_largeur, 4.5 * self.nb_pixel_hauteur, text=texte,
                                          tags=("gold",))

    def creer_tour(self, evt):
        x = evt.x
        y = evt.y

        x_1 = x - 25
        y_1 = y - 25
        x_2 = x + 25
        y_2 = y + 25

        liste_objets_overlapping = self.canvas.find_overlapping(x_1, y_1, x_2, y_2)


        if not liste_objets_overlapping:
            self.controleur.creer_tour(x, y, self.tag_bouton_choisi)

        self.canvas.unbind("<Button-1>")

    def afficher_menu_upgrade(self, event):

        tag = self.canvas.itemcget(event.widget.find_withtag("current")[0], "tags")
        self.controleur.modele.tour_selectionne = self.controleur.modele.tour_courante(tag.split()[0])

        self.canvas_interface.delete("interface_tour")
        self.canvas_interface.create_rectangle(6.5 * self.nb_pixel_largeur, 2 * self.nb_pixel_hauteur,
                                               11 * self.nb_pixel_largeur, 4 * self.nb_pixel_hauteur,
                                               fill="white", tags=("menu_upgrade",))
        self.canvas_interface.create_text(8 * self.nb_pixel_largeur, 2.5 * self.nb_pixel_hauteur, text="Cout",
                                          tags=("menu_upgrade",))
        self.canvas_interface.create_text(8 * self.nb_pixel_largeur, 3 * self.nb_pixel_hauteur, text="+force: +10%",
                                          tags=("menu_upgrade",))
        self.canvas_interface.create_text(8.2 * self.nb_pixel_largeur, 3.5 * self.nb_pixel_hauteur,
                                          text=" +étendue: +4%", tags=("menu_upgrade",))

        self.canvas_interface.create_rectangle(11.2 * self.nb_pixel_largeur,
                                               2 * self.nb_pixel_hauteur,
                                               13.7 * self.nb_pixel_largeur,
                                               4 * self.nb_pixel_hauteur, fill="yellow",
                                               tags=("menu_upgrade", "upgrade_button",))
        self.canvas_interface.create_text(12.5 * self.nb_pixel_largeur, 3 * self.nb_pixel_hauteur, text="Appliquer",
                                          tags=("menu_upgrade", "upgrade_button",))
        self.canvas_interface.tag_bind("upgrade_button", "<Button-1>", self.upgrader_tour)

        self.canvas_interface.create_rectangle(14 * self.nb_pixel_largeur,
                                               2 * self.nb_pixel_hauteur,
                                               17.5 * self.nb_pixel_largeur,
                                               4 * self.nb_pixel_hauteur, fill="white", tags=("menu_upgrade",))
        self.canvas_interface.create_text(14.9 * self.nb_pixel_largeur, 2.5 * self.nb_pixel_hauteur, text="Tour",
                                          tags=("menu_upgrade",))
        texte_force_now = str(self.controleur.modele.tour_selectionne.niveau)
        self.canvas_interface.create_text(15.1 * self.nb_pixel_largeur, 3 * self.nb_pixel_hauteur, text="force: " +
                                                                                                        texte_force_now,
                                          tags=("menu_upgrade",))
        texte_etendue_now = str(self.controleur.modele.tour_selectionne.niveau)
        self.canvas_interface.create_text(15.4 * self.nb_pixel_largeur, 3.5 * self.nb_pixel_hauteur, text=" étendue: " +
                                                                                                          texte_etendue_now,
                                          tags=("menu_upgrade",))

        self.canvas_interface.create_rectangle(17 * self.nb_pixel_largeur,
                                               1 * self.nb_pixel_hauteur,
                                               18 * self.nb_pixel_largeur,
                                               2 * self.nb_pixel_hauteur, fill="red",
                                               tags=("menu_upgrade", "close_button",))
        self.canvas_interface.create_line(17 * self.nb_pixel_largeur, 1 * self.nb_pixel_hauteur,
                                          18 * self.nb_pixel_largeur,
                                          2 * self.nb_pixel_hauteur, tags=("menu_upgrade", "close_button"))
        self.canvas_interface.create_line(18 * self.nb_pixel_largeur, 1 * self.nb_pixel_hauteur,
                                          17 * self.nb_pixel_largeur,
                                          2 * self.nb_pixel_hauteur, tags=("menu_upgrade", "close_button"))

        self.canvas_interface.tag_bind("close_button", "<Button-1>", self.delete_menu_upgrade)

    def delete_menu_upgrade(self, event):
        self.canvas_interface.delete("menu_upgrade")
        self.afficher_interface()
        self.controleur.modele.tour_selectionne = None

    def afficher_upgrade_tour(self, tour):
        self.canvas.create_oval((tour.pos_x - tour.rayon * 0.5),
                                (tour.pos_y - tour.rayon * 0.5),
                                (tour.pos_x + tour.rayon * 0.5),
                                (tour.pos_y + tour.rayon * 0.5), fill="white", tags=(tour.id, "tour_projectile",))
        if self.controleur.modele.tour_selectionne.niveau == 3:
            self.canvas.create_oval((tour.pos_x - tour.rayon * 0.2),
                                    (tour.pos_y - tour.rayon * 0.2),
                                    (tour.pos_x + tour.rayon * 0.2),
                                    (tour.pos_y + tour.rayon * 0.2), fill="white", tags=(tour.id, "tour_projectile",))

    def afficher_upgrade_tour_eclair(self, tour):
        self.canvas.create_oval((tour.pos_x - tour.rayon * 0.5),
                                (tour.pos_y - tour.rayon * 0.5),
                                (tour.pos_x + tour.rayon * 0.5),
                                (tour.pos_y + tour.rayon * 0.5), fill="white", tags=(tour.id, "tour_eclair",))
        if self.controleur.modele.tour_selectionne.niveau == 3:
            self.canvas.create_oval((tour.pos_x - tour.rayon * 0.2),
                                    (tour.pos_y - tour.rayon * 0.2),
                                    (tour.pos_x + tour.rayon * 0.2),
                                    (tour.pos_y + tour.rayon * 0.2), fill="white", tags=(tour.id, "tour_eclair",))

    def afficher_upgrade_tour_poison(self, tour):
        self.canvas.create_oval((tour.pos_x - tour.rayon * 0.5),
                                (tour.pos_y - tour.rayon * 0.5),
                                (tour.pos_x + tour.rayon * 0.5),
                                (tour.pos_y + tour.rayon * 0.5), fill="white", tags=(tour.id, "tour_poison",))
        if self.controleur.modele.tour_selectionne.niveau == 3:
            self.canvas.create_oval((tour.pos_x - tour.rayon * 0.2),
                                    (tour.pos_y - tour.rayon * 0.2),
                                    (tour.pos_x + tour.rayon * 0.2),
                                    (tour.pos_y + tour.rayon * 0.2), fill="white", tags=(tour.id, "tour_poison",))

    def upgrader_tour(self, event):
        self.controleur.upgrader_tour()


