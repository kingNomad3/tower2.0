import random
import requests
import json
from TD_modele import Modele
from TD_vue import Vue
from TD_agent_BD import Agent_BD

class Controleur():
    def __init__(self):
        self.nom_joueur_local= self.generer_pseudo_nom()  # fonction au bas de la page
        self.egoserveur = False # devient vrai si on creer une partie
        self.modele = Modele(self) # info generique
        self.agent_bd = Agent_BD(self)
        # Info pour la boucle de jeu
        self.partie_locale = True # si False, on joue reseau
        self.iteration_boucle_jeu = 0
        self.pause_jeu = 0
        self.prochainsplash = 0
        self.partie_active = None
        self.on_joue = 1 # devient 0 si le serveur envoie un probleme de synchro
        self.boucle_after_active = None  # renvoie la derniere commande prevu par un appel a after - permet de l'annuler
        self.actions_requises = [] # arrive via l'interface graphique
        # Info reseau
        self.session = None #requests.Session()
        self.url_serveur = None
        self.modulo_appeler_serveur = 2
        self.delai_de_boucle_de_jeu = 20  # millisecondes avant que la boucle_de_jeu se rappelle
        # creation de la l'objet vue pour l'affichage
        self.vue = Vue(self, self.nom_joueur_local)
        self.vue.afficher_cadre("cadre_splash")
        self.vue.root.mainloop()

    def initialiser_splash_post_connection(self,url_serveur):
        self.session = requests.Session()
        self.url_serveur = url_serveur
        self.boucler_sur_splash()

    def boucler_sur_splash(self):
        url = self.url_serveur + "/tester_jeu"
        params = {"nom": self.nom_joueur_local}
        mondict = self.appeler_serveur(url, params)
        if mondict:
            self.vue.update_splash(mondict[0])
        self.prochainsplash = self.vue.root.after(50, self.boucler_sur_splash)

    # on boucle sur le lobby en attendant l'inscription de tous les joueurs attendus
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

    # fonction pour demarrer une partie locale (une seul joueur)
    def creer_partie_locale(self, nom_joueur_local):
        if self.prochainsplash:
            self.vue.root.after_cancel(self.prochainsplash)
            self.prochainsplash = None
        self.nom_joueur_local = nom_joueur_local

        reptext = "" ##self.appeler_serveur(url, data, "POST")
        self.partie_locale = True  # on est coop
        self.egoserveur = True  # je suis la personne qui a demarrer une nouvelle partie
        self.vue.root.title("je suis " + self.nom_joueur_local)
        self.vue.creer_cadre_lobby("local", reptext)
        self.vue.afficher_cadre("cadre_lobby")
        #self.boucler_sur_lobby()

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

########################################################################
    # methode speciale pour remettre les parametres du serveur a leurs valeurs par defaut
    # (jeu disponible, pas de joueur)
    # indique le resultat dans le splash
    def reset_partie(self):
        leurl = self.url_serveur + "/reset_jeu"
        reptext = self.appeler_serveur(leurl, 0)
        self.vue.update_splash(reptext[0][0]) #
        return reptext

    # fonction qui fait les appels au serveur
    def appeler_serveur(self, url, params, method="GET"):
        if method == "GET":
            response = self.session.get(url, params=params)
        elif method == "POST":
            response = self.session.post(url, json=params)
        response.raise_for_status()
        return response.json()

    def lancer_partie(self):
        url = self.url_serveur + "/lancer_partie"
        data = {
            'nom': self.nom_joueur_local  # Make sure to include this parameter
        }
        reptext = self.appeler_serveur(url, data, "POST")
        #self.pause = 1
        #self.boucler_en_attente()

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
        self.partie_active = self.modele.lancer_partie(listejoueurs)
        # on passe le modele a la vue puisqu'elle trouvera toutes le sinfos a dessiner
        self.vue.modele = self.partie_active
        # on met la vue a jour avec les infos de partie
        self.vue.creer_cadre_jeu()
        # on change le cadre la fenetre pour passer dans l'interface de jeu
        self.vue.afficher_cadre("cadre_jeu")
        self.boucler_en_attente()

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
        self.partie_active = self.modele.lancer_partie([self.nom_joueur_local])
        # on passe le modele a la vue puisqu'elle trouvera toutes le sinfos a dessiner
        self.vue.modele = self.partie_active
        # on met la vue a jour avec les infos de partie
        self.vue.creer_cadre_jeu()
        # on change le cadre la fenetre pour passer dans l'interface de jeu
        self.vue.afficher_cadre("cadre_jeu")
        #self.boucler_en_attente()

    def boucler_en_attente(self):
        url = self.url_serveur + "/verifier_activation_partie"
        data = {
            'nom': self.nom_joueur_local  # Make sure to include this parameter
        }
        info_etat_joueur = self.appeler_serveur(url, data, "POST")
        if "activer" in info_etat_joueur[0]:
            self.boucler_sur_jeu()
        else:
            self.vue.root.after(50, self.boucler_en_attente)

    # La boucle principale pour jouer une partie
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
                        self.partie_active.ajouter_actions_a_faire(self.iteration_boucle_jeu,mondict)

                except requests.exceptions.RequestException as e:
                    print("An error occurred:", e)
                    self.on_joue = 0
        else:
            if self.actions_requises:
                actions = self.actions_requises
                self.actions_requises = []
                self.partie_active.ajouter_actions_a_faire(self.iteration_boucle_jeu+1,
                                                           [[self.iteration_boucle_jeu+1, json.dumps(actions)]])

        if self.on_joue:
            # envoyer les messages au modele et a la vue de faire leur job
            self.partie_active.jouer_coup(self.iteration_boucle_jeu)
            self.vue.afficher_partie()
        else:
            self.iteration_boucle_jeu -= 1
            self.on_joue = 1
        # appel ulterieur de la meme fonction jusqu'a l'arret de la partie
        self.vue.root.after(self.delai_de_boucle_de_jeu, self.boucler_sur_jeu)

    # generateur de nouveau nom
    def generer_pseudo_nom(self):
        nom_joueur_local = "Claude" + str(random.randrange(100, 1000))
        return nom_joueur_local

    def abandonner(self):
        action = [self.nom_joueur_local, "abandonner", [self.nom_joueur_local + ": J'ABANDONNE !"]]
        self.actions_requises = action
        self.vue.root.after(500, self.vue.root.destroy)

############################################################################
    # ACTIONA ISSUES DE LA VUE
    def ajouter_tour(self,x,y):
        action_demander = [self.nom_joueur_local,"ajouter_tour",[x,y]]
        self.actions_requises.append(action_demander)

    def ajouter_poison(self,x,y):
        action_demander = [self.nom_joueur_local,"ajouter_poison",[x,y]]
        self.actions_requises.append(action_demander)

    # ACTION SPECIALE RECLAME A LA VUE
    def afficher_message(self,txt):
        self.vue.afficher_message(txt)

    def dessiner_tour(self,tour):
        self.vue.dessiner_tour(tour)

    def requerir_info(self, table, colonnes):
        db_rep = self.agent_bd.requerir_info(table, colonnes)
        return db_rep

if __name__ == '__main__':
    c=Controleur()
    print("FIN")