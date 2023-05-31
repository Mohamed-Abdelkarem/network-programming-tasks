import socket
from tkinter import *
from threading import Thread

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

def send_choice(choice):
    client.send(choice.encode())

def receive():
    while True:
        try:
            msg = client.recv(1024).decode() # recieve [won/lost/draw] won from the server
            if msg: 
                if msg == "You won!":
                    result_label.config(text=msg, foreground="green") # show the result on the Label
                elif msg == "You lost!":
                    result_label.config(text=msg, foreground="red")
                elif msg == "Draw!":
                    result_label.config(text=msg, foreground="blue")
        except:
            break

def on_closing():
    client.close()
    window.destroy()

window = Tk()
window.title("Rock-Paper-Scissors")
window.protocol("WM_DELETE_WINDOW", on_closing)

frame = Frame(window)
frame.pack()

# Import the image files
rock_image = PhotoImage(file="rock.png")
paper_image = PhotoImage(file="paper.png")
scissors_image = PhotoImage(file="scissors.png")

# Create the buttons
rock_button = Button(frame, image=rock_image, command=lambda: send_choice("rock"))
rock_button.pack(side=LEFT)

paper_button = Button(frame, image=paper_image, command=lambda: send_choice("paper"))
paper_button.pack(side=LEFT)

scissors_button = Button(frame, image=scissors_image, command=lambda: send_choice("scissors"))
scissors_button.pack(side=LEFT)

# Create the label to show the result
result_label = Label(window, text="Waiting for opponent...", font=("Helvetica", 20))
result_label.pack()

# Create a thread to run the receive function
receive_thread = Thread(target=receive)
receive_thread.start()

window.mainloop()
