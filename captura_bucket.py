import psutil
from time import sleep,time
import json
from socket import gethostname
from platform import system
from os import getenv, path
from dotenv import load_dotenv
from boto3 import Session
from datetime import datetime
from mysql.connector import connect
from atlassian import Jira
from collections import defaultdict
load_dotenv()

jira = Jira(
    url = getenv('URL_JIRA'), 
    username = getenv('EMAIL_JIRA'),
    password = getenv('TOKEN_JIRA')
)

mydb = connect(
    user=getenv('USUARIO_BANCO'), 
    password=getenv('SENHA_BANCO'), 
    host=getenv('HOST_BANCO'),
    database=getenv('NOME_BANCO'),
    port=getenv('PORTA_BANCO')
)

session = Session(
    aws_access_key_id=getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=getenv('AWS_SESSION_TOKEN'),
    region_name=getenv('AWS_REGION')
)

cursor = mydb.cursor()
s3_client = session.client('s3')

nomeMaquina = gethostname()
sistemaOperacional = system()

freqTotalProcessador = round(psutil.cpu_freq().max, 2)
memoriaTotal = round(psutil.virtual_memory().total/pow(10, 9),0)

cursor.execute(f"SELECT * FROM CaixaEletronico WHERE nomeEquipamento = '{nomeMaquina}'")
for i in cursor.fetchall():
    print(i)

if cursor.rowcount < 1: 
    cursor.execute(f"INSERT INTO CaixaEletronico VALUES (default, '{nomeMaquina}', '{sistemaOperacional}', {memoriaTotal}, {freqTotalProcessador}, 1)") 
    mydb.commit()
    idEquipamento = cursor.lastrowid
else: 
    cursor.execute(f"SELECT idCaixa FROM CaixaEletronico WHERE nomeEquipamento LIKE '{nomeMaquina}'")
    idEquipamento_tupla = cursor.fetchone()
    idEquipamento = idEquipamento_tupla[0]


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

def get_processos_ativos(idRegistro):
    for processo in psutil.process_iter(attrs=['pid', 'name']):
        processo.cpu_percent(interval=None)
    
    sleep(1)

    num_nucleos = psutil.cpu_count(logical=True)

    processos = defaultdict(lambda: {'cpu': 0.0, 'mem': 0.0, 'pids': set()})

    for processo in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            pid = processo.info['pid']
            nome_processo = processo.info['name'].split('/')[-1].split(' ')[0] 
            uso_cpu = processo.info['cpu_percent'] / num_nucleos 
            uso_mem = processo.info['memory_percent']

            if uso_cpu > 0.2:
                processos[nome_processo]['cpu'] += uso_cpu
                processos[nome_processo]['mem'] += uso_mem
                processos[nome_processo]['pids'].add(pid) 
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    for nome_processo, valores in processos.items():
        cursor.execute(f"INSERT INTO Processo VALUES (DEFAULT, {valores['cpu']:.2f}, {valores['mem']:.2f}, DEFAULT, {idRegistro}, {idEquipamento})") 
        print("Cadastrando processo ")
        idProcesso = cursor.lastrowid
        for pid in valores['pids']:
            cursor.execute(f"INSERT INTO PID VALUES (DEFAULT, {pid}, {2}, {idProcesso}, {idRegistro}, {idEquipamento})")

