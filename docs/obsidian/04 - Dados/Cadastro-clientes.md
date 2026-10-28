# Cadastro de clientes

Voltar para [[04 - Dados/Indice|Índice de Dados]] · Módulo de persistência em [[02 - Modulos/gerenciador-os|gerenciador_os.py]].

## Modelo persistido

O código usa um arquivo JSON local com duas categorias. Cada chave é o nome do cliente e cada valor é o número da O.S.; a listagem do robô e as operações de cadastro tratam esse valor como texto.

```json
{
  "CLIENTES_CONTRATO": {
    "<nome do cliente>": "<número da O.S.>"
  },
  "CLIENTES_AVULSOS": {
    "<nome do cliente>": "<número da O.S.>"
  }
}
```

O código usa `.get(categoria, {})` quando lê as seções. Não foi encontrada validação formal de esquema nem arquivo JSON de exemplo versionado. O cadastro é a única persistência de domínio identificada; não há banco de dados ou ORM no inventário.

## Caminho do arquivo

`robo_os.py` usa `CAMINHO_JSON`, com padrão `Clientes/clientes_os.json`; `gerenciador_os.py` usa o mesmo nome de variável, mas seu padrão é `clientes_os.json`. Ambos resolvem o caminho relativamente à pasta base dos scripts. Para que comandos e geração Gemini compartilhem o cadastro, configure o mesmo valor explicitamente.

O `.gitignore` contém `Clientes/clientes_os.json` (C maiúsculo). Em sistemas de arquivos sensíveis a maiúsculas, isso não equivale a `clientes_os.json` na raiz. Ver [[08 - Pendencias/Lacunas-confirmacao|pontos a confirmar]].

## Relacionamentos e manutenção

- Um cliente está previsto em uma das duas seções: contrato ou avulso.
- Atualizar troca o cliente de seção se necessário, comparando nomes sem diferenciar maiúsculas/minúsculas.
- Excluir pesquisa ambas as seções.
- A O.S. não é entidade separada no código: o número está armazenado diretamente como valor associado ao cliente.

Operações expostas: [[03 - Fluxos/Comandos-WhatsApp|comandos WhatsApp]].
