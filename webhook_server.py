import os
import sys

# Redireciona saídas e silencia logs
sys.stdout = open(os.devnull, "w", encoding="utf-8")
sys.stderr = open(os.devnull, "w", encoding="utf-8")

import logging
import requests
from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn
from dotenv import load_dotenv

from gerenciador_os import atualizar_os_cliente, deletar_cliente, listar_clientes

def obter_caminho_base():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(obter_caminho_base(), '.env'))

JID_AUTORIZADO = os.getenv("JID_WHATSAPP")
EVOLUTION_URL = os.getenv("EVOLUTION_URL", "http://localhost:8080")
EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE", "Automacao-OS")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "")

# Desativa logs do Uvicorn e FastAPI no terminal
logging.getLogger("uvicorn").setLevel(logging.CRITICAL)
logging.getLogger("uvicorn.access").setLevel(logging.CRITICAL)
logging.getLogger("fastapi").setLevel(logging.CRITICAL)

app = FastAPI()

def responder_whatsapp(remote_jid: str, texto: str):
    base_url = EVOLUTION_URL.rstrip('/')
    url = f"{base_url}/message/sendText/{EVOLUTION_INSTANCE}"
    
    headers = {
        "Content-Type": "application/json",
        "apikey": EVOLUTION_API_KEY
    }
    
    payload = {
        "number": remote_jid,
        "text": texto
    }

    try:
        requests.post(url, json=payload, headers=headers, timeout=10)
    except Exception:
        pass

@app.post("/webhook/whatsapp")
async def receber_webhook(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()
        
        payload = data.get("data", {})
        key = payload.get("key", {})
        remote_jid = key.get("remoteJid", "")
        from_me = key.get("fromMe", False)

        if remote_jid != JID_AUTORIZADO:
            return {"status": "ignored"}

        message_data = payload.get("message", {})
        texto = (
            message_data.get("conversation") or 
            message_data.get("extendedTextMessage", {}).get("text") or 
            message_data.get("imageMessage", {}).get("caption") or 
            ""
        ).strip()

        if from_me and (texto.startswith("✅") or texto.startswith("❌") or texto.startswith("⚠️") or texto.startswith("📋")):
            return {"status": "ignored"}

        # --- COMANDO: !atualizar ---
        if texto.startswith("!atualizar"):
            conteudo = texto.replace("!atualizar", "").strip()
            partes = [p.strip() for p in conteudo.split(",")]

            if len(partes) < 3:
                msg_erro = "⚠️ *Formato inválido!*\nUse: `!atualizar Nome do Cliente, Numero_OS, sim/nao`"
                background_tasks.add_task(responder_whatsapp, remote_jid, msg_erro)
                return {"status": "error"}

            nome_cliente = partes[0]
            nova_os = partes[1]
            e_contrato = partes[2].lower() in ["sim", "s", "true", "1"]

            sucesso, msg = atualizar_os_cliente(nome_cliente, nova_os, e_contrato)
            prefixo = "✅ " if sucesso else "❌ "
            
            background_tasks.add_task(responder_whatsapp, remote_jid, f"{prefixo}{msg}")
            return {"status": "success"}

        # --- COMANDO: !deletar ou !remover ---
        if texto.startswith("!deletar") or texto.startswith("!remover"):
            nome_cliente = texto.replace("!deletar", "").replace("!remover", "").strip()

            if not nome_cliente:
                msg_erro = "⚠️ *Formato inválido!*\nUse: `!deletar Nome do Cliente`"
                background_tasks.add_task(responder_whatsapp, remote_jid, msg_erro)
                return {"status": "error"}

            sucesso, msg = deletar_cliente(nome_cliente)
            prefixo = "✅ " if sucesso else "❌ "

            background_tasks.add_task(responder_whatsapp, remote_jid, f"{prefixo}{msg}")
            return {"status": "success"}

        # --- COMANDO: !listar ou !clientes ---
        if texto in ["!listar", "!clientes"]:
            sucesso, msg = listar_clientes()
            background_tasks.add_task(responder_whatsapp, remote_jid, msg)
            return {"status": "success"}

        return {"status": "ignored"}

    except Exception as e:
        return {"status": "error", "detail": str(e)}

def iniciar_servidor():
    uvicorn.run(app, host="0.0.0.0", port=5050, log_level="critical")