import psutil
import time
from socket import gethostname
import platform
import csv
import boto3

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
with open('Seu CAMINHO', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',')
    csv_writer.writerow(['Uso CPU (%)', 'Freq CPU (MHz)', 'Mem Total (GB)', 'Mem Usada (GB)', 'Uso Memória (%)', 'Disco Total (GB)', 'Disco Usado (GB)', 'Uso Disco (%)'])


def upload_to_s3(file_name, bucket, object_name=None):
    # Se não foi especificado o nome do objeto no S3, usar o nome do arquivo
    if object_name is None:
        object_name = file_name

    session = boto3.Session(
        aws_access_key_id='',
        aws_secret_access_key='',
        aws_session_token= '',
        region_name='us-east-1',    
    )

    s3_client = session.client('s3')


    # Criar uma sessão e um cliente do S3
    try:
        # Realizar o upload
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"Arquivo '{file_name}' enviado com sucesso para o bucket '{bucket}'!")
    except FileNotFoundError:
        print(f"Arquivo '{file_name}' não encontrado.")



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
    
    with open('Seu CAMINHO', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow([porcent_cpu, round(freq_cpu), round(memoria.total/pow(10, 9), 2), round(memoria.used/pow(10, 9), 2), memoria.percent, round(disco.total/pow(10, 9), 2), round(disco.used/pow(10, 9), 2), disco.percent])  
    
    #Tempo de captura de dados
    file_name = 'NOME DO AQRQUIVO NO '
    bucket_name = 'bucket-raw-lab'
    upload_to_s3(file_name, bucket_name)
    time.sleep(intervalo)
