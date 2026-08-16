import os
import json
import sys
from dotenv import load_dotenv

def obter_caminho_base():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# Carrega as variáveis do .env
load_dotenv(os.path.join(obter_caminho_base(), '.env'))

def carregar_dados_json() -> tuple[dict, str]:
    """Função auxiliar para carregar o JSON com segurança."""
    nome_arquivo_json = os.getenv("CAMINHO_JSON", "clientes_os.json")
    caminho_json = os.path.join(obter_caminho_base(), nome_arquivo_json)
    
    if not os.path.exists(caminho_json):
        return None, f"Arquivo '{nome_arquivo_json}' não foi encontrado."

    try:
        with open(caminho_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        return dados, caminho_json
    except Exception as e:
        return None, f"Erro ao ler arquivo JSON: {str(e)}"

def atualizar_os_cliente(nome_cliente: str, nova_os: str, e_contrato: bool) -> tuple[bool, str]:
    dados, caminho_json = carregar_dados_json()
    if dados is None:
        return False, caminho_json

    try:
        secao_alvo = "CLIENTES_CONTRATO" if e_contrato else "CLIENTES_AVULSOS"
        secao_oposta = "CLIENTES_AVULSOS" if e_contrato else "CLIENTES_CONTRATO"

        # Remove do outro bloco caso o cliente tenha mudado de tipo
        for key in list(dados.get(secao_oposta, {}).keys()):
            if key.lower() == nome_cliente.lower():
                del dados[secao_oposta][key]

        # Preserva a formatação exata do nome se o cliente já existir no JSON
        nome_exato = nome_cliente
        for key in dados.get(secao_alvo, {}).keys():
            if key.lower() == nome_cliente.lower():
                nome_exato = key
                break

        dados[secao_alvo][nome_exato] = str(nova_os)

        with open(caminho_json, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

        tipo_str = "CONTRATO" if e_contrato else "AVULSO"
        return True, f"OS do cliente *{nome_exato}* atualizada para *{nova_os}* [{tipo_str}]."

    except Exception as e:
        return False, f"Erro ao atualizar o JSON: {str(e)}"

def deletar_cliente(nome_cliente: str) -> tuple[bool, str]:
    dados, caminho_json = carregar_dados_json()
    if dados is None:
        return False, caminho_json

    try:
        encontrado = False
        nome_removido = nome_cliente

        # Procura e remove de CLIENTES_CONTRATO
        for key in list(dados.get("CLIENTES_CONTRATO", {}).keys()):
            if key.lower() == nome_cliente.lower():
                nome_removido = key
                del dados["CLIENTES_CONTRATO"][key]
                encontrado = True

        # Procura e remove de CLIENTES_AVULSOS
        for key in list(dados.get("CLIENTES_AVULSOS", {}).keys()):
            if key.lower() == nome_cliente.lower():
                nome_removido = key
                del dados["CLIENTES_AVULSOS"][key]
                encontrado = True

        if not encontrado:
            return False, f"Cliente *{nome_cliente}* não foi encontrado no JSON."

        # Salva o arquivo atualizado
        with open(caminho_json, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

        return True, f"Cliente *{nome_removido}* removido do JSON com sucesso!"

    except Exception as e:
        return False, f"Erro ao deletar cliente do JSON: {str(e)}"

def listar_clientes() -> tuple[bool, str]:
    dados, mensagem_erro = carregar_dados_json()
    if dados is None:
        return False, mensagem_erro

    contratos = dados.get("CLIENTES_CONTRATO", {})
    avulsos = dados.get("CLIENTES_AVULSOS", {})

    if not contratos and not avulsos:
        return True, "Nenhum cliente cadastrado no momento."

    # Monta a tabela formatada
    resposta = ["📋 *LISTA DE CLIENTES E ORDENS DE SERVIÇO*\n"]
    resposta.append("```")
    resposta.append(f"{'CLIENTE':<20} | {'Nº OS':<8} | {'TIPO'}")
    resposta.append("-" * 38)

    for cliente, os_num in contratos.items():
        resposta.append(f"{cliente[:20]:<20} | {str(os_num):<8} | Contrato")

    for cliente, os_num in avulsos.items():
        resposta.append(f"{cliente[:20]:<20} | {str(os_num):<8} | Avulso")

    resposta.append("```")
    
    return True, "\n".join(resposta)