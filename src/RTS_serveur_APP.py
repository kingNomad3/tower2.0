# -*- coding: utf-8 -*-


from flask import Flask, request, json, jsonify
from werkzeug.wrappers import Response
import random
import sqlite3


app = Flask(__name__)

app.secret_key = "qwerasdf1234"

class Dbman():
    def __init__(self):
        self.conn = sqlite3.connect("RTS_serveur_DB.db")
        self.curs = self.conn.cursor()
        
        self.create_table_tableau()
        
    def create_table_tableau(self):
        self.curs.execute("CREATE TABLE IF NOT EXISTS tableau (tableau_choisi NUMBER);")
        self.conn.commit()
        
    def settableauchoisi(self, tableau):
        self.curs.execute("INSERT into tableau (tableau_choisi) VALUES(?);", (tableau,))
        self.conn.commit()

    def setpartiecourante(self, chose):
        self.vidertable("partiecourante")
        self.curs.execute("Insert into partiecourante (etat) VALUES(?);", (chose,))
        #print("DATABASE",chose)
        self.conn.commit()

    def setinitaleatoire(self, chose):
        self.vidertable("initaleatoire")
        self.curs.execute("Insert into initaleatoire (initaleatoire) VALUES(?);", (chose,))
        self.conn.commit()

    def setcadrecourant(self, chose):
        self.vidertable("cadrecourant")
        self.curs.execute("Insert into cadrecourant (cadrecourant) VALUES(?);", (chose,))
        self.conn.commit()

    def ajouterjoueur(self, nom):
        self.curs.execute("Insert into joueurs (nom) VALUES(?);", (nom,))
        self.conn.commit()

    def ajouteractionaujoueur(self, nom, cadrejeu, action):
        self.curs.execute("Insert into actionsenattente (nom,cadrejeu,action) VALUES(?,?,?);",
                          (nom, cadrejeu, json.dumps(action)))
        self.conn.commit()

    def getinfo(self, table):
        sqlnom = "select * from '" + table + "'"
        self.curs.execute(sqlnom)
        info = self.curs.fetchall()
        return info

    def getinfoconditionel(self, table, champ, valeur):
        sqlnom = "select * from '" + table + "' WHERE nom=?"
        self.curs.execute(sqlnom, (valeur))
        info = self.curs.fetchall()
        return info

    def resetdb(self):
        tables = ["partiecourante", "joueurs", "cadrecourant", "actionsenattente", "initaleatoire", "nbrIA"]
        for i in tables:
            self.vidertable(i)

        self.curs.execute("Insert into partiecourante (etat) VALUES(?);", ("dispo",))
        self.curs.execute("Insert into cadrecourant (cadrecourant) VALUES(?);", (0,))
        self.curs.execute("Insert into initaleatoire (initaleatoire) VALUES(?);", (2020,))
        self.curs.execute("Insert into nbrIA (nbrIA) VALUES(?);", (0,))
        self.conn.commit()

    def effaceractionsjoueur(self, joueur):
        self.curs.execute("DELETE from actionsenattente WHERE  nom=?", (joueur,))
        self.conn.commit()

    def vidertable(self, table):
        self.curs.execute("DELETE from " + table)
        self.conn.commit()

    def fermerdb(self):
        self.conn.close()

    def updatejoueur(self, nomjoueur, cadre):
        monsql = "UPDATE joueurs SET derniercadrejeu = ? WHERE nom = ? ;"
        self.curs.execute(monsql, (cadre, nomjoueur))
        self.conn.commit()

#################################################################################################

@app.route("/tester_jeu", methods=["GET", "POST"])
def tester_jeu():
    db = Dbman()
    info = db.getinfo("partiecourante")
    return jsonify(info)

@app.route("/reset_jeu", methods=["GET", "POST"])
def reset_jeu():
    db = Dbman()
    db.resetdb()
    info = db.getinfo("partiecourante")
    #print("RESET",info)
    return jsonify(info)

@app.route("/creer_partie", methods=["GET", "POST"])
def creer_partie():
    db = Dbman()
    info = db.getinfo("partiecourante")
    #print("CREER PARTIE ",info)
    if "dispo" in info[0]:
        data = request.get_json()
        db.ajouterjoueur(data['nom'])
        db.setpartiecourante("attente")

        joueurs = db.getinfo("joueurs")
        return jsonify(joueurs)

