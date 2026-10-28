# Comportamento operacional e observabilidade

Voltar para [[07 - Operacao/Indice|Índice de Operação]] · Execução em [[06 - Desenvolvimento/Execucao-validacao|Execução e validação]].

## Processo residente

Ao executar `robo_os.py`, o servidor FastAPI é iniciado em thread daemon e o loop de processamento roda no processo principal com intervalo de 10 segundos. Uvicorn escuta `0.0.0.0:5050`. Não há arquivo de serviço, container, configuração de proxy, deployment ou instrução de reinício versionada.

## Marcadores do calendário

- `[ENVIADO]`: evento já processado e enviado, segundo o título.
- `[ALERTA_ENVIADO]`: evento sem indicação de tempo, alertado e marcado para não repetir o alerta.

`faxina.py` também usa `[ENVIADO]` para prefixar títulos no intervalo fixo descrito em [[02 - Modulos/faxina|utilitário faxina]].

## Limites de observabilidade confirmados

`robo_os.py` redireciona stdout/stderr para `/dev/null` e substitui `print` por função vazia. O webhook também redireciona saídas e reduz logs de Uvicorn/FastAPI. Além disso, chamadas HTTP de envio ignoram exceções e não verificam respostas HTTP. Assim, os arquivos examinados não oferecem evidência de logging operacional ou métricas suficientes para confirmar entrega de mensagens.

Não foram encontrados health checks, métricas, alertas externos ou política de retry persistente. O fluxo funcional está em [[03 - Fluxos/Processamento-calendario|Processamento do Calendar]].
