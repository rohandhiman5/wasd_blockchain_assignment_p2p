import socket
import threading

class Peer:
    def __init__(self, port):
        self.host = "127.0.0.1"
        self.port = port
        self.peers = {}  # Dictionary with keys as (ip, port) strings

        # Create a socket for listening (server)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        # Start listening thread
        threading.Thread(target=self.listen_for_connections, daemon=True).start()

    def listen_for_connections(self):
        print(f"Server listening on port {self.port}...")
        while True:
            client_socket, client_address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                # Expecting data in the format "sender_ip:sender_port:message"
                ip, port, message = data.split(":", 2)

                if message.lower() == "exit":
                    if (ip, port) in self.peers:
                        del self.peers[(ip, port)]
                    print(f"Peer {ip}:{port} disconnected.")
                elif message.lower() == "connect":
                    print(f"Received connection message from {ip}:{port}")
                    self.peers[(ip, port)] = client_socket  # Store or update peer details
                else:
                    print(f"Message from {ip}:{port} -> {message}")
                    self.peers[(ip, port)] = client_socket  # Store peer details

            except ConnectionResetError:
                break
            except Exception as e:
                print(f"Error handling message: {e}")
                break

        client_socket.close()

    def send_message(self, target_ip, target_port, message):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((target_ip, int(target_port)))
            # Include your own host and port so the receiver can update its peer list
            full_message = f"{self.host}:{self.port}:{message}"
            client_socket.send(full_message.encode())
            print(f"Message sent to {target_ip}:{target_port}")
        except Exception as e:
            print(f"Failed to send message: {e}")
        finally:
            client_socket.close()

    def query_peers(self):
        print("\nConnected Peers:")
        if self.peers:
            for (ip, port) in self.peers.keys():
                print(f"{ip}:{port}")
        else:
            print("No connected peers.")

    def connect_to_active_peers(self):
       
        print("\nConnecting to active peers...")
        if self.peers:
            # Use a list() to avoid modifying the dictionary during iteration
            for (ip, port) in list(self.peers.keys()):
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((ip, int(port)))
                    # Send a connection message
                    client_socket.send(f"{self.host}:{self.port}:connect".encode())
                    print(f"Connection message sent to {ip}:{port}")
                except Exception as e:
                    print(f"Failed to connect to {ip}:{port} - {e}")
                finally:
                    client_socket.close()
        else:
            print("No connected peers to connect to.")

def main():
    port = int(input("Enter your port number: "))
    peer = Peer(port)

    while True:
        print("\n***** Menu *****")
        print("1. Send message")
        print("2. Query connected peers")
        print("3. Connect to active peers   (Bonus)")
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
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
