🤖 Automação de Ordens de Serviço (Google Calendar + Gemini + WhatsApp)Sistema automatizado em Python que monitora eventos do Google Calendar, processa as anotações de chamados técnicos utilizando a API Gemini (Google AI) para formatá-las como Ordens de Serviço (O.S.) e envia a notificação automaticamente via WhatsApp (Evolution API).O projeto também inclui um servidor FastAPI com Webhook para gerenciar dinamicamente a tabela de clientes e números de O.S. via comandos no próprio WhatsApp.🛠️ Tecnologias UtilizadasPython 3.10+Google Gemini API (google-genai) - Inteligência Artificial para reescrita e estruturação técnica de O.S.Google Calendar API - Leitura e sincronização dos eventos/chamados.FastAPI \& Uvicorn - Webhook assíncrono para integração com WhatsApp.Evolution API - Gateway de envio e recebimento de mensagens do WhatsApp.

📋 Estrutura do ProjetoPlaintext
├── main.py                # Loop principal de leitura do Calendar e processamento Gemini

├── webhook\_server.py     # Servidor FastAPI para receber comandos do WhatsApp

├── gerenciador\_os.py     # Manipulação e persistência do JSON de clientes

├── limpar\_passado.py     # Utility script para marcar eventos antigos como \[ENVIADO] (Se usar, lembre-se de colocar a data (de inicio) que preferir)

├── .env.example          # Modelo de variáveis de ambiente

├── requirements.txt      # Dependências do projeto

└── README.md             # Documentação



🚀 Como Configurar e Executar1. Pré-requisitosPython instalado (v3.10 ou superior).Uma instância da Evolution API em execução.Credenciais da API do Google Calendar (credentials.json) habilitadas no Google Cloud Console.Chave de API da Google AI Studio (GEMINI\_API\_KEY).2. InstalaçãoClone o repositório e instale as dependências:

Bashgit clone https://github.com/seu-usuario/seu-repositorio.git

cd seu-repositorio



python -m venv venv

\# No Windows:

venv\\Scripts\\activate

\# No Linux/Mac:

source venv/bin/activate



pip install -r requirements.txt


3. Configuração de Variáveis de Ambiente, Crie um arquivo .env na raiz do projeto baseado no exemplo abaixo:

Snippet de código

SCOPES=https://www.googleapis.com/auth/calendar

GEMINI\_API\_KEY=sua\_chave\_gemini\_aqui

EVOLUTION\_URL=http://localhost:8080

EVOLUTION\_INSTANCE=sua\_instancia

EVOLUTION\_API\_KEY=sua\_chave\_evolution

JID\_WHATSAPP=seu\_id\_whatsapp

CAMINHO\_JSON=clientes\_os.json


4. Estrutura do JSON de Clientes crie o arquivo clientes\_os.json (ou no caminho configurado no .env):JSON{

&#x20;   "CLIENTES\_CONTRATO": {

&#x20;       "Empresa A": "1001",

&#x20;       "Empresa B": "1002"

&#x20;   },

&#x20;   "CLIENTES\_AVULSOS": {

&#x20;       "Cliente X": "2001"

&#x20;   }

}


5\. Execução para iniciar o serviço completo (servidor Webhook + monitor do Calendar):
Bashpython 

main.py

Nota: Na primeira execução, o script abrirá uma janela no navegador para autenticação da conta Google e gerará o arquivo token.json.📱 Comandos Via WhatsAppVocê pode gerenciar as Ordens de Serviço enviando mensagens para a instância conectada:

| Comando | Descrição | Exemplo |

| :--- | :--- | :--- |

| `!listar` / `!clientes` | Lista todos os clientes e suas O.S. cadastradas | `!listar` |

| `!atualizar` | Atualiza ou adiciona um cliente e sua O.S. | `!atualizar Empresa A, 1005, sim` 'sim (para empresa de contrato) ou 'nao' (para empresa avulsa)  |

| `!deletar` / `!remover` | Remove um cliente do cadastro | `!deletar Empresa A` |