def upload_to_s3(file_name, bucket, s3_client, folder_name="dadosMaquina"):
    try:
        file_base_name = path.basename(file_name)  # Extraí apenas o nome do arquivo
        s3_file_path = f"{folder_name}/{file_base_name}"  # Define o caminho completo no S3
        s3_client.upload_file(file_name, bucket, s3_file_path)
        print(f"Arquivo '{file_base_name}' enviado com sucesso para a pasta '{folder_name}' no bucket '{bucket}'!")
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
    repeticao_CPU_RAM = 0
    repeticao_CPU = 0
    repeticao_RAM = 0
    i = 0
    last_upload_time = time()
    last_upload_time_processo = time()
    intervalo = 15
    intervaloBucket = 45
    intervalo_processos = 15
    file_name = '/home/ubuntu/script-python/dados.json'
    
    while True:
        i += 1
        porcent_cpu = psutil.cpu_percent()
        memoria = psutil.virtual_memory()
        freq_cpu = psutil.cpu_freq().current
        tempo_atividade = psutil.boot_time()
        upload_rate, download_rate = get_network_transfer_rate()
        dataHora = datetime.now()
        dataHoraTexto = dataHora.strftime('%d/%m/%Y %H:%M:%S')

        upload_kbps = (upload_rate * 8) / 1024  # de bytes para kilobits
        download_kbps = (download_rate * 8) / 1024  # de bytes para kilobits

        tempo_atual = time()
        uptime_s = tempo_atual - tempo_atividade

        cursor.execute(f"""INSERT INTO Registro (idRegistro, dtHora, percentMemoria, percentProcessador, memoriaUsada,  freqProcessador, velocidadeUpload, velocidadeDowload, tempoAtividade, fkCaixa) VALUES (DEFAULT, DEFAULT, {round(memoria.percent, 2)}, {round(porcent_cpu, 2)}, {round(memoria.used /pow(10,9), 2)}, {round(freq_cpu)}, {round(upload_kbps, 2)},
        {round(download_kbps, 2)}, {uptime_s}, {idEquipamento})""")
        mydb.commit()
        idRegistro = cursor.lastrowid

        if(round(porcent_cpu, 2) > 80 and round(memoria.percent, 2) > 80):
            cursor.execute(f"INSERT INTO Alerta VALUES (DEFAULT, 'Memória e CPU', 'Ambos acima de 80%', DEFAULT, {idRegistro}, {idEquipamento})")
            mydb.commit()
            repeticao_CPU_RAM+=1

            if(repeticao_CPU_RAM >= 5):
                    
                jira.issue_create(
                    fields={
                        'project': {
                            'key': 'VAULT' #SIGLA DO PROJETO
                        },
                        'summary': 'Alerta de CPU e RAM',
                        'description': 'CPU e RAM acima da média, necessario olhar com atenção esse Caixa em específico caso precise de manutenção em breve',
                        'issuetype': {
                            "name": "Task"
                        },
                    }
                )

                repeticao_CPU_RAM=0

        elif (round(memoria.percent, 2) > 80):
            cursor.execute(f"INSERT INTO Alerta VALUES (DEFAULT, 'Memória', 'Memória RAM acima de 80%', DEFAULT, {idRegistro}, {idEquipamento})")
            mydb.commit()
            repeticao_RAM+=1

            if(repeticao_RAM >= 5):
                
                jira.issue_create(
                        fields={
                        'project': {
                            'key': 'VAULT' #SIGLA DO PROJETO
                        },
                        'summary': 'Alerta de RAM',
                        'description': 'Memória RAM acima da média, analisar comportamento estranho e verificar se é frequente',
                        'issuetype': {
                            "name": "Task"
                        },
                    }
                )
                
                repeticao_RAM=0

        elif(round(porcent_cpu, 2) > 80):
            cursor.execute(f"INSERT INTO Alerta VALUES (DEFAULT, 'CPU', 'CPU acima de 80%', DEFAULT, {idRegistro}, {idEquipamento})")
            mydb.commit()
            repeticao_CPU+=1

            if(repeticao_CPU >= 5):

                jira.issue_create(
                    fields={
                        'project': {
                            'key': 'VAULT' #SIGLA DO PROJETO
                        },
                        'summary': 'Alerta de CPU',
                        'description': 'Processador acima da média, possível ataque no Caixa ou erro de Hardware.',
                        'issuetype': {
                            "name": "Task"
                        },
                    }
                )

                repeticao_CPU=0

        captura = {
            "idCaixaEletronico": idEquipamento,
            "dataHora": dataHoraTexto,
            "tempo_atividade": round(uptime_s, 2),\
            "porcCPU": porcent_cpu,
            "freqCpu": round(freq_cpu, 2),
            "usadaMem": round(memoria.used / (1024 ** 3), 2),
            "porcMem": memoria.percent,
            "upload_kbps": round(upload_kbps, 2),
            "download_kbps": round(download_kbps, 2)
        }

        # Adiciona a captura ao arquivo JSON sem sobrescrever os dados existentes
        adicionar_ao_json(file_name, captura)
        
        current_time = time() 
        if current_time - last_upload_time_processo >= intervalo_processos:
            get_processos_ativos(idRegistro)
            last_upload_time_processo = current_time

        if current_time - last_upload_time >= intervaloBucket:
            upload_to_s3(file_name, getenv('AWS_BUCKET_NAME'), s3_client, folder_name="dadosMaquina")
            last_upload_time = current_time

        print(f"Captura {i} realizada com sucesso.")
        sleep(intervalo)

if __name__ == "__main__":
    main()
