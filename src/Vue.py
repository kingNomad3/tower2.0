from tkinter import *
from Modele import *

class Vue:
    def __init__(self, parent, modele):
        self.controleur = parent
        self.modele = modele
        self.root = Tk()

        self.largeur = 1152
        self.hauteur = 648
        self.largeur_chemin = 45

        self.ratio_x = 1
        self.ratio_y = 1

        self.font = "Arial " + str(int(15 * ((self.ratio_y + self.ratio_x) / 2)))
        self.font_2 = "Arial " + str(int(10 * ((self.ratio_y + self.ratio_x) / 2)))

        # frame interne
        self.interface_panel = None
        self.toggle_menu_tour = None
        self.frame = Frame(self.root)
        self.frame.pack(fill=BOTH, expand=YES)

        # canvas
        self.canvas = Canvas(self.frame, width=self.largeur, height=self.hauteur, bg="lightgreen", highlightthickness=0)
        self.canvas.bind("<Configure>", self.resize)
        self.canvas.pack(fill=BOTH, expand=YES)

        self.dessiner_segments()

        self.canvas.addtag_all("all")

        self.root.bind('<KeyPress-space>', self.skip)

        self.dessiner_interface_info()
        self.dessiner_chateau()
        self.dessiner_information()
        
        
    def afficher_choix_tours(self):
        self.canvas.create_rectangle(250 - 40, 640 - 40, 250 + 40,
                                     640 + 40,
                                     fill="BLACK", tags=('TO','TO_carre', ))
        self.canvas.create_rectangle(350 - 40, 640 - 40, 350 + 40,
                                     640 + 40,
                                     fill="BLACK", tags=('UP', 'TE', 'TE_carre', ))
        self.canvas.create_rectangle(450 - 40, 640 - 40, 450 + 40,
                                     640 + 40,
                                     fill="BLACK",tags=('TP', 'TP_carre',) )


    def skip(self, event):
        print(event.keysym)

    def dessiner_chateau(self):
        length = len(self.modele.partie.chemin.pivots)
        x = self.modele.partie.chemin.pivots[length-1][0]
        y = self.modele.partie.chemin.pivots[length-1][1]
        self.canvas.create_rectangle(x - 30, y - 30 , x + 30, y + 30, fill="GREY", outline="")
        self.canvas.create_rectangle(x - 15, 465 - 15, x + 15, 465 + 15, fill="RED", outline='')


    def dessiner_creeps(self):
        self.canvas.delete("creep")
        creep_largeur = Creep.largeur * self.ratio_x
        creep_hauteur = Creep.largeur * self.ratio_y
        # taille_vie = 10 * ((self.ratio_y + self.ratio_x) / 2) #supprimer, juste pour voir vie
        # font = "Arial " + str(int(taille_vie)) #
        # self.canvas.delete("creep_mana") #

        for creep in self.modele.partie.liste_creeps:

            self.canvas.create_oval(
                creep.pos_x * self.ratio_x - creep_largeur,
                creep.pos_y * self.ratio_y - creep_hauteur,
                creep.pos_x * self.ratio_x + creep_largeur,
                creep.pos_y * self.ratio_y + creep_hauteur,
                fill="red", tags=("creep", creep.id,))

            # self.canvas.create_text( #
            #     i.x * self.ratio_x, #
            #     i.y * self.ratio_y, #
            #     text=i.mana, tags=("creep_mana", ), font=font) #


    def creer_tour(self, event):
        # on clic : créé un tour dans le modèle
        tour_largeur = Tour.largeur * self.ratio_x
        tour_hauteur = Tour.largeur * self.ratio_y

        temp = self.canvas.find_overlapping(event.x - tour_largeur,
                                            event.y - tour_hauteur,
                                            event.x + tour_largeur,
                                            event.y + tour_hauteur)

        chemins = self.canvas.find_withtag("chemin")
        tours = self.canvas.find_withtag("tour")

        if not any(i in temp for i in chemins) and event.y + tour_largeur < 570 and not any(i in temp for i in tours):
            x = event.x / self.ratio_x
            y = event.y / self.ratio_y
            self.controleur.creer_tour(x, y)
            self.dessiner_icone_tour(self.modele.partie.liste_tours[-1])  # dessine la dernière tour mise
            self.canvas.unbind("<Button>", self.creation) #unbin apres avoir poser une tour
            self.reset_border()

    def reset_border(self):
        self.canvas.itemconfig('TO_carre', outline="")
        self.canvas.itemconfig('TP_carre', outline="")
        self.canvas.itemconfig('TE_carre', outline="")

    def dessiner_tours(self):
        # dessines les tours du modèle
        for tour in self.modele.partie.liste_tours:
            self.dessiner_icone_tour(tour)

    def dessiner_icone_tour(self, tour):
        # dessine une tour sur le canvas
        x = tour.pos_x * self.ratio_x
        y = tour.pos_y * self.ratio_y
        tour_largeur = tour.rayon * self.ratio_x
        tour_hauteur = tour.rayon * self.ratio_y
        tour_radius_x = tour.champ_action * self.ratio_x
        tour_radius_y = tour.champ_action * self.ratio_y
        radius_largeur = 5 * (self.ratio_y + self.ratio_x) / 2

        self.canvas.create_rectangle(x - tour_largeur, y - tour_hauteur, x + tour_largeur,
                                    y + tour_hauteur,
                                    fill="WHITE", tags=('tour',tour.id, ))

        self.canvas.create_oval(x - tour_radius_x, y - tour_radius_y, x + tour_radius_x,
                               y + tour_radius_y,
                                dash= (5,2), fill="", tags=('tour_radius',),
                                width=radius_largeur, outline="red")

        self.information = self.canvas.tag_bind('tour', "<Button>", self.get_info_tour)

        self.canvas.tag_lower('tour_radius')
        self.canvas.tag_lower('chemin')

    def get_info_tour(self, event):
        self.canvas.tag_unbind('TO', '<Button>', self.activation_to)
        self.canvas.tag_unbind('TO', '<Button>', self.activation_te)
        self.canvas.tag_unbind('TO', '<Button>', self.activation_tp)
        target = self.canvas.gettags("current")[1]


        for tour in self.modele.partie.liste_tours:
            if tour.id == target:
                self.afficher_info_tour(tour)


    def afficher_info_tour(self,tour):
        self.reset_border()
        self.canvas.tag_unbind('tour', '<Button>', self.information)
        self.tour_choisi = tour

        self.canvas.delete('choix_tour')
        self.canvas.create_text(330 * self.ratio_x, 585 * self.ratio_y, text="Amélioration sur tour selectionnée", font=self.font_2,
                                tags=("info_tour", "choix_tour",))
        self.canvas.create_text(250 * self.ratio_x, 620 * self.ratio_y, text="Cout", font=self.font_2,
                                tags=("info_tour",), fill="WHITE")
        self.canvas.create_text(250 * self.ratio_x, 640 * self.ratio_y, text="+Force", font=self.font_2,
                                tags=("info_tour",), fill="WHITE")
        self.canvas.create_text(250 * self.ratio_x, 660 * self.ratio_y, text="+Etendu", font=self.font_2,
                                tags=("info_tour",), fill="WHITE")
        self.canvas.create_text(450 * self.ratio_x, 620 * self.ratio_y, text="Tour", font=self.font_2,
                                tags=("info_tour",), fill="WHITE")
        self.canvas.create_text(450 * self.ratio_x, 640 * self.ratio_y, text="Lvl" + str(tour.niveau_amelioration), font=self.font_2,
                                tags=("info_tour", 'tour_lvl'), fill="WHITE")
        self.canvas.create_text(450 * self.ratio_x, 660 * self.ratio_y, text="Rayon" + str(tour.champ_action), font=self.font_2,
                                tags=("info_tour",), fill="WHITE")

        # bouton_x
        self.canvas.create_rectangle(510 - 7, 585 - 7, 510 + 7, 585 + 7, fill="gray75", tags=('btn_x', ))
        self.canvas.create_text(510, 585, text='X', font=self.font_2, tags=("info_tour", 'btn_x', ))
        self.btn_x = self.canvas.tag_bind('btn_x', '<Button>', self.fermer_info_tour)

        #bouton upgrade
        self.canvas.create_text(350 * self.ratio_x, 640 * self.ratio_y, text="Up", font=self.font_2,
                                tags=("info_tour", 'UP'), fill="WHITE")
        self.upgrade = self.canvas.tag_bind('UP', '<Button>', self.upgrade_tour)

    def upgrade_tour(self, evt):
        self.tour_choisi.update()
        self.canvas.itemconfig('tour_lvl', text="Lvl" + str(self.tour_choisi.niveau_amelioration))


    def fermer_info_tour(self, evt):
        self.canvas.tag_unbind('UP', '<Button>', self.upgrade)
        self.information = self.canvas.tag_bind('tour', "<Button>", self.get_info_tour)
        self.dessiner_information()


    def dessiner_obus(self):
        self.canvas.delete("projectile")
        projectile_largeur = Projectile.largeur * self.ratio_x
        projectile_hauteur = Projectile.largeur * self.ratio_y


        for tour in self.modele.partie.liste_tours:
            for projectile in tour.liste_projectiles:
                self.canvas.create_oval(
                projectile.pos_x * self.ratio_x - projectile_largeur,
                projectile.pos_y * self.ratio_y - projectile_hauteur,
                projectile.pos_x * self.ratio_x + projectile_largeur,
                projectile.pos_y * self.ratio_y + projectile_hauteur,
                fill="pink", tags=("projectile", projectile.id))

    def dessiner_jeu(self):
        self.dessiner_creeps()
        self.dessiner_obus()
        self.update_info_partie()

    # Caller dans le controleur a chaque tick de boucle
    # Update les valeurs dynamique du InterfacePannel    
    def update_info_partie(self):
        self.interface_panel.chrono_info['text'] = str(self.modele.partie.chrono)
        self.interface_panel.vague_info['text'] = str(self.modele.partie.vague)
        self.interface_panel.vie_info['text'] = str(self.modele.partie.vie)
        self.interface_panel.argent_info['text'] = str(self.modele.partie.argent_courant)
        
    # Dessine InterfacePannel et le Bouton ChoixTour
    def dessiner_interface_info(self):        
        if self.interface_panel and self.toggle_menu_tour:
            self.interface_panel.destroy()
            self.toggle_menu_tour.destroy()
            
        self.interface_panel = InterfacePannel(250 * self.ratio_x, 50 * self.ratio_y)
        self.interface_panel.place(anchor="ne", x=self.largeur-10, y=10)
        
        # # fuck le scalling???
        # self.toggle_menu_tour = PacManButton(50 * self.ratio_x, 10 * self.ratio_y, "tours")
        # self.toggle_menu_tour.place(anchor="ne", x=250, y=40)
    

    # def update_info_partie(self):
    #     timer = self.controleur.get_timer_str()
    #     self.canvas.itemconfig('vie', text=self.modele.partie.vie)
    #     self.canvas.itemconfig('vague', text=self.modele.partie.vague)
    #     self.canvas.itemconfig('argent', text=self.modele.partie.argent)
    #     self.canvas.itemconfig('timer', text=timer)


    def resize(self, evt):
        w = evt.width / self.largeur
        h = evt.height / self.hauteur
        self.largeur = evt.width
        self.hauteur = evt.height
        self.ratio_x *= w
        self.ratio_y *= h
        
        self.dessiner_interface_info()
        
        # reconfig
        self.canvas.config(width=self.largeur, height=self.hauteur)
        self.canvas.scale("all", 0, 0, w, h)
        self.canvas.itemconfig("chemin", width=self.largeur_chemin * (self.ratio_x + self.ratio_y) / 2)
        self.canvas.itemconfig("tour_radius", width=5 * (self.ratio_y + self.ratio_x) / 2)
        
        self.font = "Arial " + str(int(15 * ((self.ratio_y + self.ratio_x) / 2)))
        self.font_2 = "Arial " + str(int(11 * ((self.ratio_y + self.ratio_x) / 2)))

        self.canvas.itemconfig("info", font=self.font)
        self.canvas.itemconfig("info_tour", font=self.font_2)


    def dessiner_information(self):
        self.canvas.delete('info_tour', 'btn_x')

        self.canvas.create_text(90 * self.ratio_x, 585 * self.ratio_y, text="Chrono", font=self.font, tags=("info",))
        # self.canvas.create_text(90 * self.ratio_x, 615 * self.ratio_y, text=self.controleur.get_timer_str(), tags=("info",'timer', ), font=self.font)
        self.canvas.create_text(90 * self.ratio_x, 645 * self.ratio_y, text="Vague", font=self.font, tags=("info", ))
        self.canvas.create_text(90 * self.ratio_x, 675 * self.ratio_y, text=self.modele.partie.vague, tags=("info",'vague', ), font=self.font)
        self.canvas.create_text(260 * self.ratio_x, 585 * self.ratio_y, text="Choix de tours", font=self.font, tags=("info", "choix_tour", ))
        self.canvas.create_text(250 * self.ratio_x, 640 * self.ratio_y, text="TO", font=self.font, tags=("info", "choix_tour",'TO', ), fill="WHITE")
        self.canvas.create_text(350 * self.ratio_x, 640 * self.ratio_y, text="TE", font=self.font, tags=("info", "choix_tour", 'TE',), fill="WHITE")
        self.canvas.create_text(450 * self.ratio_x, 640 * self.ratio_y, text="TP", font=self.font, tags=("info", "choix_tour", 'TP',), fill="WHITE")
        self.canvas.create_text(760 * self.ratio_x, 585 * self.ratio_y, text="Vies", font=self.font, tags=("info", ))
        self.canvas.create_text(760 * self.ratio_x, 615 * self.ratio_y, text=self.modele.partie.vie, tags=("info",'vie', ), font=self.font, fill="RED")
        self.canvas.create_text(760 * self.ratio_x, 645 * self.ratio_y, text="Argent", font=self.font, tags=("info", ))
        self.canvas.create_text(760 * self.ratio_x, 675 * self.ratio_y, text=self.modele.partie.argent_courant, tags=("info",'argent', ), font=self.font)


        self.activation_to = self.canvas.tag_bind('TO', '<Button>', self.activer_creation_tour_to)
        self.activation_te = self.canvas.tag_bind('TE', '<Button>', self.activer_creation_tour_te)
        self.activation_tp = self.canvas.tag_bind('TP', '<Button>', self.activer_creation_tour_tp)

    def activer_creation_tour_to(self, event):
        # if self.modele.partie.peut_acheter_tour():
        self.reset_border()
        self.canvas.itemconfig('TO_carre',outline="RED", width=10)
        self.creation = self.canvas.bind("<Button>", self.creer_tour)

    def activer_creation_tour_te(self, event):
        # if self.modele.partie.peut_acheter_tour():
        self.reset_border()
        self.canvas.itemconfig('TE_carre',outline="RED", width=10)
        self.creation = self.canvas.bind("<Button>", self.creer_tour)

    def activer_creation_tour_tp(self, event):
        # if self.modele.partie.peut_acheter_tour():
        self.reset_border()
        self.canvas.itemconfig('TP_carre',outline="RED", width=10)
        self.creation = self.canvas.bind("<Button>", self.creer_tour)

    def dessiner_segments(self):
        segments = self.modele.partie.chemin.segments #self.chemin.segments

        for i, segment in enumerate(segments):
            try:
                x0 = segment[0]
                y0 = segment[1]
                x1 = segments[i + 1][0]
                y1 = segments[i + 1][1]

                self.canvas.create_line(x0, y0, x1, y1,
                                        tags=("chemin",), joinstyle=MITER)
            except IndexError:
                break

