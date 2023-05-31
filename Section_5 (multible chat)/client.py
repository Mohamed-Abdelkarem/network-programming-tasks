import socket
import threading
import tkinter as tk

class Client:
    def __init__(self, master):
        self.master = master
        self.username = None
        self.socket = None

        self.message_frame = tk.Frame(master)
        self.message_frame.pack()

        self.scrollbar = tk.Scrollbar(self.message_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_list = tk.Listbox(self.message_frame, yscrollcommand=self.scrollbar.set)
        self.message_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.message_list.yview) #attach the scrollbar with list

        self.input_frame = tk.Frame(master)
        self.input_frame.pack()

        self.username_entry = tk.Entry(self.input_frame, width=10)
        self.username_entry.pack(side=tk.LEFT)

        self.connect_button = tk.Button(self.input_frame, text="Connect", command=self.connect)
        self.connect_button.pack(side=tk.LEFT)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message, state=tk.DISABLED)
        self.send_button.pack(side=tk.RIGHT)

        self.input_entry = tk.Entry(self.input_frame, width=50, state=tk.DISABLED)
        self.input_entry.pack(side=tk.RIGHT)

    def connect(self): #connect the user to the network through socket (and infrom others of him)
        self.username = self.username_entry.get().strip() # get username from Entry box
        if not self.username:
            return

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("localhost", 8000))

        threading.Thread(target=self.receive_messages).start()

        self.send_message("{} has joined the chat.".format(self.username))

        self.username_entry.config(state=tk.DISABLED)
        self.connect_button.config(state=tk.DISABLED)
        self.input_entry.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode()
                if not message:
                    break

                self.message_list.insert(tk.END, message) # add the recieved message to the list
            except ConnectionResetError:
                break

        self.disconnect() #self.socket.close()

    def send_message(self, message=None):
        if not message:
            message = self.input_entry.get().strip()
            self.input_entry.delete(0, tk.END)

        if message:
            self.socket.sendall(message.encode()) #??? send to all clients? or just server, and server will broadcast?

    def disconnect(self):
        self.socket.close()

        self.username_entry.config(state=tk.NORMAL)
        self.connect_button.config(state=tk.NORMAL)
        self.input_entry.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)

        self.message_list.insert(tk.END, "Disconnected from server.")

    def on_close(self):
        self.disconnect()

    def run(self):
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chat Room Client")

    client = Client(root)
    client.run()