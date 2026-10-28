# Lacunas e confirmações necessárias

Voltar para [[08 - Pendencias/Indice|Índice de Pendências]] · Escopo inspecionado em [[00 - Inicio/Mapa|Mapa da documentação]].

Os itens abaixo são lacunas ou divergências observadas nos arquivos versionados; não são afirmações sobre configurações externas ao repositório.

## Divergências entre README e repositório

- O README apresenta `main.py`, `limpar_passado.py`, `.env.example` e um diretório `Clientes/`; o inventário Git atual contém `robo_os.py`, `faxina.py` e nenhum desses outros caminhos.
- O comando `python main.py` do README não corresponde ao ponto de entrada versionado. O script atual com loop principal é `robo_os.py`.
- O README cita `CAMINHO_JSON=clientes_os.json`, o robô usa por padrão `Clientes/clientes_os.json` e o gerenciador usa `clientes_os.json` na pasta base.
- `.gitignore` ignora `Clientes/clientes_os.json`, mas não o padrão alternativo na raiz. Em sistemas sensíveis a maiúsculas/minúsculas, os caminhos são distintos.

Confirme se o README precisa ser atualizado, se existem arquivos ignorados que devem permanecer locais e qual caminho de dados é o pretendido. Não foi necessário abrir arquivos ignorados ou locais para produzir esta documentação.

## Comportamento externo não confirmado

- Não há configuração de deploy da Evolution API nem confirmação de como o webhook remoto é autenticado/protegido.
- O handler compara `remoteJid` recebido com `JID_WHATSAPP`, mas não valida assinatura/token na requisição HTTP. Confirme proteção na borda/provider antes de expor a porta.
- O código não valida código HTTP das mensagens enviadas; confirme como falhas de entrega devem ser detectadas.
- O formato exato de eventos entregues pelo provedor depende da configuração do Evolution API; os campos consumidos no código estão descritos em [[05 - Interfaces e Integracoes/Contratos-externos|interfaces externas]].
- Não há testes automatizados versionados; não foi possível confirmar comportamento em execução, nem a compatibilidade das APIs externas com as versões atualmente instaladas.

## Decisões de produto/técnicas em aberto

- Confirmar se marcadores no título do Calendar são o mecanismo pretendido de idempotência e se o `faxina.py` ainda deve cobrir o intervalo fixo de 2025-01-01 a 2026-06-15.
- Confirmar se o JSON é o armazenamento pretendido e se há necessidade de controlar escritas simultâneas e validar seu formato.
- Confirmar a estratégia de logs e tratamento de erros; atualmente parte das falhas é silenciosa.

Esses pontos não foram alterados: o pedido limita o trabalho à documentação.
