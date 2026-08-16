import os
import sys

# Redireciona completamente a saída e impede qualquer erro de encode do terminal
sys.stdout = open(os.devnull, "w", encoding="utf-8")
sys.stderr = open(os.devnull, "w", encoding="utf-8")

# Desativa a função print no script
def print(*args, **kwargs):
    pass

import datetime
import time
import requests
import re
import json
import threading
from dotenv import load_dotenv

# Importa o servidor do arquivo webhook_server.py
from webhook_server import iniciar_servidor

# Dependências do Google
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google import genai
from google.genai import types


def obter_caminho_base():
    """ Retorna o caminho da pasta raiz, mesmo se executado via arquivo .exe """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


# --- CARREGA O ARQUIVO .ENV DINAMICAMENTE ---
pasta_base = obter_caminho_base()
caminho_env = os.path.join(pasta_base, '.env')
load_dotenv(dotenv_path=caminho_env)

# --- CONFIGURAÇÕES DO .ENV ---
SCOPES = [s.strip() for s in os.getenv("SCOPES", "").split(",") if s.strip()]
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EVOLUTION_URL = os.getenv("EVOLUTION_URL")
EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY")
JID_WHATSAPP = os.getenv("JID_WHATSAPP")
CAMINHO_JSON_ENV = os.getenv("CAMINHO_JSON", os.path.join("Clientes", "clientes_os.json"))
# -----------------------------

client = genai.Client(api_key=GEMINI_API_KEY)

ALERTA_VIRADA_ENVIADO = False
DATA_ULTIMO_ALERTA = None
SERVICE_GOOGLE = None


