from Vue import *
from Modele import *
from Tour import *
import random
import requests
import json
from TD_agent_BD import *

class Controleur:
    def __init__(self):
        self.nom_joueur_local = self.generer_pseudo_nom()
        self.modele = Modele(self) # fonction au bas de la page, devrait être envoyée par la vue
        self.partie = None
        self.timer = 0
        self.egoserveur = False # devient vrai si on creer une partie
        self.partie_locale = True # si False, on joue reseau
        self.iteration_boucle_jeu = 0
        self.prochainsplash = 0
        self.on_joue = 1 # devient 0 si le serveur envoie un probleme de synchro
        self.actions_requises = [] # arrive via l'interface graphique
        #info reseau
        self.session = None
        self.modulo_appeler_serveur = 2     # on appelle le serveur mois souvent que la buocle de jeu
        self.delai_de_boucle_de_jeu = 20    # millisecondes avant que la boucle_de_jeu se rappelle      
        self.url_serveur = None
        #vue
        self.vue = Vue(self, self.nom_joueur_local)
        self.vue.afficher_cadre("cadre_splash")
        self.vue.root.mainloop()
        self.agent_bd = Agent_BD(self)

    # pour du visuel et le modèle (en cas de besoin)
    def incrementer_timer(self):
        self.timer += 0.5 

    def get_timer_str(self):
        return f"{int(self.timer//10)}s"

    # Lié à l'intéraction usager...
    def traiter_gameover(self):
        self.vue.root.destroy()

    def creer_tour(self, type_tour, x, y):
        action_demande = [self.nom_joueur_local,"creer_tour",[type_tour,x,y]]
        self.actions_requises.append(action_demande)
        
    def generer_pseudo_nom(self):
        nom_joueur_local = "robert" + str(random.randrange(100, 1000))
        return nom_joueur_local
    
    def boucler_sur_splash(self):
        url = self.url_serveur + "/tester_jeu"
        params = {"nom": self.nom_joueur_local}
        mondict = self.appeler_serveur(url, params)
        if mondict:
            self.vue.update_splash(mondict[0])
        self.prochainsplash = self.vue.root.after(50, self.boucler_sur_splash)

    def initialiser_splash_post_connection(self, url_serveur): 
        self.session = requests.Session()
        self.url_serveur = url_serveur
        self.boucler_sur_splash()

    def boucler_sur_lobby(self):
        url = self.url_serveur + "/boucler_sur_lobby"
        params = {"nom": self.nom_joueur_local}
        info_etat_joueur = self.appeler_serveur(url, params)
        # si l'etat est courant, c'est que la partie vient d'etre lancer
        if "courante" in info_etat_joueur[0]:
            self.initialiser_partie(info_etat_joueur)
        else:
            self.joueurs = info_etat_joueur
            self.vue.update_lobby(info_etat_joueur)
            self.vue.root.after(50, self.boucler_sur_lobby)
            
    def initialiser_partie(self, mondict):
        # on recoit les divers parametres d'initialisation du serveur
        initaleatoire = mondict[1][0][0]
        # POUR TEST
        # random ALEATOIRE fourni par le serveur
        # random.seed(int(initaleatoire))
        # random FIXE pour test - generera la meme suite de nombre chaque fois
        random.seed(12473)

        # on recoit la derniere liste des joueurs pour la partie
        listejoueurs = []
        for i in self.joueurs:
            listejoueurs.append(i[0])

        # on cree le modele (la partie)
        self.partie = self.modele.lancer_partie(listejoueurs)
        # on passe le modele a la vue puisqu'elle trouvera toutes le sinfos a dessiner
        self.vue.modele = self.partie
        # on met la vue a jour avec les infos de partie
        self.vue.creer_cadre_jeu()
        # on change le cadre la fenetre pour passer dans l'interface de jeu
        self.vue.afficher_cadre("cadre_jeu")
        self.boucler_en_attente()

    # provient du bouton Debuter_partie
    def initialiser_partie_locale(self):
        # on recoit les divers parametres d'initialisation du serveur
        #initaleatoire = mondict[1][0][0]
        # POUR TEST
        # random ALEATOIRE fourni par le serveur
        # random.seed(int(initaleatoire))
        # random FIXE pour test - generera la meme suite de nombre chaque fois
        random.seed(12473)

        # on recoit la derniere liste des joueurs pour la partie
        #listejoueurs = []
        #for i in self.joueurs:
        #    listejoueurs.append(i[0])

        # on cree le modele (la partie)
        self.partie = self.modele.lancer_partie([self.nom_joueur_local])
        print("allo")
        # on passe le modele a la vue puisqu'elle trouvera toutes le sinfos a dessiner
        self.vue.modele = self.modele
        # on met la vue a jour avec les infos de partie
        self.vue.creer_cadre_jeu()
        # on change le cadre la fenetre pour passer dans l'interface de jeu
        self.vue.afficher_cadre("cadre_jeu")
        #self.boucler_en_attente()
    
    def reset_partie(self):
            le_url = self.url_serveur + "/reset_jeu"
            reptext = self.appeler_serveur(le_url, 0)
            self.vue.update_splash(reptext[0][0]) #
            return reptext
    
    # fonction pour demarrer une partie coop
    def creer_partie(self, nom_joueur_local):
        if self.prochainsplash:
            self.vue.root.after_cancel(self.prochainsplash)
            self.prochainsplash = None
        self.nom_joueur_local = nom_joueur_local
        url = self.url_serveur + "/creer_partie"
        data = {
            'nom': self.nom_joueur_local
        }
        reptext = self.appeler_serveur(url, data, "POST")
        self.partie_locale = False # on est coop
        self.egoserveur = True # je suis la personne qui a demarrer une nouvelle partie
        self.vue.root.title("je suis " + self.nom_joueur_local)
        self.vue.creer_cadre_lobby("reseau",reptext)
        self.vue.afficher_cadre("cadre_lobby")
        self.boucler_sur_lobby()
    
    # fonction pour demarrer une partie locale (une seul joueur)
    def creer_partie_locale(self, nom_joueur_local):
        if self.prochainsplash:
            self.vue.root.after_cancel(self.prochainsplash)
            self.prochainsplash = None
        self.nom_joueur_local = nom_joueur_local

        reptext = ""
        self.partie_locale = True  # on est coop
        self.egoserveur = True  # je suis la personne qui a demarrer une nouvelle partie
        self.vue.root.title("je suis " + self.nom_joueur_local)
        self.vue.creer_cadre_lobby("local", reptext)
        self.vue.afficher_cadre("cadre_lobby")
        
    # fonction pour s'inscrire a une partie creer (mais non lancer...)
    def inscrire_joueur(self, nom, urljeu):
        if self.prochainsplash:
            self.vue.root.after_cancel(self.prochainsplash)
            self.prochainsplash = None
        self.nom_joueur_local = nom
        url = self.url_serveur + "/inscrire_joueur"
        data = {
            'nom': self.nom_joueur_local
        }
        reptext = self.appeler_serveur(url, data, "POST")
        self.vue.root.title("je suis " + self.nom_joueur_local)
        self.vue.creer_cadre_lobby("reseau",reptext)
        self.partie_locale = False
        self.vue.afficher_cadre("cadre_lobby")
        self.boucler_sur_lobby()
        
    def lancer_partie(self):
        url = self.url_serveur + "/lancer_partie"
        data = {
            'nom': self.nom_joueur_local  # Make sure to include this parameter
        }
        reptext = self.appeler_serveur(url, data, "POST")

    def activer_partie(self):
        if self.partie_locale:
            self.boucler_sur_jeu()
        else:
            url = self.url_serveur + "/activer_partie"
            data = {
                'nom': self.nom_joueur_local  # Make sure to include this parameter
            }
            reptext = self.appeler_serveur(url, data, "POST")
        #self.pause = 1
        #self.boucler_en_attente()
        
    def boucler_sur_jeu(self):
        self.iteration_boucle_jeu += 1
        # test pour communiquer avec le serveur periodiquement
        if self.partie_locale == False:
            if self.iteration_boucle_jeu % self.modulo_appeler_serveur == 0:
                actions = []
                if self.actions_requises:
                    actions = self.actions_requises
                    self.actions_requises = []
                url = self.url_serveur + "/boucler_sur_jeu"
                params = {"nom": self.nom_joueur_local,
                          "iteration_boucle_jeu": self.iteration_boucle_jeu,
                          "actions_requises": actions}

                try:
                    mondict = self.appeler_serveur(url, params, method = "POST")
                    # verifie pour requete d'attente d'un joueur plus lent
                    if "ATTENTION" in mondict:
                        print("SAUTEEEEE")
                        self.on_joue = 0

                    elif mondict:
                        self.partie.ajouter_actions_a_faire(self.iteration_boucle_jeu,mondict)

                except requests.exceptions.RequestException as e:
                    print("An error occurred:", e)
                    self.on_joue = 0
        else:
            if self.actions_requises:
                actions = self.actions_requises
                self.actions_requises = []
                self.partie.ajouter_actions_a_faire(self.iteration_boucle_jeu+1,
                                                           [[self.iteration_boucle_jeu+1, json.dumps(actions)]]) #json.dumps genere du json

        if self.on_joue:
            # envoyer les messages au modele et a la vue de faire leur job
            self.partie.jouer_coup(self.iteration_boucle_jeu)
            self.incrementer_timer()
            self.vue.dessiner_jeu()
        else:
            self.iteration_boucle_jeu -= 1
            self.on_joue = 1
        # appel ulterieur de la meme fonction jusqu'a l'arret de la partie
        self.vue.root.after(self.delai_de_boucle_de_jeu, self.boucler_sur_jeu)
        
       # ACTION RECLAMEE À LA BASE DE DONNEE LOCALE
    def requerir_info(self, table, colonnes):
        db_rep = self.agent_bd.requerir_info(table, colonnes)
        return db_rep
    
    # fonction qui fait les appels au serveur
    def appeler_serveur(self, url, params, method="GET"):
        if method == "GET":
            response = self.session.get(url, params=params)
        elif method == "POST":
            response = self.session.post(url, json=params)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    c = Controleur()