class InterfacePannel(Frame):
    
    def __init__(self, width, height):
        super().__init__()
        self['bg'] = 'black'
        self['width'] = width
        self['height'] = height
        self['highlightthickness'] = 3
        self['highlightbackground'] = 'blue'
        
        self.chrono_info = Label(self, text="$ 00:00", font=("arial", 11), fg="blue", bg="black")
        self.vague_info = Label(self, text="$ 100", font=("arial", 11), fg="blue",  bg="black")
        self.vie_info = Label(self, text="$ 20", font=("arial", 11), fg="blue",  bg="black")
        self.argent_info = Label(self, text="$ 10,000", font=("arial", 11), fg="blue", bg="black")
        
        self.chrono_info.place(anchor="center", relx= 0.15, rely=0.5)
        self.vague_info.place(anchor="center", relx= 0.4, rely=0.5)
        self.vie_info.place(anchor="center", relx= 0.6, rely=0.5)
        self.argent_info.place(anchor="center", relx= 0.85, rely=0.5)
    
    
        # #choix button qui trigger le menu placer tour
        
class PacManButton(Frame):
    def __init__(self, width, height, text):
        super().__init__()
        self['bg'] = 'black'
        self['width'] = width
        self['height'] = height
        self['highlightthickness'] = 2
        self['highlightbackground'] = 'goldenrod3'
        
        button = Button(self, bg='black', fg='goldenrod3', font=("Gill Sans Ultra Bold", 10), width=width, height=height, text=text)
        button.pack()
    
    