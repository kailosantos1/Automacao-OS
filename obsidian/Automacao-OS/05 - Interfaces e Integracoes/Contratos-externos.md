# Contratos externos observáveis

Voltar para [[05 - Interfaces e Integracoes/Indice|Índice de Interfaces e Integrações]] · Contexto em [[01 - Arquitetura/Visao-geral|Arquitetura]].

## Google Calendar

- Cliente construído com API `calendar` v3 e credenciais OAuth de usuário.
- Os scripts consultam e atualizam o calendário `primary`.
- `robo_os.py` lista eventos com `timeMin`, `timeMax`, paginação, `singleEvents=True` e ordenação por `startTime`; atualizações substituem `summary` e enviam o evento atualizado.
- `faxina.py` usa `token.json` do diretório de execução e um intervalo fixo; veja [[02 - Modulos/faxina|faxina.py]].

Não há configuração de ID de calendário além de `primary` nos caminhos examinados.

## Gemini

`robo_os.py` chama `client.models.generate_content` com modelo `gemini-2.5-flash`, anotações do evento como conteúdo e instrução de sistema com clientes atuais e o template da O.S. Há até três tentativas para exceções que não sejam identificadas como `RESOURCE_EXHAUSTED`/`429`; essas condições são propagadas sem repetição adicional. Não há contrato de resposta validado por parser no código: o texto é enviado como recebido após `strip()`.

## Evolution API — envio

O robô e o webhook constroem a rota:

```text
POST {EVOLUTION_URL}/message/sendText/{EVOLUTION_INSTANCE}
```

Enviam `Content-Type: application/json`, cabeçalho `apikey` e JSON com `number` e `text`. No webhook, o POST tem timeout de 10 segundos; no robô, não há timeout explícito. O código não valida código HTTP nem corpo da resposta.

## Evolution API — webhook de entrada

FastAPI declara `POST /webhook/whatsapp` e lê campos `data.key.remoteJid`, `data.key.fromMe` e texto de `data.message.conversation`, `extendedTextMessage.text` ou `imageMessage.caption`. O remetente é comparado com `JID_WHATSAPP`. Não há esquema formal, assinatura ou token de webhook visível no handler; a segurança da origem depende de configuração externa não incluída no repositório.

Detalhes de processamento: [[02 - Modulos/webhook-server|módulo webhook]] e [[03 - Fluxos/Comandos-WhatsApp|fluxo de comandos]].
