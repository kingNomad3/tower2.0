from tkinter import *
from Modele import *
from tkinter import ttk

from PIL import Image, ImageTk

class Vue:
    def __init__(self, parent, nom_joueur_local):
        self.controleur = parent
        self.modele = None
        self.root = Tk()
        self.nom_joueur_local = nom_joueur_local
        self.partie_active = False
        self.demarrer_partie = None
        
        self.cadres = {}    # dictionnaire des Frame pour changer la fen root d'etat
        self.cadre_courant = None
        self.images = {}
        self.creer_cadres(self.nom_joueur_local)
        self.tableau_choisi = None

        self.largeur = 1200
        self.hauteur = 648
        self.largeur_chemin = 55

        self.ratio_x = 1
        self.ratio_y = 1

        self.font = "Arial " + str(int(15 * ((self.ratio_y + self.ratio_x) / 2)))
        self.font_2 = "Arial " + str(int(10 * ((self.ratio_y + self.ratio_x) / 2)))
        
        self.menu_tour = None
        self.tag_bouton_choisi = None
        
    def afficher_cadre(self,cadre_demande):
        if self.cadre_courant:
            self.cadre_courant.pack_forget()
        self.cadre_courant = self.cadres[cadre_demande]
        self.cadre_courant.pack(expand=1,fill=BOTH)
        
    def creer_cadres(self,nom_joueur_local):
        self.cadres["cadre_splash"] = self.creer_cadre_splash(nom_joueur_local)
        
    def creer_cadre_splash(self, nom_joueur_local):
        # cadre pour toute la fenetre, contient 2 aires distinctes
        cadre_splash = Frame(self.root)
        self.canevas_splash = Canvas(cadre_splash,width=800,
                              height=800,bg="pink")
        # section Titre
        etiquette_entree = Etiquette(self.canevas_splash,text="Tours du CVM")
        self.canevas_splash.create_window(500,50,anchor="center",window=etiquette_entree)
        self.canevas_splash.pack()
        # section Identification
        self.canevas_splash.create_text(480,150,anchor="e",text="Identification",font=("Arial",18))
        values = []
        values.insert(0,nom_joueur_local)
        self.drop_nom = ttk.Combobox(self.canevas_splash,state="normal",
                                     values = values)
        self.drop_nom.set(nom_joueur_local)
        self.canevas_splash.create_window(520,150,anchor="w",window=self.drop_nom)

        # creation ds divers widgets (champ de texte 'Entry' et boutons cliquables (Button)
        # les champs et
        self.etat_du_jeu = Label(text="Non connecter", font=("Arial", 16), borderwidth=2, relief=RIDGE)
        self.url_initial = Entry(font=("Arial", 14))

        #self.url_initial.insert(0, "http://jmdeschamps.pythonanywhere.com")
        self.url_initial.insert(0, "http://127.0.0.1:8000") #"http://jmdeschamps.pythonanywhere.com"
        self.btnurlconnect = Button(text="Connecter", font=("Arial", 12), command=self.initialiser_splash_post_connection)
        # on les place sur le canevas_splash
        self.canevas_splash.create_window(220, 250, window=self.url_initial, width=200, height=30)
        self.canevas_splash.create_window(220, 300, window=self.btnurlconnect, width=100, height=30)
        self.canevas_splash.create_window(220, 350, window=self.etat_du_jeu, width=300, height=30)

        # section pour partie reseau
        self.btncreerpartie = Button(text="Creer partie reseau", font=("Arial", 12), state=DISABLED, command=self.creer_partie)
        self.btninscrirejoueur = Button(text="Inscrire a partie reseau", font=("Arial", 12), state=DISABLED,
                                        command=self.inscrire_joueur)
        self.btnreset = Button(text="Reinitialiser partie", font=("Arial", 9), state=DISABLED,
                               command=self.reset_partie)
        # on place les boutons
        self.canevas_splash.create_window(220, 400, window=self.btncreerpartie, width=200, height=30)
        self.canevas_splash.create_window(220, 450, window=self.btninscrirejoueur, width=200, height=30)
        self.canevas_splash.create_window(220, 500, window=self.btnreset, width=200, height=30)

        # section pour partie locale
        self.btn_ouvrir_lobby_local=Button(cadre_splash,text="Creer partie locale",command=self.ouvrir_lobby_local)
        self.btn_ouvrir_bonus=Button(cadre_splash,text="Ouvrir magasin de Bonus",command=self.ouvrir_bonus)

        self.canevas_splash.create_window(680,450,anchor="center",window=self.btn_ouvrir_lobby_local)
        self.canevas_splash.create_window(680,500,anchor="center",window=self.btn_ouvrir_bonus)
        return cadre_splash

    def creer_cadre_lobby_reseau(self):
        pass

    def creer_cadre_lobby(self, local_ou_reseau, joueurs):
        # cadre pour toute la fenetre, contient 2 aires distinctes
        cadre_lobby = Frame(self.root)
        self.canevas_lobby = Canvas(cadre_lobby,width=800,
                              height=800,bg="lightgreen")
        self.canevas_lobby.pack()

        self.canevas_lobby.create_text(400,50,anchor="center",text="Lobby des Tours du CVM",font=("Arial",24))
        self.canevas_lobby.create_text(400,100,anchor="center",text=local_ou_reseau,font=("Arial",18))

        self.btn_lancer_partie=Button(self.canevas_lobby,text="Debuter la partie",
                                      command=self.lancer_partie,)
        self.canevas_lobby.create_window(400,700,anchor="center",window=self.btn_lancer_partie)
        #
        if local_ou_reseau == "reseau":
            if len(joueurs)== 1:
                self.canevas_lobby.create_text(200,200,text="Createur de la partie")
                joueur_createur = joueurs[0][0]
                self.label_joueur_createur = Label(self.canevas_lobby,text = joueur_createur)
                self.canevas_lobby.create_window(200,250,window=self.label_joueur_createur)
            #
                self.canevas_lobby.create_text(500, 200, text="Joueur Coop de la partie")
                self.label_joueur_coop = Label(self.canevas_lobby, text="Inconnu")
                self.canevas_lobby.create_window(500, 250, window=self.label_joueur_coop)
            else:
                self.canevas_lobby.create_text(200,200,text="Createur de la partie")
                joueur_createur = joueurs[0][0]
                self.label_joueur_createur = Label(self.canevas_lobby,text = joueur_createur)
                self.canevas_lobby.create_window(200,250,window=self.label_joueur_createur)
            #
                self.canevas_lobby.create_text(500, 200, text="Joueur Coop de la partie")
                joueur_coop = joueurs[1][0]
                self.label_joueur_coop = Label(self.canevas_lobby, text=joueur_coop)
                self.canevas_lobby.create_window(500, 250, window=self.label_joueur_coop)
                self.btn_lancer_partie.config(state="disabled")
        else:
            self.btn_lancer_partie.config(command=self.lancer_partie_locale)

        ##
        # Create a matrix of buttons for board selection on the canvas
        x = 200
        y = 350
        for rang in range(3):
            x = x + 100
            no_tablo = rang
            self.btn_tablo = Button(self.canevas_lobby, text=f"Tablo {no_tablo}")
            self.btn_tablo.bind("<Button>",self.choisir_tablo)
            self.canevas_lobby .create_window(x, y, anchor="center", window=self.btn_tablo)
        ##
        self.cadres["cadre_lobby"] = cadre_lobby
        
    def creer_cadre_jeu(self):
        self.interface_panel = None
        self.toggle_menu_tour = None
        cadre_jeu = Frame(self.root)
        cadre_jeu.pack(fill=BOTH, expand=YES)

        self.canvas = Canvas(cadre_jeu, width=self.largeur, height=self.hauteur, bg="black", highlightthickness=0)
        self.canvas.bind("<Configure>", self.resize)
        self.canvas.pack(fill=BOTH, expand=YES)

        self.dessiner_segments()

        self.canvas.addtag_all("all")

        self.root.bind('<KeyPress-space>', self.skip)

        self.dessiner_interface_info()
        self.dessiner_interface_tour()
        # self.dessiner_menu()
        self.dessiner_chateau()
        # on place ce cadre parmi l'ensemble des cadres
        self.cadres["cadre_jeu"]= cadre_jeu
        
    def initialiser_splash_post_connection(self):
        self.btninscrirejoueur.config(state=NORMAL)
        self.btncreerpartie.config(state=NORMAL)
        self.btnreset.config(state=NORMAL)
        url_serveur = self.url_initial.get()
        if url_serveur:
            self.controleur.initialiser_splash_post_connection(url_serveur)
        else:
            self.etat_du_jeu.config(text="Aucune adresse de serveur")

    def update_splash(self, etat):
        if "attente" in etat or "courante" in etat:
            self.btncreerpartie.config(state=DISABLED)
        if "courante" in etat:
            self.etat_du_jeu.config(text="Desole - partie encours !")
            self.btninscrirejoueur.config(state=DISABLED)
        elif "attente" in etat:
            self.etat_du_jeu.config(text="Partie en attente de joueurs !")
            self.btninscrirejoueur.config(state=NORMAL)
        elif "dispo" in etat:
            self.etat_du_jeu.config(text="Bienvenue ! Serveur disponible")
            self.btninscrirejoueur.config(state=DISABLED)
            self.btncreerpartie.config(state=NORMAL)
        else:
            self.etat_du_jeu.config(text="ERREUR - un probleme est survenu")

    def update_lobby(self, joueurs):
        if len(joueurs) == 2:
            self.label_joueur_coop.config(text=joueurs[1][0])
            if self.controleur.egoserveur == True:
                self.btn_lancer_partie.config(state=NORMAL)

    def creer_partie(self):
        nom = self.drop_nom.get()
        self.controleur.creer_partie(nom)

    def lancer_partie_locale(self):
        self.controleur.initialiser_partie_locale()

    def lancer_partie(self):
        self.controleur.lancer_partie()

    def inscrire_joueur(self):
        nom = self.drop_nom.get()
        urljeu = self.url_initial.get()
        self.controleur.inscrire_joueur(nom, urljeu)

    def reset_partie(self):
        rep = self.controleur.reset_partie()

    def choisir_tablo(self, evt):
        tablo_choisi = evt.widget
        self.tableau_choisi = int(tablo_choisi.cget("text")[-1:])
        self.controleur.choisir_tablo(self.tableau_choisi)

    def trouver_usagers_locaux(self):
        nom_values = self.controleur.requerir_info("joueurs_locaux",["nom"] )
        return nom_values

    def ouvrir_lobby_local(self):
        nom_values = self.controleur.agent_bd.chercher_usagers()
        nom_joueur_courant = self.drop_nom.get()
        if nom_joueur_courant not in nom_values:
            self.controleur.agent_bd.ajouter_aux_usagers_locaux(nom_joueur_courant)
        self.controleur.creer_partie_locale(nom_joueur_courant)

    def ouvrir_bonus(self):
        pass #self.afficher_cadre("cadre_jeu")   
    
    def activer_partie(self):
        self.controleur.activer_partie()
        self.demarrer_partie.destroy()
        self.partie_active = True
    
    def afficher_choix_tours(self):
        self.canvas.create_rectangle(250 - 40, 640 - 40, 250 + 40,
                                     640 + 40,
                                     fill="white", tags=('TO','TO_carre', ))
        self.canvas.create_rectangle(350 - 40, 640 - 40, 350 + 40,
                                     640 + 40,
                                     fill="white", tags=('UP', 'TE', 'TE_carre', ))
        self.canvas.create_rectangle(450 - 40, 640 - 40, 450 + 40,
                                     640 + 40,
                                     fill="white",tags=('TP', 'TP_carre',) )


    def skip(self, event):
        print(event.keysym)

    def dessiner_chateau(self):
        x = self.modele.partie.chemin.pivots[self.tableau_choisi][-1][0]
        y = self.modele.partie.chemin.pivots[self.tableau_choisi][-1][1]
        self.canvas.create_rectangle(x - 30, y - 30 , x + 30, y + 30, fill="GREY", outline="")
        self.canvas.create_rectangle(x - 15, 465 - 15, x + 15, 465 + 15, fill="RED", outline='')


    def dessiner_creeps(self):
        self.canvas.delete("creep")
        creep_largeur = Creep.largeur * self.ratio_x
        creep_hauteur = Creep.largeur * self.ratio_y

        for creep in self.modele.partie.liste_creeps:
            img = Image.open(creep.img_src)
            img = img.resize((int(creep_largeur), int(creep_hauteur)), Image.Resampling.NEAREST)
            tk_img = ImageTk.PhotoImage(img)
            
            # Store the image reference to prevent garbage collection
            self.images[creep.id] = tk_img
            
            self.canvas.create_image((creep.pos_x * self.ratio_x, creep.pos_y * self.ratio_y), anchor='center', image=tk_img, tags=("creep", creep.id,))


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
            self.controleur.creer_tour(self.tag_bouton_choisi, x, y)

            if self.modele.partie.joueurs[self.controleur.nom_joueur_local].tours:
                self.dessiner_icone_tour(self.modele.partie.joueurs[self.controleur.nom_joueur_local].tours[-1])  # dessine la dernière tour mise
            self.canvas.unbind("<Button>", self.creation) #unbin apres avoir poser une tour
            # self.reset_border()
    

    def dessiner_tours(self):
        # dessines les tours du modèle
        self.canvas.delete('dynamique')
        for tour in self.modele.partie.joueurs[self.controleur.nom_joueur_local].tours:
            self.dessiner_icone_tour(tour)

    def dessiner_icone_tour(self, tour):
        size = 50
        # dessine une tour sur le canvas
        x = tour.pos_x * self.ratio_x
        y = tour.pos_y * self.ratio_y
        tour_largeur = size * self.ratio_x
        tour_hauteur = size * self.ratio_y
        tour_radius_x = tour.champ_action * self.ratio_x
        tour_radius_y = tour.champ_action * self.ratio_y
        radius_largeur = 1 * (self.ratio_y + self.ratio_x) / 2
        
        img = Image.open(tour.img_src)
        img = img.resize((int(tour_largeur), int(tour_hauteur)), Image.Resampling.NEAREST)
        
        if tour.cible:
            angle = (hp.Helper.calcAngle(tour.pos_x, tour.pos_y, tour.cible.pos_x, tour.cible.pos_y) * 180) % 360 * - 1
            img = img.rotate(angle)
            
        tk_img = ImageTk.PhotoImage(img)
        
        # Store the image reference to prevent garbage collection
        self.images[tour.id] = tk_img

        self.canvas.create_image((x, y), anchor='center',
                                    image=tk_img, tags=('tour','dynamique',tour.id, ))

        self.canvas.create_oval(x - tour_radius_x, y - tour_radius_y, x + tour_radius_x,
                               y + tour_radius_y,
                                dash= (3,5), fill="", width= radius_largeur, tags=('tour_radius', 'dynamique'), outline="lightblue")
    
        self.information = self.canvas.tag_bind('tour', "<Button>", self.get_info_tour)

        self.canvas.tag_lower('tour_radius')
        self.canvas.tag_lower('chemin')
        self.canvas.tag_lower('chemin_outline')

    def get_info_tour(self, event):
        self.canvas.tag_unbind('TO', '<Button>', self.activation_to)
        self.canvas.tag_unbind('TE', '<Button>', self.activation_te)
        self.canvas.tag_unbind('TP', '<Button>', self.activation_tp)
        target = self.canvas.gettags("current")[1]

        for tour in self.modele.partie.joueurs[self.controleur.nom_joueur_local].tours:
            if tour.id == target:
                self.afficher_info_tour(tour)


    def afficher_info_tour(self,tour):
        # self.reset_border()
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


    def dessiner_obus(self):
        self.canvas.delete("projectile")
        projectile_largeur = Projectile.largeur * self.ratio_x
        projectile_hauteur = Projectile.largeur * self.ratio_y

        for tour in self.modele.partie.joueurs[self.controleur.nom_joueur_local].tours:
            for projectile in tour.liste_projectiles:
                self.canvas.create_rectangle(
                projectile.pos_x * self.ratio_x - projectile_largeur,
                projectile.pos_y * self.ratio_y - projectile_hauteur,
                projectile.pos_x * self.ratio_x + projectile_largeur,
                projectile.pos_y * self.ratio_y + projectile_hauteur,
                fill="yellow", outline="yellow",stipple="gray50", tags=("projectile", projectile.id))

    def dessiner_jeu(self):
        # print(len(self.canvas.find_all()))
        self.images = {}
        self.dessiner_creeps()
        self.dessiner_obus()
        self.dessiner_tours()
        self.update_info_partie()

    # Caller dans le controleur a chaque tick de boucle
    # Update les valeurs dynamique du InterfacePannel    
    def update_info_partie(self):
        self.interface_panel.chrono_info['text'] = str(round(self.modele.partie.chrono))
        self.interface_panel.vague_info['text'] = str(self.modele.partie.vague)
        self.interface_panel.vie_info['text'] = str(self.modele.partie.vie)
        self.interface_panel.argent_info['text'] = str(self.modele.partie.argent_courant)
        
    # Dessine InterfacePannel et le Bouton ChoixTour
    def dessiner_interface_info(self):        
        if self.interface_panel:
            self.interface_panel.destroy()
            
        if not self.partie_active:
            if self.demarrer_partie:
                self.demarrer_partie.destroy()
            self.demarrer_partie = PacManButton(int(20 * self.ratio_x), int(2 * self.ratio_y), "Démarrer la partie", self.activer_partie)
            self.demarrer_partie.place(anchor="center", relx=0.5, y=40)
            
        self.interface_panel = InterfacePannel(250 * self.ratio_x, 50 * self.ratio_y)
        self.interface_panel.place(anchor="ne", x=self.largeur-10, y=10)

    def dessiner_interface_tour(self):
        if self.menu_tour:
            self.destroy_menu_tour()
        
        self.menu_tour =  InterfaceTour(self.largeur, 250 * self.ratio_x, 500 * self.ratio_y, self.ratio_x, self.ratio_y, self.bind_canvas)
        self.menu_tour.place(anchor="ne", x=self.largeur-10, y=70)

    def destroy_menu_tour(self):
        self.menu_tour.activation_to.destroy()
        self.menu_tour.activation_tp.destroy()
        self.menu_tour.activation_te.destroy()
        self.menu_tour.activation_tm.destroy()
        self.menu_tour.activation_tg.destroy()
        self.menu_tour.activation_tc.destroy()
        self.menu_tour.destroy()
        
    def resize(self, evt):
        w = evt.width / self.largeur
        h = evt.height / self.hauteur
        self.largeur = evt.width
        self.hauteur = evt.height
        self.ratio_x *= w
        self.ratio_y *= h
        
        self.dessiner_interface_info()
        self.dessiner_interface_tour()
        
        # reconfig
        self.canvas.config(width=self.largeur, height=self.hauteur)
        self.canvas.scale("all", 0, 0, w, h)
        self.canvas.itemconfig("chemin_outline", width=(self.largeur_chemin+5) * (self.ratio_x + self.ratio_y) / 2)
        self.canvas.itemconfig("chemin", width=self.largeur_chemin * (self.ratio_x + self.ratio_y) / 2)
        self.canvas.itemconfig("tour_radius", width=1 * (self.ratio_y + self.ratio_x) / 2)
        self.canvas.tag_lower('chemin_outline')

        
        self.font = "Arial " + str(int(15 * ((self.ratio_y + self.ratio_x) / 2)))
        self.font_2 = "Arial " + str(int(11 * ((self.ratio_y + self.ratio_x) / 2)))

        self.canvas.itemconfig("info", font=self.font)
        self.canvas.itemconfig("info_tour", font=self.font_2)

    def bind_canvas(self, button):
        self.tag_bouton_choisi = button
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
                                        tags=("chemin_outline",), joinstyle=MITER, fill='blue')
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
        

