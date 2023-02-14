import Pyro4
import os

def main():
    name = input('Qual seu nome? ').strip()
    server = Pyro4.Proxy('PYRONAME:server')
    print(server.welcomeMessage(name))

    print('''Lista de comandos:\n
    UPLOAD -> Faz o upload de um arquivo para o servidor.\n
    CONSULT -> Lista todos os arquivos no servidor.\n
    DOWNLOAD -> Baixa um arquivo do servidor.\n
    REGISTER -> Registra interesse em ser notificado por um arquivod do servidor.\n
    CANCEL -> Retira um interesse previamente cadastrado.\n
    LOGOUT -> Sai do sistema.
    ''')

    while True:
        command = input('O que deseja realizar?\n>>>').strip().upper()
        if command == 'UPLOAD':
            path = input('Qual o caminho do arquivo?')
            with open(f'{path}', 'r') as f:
                text = f.read()
            filename = path.split('/')[-1]
            server.uploadFile(filename, text)
            print('Arquivo enviado!')

        if command == 'CONSULT':
            print(server.listFiles())

        if command == 'DOWNLOAD':
            filename = input('Qual o nome do arquivo?')
            text = server.downloadFile(filename)
            filepath = os.path.join('client_data', filename)
            with open(filepath, 'w') as f:
                f.write(text)
            print('O download do arquivo foi concluído!')

        if command == 'REGISTER':
            filename = input('Qual o nome do arquivo que deseja ser notficado?')
            print(server.registerAtt(filename, True))

        if command == 'CANCEL':
            filename = input('Qual o nome do arquivo que deseja parar de ser notificado?')
            print(server.registerAtt(filename, False))

        if command == 'LOGOUT':
            print('Sessão finalizada!')
            break

        print(server.registerNotification(), end='')

if __name__ == '__main__':
    main()
