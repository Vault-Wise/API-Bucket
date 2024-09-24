import psutil
import time
from socket import gethostname
import platform
import csv
import boto3

nomeMaquina = gethostname()
sistemaOperacional = platform.system()
intervalo = int(input("Digite o intervalo do monitoramento: \n")) #setando o intervalo da captura

# Criar o arquivo CSV e escrever o cabeçalho uma vez
with open('/home/presilli/Documentos/ProjetoGrupo/teste.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',')
    csv_writer.writerow(['Uso CPU (%)', 'Freq CPU (MHz)', 'Mem Total (GB)', 'Mem Usada (GB)', 'Uso Memória (%)', 'Disco Total (GB)', 'Disco Usado (GB)', 'Uso Disco (%)'])


while True:
    #Variáveis de captura dos dados
    
    porcent_cpu = psutil.cpu_percent()
    memoria = psutil.virtual_memory()
    freq_cpu = psutil.cpu_freq().current

    if(sistemaOperacional == "Windows"):
        disco = psutil.disk_usage('C:\\')
    else:
        disco = psutil.disk_usage('/')
    

    print(""" 
    DADOS ARMAZENADOS
          
    (Dados sendo capturados a cada {:.2f}s)
          
    CPU:      
    Porcentagem de uso da CPU: {:.2f}%
    Freq CPU: {:f}
    
    Memória (total = {:.2f} GB):
    Porcentagem de uso memória RAM: {:.1f}
    Memoria Usada: {:f} GB
          
    Disco Rígido (total = {:.2f} GB): 
    Porcentagem de uso do disco: {:.1f}%
    Disco usado: {:f} 
          
    Pressione Ctrl+C para encerrar a captura
    """.format(intervalo, porcent_cpu, round(freq_cpu),  memoria.total/pow(10, 9), memoria.percent, round(memoria.used/pow(10,9)), disco.total/pow(10, 9), disco.percent, round(disco.used/pow(10,9))))

    
    with open('/home/presilli/Documentos/ProjetoGrupo/teste.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow([porcent_cpu, round(freq_cpu), round(memoria.total/pow(10, 9), 2), round(memoria.used/pow(10, 9), 2), memoria.percent, round(disco.total/pow(10, 9), 2), round(disco.used/pow(10, 9), 2), disco.percent])  
    
    #Tempo de captura de dados
    time.sleep(intervalo)