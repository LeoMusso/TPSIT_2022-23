from asyncio.windows_events import NULL
from socket import AF_INET, SOCK_DGRAM, socket
import os, csv, time

BUFFER_SIZE = 4096

mystr = "ciao" # str
# bytes

# POSSIBILITÀ
# LocalHOST = "127.0.0.1"
# HOST = "192.168.37.1"
HOST = "0.0.0.0"
PORT = 5000

def get_ip_locale():
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_loc = s.getsockname()[0]
    print("Indirizzo ip locale: ", ip_loc)
    s.close()
    return ip_loc

def mainChatServer():
    ip_loc = get_ip_locale()
    running = True
    with socket (AF_INET, SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print('In ascolto')
        path = os.getcwd()
        cron = path + "\\Cronologia.csv"
        while running == True:
            msg = s.recvfrom(BUFFER_SIZE)
            msg = msg[0].decode()
            mex = msg.split(',')
            data = time.strftime('%d/%m/%Y')
            ora = time.strftime("%H:%M:%S")
            nome = mex[0]
            ip = mex[2]
            port = mex[3]
            sms = mex[1]
            msg = '>>' + mex[0] + ': ' + mex[1]
            if mex[1] == 'crg' and ip == ip_loc:
                print("Cronologia")
                with open(cron) as file:
                    reader = csv.reader(file, delimiter=",")
                stampaCronologia(reader)
            elif (mex[1] == 'exit' or mex[1] == 'EXIT') and ip == ip_loc:
                print("Terminazione chat")
                running = False
            else:
                with open(cron, "a", newline="")as file:
                    writer = csv.writer(file, delimiter=",")
                    lista = (nome, ip, port, sms, data, ora)
                    writer.writerow(lista)
                    file.close()
                print(msg)

def stampaCronologia(rdr):
    dati = [(line[0], line[1], line[2], line[3], line[4], line[5]) for line in rdr if line != NULL or line != ' ']
    print(dati)
    
if __name__ == "__main__":
    path = os.getcwd()
    pathM = path + "\\Server"
    if os.path.exists(pathM) == False:
        os.chdir(path)
        os.mkdir("Server")
        os.chdir(pathM)
        os.mkdir("Cronologia")
        cron = pathM + "\\Cronologia\\Cronologia.csv"
        ceck = os.path.isfile(cron)
        pathM = pathM + "\\Cronologia"
        if ceck == False:
            os.chdir(pathM)
            with open("Cronologia.csv", "w", newline="")as file:
                writer = csv.writer(file, delimiter=",")
                header = (["NOME", "INDIRIZZO_IP", "PORTA", "MESSAGGIO", "DATA", "ORA"])
                writer.writerow(header)
                file.close()
        else:
            cron = pathM + "\\Cronologia\\Cronologia.csv"
            ceck = os.path.isfile(cron)
            if ceck == False:
                os.chdir(pathM)
                with open("Cronologia.csv", "w", newline="")as file:
                    writer = csv.writer(file, delimiter=",")
                    header = (["NOME", "INDIRIZZO_IP", "PORTA", "MESSAGGIO", "DATA", "ORA"])
                    writer.writerow(header)
                    file.close()
    else:
        cron = pathM + "\\Cronologia"
        os.chdir(cron)
    mainChatServer()

    
