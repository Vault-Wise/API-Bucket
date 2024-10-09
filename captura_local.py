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

nomeMaquina = gethostname()
sistemaOperacional = platform.system()
intervalo = int(input("Digite o intervalo do monitoramento: \n")) 
qtdCapturas = int(input("Digite quantas capturas deseja fazer: "))

dados_monitoramento = []

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
file_name = 'DIRETORIO'
with open(file_name, 'w') as jsonfile:
    json.dump(dados_monitoramento, jsonfile, indent=4)
