# Mapa da documentação

Voltar para [[00 - Inicio/Inicio|Início]].

## Áreas do vault

- [[01 - Arquitetura/Indice|01 — Arquitetura]]: visão geral, tecnologias, configuração e responsabilidades.
- [[02 - Modulos/Indice|02 — Módulos]]: os quatro scripts versionados e suas funções.
- [[03 - Fluxos/Indice|03 — Fluxos]]: processamento do Calendar e comandos recebidos pelo webhook.
- [[04 - Dados/Indice|04 — Dados]]: estrutura do JSON de clientes e persistência.
- [[05 - Interfaces e Integracoes/Indice|05 — Interfaces e Integrações]]: contratos observáveis com serviços externos.
- [[06 - Desenvolvimento/Indice|06 — Desenvolvimento]]: instalação, configuração, execução e validação.
- [[07 - Operacao/Indice|07 — Operação]]: comportamento operacional confirmado e limites de observabilidade.
- [[08 - Pendencias/Indice|08 — Pendências]]: divergências, incertezas e confirmações necessárias.

## Caminhos do repositório

| Arquivo | Papel documentado |
|---|---|
| [`robo_os.py`](../../../robo_os.py) | Loop principal, Calendar, Gemini e envio WhatsApp. |
| [`webhook_server.py`](../../../webhook_server.py) | Endpoint FastAPI e interpretação dos comandos de WhatsApp. |
| [`gerenciador_os.py`](../../../gerenciador_os.py) | Leitura, atualização, remoção e listagem do JSON de clientes. |
| [`faxina.py`](../../../faxina.py) | Utilitário para marcar eventos de um intervalo fixo como enviados. |
| [`requirements.txt`](../../../requirements.txt) | Dependências Python declaradas. |
| [`README.md`](../../../README.md) | Documentação existente, com divergências em relação aos arquivos versionados. |
| [`.gitignore`](../../../.gitignore) | Exclusões de credenciais, ambiente e arquivos locais de dados. |

## Cobertura

Todos os sete caminhos versionados foram inspecionados. Não foram lidos `.env`, credenciais, tokens, dependências instaladas, caches, builds ou arquivos binários. A ausência de testes, configurações de lint e configuração de build foi determinada pelo inventário do repositório, não por execução de testes inexistentes.
