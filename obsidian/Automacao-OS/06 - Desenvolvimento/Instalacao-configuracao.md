# Instalação e configuração

Voltar para [[06 - Desenvolvimento/Indice|Índice de Desenvolvimento]] · Execução em [[06 - Desenvolvimento/Execucao-validacao|Execução e validação]].

## Pré-requisitos identificados

O README declara Python 3.10 ou superior, credenciais OAuth para o Google Calendar, uma instância Evolution API e uma chave Gemini. O repositório não contém ambiente virtual, credenciais, `.env`, JSON de clientes ou arquivo de exemplo de configuração versionados.

## Instalação local

O README sugere criar `venv`; os comandos abaixo usam `.venv` para corresponder ao diretório ignorado no `.gitignore`. São comandos de instalação identificados/adaptados para o projeto, não executados:

```bash
python -m venv .venv
```

Ativação em Linux/macOS:

```bash
source .venv/bin/activate
```

Ativação no Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instalação (o README usa `pip install -r requirements.txt`; abaixo, `python -m pip` invoca o mesmo instalador):

```bash
python -m pip install -r requirements.txt
```

## Arquivos locais e configuração

1. Crie `.env` na pasta base do projeto sem registrar seus valores no Git.
2. Configure os nomes de variáveis listados em [[01 - Arquitetura/Tecnologias-e-configuracao|Tecnologias e configuração]]. Para Calendar, `SCOPES` deve conter o escopo desejado; o README sugere `https://www.googleapis.com/auth/calendar`.
3. Coloque `credentials.json` OAuth na pasta base. Na primeira autenticação do robô, o código obtém autorização local e salva `token.json`.
4. Crie o JSON de clientes conforme [[04 - Dados/Cadastro-clientes|modelo de dados]].
5. Defina `CAMINHO_JSON` explicitamente para que o processador e o webhook leiam o mesmo arquivo; seus padrões não coincidem.
6. Confirme a rota de entrada configurada na Evolution API: o handler local é `POST /webhook/whatsapp` na porta 5050.

O README fornece nomes e exemplos de configuração, mas não substitui a configuração real do ambiente. Não copie credenciais para este vault.
