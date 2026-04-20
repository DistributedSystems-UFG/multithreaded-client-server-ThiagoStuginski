# Calculadora Remota Multi-thread
### Experimento de Desempenho e Concorrência em Sistemas Distribuídos

Este projeto consiste em um sistema de rede (Cliente-Servidor) desenvolvido em Python para realizar operações matemáticas via sockets TCP. O código original foi refatorado para suportar **concorrência**, permitindo a medição da diferença de performance entre o processamento sequencial e o paralelo.

---

## Modificações Realizadas

### 1. Servidor (`server.py`)
* **Implementação de Threads:** O servidor agora utiliza o módulo `threading` para disparar uma nova thread a cada conexão (`handle_client`). Isso permite que múltiplos cálculos sejam feitos simultaneamente sem bloquear a fila de entrada.
* **Controle de Modo:** Adição da flag `MULTI_THREAD = True/False`, que permite alternar o comportamento do servidor para fins de teste comparativo.
* **Otimização de Socket:** Inclusão da opção `SO_REUSEADDR` para evitar erros de "porta já em uso" ao reiniciar o servidor rapidamente durante os testes.
* **Aumento de Backlog:** O método `s.listen()` foi ajustado para suportar uma fila maior de conexões pendentes, mitigando recusas imediatas do sistema operacional sob carga.

### 2. Cliente (`client.py`)
* **Automação de Requisições:** Substituição da entrada manual (`input()`) por um gerador aleatório que utiliza `random.choice` e `random.uniform` para criar uma carga de trabalho instantânea.
* **Disparo em Paralelo:** O cliente pode criar suas próprias threads para enviar várias requisições ao mesmo tempo, simulando uma carga real de múltiplos usuários simultâneos.
* **Cronometragem:** Implementação de medição de tempo com `time.time()` para capturar com precisão o tempo total de processamento do lote de requisições.

---

## O Experimento de Desempenho

O objetivo das modificações é observar como a arquitetura do servidor impacta a escalabilidade do sistema.

| Cenário | Configuração | Comportamento Observado |
| :--- | :--- | :--- |
| **Sequencial** | `MULTI_THREAD = False` | O servidor atende uma requisição por vez. O tempo total é a soma linear de cada tarefa. É comum ocorrer o erro `WinError 10061` se o volume de requisições exceder a capacidade da fila (backlog) do SO. |
| **Paralelo** | `MULTI_THREAD = True` | O servidor aceita conexões e delega o processamento para threads em background. O tempo total cai drasticamente e a taxa de erro de conexão é minimizada. |

---

## Como Executar o Teste

1.  **Configure o Servidor:** Defina `MULTI_THREAD` no topo do arquivo `server.py`.
2.  **Inicie o Servidor:** Execute `python server.py`.
3.  **Configure o Cliente:** Defina o número de requisições desejado (`NUM_REQUISICOES`) e o modo de disparo em `client.py`.
4.  **Inicie o Cliente:** Execute `1..3 | ForEach-Object { Start-Process python "client.py" }`.
5.  **Analise os Resultados:** Compare o "Tempo Total" exibido no terminal do cliente ao final de cada cenário.

---
