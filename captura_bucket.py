import psutil
from time import sleep,time
import json
from socket import gethostname
from platform import system
from os import getenv, path 
from dotenv import load_dotenv
from boto3 import Session
from datetime import datetime

load_dotenv()

nomeMaquina = gethostname()
sistemaOperacional = system()

session = Session(
    aws_access_key_id=getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=getenv('AWS_SESSION_TOKEN'),
    region_name=getenv('AWS_REGION')
)
s3_client = session.client('s3')

def get_network_transfer_rate(interval=1):
    net_io_start = psutil.net_io_counters()
    bytes_sent_start = net_io_start.bytes_sent
    bytes_recv_start = net_io_start.bytes_recv
    
    sleep(interval)
    
    net_io_end = psutil.net_io_counters()
    bytes_sent_end = net_io_end.bytes_sent
    bytes_recv_end = net_io_end.bytes_recv
    
    bytes_sent_per_sec = (bytes_sent_end - bytes_sent_start) / interval
    bytes_recv_per_sec = (bytes_recv_end - bytes_recv_start) / interval
    
    return bytes_sent_per_sec, bytes_recv_per_sec

def upload_to_s3(file_name, bucket, s3_client):
    try:
        s3_client.upload_file(file_name, bucket, file_name)
        print(f"Arquivo '{file_name}' enviado com sucesso para o bucket '{bucket}'!")
    except FileNotFoundError:
        print(f"Arquivo '{file_name}' não encontrado.")
    except Exception as e:
        print(f"Erro ao enviar o arquivo para o S3: {e}")

def ler_json_existente(file_name):
    if path.exists(file_name):
        with open(file_name, 'r') as json_file:
            try:
                return json.load(json_file)
            except json.JSONDecodeError:
                return []  # Retorna uma lista vazia se o JSON estiver malformado
    return []

def adicionar_ao_json(file_name, novos_dados):
    dados_existentes = ler_json_existente(file_name)  
    dados_existentes.append(novos_dados) 
    
    with open(file_name, 'w') as json_file:
        json.dump(dados_existentes, json_file, indent=4)

def main():
    i = 0
    intervalo = 10
    file_name = '/home/presilli/Documentos/ProjetoGrupo/dados.json'
    
    while True:
        i += 1
        porcent_cpu = psutil.cpu_percent()
        memoria = psutil.virtual_memory()
        freq_cpu = psutil.cpu_freq().current
        tempo_atividade = psutil.boot_time()
        upload_rate, download_rate = get_network_transfer_rate()
        dataHora = datetime.now()
        data_e_hora_em_texto = dataHora.strftime('%d/%m/%Y %H:%M:%S')


        upload_kbps = (upload_rate * 8) / 1024  # de bytes para kilobits
        download_kbps = (download_rate * 8) / 1024  # de bytes para kilobits

        tempo_atual = time()
        uptime_s = tempo_atual - tempo_atividade

        if sistemaOperacional == "Windows":
            disco = psutil.disk_usage('C:\\')
        else:
            disco = psutil.disk_usage('/')

        captura = {
            "dataHora": data_e_hora_em_texto,
            "tempo_atividade": round(uptime_s, 2),
            "intervalo": intervalo,
            "porcCPU": porcent_cpu,
            "freqCpu": round(freq_cpu, 2) ,
            "totalMEM": round(memoria.total / (1024 ** 3), 2),
            "usadaMEM": round(memoria.used / (1024 ** 3), 2),
            "porcMEM": memoria.percent,
            "totalDisc": round(disco.total / (1024 ** 3), 2),
            "usadoDisc": round(disco.used / (1024 ** 3), 2),
            "usoDisc": disco.percent,
            "upload_kbps": round(upload_kbps, 2),
            "download_kbps": round(download_kbps, 2)
        }

        # Adiciona a captura ao arquivo JSON sem sobrescrever os dados existentes
        adicionar_ao_json(file_name, captura)
        
        # Faz o upload para o S3
        upload_to_s3(file_name, getenv('AWS_BUCKET_NAME'), s3_client)

        print(f"Captura {i} realizada com sucesso.")
        sleep(intervalo)

if __name__ == "__main__":
    main()
