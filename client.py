from socket import *
from constCS import *
import struct
import threading
import random
import time

# Configurações do Experimento
NUM_REQUISICOES = 100
MULTI_THREAD = False 

def enviar_requisicao(id_req):
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((HOST, PORT))
        
        # Gera dados aleatórios
        op = random.choice(['+', '-', '*', '/']).encode('ascii')
        n1 = random.uniform(1, 100)
        n2 = random.uniform(1, 100)

        pacote = struct.pack('!cdd', op, n1, n2)
        sock.send(pacote)
        
        data = sock.recv(8)
        if data:
            resultado = struct.unpack('!d', data)[0]
            # print(f"Req {id_req}: {resultado}") # Opcional: log de progresso
            
        sock.close()
    except Exception as e:
        print(f"Erro na requisição {id_req}: {e}")

# Início do Experimento
print(f"Iniciando {NUM_REQUISICOES} requisições...")
inicio = time.time()

threads = []
if MULTI_THREAD:
    for i in range(NUM_REQUISICOES):
        t = threading.Thread(target=enviar_requisicao, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
else:
    for i in range(NUM_REQUISICOES):
        enviar_requisicao(i)

fim = time.time()
print("-" * 30)
print(f"Configuração: {'Multi-thread' if MULTI_THREAD else 'Sequencial'}")
print(f"Tempo total: {fim - inicio:.4f} segundos")
print("-" * 30)
