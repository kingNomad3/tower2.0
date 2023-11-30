from Vue import *
from Modele import *
from Tour import *
import random
import requests
import json

class Controleur:
    def __init__(self):
        self.modele = Modele(self)
        self.timer = 0
        self.vue = Vue(self, self.modele)
        self.nom_joueur_local= self.generer_pseudo_nom()  # fonction au bas de la page, devrait être envoyée par la vue
        self.egoserveur = False # devient vrai si on creer une partie
        self.partie_locale = True # si False, on joue reseau
        self.iteration_boucle_jeu = 0
        self.prochainsplash = 0
        self.partie = None
        self.on_joue = 1 # devient 0 si le serveur envoie un probleme de synchro
        self.actions_requises = [] # arrive via l'interface graphique
        #info reseau
        # self.session = None
        # self.modulo_appeler_serveur = 2     # on appelle le serveur mois souvent que la buocle de jeu
        # self.delai_de_boucle_de_jeu = 20    # millisecondes avant que la boucle_de_jeu se rappelle      
        self.url_serveur = None
        #vue
        self.vue.root.after(300, self.boucler_jeu) 
        self.vue.root.mainloop()

    def boucler_jeu(self):
        self.iteration_boucle_jeu += 1
        if not self.modele.partie.fin_partie:
            self.incrementer_timer()
            self.modele.jouer()
            self.vue.dessiner_jeu()
            self.vue.root.after(50, self.boucler_jeu)
        else:
           self.traiter_gameover()


    # pour du visuel et le modèle (en cas de besoin)
    def incrementer_timer(self):
        self.timer += 0.5 

    def get_timer_str(self):
        return f"{int(self.timer//10)}s"

    # Lié à l'intéraction usager...
    def traiter_gameover(self):
        self.vue.root.destroy()

    def creer_tour(self, x, y):
        self.modele.partie.creer_tour(x, y, "TourMitrailleuse")
        
    def generer_pseudo_nom(self):
        nom_joueur_local = "robert" + str(random.randrange(100, 1000))
        return nom_joueur_local
    
    # def boucler_sur_splash(self):
    #     url = self.url_serveur + "/tester_jeu"
    #     params = {"nom": self.nom_joueur_local}
    #     mondict = self.appeler_serveur(url, params)
    #     if mondict:
    #         self.vue.update_splash(mondict[0])
    #     self.prochainsplash = self.vue.root.after(50, self.boucler_sur_splash)

    # def initialiser_splash_post_connection(self,url_serveur): #
    #     self.session = requests.Session()
    #     self.url_serveur = url_serveur
    #     self.boucler_sur_splash()

    # def boucler_sur_lobby(self):
    #     url = self.url_serveur + "/boucler_sur_lobby"
    #     params = {"nom": self.nom_joueur_local}
    #     info_etat_joueur = self.appeler_serveur(url, params)
    #     # si l'etat est courant, c'est que la partie vient d'etre lancer
    #     if "courante" in info_etat_joueur[0]:
    #         self.initialiser_partie(info_etat_joueur)
    #     else:
    #         self.joueurs = info_etat_joueur
    #         self.vue.update_lobby(info_etat_joueur)
    #         self.vue.root.after(50, self.boucler_sur_lobby)
    
    # def reset_partie(self):
    #         leurl = self.url_serveur + "/reset_jeu"
    #         reptext = self.appeler_serveur(leurl, 0)
    #         self.vue.update_splash(reptext[0][0]) #
    #         return reptext
    
     # fonction pour demarrer une partie locale (une seul joueur)
    
    #  # fonction pour demarrer une partie coop
    # def creer_partie(self, nom_joueur_local):
    #     if self.prochainsplash:
    #         self.vue.root.after_cancel(self.prochainsplash)
    #         self.prochainsplash = None
    #     self.nom_joueur_local = nom_joueur_local
    #     url = self.url_serveur + "/creer_partie"
    #     data = {
    #         'nom': self.nom_joueur_local
    #     }
    #     reptext = self.appeler_serveur(url, data, "POST")
    #     self.partie_locale = False # on est coop
    #     self.egoserveur = True # je suis la personne qui a demarrer une nouvelle partie
    #     self.vue.root.title("je suis " + self.nom_joueur_local)
    #     self.vue.creer_cadre_lobby("reseau",reptext)
    #     self.vue.afficher_cadre("cadre_lobby")
    #     self.boucler_sur_lobby()

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
        #self.boucler_sur_lobby()
        
    # # fonction pour s'inscrire a une partie creer (mais non lancer...)
    # def inscrire_joueur(self, nom, urljeu):
    #     if self.prochainsplash:
    #         self.vue.root.after_cancel(self.prochainsplash)
    #         self.prochainsplash = None
    #     self.nom_joueur_local = nom
    #     url = self.url_serveur + "/inscrire_joueur"
    #     data = {
    #         'nom': self.nom_joueur_local
    #     }
    #     reptext = self.appeler_serveur(url, data, "POST")
    #     self.vue.root.title("je suis " + self.nom_joueur_local)
    #     self.vue.creer_cadre_lobby("reseau",reptext)
    #     self.partie_locale = False
    #     self.vue.afficher_cadre("cadre_lobby")
    #     self.boucler_sur_lobby()
        
    # def lancer_partie(self):
    #     url = self.url_serveur + "/lancer_partie"
    #     data = {
    #         'nom': self.nom_joueur_local  # Make sure to include this parameter
    #     }
    #     reptext = self.appeler_serveur(url, data, "POST")

    def activer_partie(self):
        if self.partie:
            self.boucler_sur_jeu()
        else:
            url = self.url_serveur + "/activer_partie"
            data = {
                'nom': self.nom_joueur_local  # Make sure to include this parameter
            }
            reptext = self.appeler_serveur(url, data, "POST")
        #self.pause = 1
        #self.boucler_en_attente()
    
        
        
        
        
        
if __name__ == "__main__":
    c = Controleur()