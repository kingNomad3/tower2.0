import tkinter as tk
import requests

server_url = "http://your-server-url/endpoint"
session = requests.Session()

# Initialize the player ID and iteration number
player_id = "local_player"
iteration_number = 0

def poll_server(player_id, iteration_number):
    params = {'player_id': player_id, 'iteration_number': iteration_number}

    response = session.get(server_url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Process the data received from the server
        print(data)

def game_loop():
    global iteration_number  # Make sure to use the global iteration_number variable
    # Update your game model and view objects
    # ...

    # Call the poll_server function within the game loop and pass the current player ID and iteration number
    poll_server(player_id, iteration_number)

    iteration_number += 1  # Increment the iteration number

    # Schedule the game loop to run again after 50 milliseconds
    root.after(50, game_loop)

# Create a tkinter window
root = tk.Tk()
root.title("Game Window")

# Initialize your game and view objects here

# Start the game loop
root.after(0, game_loop)

root.mainloop()
