# Automação de Ordens de Serviço

Este vault documenta o repositório **Automacao-OS**: um serviço Python que lê eventos do Google Calendar, transforma anotações em Ordens de Serviço com Gemini e as envia pelo WhatsApp via Evolution API. Um webhook permite consultar e manter o cadastro de clientes e números de O.S.

## Comece por aqui

- [[00 - Inicio/Mapa|Mapa da documentação]]
- [[01 - Arquitetura/Visao-geral|Arquitetura e componentes]]
- [[03 - Fluxos/Processamento-calendario|Fluxo de processamento dos chamados]]
- [[03 - Fluxos/Comandos-WhatsApp|Fluxo dos comandos WhatsApp]]
- [[04 - Dados/Cadastro-clientes|Modelo do cadastro de clientes]]
- [[05 - Interfaces e Integracoes/Contratos-externos|Interfaces e integrações]]
- [[06 - Desenvolvimento/Instalacao-configuracao|Instalação e configuração]]
- [[08 - Pendencias/Lacunas-confirmacao|Limitações e pontos a confirmar]]

## Navegação

Os índices de cada área estão reunidos em [[00 - Inicio/Mapa|Mapa da documentação]]. As afirmações sobre o comportamento atual foram verificadas nos arquivos versionados; hipóteses ou detalhes externos não confirmados estão identificados como tais.

## Escopo analisado

O inventário completo do Git contém sete arquivos: quatro scripts Python, `requirements.txt`, `README.md` e `.gitignore`. Não há outros diretórios ou arquivos de teste/build versionados. O README descreve nomes de arquivos que não existem no inventário atual; essa divergência está registrada em [[08 - Pendencias/Lacunas-confirmacao|Lacunas e confirmações necessárias]].

## Fonte primária

Este vault complementa, mas não substitui, o [README.md](../../../README.md) do repositório. Para execução/configuração, consulte também [[06 - Desenvolvimento/Execucao-validacao|Execução e validação]].
