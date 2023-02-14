import Pyro4
import os
#Para iniciar o servidor é necessário iniciar esse comando no prompt
#python -m Pyro4.naming
class Server(object):
    register = []
    @Pyro4.expose
    def welcomeMessage(self, name):
        return ('Olá, Bem vindo!' + str(name))

    def uploadFile(self, filename, text):
            filepath = os.path.join('server_data', filename)
            with open(filepath, 'w') as f:
                f.write(text)

    def listFiles(self):
        files = os.listdir('server_data')
        if len(files) == 0:
                return('O diretório do servidor está vazio')
        else:
            return(files)

    def downloadFile(self, filename):
        with open(f'server_data/{filename}', 'r') as f:
            text = f.read()
        return(text)

    def registerNotification(self):
        if len(self.register) == 0:
            return ''
        else:
            files = os.listdir('server_data')
            for f in files:
                if f in self.register:
                    return(f'O arquivo {f} já está disponível para download!\n')
    
    def registerAtt(self, self_register, state):
        if state == True:
            self.register.append(self_register)
            return 'Interesse registrado!'
        if self_register in self.register:
            self.register.remove(self_register)
            return 'Interesse removido!'
        return 'Esse registro não existe.'
        


def startServer():
    server = Server()
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(server)
    ns.register('server', uri)
    print(f'Ready. object uri = {uri}')
    daemon.requestLoop()

if __name__ == '__main__':
    startServer()
