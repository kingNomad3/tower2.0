import sqlite3
import datetime

class Agent_BD():
    def __init__(self, parent):
        self.parent = parent
        self.conn = sqlite3.connect("./base_TD.db")
        #  2: Cree l'objet cursor qui executera les requetes SQL
        self.cursor = self.conn.cursor()
        #  3: Cree table avec joueurs_locaux et date
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS joueurs_locaux (
                id INTEGER PRIMARY KEY,
                nom TEXT,
                date DATE                
            )           
        ''')
        # self.cursor.execute("DROP TABLE joueurs_defis")
        self.cursor.execute('''
               CREATE TABLE IF NOT EXISTS joueurs_defis (
                   id INTEGER PRIMARY KEY, 
                   nom TEXT UNIQUE,                    
                   creeps_tue INTEGER DEFAULT 0,
                   credits INTEGER DEFAULT 0                
               )           
           ''')
        self.populate_defis()
        
    def populate_defis(self):
        cursor = self.conn.cursor()
        for nom in self.chercher_usagers():
            cursor.execute("INSERT OR IGNORE INTO joueurs_defis (nom) VALUES (?)", (nom, ))
            self.conn.commit()

    def ajouter_aux_defis(self, nom, creeps_tue):
        cursor = self.conn.cursor()
        # Execute une requete qui insere le nom du joueur et la date courante d'inscription
        try:
            cursor.execute("UPDATE joueurs_defis SET creeps_tue = creeps_tue + ? WHERE nom = ?", (creeps_tue, nom))
            self.conn.commit()
        except sqlite3.Error as e:
            print("SQLite error:", e)
        
        cursor.execute("SELECT creeps_tue FROM joueurs_defis WHERE nom = (?)", (nom,))
        nb_creeps_tues = cursor.fetchall()
        if nb_creeps_tues[0][0] > 1000000:
            cursor.execute("INSERT INTO joueurs_defis (credits) VALUES (500) WHERE nom = (?)", (nom, ))
        cursor.close()

    def voir_defis(self, nom):
        cursor = self.conn.cursor()
        cursor.execute("SELECT creeps_tue FROM joueurs_defis WHERE nom = (?)", (nom,))
        valeurs = cursor.fetchall()[0][0]
        cursor.close()
        return valeurs

    def chercher_usagers(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT nom FROM joueurs_locaux")
        # Fetch toutes les valeurs de la colone nom
        nom_values = cursor.fetchall()
        # Close the cursor and the connection
        cursor.close()
        # nom_values est une liste de tuple a un seul element
        # la comprehension de liste suivante nous donne une liste des elements en position 0 de chaque tuple
        nom_values = [item[0] for item in nom_values]
        return nom_values

    def ajouter_aux_usagers_locaux(self, nom):
        cursor = self.conn.cursor()
        # Execute une requete qui insere le nom du joueur et la date courante d'inscription
        date_courante = datetime.datetime.now()
        cursor.execute("INSERT INTO joueurs_locaux (nom, date) VALUES (?, ?)", (nom, date_courante))
        self.conn.commit()
        cursor.close()

    def generer_sql(self,table, colonnes, conditions=None):
        # Construction du SELECT
        mon_sql = "SELECT {columns} FROM {table}".format(columns=", ".join(colonnes), table=table)

        # Ajouter les conditions s'il y a lieu
        if conditions:
            mon_sql += " WHERE {conditions}".format(conditions=conditions)
        return mon_sql

    def requerir_info(self, table, colonnes, conditions= None):
        mon_sql = self.generer_sql(table, colonnes, conditions)
        cursor = self.conn.cursor()
        cursor.execute(mon_sql)
        # Fetch toutes les valeurs de la colone nom
        nom_values = cursor.fetchall()
        # fermer le cursor
        cursor.close()
        # nom_values est une liste de tuple a un seul element
        # la comprehension de liste suivante nous donne une liste des elements en position 0 de chaque tuple
        nom_values = [item[0] for item in nom_values]
        return nom_values



