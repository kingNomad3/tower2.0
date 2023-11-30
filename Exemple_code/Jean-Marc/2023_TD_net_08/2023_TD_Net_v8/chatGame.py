import tkinter as tk
from tkinter import messagebox
import requests
import json

class TDGameApp:
    def __init__(self, root):
        self.root = root
        self.session = requests.session()
        root.title("Tower Defense Game")
        self.player_name = None
        self.frames = {}  # Dictionary to store frames
        self.active_frame = None  # Track the active frame
        self.create_frames()

    def create_frames(self):
        # Create a dictionary of frames and associate them with text names
        self.frames['SplashScreen'] = self.create_splash_screen()
        #self.frames['LocalLobby'] = self.create_local_lobby("Local Lobby")
        #self.frames['CoopLobby'] = self.create_coop_lobby("Cooperative Lobby")

        # Set the initial active frame
        self.activate_frame('SplashScreen')


    def activate_frame(self, frame_name):
        # Hide the current active frame
        if self.active_frame:
            self.active_frame.pack_forget()

        # Show the new active frame
        frame = self.frames.get(frame_name)
        if frame:
            frame.pack()
            self.active_frame = frame

    def create_splash_screen(self):
        # Create a canvas that occupies the whole frame
        self.splash_screen_frame = tk.Frame(self.root)
        canvas = tk.Canvas(self.splash_screen_frame, width=400, height=300)
        canvas.pack()

        # Add a background image to the canvas (customize this part as needed)
        # background_image = tk.PhotoImage(file="background.png")
        # canvas.create_image(0, 0, anchor="nw", image=background_image)

        # Label for player identification
        player_label = tk.Label(canvas, text="Enter Your Name:")
        player_label_window = canvas.create_window(200, 100, anchor="center", window=player_label)

        # Entry widget to input player's name
        self.player_name_entry = tk.Entry(canvas)
        self.player_name_entry.insert(0,"jmd")
        player_name_window = canvas.create_window(200, 140, anchor="center", window=self.player_name_entry)

        # Button to start the game in single-player mode
        single_player_button = tk.Button(canvas, text="Single Player", command=self.show_local_lobby)
        single_player_window = canvas.create_window(200, 180, anchor="center", window=single_player_button)

        # Button to start the game in cooperative mode
        coop_button = tk.Button(canvas, text="Cooperative Mode", command=self.show_coop_lobby)
        coop_window = canvas.create_window(200, 220, anchor="center", window=coop_button)
        return self.splash_screen_frame

    def show_local_lobby(self):
        self.player_name = self.player_name_entry.get()

        self.frames['LocalLobby'] = self.create_local_lobby(self.player_name)
        if self.player_name:
            self.activate_frame('LocalLobby')

    def show_coop_lobby(self):
        self.player_name = self.player_name_entry.get()

        self.frames['CoopLobby'] = self.create_coop_lobby(self.player_name)
        if self.player_name:
            self.activate_frame('CoopLobby')

    def create_local_lobby(self, player_name):
        # Create a local lobby frame
        self.local_lobby_frame = tk.Frame(self.root)

        # Label to indicate it's the local lobby
        lobby_label = tk.Label(self.local_lobby_frame, text="Local Lobby")
        lobby_label.pack()

        # Label to display the player's name
        player_label = tk.Label(self.local_lobby_frame, text=f"Player: {player_name}")
        player_label.pack()

        # Create a canvas for the grid of buttons
        canvas = tk.Canvas(self.local_lobby_frame, width=400, height=300)
        canvas.pack()

        # Create a matrix of buttons for board selection on the canvas
        for row in range(3):
            for col in range(4):
                x = col * 100 + 50
                y = row * 100 + 50
                board_num = row * 4 + col + 1
                board_button = tk.Button(canvas, text=f"Board {board_num}", command=lambda num=board_num: self.select_board(num))
                canvas.create_window(x, y, anchor="center", window=board_button)
        return self.local_lobby_frame

    def create_coop_lobby(self, player_name):
        # Create a coop lobby frame
        self.coop_lobby_frame = tk.Frame(self.root)
        #self.coop_lobby_frame.pack()

        # Label to indicate it's the coop lobby
        lobby_label = tk.Label(self.coop_lobby_frame, text="Cooperative Lobby")
        lobby_label.pack()

        # Label to display the player's name
        player_label = tk.Label(self.coop_lobby_frame, text=f"Player: {player_name}")
        player_label.pack()

        # Entry field for specifying the server address
        server_label = tk.Label(self.coop_lobby_frame, text="Server Address:")
        server_label.pack()
        self.server_entry = tk.Entry(self.coop_lobby_frame)
        self.server_entry.pack()
        #self.server_entry.insert(0,"127.0.0.1:8000")
        self.server_entry.insert(0,"jmdeschamps.pythonanywhere.com")
        server_connection = tk.Button(self.coop_lobby_frame, text="Connecter",command=self.connecter)
        server_connection.pack()

        # Create a canvas for the grid of buttons
        canvas = tk.Canvas(self.coop_lobby_frame, width=400, height=300)
        canvas.pack()

        # Create a matrix of buttons for board selection on the canvas
        for row in range(3):
            for col in range(4):
                x = col * 100 + 50
                y = row * 100 + 50
                board_num = row * 4 + col + 1
                board_button = tk.Button(canvas, text=f"Board {board_num}", command=lambda num=board_num: self.select_board(num))
                canvas.create_window(x, y, anchor="center", window=board_button)

        return self.coop_lobby_frame

    def select_board(self, board_num):
        print(board_num)
        # Add the logic to handle board selection here
        # You can store the selected board number and perform further actions
    def connecter(self):
        self.url_serveur = "http://"+self.server_entry.get()
        print(self.url_serveur)
        self.tester_etat_serveur()

    def tester_etat_serveur(self):
        leurl = self.url_serveur + "/tester_jeu"
        for i in range(10):
            repdecode = self.appeler_serveur(leurl, None)
            print("Reponse: ",repdecode)

    def appeler_serveur(self, url, params, method="GET"):
        if method == "GET":
            response = self.session.get(url, json=params)
        elif method == "POST":
            response = self.session.post(url, json=params)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    root = tk.Tk()
    app = TDGameApp(root)
    root.mainloop()
