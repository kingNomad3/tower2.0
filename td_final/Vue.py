from tkinter import *
from Modele import *
from tkinter import ttk
import math

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
        self.tableau_choisi = None

        self.largeur = 1260
        self.hauteur = 648
        self.largeur_chemin = 55

        self.ratio_x = 1
        self.ratio_y = 1

        self.btn_tablo = []
        
        self.creer_cadres(self.nom_joueur_local)
        self.menu_tour = None
        self.tag_bouton_choisi = None
        self.tour_choisi = None
        self.btn_upgrade = None
        self.champ_action_toggled = False
        self.toggle_radius = None
        
    def afficher_cadre(self,cadre_demande):
        if self.cadre_courant:
            self.cadre_courant.pack_forget()
        self.cadre_courant = self.cadres[cadre_demande]
        self.cadre_courant.pack(expand=1,fill=BOTH)
        
    def creer_cadres(self,nom_joueur_local):
        self.cadres["cadre_splash"] = self.creer_cadre_splash(nom_joueur_local)
        
    def creer_cadre_splash(self, nom_joueur_local):
        self.root.resizable(False,False)
        fontStyleTitle = ("Gill Sans Ultra", 14)
        fontStyle = ("Gill Sans Ultra", 10)
        
        # cadre pour toute la fenetre, contient 2 aires distinctes
        cadre_splash = Frame(self.root)
        self.canevas_splash = Canvas(cadre_splash,width=self.largeur,
                              height=self.hauteur,bg="black")
        # section Titre
        self.img= ImageTk.PhotoImage(Image.open("img/logo.png"))
        self.canevas_splash.create_image(self.largeur/2,0, anchor="n",image=self.img)
        self.canevas_splash.pack()
        
        # Image splash
        self.img2= ImageTk.PhotoImage(Image.open("img/pacman_splashScreen.png"))
        self.canevas_splash.create_image(620,180, anchor="n",image=self.img2)
        self.canevas_splash.pack()
        
        # section Identification
        self.canevas_splash.create_text(self.largeur/6*2+20,170,anchor="n",text="Identification",font=fontStyleTitle, fill='yellow')
        values = self.controleur.agent_bd.chercher_usagers()
        self.drop_nom = ttk.Combobox(self.canevas_splash,state="normal",
                                     values = values, font=fontStyleTitle, justify='center')
        self.drop_nom.set(values[0])
        self.drop_nom.bind("<<ComboboxSelected>>", self.on_combobox_select)
        self.canevas_splash.create_window(self.largeur/6*3.5,170,anchor="n",window=self.drop_nom)

        # creation ds divers widgets (champ de texte 'Entry' et boutons cliquables (Button)
        # les champs et
        self.etat_du_jeu = Label(text="Non connecté", font=fontStyle, borderwidth=2, relief=RIDGE)
        self.url_initial = Entry(font=fontStyle, justify='center')

        self.url_initial.insert(0, "http://127.0.0.1:8000")    
        self.btnurlconnect = PacManButton(20, 1, "Connecter", command=self.initialiser_splash_post_connection)
        
        # on les place sur le canevas_splash
        self.canevas_splash.create_window(200, 250, window=self.url_initial, width=270, height=30)
        self.btnurlconnect.place(x=206, y=300,anchor="n")
        self.canevas_splash.create_window(206, 360, window=self.etat_du_jeu, width=310, height=30)

        # section pour partie reseau
        self.btncreerpartie = PacManButton(20, 1, "Creer partie reseau", command=self.creer_partie)
        self.btncreerpartie.button.config(state=DISABLED)
        self.btncreerpartie.place(x=206, y=400, anchor="n")
        
        self.btninscrirejoueur = PacManButton(20, 1, "Inscrire a partie reseau", command=self.inscrire_joueur)
        self.btninscrirejoueur.button.config(state=DISABLED)
        self.btninscrirejoueur.place(x=206, y=440, anchor="n")
        
        self.btnreset = PacManButton(20, 1, "Reinitialiser partie", command=self.reset_partie)
        self.btnreset.button.config(state=DISABLED)
        self.btnreset.place(x=206, y=480, anchor="n")

        # section pour partie locale        
        self.btn_ouvrir_lobby_local = PacManButton(20, 1, "Creer partie locale", command=self.ouvrir_lobby_local)
        self.btn_ouvrir_lobby_local.place(x=1000, y=230, anchor="n")
        
        self.btn_ouvrir_bonus = PacManButton(25, 1, "Ouvrir le panneau des défis", command=self.ouvrir_bonus)
        self.btn_ouvrir_bonus.place(x=1000, y=280,anchor="n")

        self.credits = Label(text=f'Crédits : {self.controleur.agent_bd.voir_credits(self.nom_joueur_local)}', font=fontStyleTitle, borderwidth=2, bg="black", fg='#F1D92A')
        self.credits.place(x=1000, y=330,anchor="n")

        return cadre_splash
        
    def on_combobox_select(self, evt):
        self.nom_joueur_local = self.drop_nom.get()
        self.credits.config(text=f'Crédits : {self.controleur.agent_bd.voir_credits(self.nom_joueur_local)}')
    
    def ouvrir_bonus(self):
        fontStyleTitle = ("Gill Sans Ultra", 10)
        
        self.frame_defis = Frame(self.root, width=self.largeur, height=self.hauteur, highlightbackground='#F1D92A', highlightthickness=4, bg='black')
        self.canevas_splash = Canvas(self.frame_defis,width=self.largeur,
                              height=self.hauteur,bg="black")
        self.img_defis= ImageTk.PhotoImage(Image.open("img/defis.png"))
        self.canevas_splash.create_image(self.largeur/2,0, anchor="n",image=self.img_defis)
        self.canevas_splash.pack()
                
        # Carrées
        self.canevas_splash.create_rectangle(100,150,600,330, outline='orange', width=1)
        self.canevas_splash.create_rectangle(120,170,580,310, outline='orange', width=4)
        
        self.canevas_splash.create_rectangle(100,370,600,550, outline='yellow2', width=1)
        self.canevas_splash.create_rectangle(120,390,580,530, outline='yellow2', width=4)
        
        self.canevas_splash.create_rectangle(650,150,1150,330, outline='DeepSkyBlue1', width=1)
        self.canevas_splash.create_rectangle(670,170,1130,310, outline='DeepSkyBlue1', width=4)
        
        self.canevas_splash.create_rectangle(650,370,1150,550, outline='hot pink', width=1)
        self.canevas_splash.create_rectangle(670,390,1130,530, outline='hot pink', width=4)
        
        # Texte
        
        self.canevas_splash.create_text(350, 225, text=f'Tuer 1 million de creep : {self.controleur.agent_bd.voir_defis(self.nom_joueur_local)} / 1 000 000', fill='white', font=fontStyleTitle)
        self.canevas_splash.create_text(350, 250, text=f'Récompense : 500 crédits', fill='orange', font=fontStyleTitle)
        
        self.canevas_splash.create_text(350, 460, text=f'Pas encore débloqué', fill='yellow2', font=fontStyleTitle)
        
        self.canevas_splash.create_text(900, 240, text=f'Pas encore débloqué', fill='DeepSkyBlue1', font=fontStyleTitle)
        
        self.canevas_splash.create_text(900, 460, text=f'Pas encore débloqué', fill='hot pink', font=fontStyleTitle)

        # Quitter
        self.quitter_defis = PacManButton(20, 1, "Quitter", command=self.effacer_fenetre_defis)
        self.quitter_defis.place(relx=0.5, rely=0.9,anchor="n")
        
        self.frame_defis.place(relx = 0.5, rely=0.5, anchor="center")
    
    def effacer_fenetre_defis(self):
        self.frame_defis.destroy()
        self.quitter_defis.destroy()

    def creer_cadre_lobby(self, local_ou_reseau, joueurs):
        fontStyleTitle = ("Gill Sans Ultra Bold", 11)
        
        self.root.resizable(False,False)
        # cadre pour toute la fenetre, contient 2 aires distinctes
        cadre_lobby = Frame(self.root)
        self.canevas_lobby = Canvas(cadre_lobby,width=self.largeur,
                              height=self.hauteur,bg="black")      
        self.canevas_lobby.pack()
        
        #Logo lobby
        if local_ou_reseau == 'local':
            self.logo_lobby= ImageTk.PhotoImage(Image.open("img/lobby_logo.png"))
        else:
            self.logo_lobby= ImageTk.PhotoImage(Image.open("img/lobby_logo_reseau.png"))
        self.canevas_lobby.create_image(self.largeur/2,0, anchor="n",image=self.logo_lobby)
        
        #Image lobby
        self.img= ImageTk.PhotoImage(Image.open("img/bg_lobby.jpg"))
        self.canevas_lobby.create_image(self.largeur/2, self.hauteur-300, anchor="n",image=self.img)

        self.btn_lancer_partie = PacManButton(15, 1, "Debuter la partie", self.lancer_partie)
        self.btn_lancer_partie.place(x=600, y=400, anchor="center")
        self.btn_lancer_partie.button.config(state=DISABLED)    
        self.canevas_lobby.create_window(600,400,anchor="center", window=self.btn_lancer_partie)
        
        ##
        # Create a matrix of buttons for board selection on the canvas
        x = 400
        y = 350
        for rang in range(3):
            x = x + 120
            no_tablo = rang
            btn = PacManButton(8, 1, f"Tableau {no_tablo}", command="")
            btn.button.bind("<Button>", self.choisir_tablo)
            btn.place(x=x-50, y=y, anchor="center")
            self.btn_tablo.append(btn)
        ##

        if local_ou_reseau == "reseau":
            if len(joueurs) == 1:
                self.canevas_lobby.create_text(200,490,text="Createur de la partie", font=fontStyleTitle, fill='yellow')
                joueur_createur = joueurs[0][0]
                self.label_joueur_createur = Label(self.canevas_lobby,text = joueur_createur, font=fontStyleTitle, fg='black')
                self.canevas_lobby.create_window(200,520,window=self.label_joueur_createur)
            #
                self.canevas_lobby.create_text(1050, 490, text="Joueur Coop de la partie", font=fontStyleTitle, fill='yellow')
                self.label_joueur_coop = Label(self.canevas_lobby, text="Inconnu", font=fontStyleTitle, fg='black')
                self.canevas_lobby.create_window(1050, 520, window=self.label_joueur_coop)
            else:
                self.canevas_lobby.create_text(200,490,text="Createur de la partie", font=fontStyleTitle)
                joueur_createur = joueurs[0][0]
                self.label_joueur_createur = Label(self.canevas_lobby,text = joueur_createur)
                self.canevas_lobby.create_window(200,520,window=self.label_joueur_createur)
            #
                self.canevas_lobby.create_text(1050, 490, text="Joueur Coop de la partie", font=fontStyleTitle)
                joueur_coop = joueurs[1][0]
                self.label_joueur_coop = Label(self.canevas_lobby, text=joueur_coop)
                self.canevas_lobby.create_window(1050, 520, window=self.label_joueur_coop)

                for i in range(3):
                    self.btn_tablo[i].button.config(state="disabled")

                self.btn_lancer_partie.button.config(state="disabled")
        else:
            self.btn_lancer_partie.button.config(command=self.lancer_partie_locale)

        
        self.cadres["cadre_lobby"] = cadre_lobby
        
    def creer_cadre_jeu(self):
        self.root.resizable(True,True)
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
        self.dessiner_chateau()

        self.cadres["cadre_jeu"]= cadre_jeu
        
    def initialiser_splash_post_connection(self):
        self.btninscrirejoueur.button.config(state=NORMAL)
        self.btncreerpartie.button.config(state=NORMAL)
        self.btnreset.button.config(state=NORMAL)
        url_serveur = self.url_initial.get()
        if url_serveur:
            self.controleur.initialiser_splash_post_connection(url_serveur)
        else:
            self.etat_du_jeu.config(text="Aucune adresse de serveur")

    def update_splash(self, etat):
        if "attente" in etat or "courante" in etat:
            self.btncreerpartie.button.config(state=DISABLED)
        if "courante" in etat:
            self.etat_du_jeu.config(text="Desole - partie encours !")
            self.btninscrirejoueur.button.config(state=DISABLED)
        elif "attente" in etat:
            self.etat_du_jeu.config(text="Partie en attente de joueurs !")
            self.btninscrirejoueur.button.config(state=NORMAL)
        elif "dispo" in etat:
            self.etat_du_jeu.config(text="Bienvenue ! Serveur disponible")
            self.btninscrirejoueur.button.config(state=DISABLED)
            self.btncreerpartie.button.config(state=NORMAL)
        else:
            self.etat_du_jeu.config(text="ERREUR - un probleme est survenu")

    def update_lobby(self, joueurs):
        if self.tableau_choisi != None:
            self.btn_lancer_partie.button.config(state=NORMAL)
        if len(joueurs) == 2:
            self.label_joueur_coop.config(text=joueurs[1][0])
            if self.controleur.egoserveur == True:
                self.btn_lancer_partie.button.config(state=NORMAL)

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
        self.btn_lancer_partie.button.config(state=NORMAL)    


    def trouver_usagers_locaux(self):
        nom_values = self.controleur.requerir_info("joueurs_locaux",["nom"] )
        return nom_values

    def ouvrir_lobby_local(self):
        nom_values = self.controleur.agent_bd.chercher_usagers()
        nom_joueur_courant = self.drop_nom.get()
        if nom_joueur_courant not in nom_values:
            self.controleur.agent_bd.ajouter_aux_usagers_locaux(nom_joueur_courant)
        self.controleur.creer_partie_locale(nom_joueur_courant)

    def activer_partie_reseau(self):
        self.demarrer_partie.destroy()
        self.partie_active = True

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
        
    def game_over(self):
        fontStyleTitle = ("Gill Sans Ultra Bold", 14)
        
        self.frame_game_over = Frame(self.root, width=self.largeur/2, height=self.hauteur/2, highlightbackground='#F1D92A', highlightthickness=4, bg='black')
        
        self.canevas_splash = Canvas(self.frame_game_over,width=self.largeur/2,
                              height=self.hauteur/2,bg="black")
        image_originale = Image.open("img/game_over.png")
        image_modifiee = image_originale.resize((350, 175), Image.Resampling.NEAREST)
        self.img_defis = ImageTk.PhotoImage(image_modifiee)
        self.canevas_splash.create_image(330, 100, anchor="center", image=self.img_defis)
        self.canevas_splash.pack()
        
        label_partie_termine = Label(self.frame_game_over, text="La partie est terminée!", bg="black", fg='#F1D92A', font=fontStyleTitle)
        label_partie_termine.place(relx=0.5, rely=0.6, anchor="center")
        label_score = Label(self.frame_game_over, text=f'Score :{self.modele.partie.score}', bg="black", fg='#F1D92A', font=fontStyleTitle)
        label_score.place(relx=0.5, rely=0.7, anchor="center")
        label_niveau_max = Label(self.frame_game_over, text=f'Niveau maximal atteint : {self.modele.partie.vague}', bg="black", fg='#F1D92A', font=fontStyleTitle)
        label_niveau_max.place(relx=0.5, rely=0.8, anchor="center")
        
        self.quitter_jeu = PacManButton(20, 1, "Quitter", command=self.quitter_jeu_over)
        self.quitter_jeu.place(relx=0.5, rely=0.73,anchor="n")

        self.controleur.agent_bd.ajouter_credits(self.nom_joueur_local, self.modele.partie.score * 5)
        
        self.frame_game_over.place(relx = 0.5, rely=0.5, anchor="center")
        self.desactiver_btn()

    def quitter_jeu_over(self):
        self.destroy_menu_tour()
        self.frame_game_over.destroy()
        self.interface_panel.destroy()
        self.quitter_jeu.destroy()
        self.partie_active = False
        self.ouvrir_lobby_local()

    def dessiner_chateau(self):
        self.canvas.delete("chateau")
        
        largeur = 130
        hauteur = 200
        
        x = self.modele.partie.chemin.pivots[self.tableau_choisi][-1][0]
        y = self.modele.partie.chemin.pivots[self.tableau_choisi][-1][1]
        
        img = Image.open("./img/chateau.png")
        tk_img = img.resize((int(largeur), int(hauteur)), Image.Resampling.NEAREST)
        tk_img = ImageTk.PhotoImage(img)
        
        # Store the image reference to prevent garbage collection
    
        self.images[-1] = tk_img
        self.canvas.create_image((x * self.ratio_x, y * self.ratio_y), anchor='w', image=tk_img, tags=("chateau",))

    def dessiner_creeps(self):
        self.canvas.delete("creep")
        creep_largeur = Creep.largeur * self.ratio_x
        creep_hauteur = Creep.largeur * self.ratio_y

        for creep in self.modele.partie.liste_creeps:
            if creep.est_empoisone:
                img = Image.open("./img/creep_poison.png")
            elif creep.est_electrocute:
                img = Image.open("./img/creep_elect.png")
            else:
                img = Image.open(creep.img_src)
                
            img = img.resize((int(creep_largeur), int(creep_hauteur)), Image.Resampling.NEAREST)
            tk_img = ImageTk.PhotoImage(img)
            
            # Store the image reference to prevent garbage collection
            self.images[creep.id] = tk_img
            
            self.canvas.create_image((creep.pos_x * self.ratio_x, creep.pos_y * self.ratio_y), anchor='center', image=tk_img, tags=("creep", creep.id,))

    def dessiner_explosions(self):
        for i in self.modele.partie.explosions:
            for j in i.nuages:
                img = Image.open(j.img_src)
                
                img = img.resize((int(j.largemax), int(j.largemax)), Image.Resampling.NEAREST)
                tk_img = ImageTk.PhotoImage(img)
                
                # Store the image reference to prevent garbage collection
                self.images[j.id] = tk_img
                
                self.canvas.create_image((j.x1 * self.ratio_x, j.y1 * self.ratio_y), anchor='center', image=tk_img, tags=("dynamique","explosion",))
                
    
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

    def dessiner_tours(self):
        # dessines les tours du modèle
        for joueur in self.modele.partie.joueurs:
            for tour in self.modele.partie.joueurs[joueur].tours:
                self.dessiner_icone_tour(tour)

    def dessiner_icone_tour(self, tour):
        size = 50
        # dessine une tour sur le canvas
        x = tour.pos_x * self.ratio_x
        y = tour.pos_y * self.ratio_y
        tour_largeur = size * self.ratio_x
        tour_hauteur = size * self.ratio_y
        
        img = Image.open(tour.img_src)
        img = img.resize((int(tour_largeur), int(tour_hauteur)), Image.Resampling.NEAREST)
        
        bg_img = Image.open(tour.background_src)
        bg_img = bg_img.resize((int(tour_largeur + 30), int(tour_hauteur + 30)), Image.Resampling.NEAREST)

        if tour.cible:
            angle_radians = hp.Helper.calcAngle(tour.pos_x, tour.pos_y, tour.cible.pos_x, tour.cible.pos_y)
            angle_degrees = math.degrees(angle_radians)
            img = img.rotate(-angle_degrees)
            
        tk_img = ImageTk.PhotoImage(img)
        tk_bg = ImageTk.PhotoImage(bg_img)
        
        # Store the image reference to prevent garbage collection
        self.images[tour.id] = [tk_img, tk_bg]
        
        self.canvas.create_image((x, y), anchor='center',
                                    image=tk_bg, tags=('tour','dynamique',tour.id, ))

        self.canvas.create_image((x, y), anchor='center',
                                    image=tk_img, tags=('tour','dynamique',tour.id, ))
    
        self.canvas.tag_bind("tour", "<Button>", self.selectionne_tour)
        self.canvas.tag_lower('chemin')
        self.canvas.tag_lower('chemin_outline')  
        
    # Permet d'afficher le champ d'action des tours.  
    
    def toggle_champ_action(self):
        if not self.champ_action_toggled:
            for joueur in self.modele.partie.joueurs:
                for tour in self.modele.partie.joueurs[joueur].tours:
                    self.dessiner_champ_action(tour)
                    self.champ_action_toggled = True
        else:
            self.canvas.delete('tour_radius')
            self.champ_action_toggled = False      
    
    def dessiner_champ_action(self, tour, select = False):
        x = tour.pos_x * self.ratio_x
        y = tour.pos_y * self.ratio_y
        
        tour_radius_x = tour.champ_action * self.ratio_x
        tour_radius_y = tour.champ_action * self.ratio_y
        radius_largeur = 1 * (self.ratio_y + self.ratio_x) / 2  
        
        if not select:
            self.canvas.create_oval(x - tour_radius_x, y - tour_radius_y, x + tour_radius_x,
                                y + tour_radius_y,
                                dash= (3,5), fill="", width= radius_largeur, tags=('tour_radius'), outline="lightblue")
        else:
            self.canvas.create_oval(x - tour_radius_x, y - tour_radius_y, x + tour_radius_x,
                                y + tour_radius_y,
                                dash= (3,5), fill="", width= radius_largeur + 2, tags=('tour_radius_select'), outline="limegreen")
            
        
        self.canvas.tag_lower('tour_radius')
        self.canvas.tag_lower('tour_radius_select')

    # Sélectionne une tour pour pouvoir l'upgrader. 
    
    def selectionne_tour(self, event):

        if self.tour_choisi is not None:
            return

        id_tour = self.canvas.itemcget(event.widget.find_withtag("current")[0], "tags").split(" ")[2]
        
        for joueur in self.modele.partie.joueurs:
            for tour in self.modele.partie.joueurs[joueur].tours:
                if tour.id == id_tour:
                    self.tour_choisi = tour
                    break

        self.btn_upgrade = PacManButton(int(20 * self.ratio_x), int(2 * self.ratio_y), "Upgrade", self.upgrade_tour)
        self.btn_upgrade.place(x=self.largeur-27 * self.ratio_x, y=350, anchor="ne")

        self.menu_upgrade()
        
        self.dessiner_champ_action(self.tour_choisi, True)
        self.upgrade = self.canvas.bind("<Button-1>", self.cancel_upgrade)
        
        if self.tour_choisi.cout_amelioration <= self.modele.partie.argent_courant and self.tour_choisi.niveau_amelioration != 3:
            self.btn_upgrade.button.config(state = NORMAL)
        else:
            self.btn_upgrade.button.config(state = DISABLED) 
    
    def menu_upgrade(self):
        self.frame_upgrade = Frame(self.root, width=215 * self.ratio_x, height=140*self.ratio_y, highlightbackground='#F1D92A', highlightthickness=4, bg='black')
        self.frame_upgrade.place(x=self.largeur-27 * self.ratio_x, y=410, anchor="ne")

        if self.tour_choisi.niveau_amelioration != 3:
            self.label_upgrade = Label(self.frame_upgrade, text="Amélioration de la tour", bg="black", fg='#F1D92A', font=("Gill Sans Ultra", 10))
            self.label_upgrade.place(relx=0.5, rely=0.2, anchor="center")

            self.label_cout = Label(self.frame_upgrade, text=f'Cout : {self.tour_choisi.cout_amelioration}', bg="black", fg='#F1D92A', font=("Gill Sans Ultra", 8))
            self.label_cout.place(relx=0.5, rely=0.4, anchor="center")

            self.label_dommage = Label(self.frame_upgrade, text=f'Dommage : +10%', bg="black", fg='#F1D92A', font=("Gill Sans Ultra", 8))
            self.label_dommage.place(relx=0.5, rely=0.6, anchor="center")

            self.label_portee = Label(self.frame_upgrade, text=f'Portée : +15%', bg="black", fg='#F1D92A', font=("Gill Sans Ultra", 8))
            self.label_portee.place(relx=0.5, rely=0.8, anchor="center")
        else:
            self.label_upgrade = Label(self.frame_upgrade, text="Niveau maximal", bg="black", fg='#F1D92A', font=("Gill Sans Ultra", 10))
            self.label_upgrade.place(relx=0.5, rely=0.2, anchor="center")


    def upgrade_tour(self):
        self.controleur.ameliorer_tour(self.tour_choisi.id)
        self.tour_choisi = None
        self.canvas.unbind("<Button-1>", self.upgrade)       
        self.canvas.delete('tour_radius_select')
        self.btn_upgrade.destroy()
        self.frame_upgrade.destroy()
            
    def cancel_upgrade(self, event):
        self.tour_choisi = None
        self.canvas.unbind("<Button-1>", self.upgrade)       
        self.canvas.delete('tour_radius_select')
        self.btn_upgrade.destroy()
        self.frame_upgrade.destroy()

    def dessiner_projectiles(self):
        self.canvas.delete("projectile")
        projectile_largeur = Projectile.largeur * self.ratio_x
        projectile_hauteur = Projectile.largeur * self.ratio_y
        
        for joueur in self.modele.partie.joueurs:
            for tour in self.modele.partie.joueurs[joueur].tours:
                for projectile in tour.liste_projectiles:
                    if isinstance(projectile, Balle):
                        self.canvas.create_rectangle(
                        projectile.pos_x * self.ratio_x - projectile_largeur,
                        projectile.pos_y * self.ratio_y - projectile_hauteur,
                        projectile.pos_x * self.ratio_x + projectile_largeur,
                        projectile.pos_y * self.ratio_y + projectile_hauteur,
                        fill="yellow", outline="yellow",stipple="gray50", tags=("projectile", projectile.id))
                    elif isinstance(projectile, Eclair):
                        self.canvas.create_line(tour.pos_x * self.ratio_x, tour.pos_y * self.ratio_y, projectile.pos_x * self.ratio_x, projectile.pos_y * self.ratio_y,fill="light blue", width=2, tags=("projectile", projectile.id))
                        for i in range(3):
                            end_x = projectile.pos_x * self.ratio_x + random.randint(-5, 5)
                            end_y = projectile.pos_y * self.ratio_y + random.randint(-5, 5)  
                            width = random.randint(1, 3)  
                            
                            color = ["#01065A", "#3393FF", "#F5FAFF"]
                            self.canvas.create_line(tour.pos_x + random.randint(-5, 5) * self.ratio_x, tour.pos_y + random.randint(-5, 5)* self.ratio_y, 
                                                    end_x, end_y, 
                                                    fill=color[random.randint(0,2)], width=width, tags=("projectile", projectile.id))
                    elif isinstance(projectile, Poison):
                        self.canvas.create_oval(
                        projectile.pos_x * self.ratio_x - (projectile_largeur + 5),
                        projectile.pos_y * self.ratio_y - (projectile_hauteur + 5),
                        projectile.pos_x * self.ratio_x + (projectile_largeur + 5),
                        projectile.pos_y * self.ratio_y + (projectile_hauteur + 5),
                        fill="limegreen", outline="limegreen",stipple="gray50", tags=("projectile", projectile.id))
                    elif isinstance(projectile, Obus):
                        self.canvas.create_oval(
                        projectile.pos_x * self.ratio_x - (projectile_largeur + 3),
                        projectile.pos_y * self.ratio_y - (projectile_hauteur + 8),
                        projectile.pos_x * self.ratio_x + (projectile_largeur + 3),
                        projectile.pos_y * self.ratio_y + (projectile_hauteur + 8),
                        fill="grey", outline="grey",stipple="gray50", tags=("projectile", projectile.id))
                    elif isinstance(projectile, Grenade):
                        self.canvas.create_oval(
                        projectile.pos_x * self.ratio_x - (projectile_largeur + 4),
                        projectile.pos_y * self.ratio_y - (projectile_hauteur + 4),
                        projectile.pos_x * self.ratio_x + (projectile_largeur + 4),
                        projectile.pos_y * self.ratio_y + (projectile_hauteur + 4),
                        fill="red", outline="red",stipple="gray50", tags=("projectile", projectile.id))
                    else:
                        img = Image.open(projectile.img_src)
                
                        img = img.resize((int(projectile_hauteur + 20), int(projectile_largeur + 20)), Image.Resampling.NEAREST)
                        tk_img = ImageTk.PhotoImage(img)
            
                        # Store the image reference to prevent garbage collection
                        self.images[projectile.id] = tk_img
                        
                        self.canvas.create_image((projectile.pos_x * self.ratio_x, projectile.pos_y * self.ratio_y), anchor='center', image=tk_img, tags=("projectile", "mine", projectile.id,))              
                        self.canvas.tag_lower('mine')

    def dessiner_jeu(self):
        self.images = {}
        self.canvas.delete('dynamique')
        self.dessiner_explosions()
        self.dessiner_creeps()
        self.dessiner_projectiles()
        self.dessiner_chateau()
        self.dessiner_tours()
        self.update_info_partie()
        self.desactiver_btn_tour()

    # Caller dans le controleur a chaque tick de boucle
    # Update les valeurs dynamique du InterfacePannel    
    def update_info_partie(self):
        self.interface_panel.chrono_info['text'] = str(round(self.modele.partie.chrono)) + " s"
        self.interface_panel.vague_info['text'] = "lvl " + str(self.modele.partie.vague)
        self.interface_panel.vie_info['text'] = str(self.modele.partie.vie) + " HP"
        self.interface_panel.argent_info['text'] = str(self.modele.partie.argent_courant) + " $"
        
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
        
        self.menu_tour = InterfaceTour(self.largeur, 250 * self.ratio_x, 500 * self.ratio_y, self.ratio_x, self.ratio_y, self.bind_canvas)
        self.menu_tour.place(anchor="ne", x=self.largeur-10, y=70)
        
        self.toggle_radius = PacManButton(int(20*self.ratio_x), int(1*self.ratio_y), "Afficher champ d'action", command=self.toggle_champ_action)
        self.toggle_radius.place(x=self.largeur-27 * self.ratio_x, y=self.hauteur - 20 * self.ratio_y, anchor="se")
        
    def desactiver_btn(self):
        self.menu_tour.activation_to.button.config(state = DISABLED)
        self.menu_tour.activation_te.button.config(state = DISABLED)
        self.menu_tour.activation_tg.button.config(state = DISABLED)
        self.menu_tour.activation_tp.button.config(state = DISABLED)
        self.menu_tour.activation_tm.button.config(state = DISABLED) 
        self.menu_tour.activation_tc.button.config(state = DISABLED)
        self.toggle_radius.button.config(state = DISABLED)

        
    def desactiver_btn_tour(self):
        if TourMitrailleuse.COUT <= self.modele.partie.argent_courant:
            self.menu_tour.activation_to.button.config(state = NORMAL)
        else:
            self.menu_tour.activation_to.button.config(state = DISABLED)
        
        if TourEclair.COUT <= self.modele.partie.argent_courant:
            self.menu_tour.activation_te.button.config(state = NORMAL)
        else:
            self.menu_tour.activation_te.button.config(state = DISABLED)
        
        if TourGrenade.COUT <= self.modele.partie.argent_courant:
            self.menu_tour.activation_tg.button.config(state = NORMAL)
        else:
            self.menu_tour.activation_tg.button.config(state = DISABLED)
        
        if TourPoison.COUT <= self.modele.partie.argent_courant:
            self.menu_tour.activation_tp.button.config(state = NORMAL)
        else:
            self.menu_tour.activation_tp.button.config(state = DISABLED)
        
        if TourMine.COUT <= self.modele.partie.argent_courant:
            self.menu_tour.activation_tm.button.config(state = NORMAL)
        else:
            self.menu_tour.activation_tm.button.config(state = DISABLED) 
            
        if TourCanon.COUT <= self.modele.partie.argent_courant:
            self.menu_tour.activation_tc.button.config(state = NORMAL)
        else:
            self.menu_tour.activation_tc.button.config(state = DISABLED)

    def destroy_menu_tour(self):
        self.menu_tour.activation_to.destroy()
        self.menu_tour.activation_tp.destroy()
        self.menu_tour.activation_te.destroy()
        self.menu_tour.activation_tm.destroy()
        self.menu_tour.activation_tg.destroy()
        self.menu_tour.activation_tc.destroy()
        self.toggle_radius.destroy()
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
        
        self.chrono_info = Label(self, text="", font=("arial", 11), fg="pink", bg="black")
        self.vague_info = Label(self, text="", font=("arial", 11), fg="pink",  bg="black")
        self.vie_info = Label(self, text="", font=("arial", 11), fg="pink",  bg="black")
        self.argent_info = Label(self, text="", font=("arial", 11), fg="pink", bg="black")
        
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

        # On utilise un lambda pour passer des arguments a la fonction
        # command = lambda: command("TypeDeTour")
        # L'argument command est une fonction qui est passé en parametre a InterfaceTour
        
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
        self['highlightbackground'] = '#F1D92A'
        
        self.button = Button(self, bg='black', fg='#F1D92A', font=("Gill Sans Ultra", 10), width=width, height=height, text=text, command=command)
        self.button.pack()
    
class Etiquette(Label):
    def __init__(self,master,*args, **kwargs):
        Label.__init__(self,master,*args, **kwargs)
        self.config(font=("arial",48,"bold"))
        self.config(fg="#F1D92A")
    