# `webhook_server.py` — webhook e comandos

Voltar para [[02 - Modulos/Indice|Índice de Módulos]] · Fluxo de comandos em [[03 - Fluxos/Comandos-WhatsApp|Comandos WhatsApp]].

Arquivo: [`webhook_server.py`](../../../webhook_server.py).

## Responsabilidades

- Cria uma aplicação FastAPI e expõe `POST /webhook/whatsapp`.
- Extrai `remoteJid`, `fromMe` e texto de campos de mensagem conhecidos no JSON recebido.
- Processa comandos `!atualizar`, `!deletar`/`!remover` e `!listar`/`!clientes`.
- Agenda o envio das respostas com `BackgroundTasks` e chama operações de [`gerenciador_os.py`](../../../gerenciador_os.py).
- Inicia Uvicorn em `0.0.0.0:5050` por `iniciar_servidor()`.

## Controle de remetente e mensagens

Compara `remoteJid` com `JID_WHATSAPP`; mensagens de outros remetentes retornam `ignored`. Algumas mensagens emitidas pelo próprio bot, identificadas por prefixo, também são ignoradas para evitar reprocessamento. A autenticação de origem do webhook HTTP não está implementada visivelmente neste arquivo; confirme como o provedor limita e protege chamadas recebidas antes de expor a porta.

Os logs do processo são fortemente silenciados no início do módulo. O POST de resposta usa timeout de 10 segundos; exceções nessa operação são descartadas.

## Relações

O robô inicia o servidor em uma thread daemon ([[02 - Modulos/robo-os|módulo principal]]). O payload e a chamada de resposta estão descritos em [[05 - Interfaces e Integracoes/Contratos-externos|interfaces externas]].
