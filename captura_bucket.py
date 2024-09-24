import psutil
import time
from socket import gethostname
import platform
import csv
import boto3
from botocore.exceptions import NoCredentialsError

nomeMaquina = gethostname()
sistemaOperacional = platform.system()
intervalo = int(input("Digite o intervalo do monitoramento: \n")) 
qtdCapturas = int(input("Digite quantas capturas deseja fazer: "))

# Nome do bucket e caminho do arquivo
nomeBucket = 'bucket-raw-lab'
caminhoArquivo = '/home/ubuntu/script-python/teste.csv'
nomeArquivoBucket = 'dadosMaquina-no-s3.csv'  # Nome que o arquivo terá no S3

# Conectar ao serviço S3
s3_client = boto3.client('s3')

# Criar o arquivo CSV e escrever o cabeçalho uma vez
with open(caminhoArquivo, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',')
    csv_writer.writerow(['Uso CPU (%)', 'Freq CPU (MHz)', 'Mem Total (GB)', 'Mem Usada (GB)', 'Uso Memória (%)', 'Disco Total (GB)', 'Disco Usado (GB)', 'Uso Disco (%)'])


for i in range(qtdCapturas):
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
    
    with open(caminhoArquivo, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow([porcent_cpu, round(freq_cpu), round(memoria.total/pow(10, 9), 2), round(memoria.used/pow(10, 9), 2), memoria.percent, round(disco.total/pow(10, 9), 2), round(disco.used/pow(10, 9), 2), disco.percent])  
    
    #Tempo de captura de dados
    time.sleep(intervalo)

try:
    # Enviar arquivo ao S3
    s3_client.upload_file(caminhoArquivo, nomeBucket, nomeArquivoBucket)
    print(f"Arquivo {nomeArquivoBucket} enviado com sucesso ao bucket {nomeBucket}!")
except NoCredentialsError:
    print("Erro: Credenciais não encontradas.")
except Exception as e:
    print(f"Erro ao enviar arquivo: {e}")