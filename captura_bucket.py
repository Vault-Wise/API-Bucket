# 1 º Passo - Trocar as variáveis com o que está escrito nela
# 2 º Passo - Mandar esse script pra EC2
# 3 º Passo - Conectar na EC2, e criar um ambiente virtual
# Dentro desse ambiente virtual de python, tem que dar pip install boto3
# Rodar o SCRIPT de PYTHON e mandar para o BUCKET

import psutil
import time
import json
from socket import gethostname
import platform
import boto3

nomeMaquina = gethostname()
sistemaOperacional = platform.system()
intervalo = int(input("Digite o intervalo do monitoramento: \n")) 
qtdCapturas = int(input("Digite quantas capturas deseja fazer: "))

s3_client = boto3.client('s3')

dados_monitoramento = []

def upload_to_s3(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    session = boto3.Session(
        aws_access_key_id='',
        aws_secret_access_key='',
        aws_session_token= '',
        region_name='us-east-1',
    )

    s3_client = session.client('s3')

    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"Arquivo '{file_name}' enviado com sucesso para o bucket '{bucket}'!")
    except FileNotFoundError:
        print(f"Arquivo '{file_name}' não encontrado.")


for i in range(qtdCapturas):
    porcent_cpu = psutil.cpu_percent()
    memoria = psutil.virtual_memory()
    freq_cpu = psutil.cpu_freq().current

    if sistemaOperacional == "Windows":
        disco = psutil.disk_usage('C:\\')
    else:
        disco = psutil.disk_usage('/')
    
    captura = {
        "captura": i + 1,
        "intervalo": intervalo,
        "porcCPU": porcent_cpu,
        "FreqCpu": freq_cpu
        ,
        "totalMEM": round(memoria.total / pow(10, 9), 2),
        "usadaMEM": round(memoria.used / pow(10, 9), 2),
        "porcMEM": memoria.percent
        ,
        "totalDisc": round(disco.total / pow(10, 9), 2),
        "usadoDisc": round(disco.used / pow(10, 9), 2),
        "usoDisc": disco.percent
    }

    dados_monitoramento.append(captura)

    print(f"Captura {i} realizada com sucesso.")
    
    time.sleep(intervalo)

# Salva os dados no arquivo JSON
file_name = '/home/ubuntu/python3/DADOSKKKK.json'
with open(file_name, 'w') as jsonfile:
    json.dump(dados_monitoramento, jsonfile, indent=4)

# Envia o arquivo JSON para o S3
bucket_name = 'bucket-raw-lab'
upload_to_s3(file_name, bucket_name)