class InterfaceTour(Frame):
    def __init__(self, largeur, width, height, ratio_x=1, ratio_y=1, command = None):
        super().__init__()
        self['bg'] = 'black'
        self['width'] = width
        self['height'] = height
        self['highlightthickness'] = 3
        self['highlightbackground'] = 'blue'
        
        self.activation_to = PacManButton(int(20*ratio_x), int(1*ratio_y), "Tour Mitrailleuse", command=lambda: command("TourMitrailleuse"))
        self.activation_te = PacManButton(int(20*ratio_x), int(1*ratio_y), "Tour Eclair" , command=lambda: command("TourEclair"))
        self.activation_tp = PacManButton(int(20*ratio_x), int(1*ratio_y), "Tour Poison", command=lambda: command("TourPoison"))
        self.activation_tg = PacManButton(int(20*ratio_x), int(1*ratio_y), "Tour Grenade", command=lambda: command("TourGrenade"))
        self.activation_tm = PacManButton(int(20*ratio_x), int(1*ratio_y), "Tour Mine", command=lambda: command("TourMine"))
        self.activation_tc = PacManButton(int(20*ratio_x), int(1*ratio_y), "Tour Canon", command=lambda: command("TourCanon"))
                
        self.activation_to.place(x=largeur-27 * ratio_x, y=90, anchor="ne")
        self.activation_te.place(x=largeur-27 * ratio_x, y=130, anchor="ne")
        self.activation_tp.place(x=largeur-27 * ratio_x, y=170, anchor="ne")
        self.activation_tg.place(x=largeur-27 * ratio_x, y=210, anchor="ne")
        self.activation_tm.place(x=largeur-27 * ratio_x, y=250, anchor="ne")
        self.activation_tc.place(x=largeur-27 * ratio_x, y=290, anchor="ne")
        
        
class PacManButton(Frame):
    def __init__(self, width, height, text, command=None):
        super().__init__()
        self['bg'] = 'black'
        self['width'] = width
        self['height'] = height
        self['highlightthickness'] = 2
        self['highlightbackground'] = 'goldenrod3'
        
        button = Button(self, bg='black', fg='goldenrod3', font=("Gill Sans Ultra Bold", 10), width=width, height=height, text=text, command=command)
        button.pack()
    
class Etiquette(Label):
    def __init__(self,master,*args, **kwargs):
        Label.__init__(self,master,*args, **kwargs)
        self.config(font=("arial",48,"bold"))
        self.config(fg="goldenrod3")
    