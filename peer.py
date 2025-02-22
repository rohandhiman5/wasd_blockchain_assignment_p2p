import socket
import threading

#function to get the ip address of the system 

def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80)) 
    ip = s.getsockname()[0]
    s.close()
    return ip


class Peer:

    def __init__(self, team_name, port): 

        self.team_name = team_name

        # self.host=socket.gethostbyname(socket.gethostname())
        self.host=get_lan_ip() ##host name / ip addresss
        self.port = port
        self.peers = {}  

        # socket for listening (server)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        self.running = True
        threading.Thread(target=self.listen_for_connections, daemon=True).start()

    ##function to check if the peer is connected or not

    def listen_for_connections(self):

        """Listens for incoming peer connections."""
        print(f"Server listening on {self.host}:{self.port}...")
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
            except OSError:
                break

   

    def handle_client(self, client_socket):

        while self.running:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break

                parts = data.split(" ", 2)
                if len(parts) < 3:
                    print("Invalid message format received:", data)
                    continue

                ip_port, team, message = parts
                ip, port = ip_port.split(":")
                
                if message.lower() == "exit":
                    if (ip, port) in self.peers:
                        del self.peers[(ip, port)]
                    print(f"Peer {ip}:{port} ({team}) disconnected.")

                elif message.lower() == "connect":
                    print(f"Received connection message from {ip}:{port} ({team})")
                    self.peers[(ip, port)] = client_socket  # Store or update peer details

                else:
                    print(f"Message from {ip}:{port} ({team}) -> {message}")
                    self.peers[(ip, port)] = client_socket  # Store peer details

            except ConnectionResetError:
                break
            except Exception as e:
                print(f"Error handling message: {e}")
                break

        client_socket.close()

    ##function to send the message to peers

    def send_message(self, target_ip, target_port, message):

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client_socket.connect((target_ip, int(target_port)))
            full_message = f"{self.host}:{self.port} {self.team_name} {message}"
            client_socket.send(full_message.encode())
            print(f"Message sent to {target_ip}:{target_port}")

        except Exception as e:
            print(f"Failed to send message: {e}")
        finally:
            client_socket.close()

    ##function to query the connected peers

    def query_peers(self):

        print("\nConnected Peers:")
        if self.peers:
            for (ip, port) in self.peers.keys():
                print(f"{ip}:{port}")
        else:
            print("No connected peers.")

    ##bonus question: connect to all the active peers 

    def connect_to_active_peers(self):

        print("\nConnecting to active peers...")
        if self.peers:
            for (ip, port) in list(self.peers.keys()):
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((ip, int(port)))
                    client_socket.send(f"{self.host}:{self.port} {self.team_name} connect".encode())
                    print(f"Connection message sent to {ip}:{port}")
                except Exception as e:
                    print(f"Failed to connect to {ip}:{port} - {e}")
                finally:
                    client_socket.close()
        else:
            print("No connected peers to connect to.")
    
    ##disconnect the corresponding peers

    def disconnect_from_peers(self):

        """Notify all peers before exiting."""
        print("\nDisconnecting from all peers...")
        for (ip, port) in list(self.peers.keys()):
            self.send_message(ip, port, "exit")  # Send exit message to all peers

        self.peers.clear()  # Remove all peer entries
        print("Disconnected successfully.")
     
     ##function to stop the server

    def stop_server(self):
        """Stop the listening server before exiting."""
        self.running = False
        self.server_socket.close()

def main():

    team_name = input("Enter your team name: ")
    port = int(input("Enter your port number: "))
    peer = Peer(team_name, port)

    while True:
        print("\n***** Menu *****")
        print("1. Send message")
        print("2. Query connected peers")
        print("3. Connect to active peers")
        print("0. Quit")
        choice = input("Enter choice: ")

        if choice == "1":
            target_ip = input("Enter recipient's IP address: ")
            target_port = input("Enter recipient's port number: ")
            message = input("Enter your message: ")
            peer.send_message(target_ip, target_port, message)

        elif choice == "2":
            peer.query_peers()

        elif choice == "3":
            peer.connect_to_active_peers()

        elif choice == "0":
            print("Exiting...")
            peer.disconnect_from_peers() 
            peer.stop_server()  
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
