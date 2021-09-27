import socket 
import threading
import ast
import time
import uvicorn

HEADER = 64
PORT = 8000
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    def handle_client(conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False

                print(f"[{addr}] {msg}")
                if msg != DISCONNECT_MESSAGE:
                    order = ast.literal_eval(msg)
                    time.sleep(float(order['max_wait']))
                    conn.send(f"Order {order['id']} done!".encode(FORMAT))
                else:
                    conn.send('Done!'.encode(FORMAT))

        conn.close()
            

    def start():
        server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


    print("[STARTING] server is starting...")
    start()

if __name__ == '__main__':
    uvicorn.run(main(), port = PORT, host = SERVER) 