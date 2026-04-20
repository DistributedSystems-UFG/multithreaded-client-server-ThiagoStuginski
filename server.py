from socket import *
from constCS import *
import struct
import threading
import time

# Configuração de teste
MULTI_THREAD = True

Contador = 1

def handle_client(conn):
    global Contador
    try:
        data = conn.recv(17)
        if data and len(data) >= 17:
            op_byte, n1, n2 = struct.unpack('!cdd', data)
            op = op_byte.decode()
            
            if op == '+': res = n1 + n2
            elif op == '-': res = n1 - n2
            elif op == '*': res = n1 * n2
            elif op == '/': res = n1 / n2 if n2 != 0 else 0.0
            else: res = 0.0
            time.sleep(.1)
            print(f"REQUESICAO TERMINADA {Contador}\n") #I/O
            Contador = Contador + 1
            conn.send(struct.pack('!d', res))
    finally:
        conn.close()

s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(128)

print(f"Servidor {'MULTI-THREAD' if MULTI_THREAD else 'SINGLE-THREAD'} aguardando...")

while True:
    conn, addr = s.accept()
    if MULTI_THREAD:
        thread = threading.Thread(target=handle_client, args=(conn,))
        thread.start()
    else:
        handle_client(conn)
