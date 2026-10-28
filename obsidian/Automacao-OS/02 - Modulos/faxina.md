# `faxina.py` — utilitário de atualização do Calendar

Voltar para [[02 - Modulos/Indice|Índice de Módulos]] · Integração Google em [[05 - Interfaces e Integracoes/Contratos-externos|Interfaces externas]].

Arquivo: [`faxina.py`](../../../faxina.py).

## Comportamento confirmado

`limpar_passado()` carrega `token.json` do diretório de trabalho atual, cria cliente Calendar v3 e consulta o calendário `primary` entre **2025-01-01 00:00 UTC** e **2026-06-15 00:00 UTC**. Para eventos cujo título não contenha a sequência exata `[ENVIADO]` (comparação sensível a maiúsculas/minúsculas), prefixa `[ENVIADO]` e atualiza o evento. O limite está codificado no script, não configurado pelo `.env`.

O script é independente de `robo_os.py` e só é executado ao invocar diretamente o arquivo (`if __name__ == '__main__'`). Alterar títulos do calendário é uma ação persistente; revise o intervalo e os eventos antes de usar em outro contexto.

Referência: [`limpar_passado()`](../../../faxina.py#L5).
