from tkinter import *

from Tour_laser import Tour_laser
from Tour_poison import Tour_poison
from Tour_projectile import Tour_projectile


class Vue:
    def __init__(self, parent, modele):
        self.parent = parent
        self.modele = modele
        self.root = Tk()
        self.init_fenetre()
        self.obus = []

    def init_fenetre(self):
        self.splash_screen = Canvas(self.root, height=-1, width=-1, bg="white")
        self.splash_screen.pack()
        self.frame_jeu = Canvas(self.root, height=960, width=1280, bg="black")
        self.frame_jeu.pack()
        self.terrain = self.frame_jeu.create_rectangle(0,0,1282,720, fill='forest green', tags="terrain_jeu") # Pixel de trop
        self.frame_jeu.tag_bind("terrain_jeu", "<Button-1>", self.coordonees_tour)
        self.frame_jeu.create_rectangle(0, 720, 1282, 740, fill='black')

        self.afficher_chemin()
        self.afficher_creep()
        self.creer_chateau()
        self.creer_menu_vague_chrono()
        self.creer_menu_choix_tours("random")
        # self.creer_menu_upgrade_tour()
        self.creer_menu_nb_vies()
        self.creer_menu_argent()


    def afficher_chemin(self):
        for i in self.modele.chemin.chemin:
            self.frame_jeu.create_rectangle(i[0][0]+40, i[0][1], i[1][0]+40, i[1][1], width=80, tags=("bordures",))

    def afficher_creep(self):
        for i in self.modele.creeps:
            self.frame_jeu.create_oval(i.dimensions["x1"], i.dimensions["y1"],i.dimensions["x2"], i.dimensions["y2"],
                                       fill="OrangeRed3", tags=("creeps",))

            self.frame_jeu.create_oval(i.dimensions["x1"] + 16 , i.dimensions["y1"]+16 ,i.dimensions["x2"] - 44,
                                       i.dimensions["y2"] - 44, fill="white", tags=("creeps",))
            self.frame_jeu.create_oval(i.dimensions["x1"] + 20, i.dimensions["y1"] + 20, i.dimensions["x2"] - 46,
                                       i.dimensions["y2"] - 46, fill="black", tags=("creeps",))
            self.frame_jeu.create_line(i.dimensions["x1"] + 12, i.dimensions["y1"] + 18, i.dimensions["x2"] - 42,
                                       i.dimensions["y2"] - 60, fill="black", width=5, tags=("creeps",))

            self.frame_jeu.create_oval(i.dimensions["x1"] + 44, i.dimensions["y1"] + 16, i.dimensions["x2"] - 16,
                                       i.dimensions["y2"] - 44, fill="white", tags=("creeps",))
            self.frame_jeu.create_oval(i.dimensions["x1"] + 46, i.dimensions["y1"] + 20, i.dimensions["x2"] - 20,
                                       i.dimensions["y2"] - 46, fill="black", tags=("creeps",))
            self.frame_jeu.create_line(i.dimensions["x1"] + 46, i.dimensions["y1"] + 20, i.dimensions["x2"] - 12,
                                       i.dimensions["y2"] - 62, fill="black", width=5, tags=("creeps",))

            self.frame_jeu.create_line(i.dimensions["x1"] + 15, i.dimensions["y1"] + 45, i.dimensions["x2"] - 30,
                                       i.dimensions["y2"] - 30, fill="black", width=5, tags=("creeps",))


    def afficher_modele(self):
        self.frame_jeu.delete("creeps", "temps", "vagueActuelle", "vieActuelle", "ArgentActuelle")
        self.afficher_creep()
        self.frame_jeu.create_text(120, 800, text=round(self.parent.temps/1000,0), fill="black", font=('Helvetica 20 bold'), tags="temps")
        self.frame_jeu.create_text(120, 882, text=self.parent.vague, fill="black", font=('Helvetica 20 bold'), tag="vagueActuelle")
        self.frame_jeu.create_text(1060, 800, text=self.parent.vies, fill="black", font=('Helvetica 30 bold'),  tag="vieActuelle")
        self.frame_jeu.create_text(1060, 930, text=self.parent.argent, fill="black", font=('Helvetica 30 bold'),
                               tag="ArgentActuelle")

    def creer_chateau(self):
        self.frame_jeu.create_rectangle(1120, 520, 1240, 680, fill="snow3", outline="snow3") #Main rectangle

        self.frame_jeu.create_rectangle(1120, 510, 1144, 520, fill="snow3", outline="snow3") # Main rectangle top
        self.frame_jeu.create_rectangle(1168, 510, 1192, 520, fill="snow3", outline="snow3")
        self.frame_jeu.create_rectangle(1216, 510, 1240, 520, fill="snow3", outline="snow3")

        self.frame_jeu.create_rectangle(1090, 560, 1270, 599, fill="snow4", outline="snow4") #Top
        self.frame_jeu.create_rectangle(1090, 540, 1110, 560, fill="snow4", outline="snow4")
        self.frame_jeu.create_rectangle(1130, 540, 1150, 560, fill="snow4", outline="snow4")
        self.frame_jeu.create_rectangle(1170, 540, 1190, 560, fill="snow4", outline="snow4")
        self.frame_jeu.create_rectangle(1210, 540, 1230, 560, fill="snow4", outline="snow4")
        self.frame_jeu.create_rectangle(1250, 540, 1270, 560, fill="snow4", outline="snow4")

        self.frame_jeu.create_rectangle(1100, 681, 1260, 700, fill="snow4", outline="gray34") #Plafond
        self.frame_jeu.create_rectangle(1090, 700, 1270, 720, fill="gray26", outline="snow4")  # Plafond

        self.frame_jeu.create_rectangle(1150, 620, 1180, 680, fill="salmon4", outline="OrangeRed4")  # Porte
        self.frame_jeu.create_rectangle(1180, 620, 1210, 680, fill="salmon4", outline="OrangeRed4")


    def creer_menu_vague_chrono(self):
        self.frame_jeu.create_rectangle(40, 760, 200, 920, fill="Yellow green", outline="white")
        self.frame_jeu.create_text(120, 770, text="Chronomètre", fill="black", font=('Helvetica 15 bold'))
        self.frame_jeu.create_line(40, 840, 200, 840, fill="white")
        self.frame_jeu.create_text(120, 852, text="Vague", fill="black", font=('Helvetica 15 bold'))


    def creer_menu_choix_tours(self, evt):
        self.frame_jeu.delete("menu_upgrade")
        self.frame_jeu.create_rectangle(240, 760, 720, 920, fill="Yellow green", outline="white",  tags=("menu_tour",))
        self.frame_jeu.create_text(350, 780, text="Choix de tours", fill="black", font=('Helvetica 15 bold'), tags=("menu_tour" ,))

        self.frame_button1 = self.frame_jeu.create_oval(315, 800, 345, 830, fill="OliveDrab2", outline="white", tags=("button1", "menu_tour",))
        self.frame_jeu.tag_bind("button1", "<Button-1>", self.creer_tour_laser)
        self.frame_jeu.create_text(330, 850, text="  TOUR \n LASER", fill="black", tags=("texte_button1", "menu_tour",), font=('Helvetica 13 bold'))

        self.frame_button2 = self.frame_jeu.create_oval(465, 800, 495, 830, fill="OliveDrab2", outline="white", tags=("button2", "menu_tour",))
        self.frame_jeu.tag_bind("button2", "<Button-1>", self.creer_tour_projectile)
        self.frame_jeu.create_text(479, 850, text="     TOUR \nPROJECTILE", fill="black", tags=("texte_button2", "menu_tour",), font=('Helvetica 13 bold'))

        self.frame_button3 = self.frame_jeu.create_oval(615, 800, 645, 830, fill="OliveDrab2", outline="white", tags=("button3", "menu_tour",))
        self.frame_jeu.tag_bind("button3", "<Button-1>", self.creer_tour_poison)
        self.frame_jeu.create_text(630, 850, text="  TOUR \n POISON", fill="black", tags=("texte_button3", "menu_tour",), font=('Helvetica 13 bold'))


    def creer_menu_upgrade_tour(self, evt):
        self.frame_jeu.delete("menu_tour")
        self.frame_jeu.create_rectangle(240, 760, 720, 920, fill="turquoise3", outline="white", tags=("menu_upgrade",))
        self.frame_jeu.create_text(350, 780, text="Upgrade tour", fill="black", font=('Helvetica 15 bold'), tags=("menu_upgrade",))

        self.frame_button1 = self.frame_jeu.create_rectangle(280, 800, 400, 880, fill="turquoise2", outline="white",
                                                             tags=("button1", "menu_upgrade",))
        self.frame_jeu.create_text(320, 850, text="", fill="black", tags=("menu_upgrade",))

        self.frame_button_upgrade = self.frame_jeu.create_rectangle(440, 800, 520, 880, fill="turquoise2", outline="white",
                                                             tags=("button_upgrade", "menu_upgrade",))
        self.frame_jeu.tag_bind("button_upgrade", "<Button-1>", self.upgrade_tour)
        self.frame_jeu.create_text(460, 850, text="", fill="black", tags=("menu_upgrade",))

        self.frame_button3 = self.frame_jeu.create_rectangle(560, 800, 680, 880, fill="turquoise2", outline="white",
                                                             tags=("button3", "menu_upgrade",))
        self.frame_jeu.create_text(460, 850, text="", fill="black", tags=("menu_upgrade",))
        self.creer_contenu_menu_upgrade_tour()


    def creer_contenu_menu_upgrade_tour(self):
        self.t_projectile_1 = "\nTir des balles \n lentement"
        self.t_projectile_2 = "\nMitrailleur tir \nplus rapidement"
        self.t_projectile_3 = "\nLance-grenade, \nplus lent mais \nplus fort"
        self.t_laser_1 = "\n\nUn éclair qui \naffecte la cible \nquelques tours \nde suite"
        self.t_laser_2 = "\n\nDevient un Laser \nfaible, qui suit \nun objectif tant \nqu’il est dans le \nchamp de la tour"
        self.t_laser_3 = "\n\nLaser puissant"
        self.t_poison_1 = "\n\nJette de l’acide \nqui agit lentement \nsur l’objet."
        self.t_poison_2 = "\nRecharge plus \nrapide"
        self.t_poison_3 = "\nAcide plus \nforte"

        self.frame_jeu.create_text(345, 820, text=self.t_laser_1, fill="black", tags=("menu_upgrade"),
                                   font=('Helvetica 13 bold'))
        self.frame_jeu.create_text(625, 820, text=self.t_laser_1, fill="black", tags=("menu_upgrade"),
                                   font=('Helvetica 13 bold'))

        # self.frame_jeu.tag_bind("tours", "<Button-1>", self.creer_menu_upgrade_tour)
        # self.upgrade_tour()

    def afficher_laser(self):
        self.frame_jeu.delete("laser")
        for i in self.modele.tours:
            if isinstance(i, Tour_laser):
                self.frame_jeu.create_line(i.dimensions["x1"], i.dimensions["y1"], i.dimensions["x2"],
                                           i.dimensions["y2"], fill="red", width=5, tags=("laser",))

    def creer_menu_nb_vies(self):
        self.frame_jeu.create_rectangle(960, 760, 1160, 840, fill="Yellow green", outline="white")
        self.frame_jeu.create_text(1060, 770, text="Vies", fill="black", font=('Helvetica 15 bold'), tags=("vie",))

    def creer_menu_argent(self):
        self.frame_jeu.create_rectangle(960, 880, 1160, 950, fill="Yellow green", outline="white")
        self.frame_jeu.create_text(1060, 900, text="argent", fill="black", font=('Helvetica 15 bold'), tags=("argent",))

    # def creer_tour(self, evt):
    #     pass

    def afficher_tours(self):
        self.frame_jeu.delete("tours")
        tours = self.modele.tours
        for i in tours:
            if isinstance(i, Tour_laser):
                self.frame_jeu.create_rectangle(i.x - 30, i.y - 30, i.x + 30, i.y + 30, fill="green", tags=("tours", i.id,))

            if isinstance(i, Tour_projectile):
                self.frame_jeu.create_rectangle(i.x - 30, i.y - 30, i.x + 30, i.y + 30, fill="pink", tags=("tours", i.id,))

            if isinstance(i, Tour_poison):
                self.frame_jeu.create_rectangle(i.x - 30, i.y - 30, i.x + 30, i.y + 30, fill="green yellow", tags=("tours", i.id,))

            self.frame_jeu.create_oval(i.x - 30, i.y - 30, i.x + 30, i.y + 30, fill="yellow", stipple='gray50',  tags=("tours", i.id,))

            self.frame_jeu.tag_bind("tours", "<Button-1>", self.creer_menu_upgrade_tour)

    def coordonees_tour(self, evt):
        print(self.frame_jeu.find_overlapping(evt.x - 30, evt.y - 30, evt.x + 30, evt.y + 30))
        if len(self.frame_jeu.find_overlapping(evt.x - 30, evt.y - 30, evt.x + 30, evt.y + 30)) <= 1:
            if self.modele.tour_a_creer != -1:
                self.modele.x = evt.x
                self.modele.y = evt.y



    def creer_tour_laser(self, evt):
        self.modele.tour_a_creer = 0
    #
    def creer_tour_projectile(self, evt):
        self.modele.tour_a_creer = 1
    #
    def creer_tour_poison(self, evt):
        self.modele.tour_a_creer = 2

    def upgrade_tour(self, evt):
        if self.parent.argent >= 50:
            self.modele.tour_a_upgrade = 0
            #self.tour_id = tour_id
            self.creer_menu_choix_tours("w")
        else:
            self.creer_menu_choix_tours("e")

    def afficher_obus(self):
        for i in self.modele.tours:
            if i.obus:
                if i.obus.alive:
                    self.frame_jeu.delete(i.obus.id)
                    obus = self.frame_jeu.create_oval(i.obus.x - 8,
                                                    i.obus.y - 8,
                                                    i.obus.x + 8,
                                                    i.obus.y + 8,
                                                    fill="grey",
                                                    tags=(i.obus.id, "obus"))
                    self.obus.append(obus)
                else:
                    self.frame_jeu.delete(i.obus.id)
                    self.obus.remove(i)

    def deplacement_obus(self):
        for i in self.modele.tours:
            self.frame_jeu.move(self.obus, i.obus.dx, i.obus.dy)


    def effacer_obus(self, obus):
        if obus.id and obus:
            self.frame_jeu.delete(obus.id)

    def afficher_fenetre_upgrade(self):
        self.frame_jeu
        self.tour_upgrade()




