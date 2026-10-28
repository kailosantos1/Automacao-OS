# `robo_os.py` — processamento principal

Voltar para [[02 - Modulos/Indice|Índice de Módulos]] · Fluxo detalhado em [[03 - Fluxos/Processamento-calendario|Processamento do Calendar]].

Arquivo: [`robo_os.py`](../../../robo_os.py).

## Responsabilidades e pontos de entrada

- `obter_caminho_base()` localiza a pasta do script (ou do executável frozen); `.env`, `credentials.json` e `token.json` são procurados nessa base.
- `obter_servico_google()` lê/renova credenciais OAuth e cria cliente Calendar v3; `garantir_servico_google()` mantém o serviço em `SERVICE_GOOGLE`.
- `listar_eventos_periodo()` percorre páginas do calendário `primary`.
- `validar_conteudo_chamado()` exige que título ou descrição contenha um tempo reconhecido por uma expressão regular.
- `reescrever_os_com_gemini()` injeta no prompt a tabela de clientes do JSON e solicita o template fixo de O.S.
- `enviar_whatsapp()` faz POST para o endpoint de envio de texto da Evolution API.
- `processar_chamados()` coordena seleção, validação, geração, envio e atualização do evento.
- O bloco principal inicia `iniciar_servidor()` em thread daemon e chama `processar_chamados()` repetidamente, com pausa de 10 segundos.

## Regras comportamentais visíveis

- A consulta cobre desde o início do mês anterior até o momento atual; eventos com `[ENVIADO]` ou `[ALERTA_ENVIADO]` no título são ignorados.
- Chamados sem uma duração explícita recebem alerta e o marcador `[ALERTA_ENVIADO]`.
- Após gerar e enviar uma O.S., o título recebe `[ENVIADO]`.
- No primeiro processamento do dia 1, envia aviso de virada do mês; o estado desse aviso é mantido somente em memória.
- O texto do Gemini instrui um formato fixo, informa campos para identificar e atribuir O.S. e contém regras para clientes de contrato. A saída real depende da resposta do serviço externo.

Implementação: [`processar_chamados()`](../../../robo_os.py#L199), [`validar_conteudo_chamado()`](../../../robo_os.py#L176), [`reescrever_os_com_gemini()`](../../../robo_os.py#L105) e [`obter_servico_google()`](../../../robo_os.py#L79).

## Relações

Compartilha o arquivo de cadastro com [[02 - Modulos/gerenciador-os|`gerenciador_os.py`]], chama a integração descrita em [[05 - Interfaces e Integracoes/Contratos-externos|interfaces externas]] e inicia [[02 - Modulos/webhook-server|`webhook_server.py`]].