@app.route("/inscrire_joueur", methods=["GET", "POST"])
def inscrire_joueur():
    db = Dbman()
    info = db.getinfo("partiecourante")
    #print("INSCRIRE JOUEUR",info)
    if "attente" in info[0]:
        data = request.get_json()
        db.ajouterjoueur(data['nom'])

        joueurs = db.getinfo("joueurs")
        return jsonify(joueurs)

@app.route("/boucler_sur_lobby", methods=["GET", "POST"])
def boucler_sur_lobby():
    db = Dbman()
    
    info = db.getinfo("partiecourante")
    #print("BOUCER SUR LOBBY",info)
    if "courante" in info[0]:
        initaleatoire = db.getinfo("initaleatoire")
        reponse = ["courante", initaleatoire]

        db.fermerdb()
        return jsonify(reponse)
    else:
        data = request.get_json()
        tableau = data["tableau"]
        
        if tableau is not None or tableau != db.getinfo(tableau)[0]:
            db.settableauchoisi(tableau)
            
        info = {"info_joueur": db.getinfo("joueurs"), "tableau": db.getinfo(tableau)[0]}
        
        db.fermerdb()
        return jsonify(info)

@app.route("/lancer_partie", methods=["GET", "POST"])
def lancer_partie():
    db = Dbman()
    initrand = random.randrange(1000, 10000)
    db.setinitaleatoire(initrand)
    db.setpartiecourante("courante")
    db.fermerdb()

    info = ["courante", initrand]
    return jsonify(info)

@app.route("/activer_partie", methods=["GET", "POST"])
def activer_partie():
    db = Dbman()
    db.setpartiecourante("activer")
    #info = ["activer"]

    db.fermerdb()
    return jsonify("batman")

@app.route("/verifier_activation_partie", methods=["GET", "POST"])
def verifier_activation_partie():
    db = Dbman()
    info = db.getinfo("partiecourante")

    # data = request.get_json()
    # #data['nom'])
    #
    # print("VERIFIER_ACTIVATION",data["nom"],info)
    if "activer" in info[0]:
        reponse = ["activer"]

        db.fermerdb()
        return jsonify(reponse)
    else:
        info = db.getinfo("joueurs")

        db.fermerdb()
        return jsonify(info)

@app.route("/boucler_sur_jeu", methods=["POST"])
def boucler_sur_jeu():
    # donnees recu d'un joueur
    data = request.get_json()
    nom = data['nom']
    cadrejeu = int(data["iteration_boucle_jeu"])
    actionsrequises = data["actions_requises"]

    # inscrire la iteration_boucle_jeu pour ce joueur
    db = Dbman()
    db.updatejoueur(nom, cadrejeu)

    joueurscadrejeu = db.getinfo("joueurs")
    # besoin de ceci pour evaluer la distance temporel entre les joueurs
    _min = min(joueurscadrejeu, key=lambda t: t[1])
    _max = max(joueurscadrejeu, key=lambda t: t[1])

    maliste = []
    # NOTE : cette section doit être revue si on a reçu une actionsrequises
    # on verifie si l'autre joueur est en retard
    #if (cadrejeu - _min[1]) > 10:
    #    # on envoie un message pour dire d'attendre
    #    maliste = ["ATTENTION"]

    # ON AJOUTE LES ACTIONS À TOUS LES JOUEURS
    if actionsrequises != "None":
        # on ajoute n (5) pour dire QUAND (en iteration_boucle_jeu) l'Action devra etre effectue
        sautdecadre = _max[1] + 5
        info = db.getinfo("joueurs")
        for i in info:
            db.ajouteractionaujoueur(i[0], sautdecadre, actionsrequises)

    # ON CHERCHE S'IL Y A DES ACTIONS QUE NOUS DEVRONS RECEPTIONNER
    info = db.getinfo("actionsenattente")

    for i in info:
        if i[0] == nom:
            maliste.append([i[1], i[2]])
    db.effaceractionsjoueur(nom)

    db.fermerdb()

    return jsonify(maliste)

if __name__ == '__main__':
   
    app.run(debug=True, port=8000)
