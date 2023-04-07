import socket

ADDRES = 'localhost'
PORT = 8000

#lista contendo os tipo de imagens que podem ser abertas
tipo_arq_binario = ['png', 'jpeg', 'webp', 'jpg', 'svg']
#lista de arquivos que podem ser abertos
tipo_arq_texto = ['html', 'css']

socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket_servidor.bind((ADDRES, PORT))
socket_servidor.listen()

while True:
    print(f'Servidor ouvindo em {ADDRES}:{PORT} pronto para receber conexões')
    socket_cliente, cliente_addr = socket_servidor.accept()

    print(f'Cliente conectado com sucesso. {cliente_addr[0]}:{cliente_addr[1]}')

    dado_recebido = socket_cliente.recv(1024)
    dado_recebido = dado_recebido.decode()

    cabecalhos = dado_recebido.split('\t\n')
    cabecalho_get = cabecalhos[0]

    arq_solicitado = cabecalho_get.split(' ')[1][1:]
    print(f'arquivo solicitado: {arq_solicitado}')


    extensao_arq = arq_solicitado.split('.')[-1]
    
    arq_binario = False
    if extensao_arq in tipo_arq_binario:
        arq_binario = True
    

    try:
        if arq_binario:
            arquivo = open(arq_solicitado, 'rb')
        else:
            arquivo = open(arq_solicitado, 'r', encoding='utf-8')
            
        conteudo_arq = arquivo.read()
    except FileNotFoundError:
        print(f'Arquivo não existe {arq_solicitado}')
        socket_cliente.sendall(b'HTTP/1.1 404 file not found\r\n\r\nFound file not found')
        socket_cliente.close()
        continue
        
        
    cabecalho_resposta = f'HTTP/1.1 200 OK\r\n\r\n'
    corpo_resposta = conteudo_arq

    if arq_binario:
        resultado_final = bytes(cabecalho_resposta,'utf-8') + corpo_resposta
        socket_cliente.sendall(resultado_final)
    else:
        resultado_final = cabecalho_resposta + corpo_resposta
        socket_cliente.sendall(resultado_final.encode('utf-8'))

    socket_cliente.close()

socket_cliente.close()