def carregar_tabela_clientes():
    caminho_json = os.path.join(obter_caminho_base(), CAMINHO_JSON_ENV)
    if not os.path.exists(caminho_json):
        return "Nenhum cliente cadastrado no JSON."

    try:
        with open(caminho_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        linhas = []
        for cliente, os_num in dados.get("CLIENTES_CONTRATO", {}).items():
            linhas.append(f"- {cliente} | OS: {os_num} | [CONTRATO]")
        for cliente, os_num in dados.get("CLIENTES_AVULSOS", {}).items():
            linhas.append(f"- {cliente} | OS: {os_num} | [NÃO É CONTRATO]")
        return "\n".join(linhas)
    except Exception:
        return "Erro ao carregar tabela de clientes do arquivo JSON."


def obter_servico_google():
    base = obter_caminho_base()
    caminho_token = os.path.join(base, 'token.json')
    caminho_credentials = os.path.join(base, 'credentials.json')

    creds = None
    if os.path.exists(caminho_token):
        creds = Credentials.from_authorized_user_file(caminho_token, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(caminho_credentials, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(caminho_token, 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)


def garantir_servico_google():
    global SERVICE_GOOGLE
    if SERVICE_GOOGLE is None:
        SERVICE_GOOGLE = obter_servico_google()
    return SERVICE_GOOGLE


def reescrever_os_com_gemini(texto_bruto):
    tabela_dinamica = carregar_tabela_clientes()
    system_instruction = f"""
    Você é um analista de service desk sênior especialista em documentação técnica de TI. 
    Sua tarefa é transformar anotações brutas de chamados em Ordens de Serviço (O.S.) profissionais.

    DIRETRIZES DE PREENCHIMENTO DO TEMPLATE:
    1. OS: Identifique o cliente na tabela abaixo. Coloque o número da O.S. correspondente. Se o cliente NÃO estiver na tabela abaixo, defina o campo OS como 'Nova / A definir'. Se o usuário passar um número explicitamente nas anotações (ex: "OS 9999"), use o número fornecido.
    2. Data: Use a data informada na instrução 'Data do Evento'. Nunca deixe como DD/MM/AAAA se a data for fornecida.
    3. Cliente: Nome oficial da empresa. Existem DOIS clientes "Gentil" na tabela: Gentil Vitoria e Gentil Angelina. Identifique pelo nome completo mencionado e preencha como 'Gentil Vitoria' ou 'Gentil Angelina'. NUNCA escreva apenas 'Gentil'.
    4. Tipo: Deve ser 'Local', 'Remoto' ou 'Laboratorio'.
    5. Quantidade de horas trabalhadas: Formate SEMPRE por extenso mantendo NÚMEROS EM ALGARISMOS ARÁBICOS (ex: 10 minutos, 1 hora, 40 minutos, 1 hora e 30 minutos). PROIBIDO CHUTAR OU INVENTAR.
    6. Equipamento: Foco do problema (Ex: Servidor, Desktop, Notebook, Rede, Câmeras, etc.). Se não houver, coloque n/a.
    7. Descrição do problema: Traduza o problema bruto para linguagem técnica. Se for genérico de contrato, use: 'Resolução de problemas diversos reportados pelos usuários da empresa.'
    8. Serviço: Solução técnica e detalhada.
    9. Usuário/Solicitado por: Nome do usuário ou 'n/a'.
    10. Material utilizado: Peças ou 'n/a'.
    11. Serviço concluído: Sempre 'sim'.
    12. Técnicos: Sempre 'Kailo'.

    REGRA CRUCIAL PARA CONTRATO:
    Se o cliente for CONTRATO e o chamado NÃO for genérico, adicione ao final do campo 'Serviço':
    - 'Horas contrato (in loco)' -> se Tipo for Local.
    - 'Horas contrato (remoto)' -> se Tipo for Remoto.
    - 'Horas contrato.' -> se Tipo for Laboratorio.

    TABELA ATUAL DE CLIENTES E ORDEM DE SERVIÇO:
    {tabela_dinamica}

    RETORNE APENAS O TEMPLATE PREENCHIDO. Mantenha a estrutura exatamente assim:
    OS: 
    Data: 
    Cliente: 
    Tipo: 
    Quantidade de horas trabalhadas: 
    Equipamento: 
    Descrição do problema: 
    Serviço: 
    Usuário/Solicitado por:
    Material utilizado: 
    Serviço concluído: 
    Técnicos:
    """

    for tentativa in range(3):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"Gere a O.S. formatada com base nesta anotação bruta:\n{texto_bruto}",
                config=types.GenerateContentConfig(system_instruction=system_instruction)
            )
            return response.text.strip()
        except Exception as e:
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                raise e
            if tentativa < 2:
                time.sleep(5)
            else:
                raise e


def enviar_whatsapp(texto):
    url = f"{EVOLUTION_URL.rstrip('/')}/message/sendText/{EVOLUTION_INSTANCE}"
    payload = {"number": JID_WHATSAPP, "text": texto}
    headers = {"Content-Type": "application/json", "apikey": EVOLUTION_API_KEY}
    try:
        requests.post(url, json=payload, headers=headers)
    except Exception:
        pass


def validar_conteudo_chamado(titulo, descricao):
    texto_completo = f"{titulo} {descricao}".lower()
    padrao_tempo = r"\d+\s*(hora|horas|min|minutos|hr|hrs|h|m)\b"
    if not re.search(padrao_tempo, texto_completo):
        return False, "Falta informar o tempo trabalhado de forma clara com números (ex: 2 horas, 40min, 1h)."
    return True, ""


def listar_eventos_periodo(service, time_min, time_max):
    eventos = []
    page_token = None
    while True:
        events_result = service.events().list(
            calendarId='primary', timeMin=time_min, timeMax=time_max,
            maxResults=100, singleEvents=True, orderBy='startTime', pageToken=page_token
        ).execute()
        eventos.extend(events_result.get('items', []))
        page_token = events_result.get('nextPageToken')
        if not page_token:
            break
    return eventos


def processar_chamados():
    global ALERTA_VIRADA_ENVIADO, DATA_ULTIMO_ALERTA, SERVICE_GOOGLE
    hoje = datetime.date.today()
    agora_utc = datetime.datetime.now(datetime.timezone.utc)
    
    if DATA_ULTIMO_ALERTA != hoje:
        ALERTA_VIRADA_ENVIADO = False
        DATA_ULTIMO_ALERTA = hoje

    if hoje.day == 1 and not ALERTA_VIRADA_ENVIADO:
        enviar_whatsapp("⚠️ *AVISO DE VIRADA DE MÊS:* Kailo, hoje é dia 1º! Lembre-se de atualizar as OSs pelo WhatsApp usando o comando `!atualizar Nome, Numero, sim/nao`.")
        ALERTA_VIRADA_ENVIADO = True

    try:
        service = garantir_servico_google()
        primeiro_deste_mes = hoje.replace(day=1)
        ultimo_do_mes_passado = primeiro_deste_mes - datetime.timedelta(days=1)
        primeiro_do_mes_passado = ultimo_do_mes_passado.replace(day=1)
        
        data_limite_inicio = datetime.datetime.combine(primeiro_do_mes_passado, datetime.time.min).astimezone(datetime.timezone.utc).isoformat()
        data_limite_fim = agora_utc.isoformat()

        events = listar_eventos_periodo(service, data_limite_inicio, data_limite_fim)
    except Exception:
        SERVICE_GOOGLE = None
        return

    if not events:
        return

    for event in events:
        titulo = event.get('summary', '').strip()
        descricao = event.get('description', '')
        
        if "[enviado]" in titulo.lower() or "[alerta_enviado]" in titulo.lower():
            continue

        start_time = event.get('start', {}).get('dateTime', event.get('start', {}).get('date', ''))
        data_formatada = "n/a"
        if start_time:
            try:
                dt = datetime.datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                data_formatada = dt.strftime('%d/%m/%Y')
            except Exception:
                data_formatada = start_time[:10]
            
        valido, motivo_erro = validar_conteudo_chamado(titulo, descricao)
        
        if not valido:
            mensagem_alerta = (
                f"⚠️ *ATENÇÃO: CHAMADO INCOMPLETO*\n\n"
                f"Kailo, o chamado *\"{titulo}\"* agendado para *{data_formatada}* não pôde ser gerado.\n\n"
                f"🚩 *Motivo:* {motivo_erro}\n"
                f"💡 _Ajuste o evento adicionando o tempo gasto (ex: 'Compasi contrato 2h')._"
            )
            enviar_whatsapp(mensagem_alerta)
            try:
                event['summary'] = f"[ALERTA_ENVIADO] {titulo}"
                service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
            except Exception:
                pass
            continue

        texto_bruto = f"Data do Evento: {data_formatada}. Título: {titulo}. Descrição: {descricao}"
        
        try:
            os_formatada = reescrever_os_com_gemini(texto_bruto)
            enviar_whatsapp(os_formatada)
            
            limpar_titulo = titulo.replace("[ALERTA_ENVIADO] ", "").replace("[alerta_enviado] ", "")
            event['summary'] = f"[ENVIADO] {limpar_titulo}"
            service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
            time.sleep(1)
        except Exception:
            continue


if __name__ == '__main__':
    thread_webhook = threading.Thread(target=iniciar_servidor, daemon=True)
    thread_webhook.start()

    while True:
        processar_chamados()
        time.sleep(10)