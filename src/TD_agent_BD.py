import sqlite3
import datetime

class Agent_BD():
    def __init__(self, parent):
        self.parent = parent
        self.conn = sqlite3.connect("base_TD.db")
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
        self.cursor.execute('''
               CREATE TABLE IF NOT EXISTS joueurs_defis (
                   nom TEXT PRIMARY KEY,                    
                   creeps_tue INTEGER                
               )           
           ''')

    def ajouter_aux_defis(self, nom, creeps_tue):
        cursor = self.conn.cursor()
        # Execute une requete qui insere le nom du joueur et la date courante d'inscription
        cursor.execute("INSERT INTO joueurs_defis (nom, creeps_tue) VALUES (?, ?) ON CONFLICT (nom) DO UPDATE SET creeps_tue = EXCLUDED.creeps_tue + joueurs_defis.creeps_tue ", (nom, creeps_tue))
        self.conn.commit()
        cursor.close()

    def voir_defis(self, nom):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM joueurs_defis WHERE nom = (?)", (nom))
        nb_creeps_tues = cursor.fetchall()
        cursor.close()
        return nb_creeps_tues

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



