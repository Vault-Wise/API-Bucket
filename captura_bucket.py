import psutil
import time
import json
from socket import gethostname
import platform
import os
from dotenv import load_dotenv
import boto3

load_dotenv()

nomeMaquina = gethostname()
sistemaOperacional = platform.system()

# Inicializa cliente S3 uma vez
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
    region_name=os.getenv('AWS_REGION')
)
s3_client = session.client('s3')

def get_network_transfer_rate(interval=1):
    net_io_start = psutil.net_io_counters()
    bytes_sent_start = net_io_start.bytes_sent
    bytes_recv_start = net_io_start.bytes_recv
    
    time.sleep(interval)
    
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
    if os.path.exists(file_name):
        with open(file_name, 'r') as json_file:
            try:
                return json.load(json_file)
            except json.JSONDecodeError:
                return []
    return []

def adicionar_ao_json(file_name, novos_dados):
    dados_existentes = [ler_json_existente(file_name)]
    dados_existentes.append(novos_dados)
    
    with open(file_name, 'w') as json_file:
        json.dump(dados_existentes, json_file, indent=4)

def main():
    i = 0
    intervalo = 10
    file_name = '/home/ubuntu/dadosMaquina.json'
    
    while True:
        i += 1
        porcent_cpu = psutil.cpu_percent()
        memoria = psutil.virtual_memory()
        freq_cpu = psutil.cpu_freq().current
        tempo_atividade = psutil.boot_time()
        upload_rate, download_rate = get_network_transfer_rate()

        upload_kbps = (upload_rate * 8) / 1024  # de bytes para kilobits
        download_kbps = (download_rate * 8) / 1024  # de bytes para kilobits

        tempo_atual = time.time()
        uptime_s = tempo_atual - tempo_atividade

        if sistemaOperacional == "Windows":
            disco = psutil.disk_usage('C:\\')
        else:
            disco = psutil.disk_usage('/')

        captura = {
            "captura": i,
            "tempo_atividade": uptime_s,
            "intervalo": intervalo,
            "porcCPU": porcent_cpu,
            "freqCpu": freq_cpu,
            "totalMEM": round(memoria.total / pow(10, 9), 2),
            "usadaMEM": round(memoria.used / pow(10, 9), 2),
            "porcMEM": memoria.percent,
            "totalDisc": round(disco.total / pow(10, 9), 2),
            "usadoDisc": round(disco.used / pow(10, 9), 2),
            "usoDisc": disco.percent,
            "upload_kbps": upload_kbps,
            "download_kbps": download_kbps
        }

        # Adiciona a captura ao arquivo JSON sem sobrescrever os dados existentes
        adicionar_ao_json(file_name, captura)
        
        # Faz o upload para o S3
        upload_to_s3(file_name='dados.json', bucket='bucket-raw-lab', s3_client=s3_client)

        print(f"Captura {i} realizada com sucesso.")
        time.sleep(intervalo)

if __name__ == "__main__":
    main()
