# Peer-to-Peer chat Program

This project implements a Peer-to-Peer (P2P) Chat Program that allows multiple peers to communicate directly with each other in a network. The program supports:
  1. Simultaneous message sending and receiving
  2. Querying and retrieving a list of active peers
  3. Bonus feature to connect with peers from whom messages have been received.

The program works by running multiple instances in separate terminal environments, where each peer can send and receive messages in real-time.

This project was made by:
| Name         | Roll No |
|--------------|---------|
| Rohan       | 230001069     |
| Mani Mathur  | 230001050    |
| Siddarth singh   | 230002068 |

## Table of Contents

1. [Project Overview](#project-overview)
2.  [Instructions to Use](#instructions-to-use)
   
## Project Overview
This Peer-to-Peer (P2P) chat program allows users to send and receive messages from other peers in a network. The communication happens via sockets and supports multiple peers connecting to each other. Peers can query each other to see a list of peers they've interacted with.
### Features:
1. **Send and Receive Messages Simultaneously**: Users can send and receive messages at the same time using multi-threading.
2. **Query Active Peers**: Retrieve the list of peers that have sent messages to the current peer.
3. **Bonus Function**: Connect to peers from whom messages have been received, establishing a mutual connection.
4. **Simultaneous Messaging**: Multiple instances of the program can run in different terminal windows or machines to simulate a real P2P network.

### Static IP Requirement:

The program connects to the following static IP addresses and ports:

    IP: 10.206.4.201, PORT: 1255
    IP: 10.206.5.228, PORT: 6555

This connection is only possible if you are connected to the IIT internal network.   

## Instructions to Use

### Prerequisites
Instructions to Use
Prerequisites

Ensure you have Python 3.x installed on your system.

1. **Clone the Repository:**
   ``` bash
   git clone https://github.com/rohandhiman5/wasd_blockchain_assignment_p2p.git
   cd wasd_blockchain_assignment_p2p

2. **Open Multiple Terminal Windows:**
  - To simulate multiple peers, open multiple terminal windows (each representing a different peer in the network).
  - In each terminal, run the program by entering the following command
  ```
    python3 peer.py
  ```
3. **Enter the Port Number:** After running the program, it will ask you to enter a port number for each instance.
   - For example:
  ``` Enter your port number: 1255 ```
 

## Menu options:
 ```
   1. Send message
   2. Query connected peers
   3. Connect to active peers 
   0. Quit
   Enter choice:
```

- Send Message (Option 1): Send a message to a specified peer by entering their IP address, port number, and message.
- Query Active Peers (Option 2): Retrieve the list of peers you've received messages from.
- Connect to Active Peers (Option 3): Actively connect to peers you've interacted with, establishing mutual awareness.
- Quit (Option 0): Exit the program






