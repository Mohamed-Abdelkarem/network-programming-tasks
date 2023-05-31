import socket
from threading import Thread

def game_logic(player1_choice, player2_choice):
    if player1_choice == player2_choice:
        return "draw"
    elif (player1_choice == "rock" and player2_choice == "scissors") or \
         (player1_choice == "paper" and player2_choice == "rock") or \
         (player1_choice == "scissors" and player2_choice == "paper"):
        return "player1"
    else:
        return "player2"
    
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(2)

clients = []
choices = {}

def handle_client(client):
    while True:
        try:
            msg = client.recv(1024).decode() # recieve from first/second player
            if msg:
                choices[client] = msg # save msg in directory for first/second player
                if len(choices) == 2: # after we recieve 2 messages
                    result = game_logic(*choices.values())
                    broadcast(result) # player1 / player2 / draw
                    choices.clear()
        except:
            clients.remove(client)
            client.close()
            break

def broadcast(result):
    for client in choices.keys():
        if result == "draw":
            client.send("Draw!".encode())
        elif result == "player1" and client == list(choices.keys())[0]: # if player1 won & we are in 1st iteration
            client.send("You won!".encode())
        elif result == "player2" and client == list(choices.keys())[1]: # if player2 won & we are in 2nd iteration
            client.send("You won!".encode())
        else:
            client.send("You lost!".encode())

def accept_connections():
    while True:
        client, addr = server.accept()
        clients.append(client)
        print(f"Connected to {addr}")
        Thread(target=handle_client, args=(client,)).start()

print("Server is ready...")
accept_connections()