## -*- Encoding: UTF-8 -*-

from tkinter import *
from tkinter import ttk


class Vue():
    def __init__(self, parent, nom_joueur_local):
        self.parent = parent
        self.modele = None #modele
        self.nom_joueur_local = nom_joueur_local
        self.root = Tk()
        self.root.iconbitmap("Tour_icon.ico")
        self.root.title("Tour du CVM")
        self.conn = None
        self.action = None  # sert a composer des actions requerant plusieurs gestes
        self.cadres = {}    # dictionnaire des Frame pour changer la fen root d'etat
        self.cadre_courant = None
        self.creer_cadres(self.nom_joueur_local)
        #self.afficher_cadre("cadre_splash")

    def afficher_cadre(self,cadre_demande):
        if self.cadre_courant:
            self.cadre_courant.pack_forget()
        self.cadre_courant = self.cadres[cadre_demande]
        self.cadre_courant.pack(expand=1,fill=BOTH)

    def creer_cadres(self,nom_joueur_local):
        self.cadres["cadre_splash"] = self.creer_cadre_splash(nom_joueur_local)
        # NOTE - les autres cadres seront construit au fur et a mesure des besoins

    def creer_cadre_bonus(self):
        pass

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

    def choisir_tablo(self, evt):
        tablo_choisi = evt.widget
        nom_tablo = tablo_choisi.cget("text")
        print("Tableau de jeu choisi ", nom_tablo)

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
        values = self.trouver_usagers()
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
            if self.parent.egoserveur == True:
                self.btn_lancer_partie.config(state=NORMAL)

    def lancer_partie_locale(self):
        self.parent.initialiser_partie_locale()

    def lancer_partie(self):
        self.parent.lancer_partie()

    def creer_cadre_jeu(self):
        # cadre pour toute la fenetre, contient 2 aires distinctes
        cadre_jeu = Frame(self.root)
        # aire de jeu (contenant un canevas) pour dessiner le jeu
        aire_jeu =Frame(cadre_jeu)
        self.canevas = Canvas(aire_jeu,width=self.modele.largeur,
                              height=self.modele.hauteur,bg="orange")
        self.canevas.grid(column=10,row=10)
        # dessin permanent du chemin
        for i in self.modele.chemin.segments:
            self.canevas.create_line(i[0],i[1], width=30, capstyle=ROUND, tags=("statique",))

        # aire pour les widgets de commande
        aire_commande =Frame(cadre_jeu, width=300,height=self.modele.hauteur,bg="pink")
        btn_activer_partie=Button(aire_commande,text="Activer la partie",command=self.activer_partie)
        btn_activer_partie.pack()

        btn_creer_tour=Button(aire_commande,text="TIR",command=self.demander_tour)
        btn_creer_tour.pack()
        # EN COURS DE CONSTRUCTION
        btn_creer_poison=Button(aire_commande,text="POISON",command=self.demander_poison)
        btn_creer_poison.pack()
        # on utilise le gestionnaire d egeometrie 'grid' requerant colonne et rangees
        aire_jeu.grid(column=10,row=10)
        aire_commande.grid(column=20,row=10,sticky=NS) # sticky indique les bordures connectees
        self.messagerie = Listbox(aire_commande,width = 15,height=6,bg="black",fg="yellow")
        self.messagerie.pack(side=BOTTOM)
        # on place ce cadre parmi l'ensemble des cadres
        self.cadres["cadre_jeu"]= cadre_jeu

    def sur_retour(self,evt):
        self.btn_ouvrir_lobby.focus_set()

    def trouver_usagers(self):
        nom_values = self.parent.requerir_info("joueurs_locaux",["nom"] )
        return nom_values

    def initialiser_splash_post_connection(self):
        self.btninscrirejoueur.config(state=NORMAL)
        self.btncreerpartie.config(state=NORMAL)
        self.btnreset.config(state=NORMAL)
        url_serveur = self.url_initial.get()
        if url_serveur:
            self.parent.initialiser_splash_post_connection(url_serveur)
        else:
            self.etat_du_jeu.config(text="Aucune adresse de serveur")

    def ouvrir_lobby_local(self):
        nom_values = self.parent.agent_bd.chercher_usagers()
        nom_joueur_courant = self.drop_nom.get()
        if nom_joueur_courant not in nom_values:
            #print(nom_joueur_courant)
            self.parent.agent_bd.ajouter_aux_usagers_locaux(nom_joueur_courant)
        self.parent.creer_partie_locale(nom_joueur_courant)

    def ouvrir_bonus(self):
        pass #self.afficher_cadre("cadre_jeu")

    def ouvrir_jeu(self):
        self.afficher_cadre("cadre_jeu")

    def afficher_partie(self):
        self.canevas.delete("dynamique")
        n = 10 # Creep.taille
        for i in self.modele.creeps_actifs:
            self.canevas.create_oval(i.x-n,i.y-n,i.x+n,i.y+n,
                                     fill="red",tags=("dynamique","creep",))

        n = 3 # Obus.taille
        for k in self.modele.joueurs:
            for j in self.modele.joueurs[k].tours:
                for a in self.modele.joueurs[k].tours[j]:
                    for b in a.mes_obus:
                        self.canevas.create_oval(b.x-n,b.y-n,b.x+n,b.y+n,
                                                 fill="white",tags=("dynamique","obus",))

                    self.canevas.create_line(a.x, a.y-6, a.gueule_canon[0],a.gueule_canon[1]-6, width=7, capstyle=ROUND,
                                             tags=("dynamique","tour","tour_canon"))

        n = 2  # Germe.taille
        for i in self.modele.germes:
            self.canevas.create_oval(i.x-n,i.y-n,i.x+n,i.y+n,
                                     fill="lightblue",tags=("dynamique","germe",))

        for i in self.modele.explosions:
            for j in i.nuages:
                self.canevas.create_oval(j.x1,j.y1,j.x2,j.y2,outline = j.couleur,dash = (1,2,1),
                                         fill=j.couleur,tags=("dynamique","explosion",))

        # maintenant le score
        self.canevas.create_text(self.modele.largeur / 4, self.modele.hauteur / 8, anchor=CENTER,
                                 font=('Helvetica', '30', 'bold'),
                                 text=self.modele.niveau, tags=("dynamique", "pointage"))
        self.canevas.create_text(self.modele.largeur / 4 * 2, self.modele.hauteur / 8, anchor=CENTER,
                                 font=('Helvetica', '30', 'bold'),
                                 text=self.modele.pointage, tags=("dynamique", "pointage"))

        self.canevas.create_text(self.modele.largeur / 4 * 3, self.modele.hauteur / 8, anchor=CENTER,
                                 font=('Helvetica', '30', 'bold'),
                                 text=self.modele.vie, tags=("dynamique", "pointage"))
    def creer_partie(self):
        nom = self.drop_nom.get()
        self.parent.creer_partie(nom)

    def inscrire_joueur(self):
        nom = self.drop_nom.get()
        urljeu = self.url_initial.get()
        self.parent.inscrire_joueur(nom, urljeu)

    def reset_partie(self):
        rep = self.parent.reset_partie()

    def demander_tour(self):
        self.action = Action(self,"tour")

    def demander_poison(self):
        self.action = Action(self,"poison")

    def creer_tour(self,evt):
        self.canevas.unbind("<Button>")
        self.action = None
        self.parent.ajouter_tour(evt.x,evt.y)

    def creer_poison(self, evt):
        self.canevas.unbind("<Button>")
        self.action = None
        self.parent.ajouter_poison(evt.x, evt.y)

    def afficher_message(self,txt):
        self.messagerie.insert(0,txt)

    def dessiner_tour(self,tour):
        i = tour
        x = i.x
        y = i.y
        eten = i.etendu
        # indicateur d'etendue
        self.canevas.create_oval(x - eten, y - eten, x + eten, y + eten, outline="green",
                                 fill="", dash=(2,1,3),tags=("tour",))
        n = 20  # Tour.base
        self.canevas.create_rectangle(x - n, y - n, x + n, y + n, outline="black",
                                      fill="black", tags=("tour",))
        self.canevas.create_rectangle(x - n, y - n, x + n - 1, y + n - 1, outline="",
                                      fill="light grey", tags=("tour",))
        n = 16  # Tour.colonne
        self.canevas.create_oval(x - n, y - n, x + n, y + n, outline="",
                                 fill="black", tags=("tour",))
        y = y - 6  # Tour.canon
        self.canevas.create_oval(x - n, y - n, x + n, y + n, outline="",
                                 fill="red", tags=("tour",))
        # dessin du canon pointe
        self.canevas.create_line(x, y, i.gueule_canon[0],i.gueule_canon[1], width=7, capstyle=ROUND,
                                 tags=("dynamique","tour","tour_canon"))

    def dessiner_poison(self):
        self.canevas.delete("poison")
        for i in self.modele.poisons:
            x = i.x
            y = i.y
            eten = i.etendu
            # indicateur d'etendue
            self.canevas.create_oval(x - eten, y - eten, x + eten, y + eten, outline="green",
                                     fill="", dash=(2,1,3),tags=("poison",))
            # tour - base, simule un 2D1/2
            n = 20 # Tour.base
            self.canevas.create_rectangle(x - n, y - n, x + n, y + n, outline="black",
                                          fill="black", tags=("poison",))
            self.canevas.create_rectangle(x - n, y - n, x + n - 1, y + n - 1, outline="",
                                          fill="light grey", tags=("poison",))
            n = 16 # Tour.colonne
            self.canevas.create_oval(x - n, y - n, x + n, y + n, outline="",
                                     fill="black", tags=("poison",))
            y = y - 6 # Tour.canon
            self.canevas.create_oval(x - n, y - n, x + n, y + n, outline="",
                                     fill="lightblue", tags=("poison",))
            # dessin du canon pointe
            self.canevas.create_line(x, y, i.gueule_canon[0],i.gueule_canon[1], width=7, capstyle=ROUND,
                                     tags=("dynamiques","poisson"))

    def activer_partie(self):
        self.parent.activer_partie()

class Action():
    # Action est un objet qui peut conserver divers etats d'une requete
    # afin que le jouer puisse faire des actions résultants d'une serie
    # de geste dans l'interface
    def __init__(self, parent: Vue, etat: str):
        self.parent = parent
        self.etat = etat
        if etat == "tour":
            self.parent.canevas.bind("<Button>",self.parent.creer_tour)
        else:
            self.parent.canevas.bind("<Button>",self.parent.creer_poison)

    def afficher_exlosion(self,x,y):
        pass

class Etiquette(Label):
    def __init__(self,master,*args, **kwargs):
        Label.__init__(self,master,*args, **kwargs)
        self.config(font=("arial",48,"bold"))
        self.config(fg="goldenrod3")

## FIN DE VUE **************************************************************************
