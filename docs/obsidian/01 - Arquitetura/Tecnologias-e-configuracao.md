# Tecnologias e configuração

Voltar para [[01 - Arquitetura/Indice|Índice de Arquitetura]] · Configuração prática em [[06 - Desenvolvimento/Instalacao-configuracao|Instalação e configuração]].

## Tecnologias confirmadas no código e dependências

| Tecnologia | Uso observado |
|---|---|
| Python | Linguagem dos quatro scripts. O README declara Python 3.10+, mas não há `pyproject.toml` ou metadado equivalente que fixe a versão. |
| Google Calendar API (`google-api-python-client`) | Consulta e atualização de eventos do calendário `primary`. |
| Google Auth (`google-auth`, `google-auth-oauthlib`) | OAuth de usuário via `credentials.json`; salva/renova `token.json`. |
| Gemini (`google-genai`) | Reescrita das anotações para um template de O.S.; modelo indicado no código: `gemini-2.5-flash`. |
| FastAPI e Uvicorn | Endpoint de webhook em `0.0.0.0:5050`. |
| Requests | Chamadas HTTP para envio de mensagens pela Evolution API. |
| python-dotenv | Carrega variáveis do `.env`. |

A lista declarada está em [`requirements.txt`](../../../requirements.txt). Não existem versões fixadas nesse arquivo.

## Configuração lida pelo código

Os nomes abaixo são identificadores de configuração observados; nenhum valor de segredo foi consultado ou copiado.

| Variável | Leitura/uso |
|---|---|
| `SCOPES` | `robo_os.py` divide uma lista separada por vírgulas. O README sugere o escopo do Calendar. |
| `GEMINI_API_KEY` | Chave passada ao cliente Gemini. |
| `EVOLUTION_URL` | URL base da Evolution API. No webhook há fallback `http://localhost:8080`; no robô não há fallback. |
| `EVOLUTION_INSTANCE` | Identificador da instância. No webhook há fallback `Automacao-OS`; no robô não há fallback. |
| `EVOLUTION_API_KEY` | Cabeçalho `apikey` das chamadas HTTP. O webhook usa string vazia como fallback. |
| `JID_WHATSAPP` | Destinatário das mensagens do robô e remetente autorizado pelo webhook. |
| `CAMINHO_JSON` | Caminho relativo à pasta base para o JSON. Os defaults diferem entre os dois módulos; ver [[04 - Dados/Cadastro-clientes|cadastro de clientes]]. |

OAuth também depende de `credentials.json` e gera/usa `token.json` na pasta base do robô. O `.gitignore` lista esses arquivos e `.env` entre as exclusões.

## Estrutura sem camadas implícitas

Não há framework de aplicação no processador: a coordenação está em funções do módulo `robo_os.py`. O webhook é a única aplicação FastAPI identificada. Não foram encontrados configuração de banco relacional, ORM, filas, testes automatizados, CI ou manifesto de implantação nos arquivos versionados.
