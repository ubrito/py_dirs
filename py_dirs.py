#!/usr/bin/env python

import argparse
import socket


def extrai_codigo_http(resposta):
    '''
    Extrai e retorna o código HTTP da resposta recebida
    '''
    return resposta[9:12]
    

def busca_diretorios(site, port, wordlist):
    '''
    Realiza a busca dos diretórios através de força bruta utilizando a wordlist apontada
    '''

    lista = open(wordlist,'r')
    print(f"Procurando por diretórios em: {site}")

    # Iterate over each line (entry) in the wordlist
    for linha in lista:

        cliente = socket.create_connection((site, port))
        cabecalho = f"GET /{linha[:-1]}/ HTTP/1.1\r\nHost: {site}\r\n\r\n"
               
        cliente.send(cabecalho.encode())

        # Recebe a resposta
        resposta = cliente.recv(1024)
        
        if (extrai_codigo_http(resposta) == b'200'):
            print("[+] DIRETÓRIO ENCONTRADO: /" + linha[:-1])

    lista.close()


if __name__ == "__main__":

    args = argparse.ArgumentParser(description="Busca por diretórios em em sites através de força bruta.")
    args.add_argument('-s', '--site', type=str, help="Site onde será realizada a busca de diretórios.", required=True)
    args.add_argument('-p', '--port', type=int, help="Porta (default 80)", default=80, required=False)
    args.add_argument('-w', '--wordlist', type=str, help="Wordlist a ser utilizado na força bruta", required=True)
    args = args.parse_args()

    busca_diretorios(args.site, args.port, args.wordlist)

    