# `gerenciador_os.py` — cadastro JSON

Voltar para [[02 - Modulos/Indice|Índice de Módulos]] · Estrutura e persistência em [[04 - Dados/Cadastro-clientes|Cadastro de clientes]].

Arquivo: [`gerenciador_os.py`](../../../gerenciador_os.py).

## Operações

- `carregar_dados_json()` resolve `CAMINHO_JSON` relativamente à pasta base, carrega JSON e devolve dados ou mensagem de erro.
- `atualizar_os_cliente()` grava o número como texto na seção de contrato ou avulso, remove correspondência sem diferenciar maiúsculas/minúsculas da seção oposta e preserva a grafia existente na seção destino.
- `deletar_cliente()` procura e remove correspondências sem diferenciar maiúsculas/minúsculas nas duas seções.
- `listar_clientes()` formata ambas as categorias em uma resposta de texto.

Chamado pelo webhook para comandos de manutenção. O robô usa o mesmo arquivo para montar o contexto da geração Gemini, conforme [[02 - Modulos/robo-os|módulo principal]].

Referências: [`carregar_dados_json()`](../../../gerenciador_os.py#L14), [`atualizar_os_cliente()`](../../../gerenciador_os.py#L29), [`deletar_cliente()`](../../../gerenciador_os.py#L61) e [`listar_clientes()`](../../../gerenciador_os.py#L96).

## Observação de persistência

As operações escrevem o arquivo JSON diretamente; não foi encontrado mecanismo de transação, bloqueio entre processos ou cópia de segurança automática. O comportamento sob escrita simultânea não foi testado.
