# Processamento periódico dos chamados

Voltar para [[03 - Fluxos/Indice|Índice de Fluxos]] · Implementação em [[02 - Modulos/robo-os|`robo_os.py`]].

## Sequência observada

```mermaid
sequenceDiagram
    participant Loop as Loop robo_os.py
    participant Cal as Google Calendar
    participant Json as JSON de clientes
    participant Gem as Gemini
    participant Evo as Evolution API

    Loop->>Cal: Lista eventos de primary (mês anterior até agora)
    Cal-->>Loop: Eventos paginados
    loop Cada evento não marcado
        Loop->>Loop: Valida duração no título/descrição
        alt Duração ausente
            Loop->>Evo: Envia alerta de chamado incompleto
            Loop->>Cal: Prefixa [ALERTA_ENVIADO]
        else Duração encontrada
            Loop->>Json: Lê clientes e números de O.S.
            Json-->>Loop: Categorias contrato/avulso
            Loop->>Gem: Solicita O.S. no template definido
            Gem-->>Loop: Texto formatado
            Loop->>Evo: Envia O.S.
            Loop->>Cal: Prefixa [ENVIADO]
        end
    end
```

## Decisões e efeitos persistentes

1. `robo_os.py` dispara o aviso mensal quando a data local é dia 1 e ainda não enviou aviso naquele dia em memória.
2. Busca eventos a partir do início do mês anterior até `agora_utc`; pagina resultados em lotes de até 100.
3. Ignora títulos que já contenham `[enviado]` ou `[alerta_enviado]`, sem diferenciar maiúsculas/minúsculas.
4. Aceita indicação de tempo reconhecida pela expressão regular em título ou descrição. Caso contrário, avisa no WhatsApp e marca o evento com `[ALERTA_ENVIADO]`.
5. Para evento válido, monta texto com data, título e descrição; Gemini é solicitado a produzir a O.S.
6. Envia o texto e atualiza o título do evento com `[ENVIADO]`; há uma pausa de um segundo após essa atualização.
7. O loop principal repete com pausa de 10 segundos.

**Limite importante:** o código não verifica o status HTTP das chamadas `requests.post`; uma falha de envio pode não ser percebida antes da atualização do evento. Exceções de processamento são capturadas e o evento pode ser tentado novamente em iterações posteriores. Isso descreve o código observado, não garante o resultado remoto.

Integrações e configuração: [[05 - Interfaces e Integracoes/Contratos-externos|contratos externos]] e [[06 - Desenvolvimento/Instalacao-configuracao|configuração]].
