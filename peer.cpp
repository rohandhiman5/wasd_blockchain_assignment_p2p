#include <iostream>
#include <thread>
#include <vector>
#include <set>
#include <mutex>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>

using namespace std;

set<string> peers;  // Stores active peers (IP:Port)
mutex peer_mutex;   // Mutex for thread safety

void handle_client(int client_socket, sockaddr_in client_addr) {
    char buffer[1024] = {0};
    int valread = read(client_socket, buffer, 1024);
    if (valread > 0) {
        string client_ip = inet_ntoa(client_addr.sin_addr);
        int client_port = ntohs(client_addr.sin_port);

        // Store the peer information
        string peer_info = client_ip + ":" + to_string(client_port);
        {
            lock_guard<mutex> lock(peer_mutex);
            peers.insert(peer_info);
        }

        cout << "Message from " << peer_info << ": " << buffer << endl;
    }
    close(client_socket);
}

void start_server(int port) {
    int server_fd;
    sockaddr_in address;
    int opt = 1;

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == -1) {
        cerr << "Socket creation failed\n";
        return;
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(port);

    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        cerr << "Binding failed\n";
        return;
    }

    if (listen(server_fd, 5) < 0) {
        cerr << "Listening failed\n";
        return;
    }

    cout << "Server listening on port " << port << endl;

    while (true) {
        sockaddr_in client_addr;
        socklen_t addr_len = sizeof(client_addr);
        int client_socket = accept(server_fd, (struct sockaddr*)&client_addr, &addr_len);
        if (client_socket >= 0) {
            thread(handle_client, client_socket, client_addr).detach();
        }
    }

    close(server_fd);
}

void send_message(string ip, int port, string message) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        cerr << "Socket creation failed\n";
        return;
    }

    sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    inet_pton(AF_INET, ip.c_str(), &server_addr.sin_addr);

    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        cerr << "Connection failed to " << ip << ":" << port << endl;
        return;
    }

    send(sock, message.c_str(), message.size(), 0);
    close(sock);
}

void query_peers() {
    lock_guard<mutex> lock(peer_mutex);
    cout << "Connected Peers:\n";
    for (const auto& peer : peers) {
        cout << peer << endl;
    }
}

// 🔹 New connect() function - Connects to active peers
void connect_to_peers() {
    lock_guard<mutex> lock(peer_mutex);
    if (peers.empty()) {
        cout << "No active peers found!\n";
        return;
    }

    for (const auto& peer : peers) {
        size_t colon_pos = peer.find(":");
        if (colon_pos != string::npos) {
            string ip = peer.substr(0, colon_pos);
            int port = stoi(peer.substr(colon_pos + 1));

            cout << "Connecting to " << ip << ":" << port << endl;
            send_message(ip, port, "CONNECT_REQUEST"); // Send connection message
        }
    }
}

int main() {
    int port;
    cout << "Enter your port number: ";
    cin >> port;

    thread server_thread(start_server, port);
    server_thread.detach();

    while (true) {
        cout << "\n***** Menu *****\n";
        cout << "1. Send message\n";
        cout << "2. Query active peers\n";
        cout << "3. Connect to active peers\n";
        cout << "0. Quit\n";
        cout << "Enter choice: ";
        int choice;
        cin >> choice;

        if (choice == 1) {
            string ip, message;
            int peer_port;
            cout << "Enter recipient IP address: ";
            cin >> ip;
            cout << "Enter recipient port number: ";
            cin >> peer_port;
            cin.ignore();  // Ignore newline left in buffer
            cout << "Enter your message: ";
            getline(cin, message);
            send_message(ip, peer_port, message);
        } 
        else if (choice == 2) {
            query_peers();
        }
        else if (choice == 3) {
            connect_to_peers();
        }
        else if (choice == 0) {
            break;
        }
    }

    return 0;
}

