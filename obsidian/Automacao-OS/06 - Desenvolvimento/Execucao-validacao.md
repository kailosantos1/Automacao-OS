# Execução e validação

Voltar para [[06 - Desenvolvimento/Indice|Índice de Desenvolvimento]] · Configuração em [[06 - Desenvolvimento/Instalacao-configuracao|Instalação e configuração]].

## Comandos identificados no código

Executar o processador e, junto dele, iniciar o webhook:

```bash
python robo_os.py
```

Executar apenas o utilitário de atualização de títulos:

```bash
python faxina.py
```

Esses comandos correspondem aos blocos `if __name__ == '__main__'` dos arquivos. **Não foram executados**: dependem de credenciais e serviços externos, e `faxina.py` altera eventos no Calendar. O README atual instrui `python main.py`, mas `main.py` não aparece no inventário versionado; consulte [[08 - Pendencias/Lacunas-confirmacao|divergências do README]].

## Testes, build e lint

Não há diretório ou arquivo de teste, configuração de test runner, lint, type checker ou build no inventário Git. Portanto não existe comando de testes/build confirmado para documentar. Não foram instaladas dependências nem feitas chamadas a serviços externos.

## Verificação desta documentação

Os links internos foram verificados contra os arquivos Markdown criados. O JSON de configuração do Obsidian foi validado sintaticamente. As referências de código foram conferidas contra caminhos versionados e âncoras de linha. Essa validação de documentação não equivale a teste funcional do aplicativo.
