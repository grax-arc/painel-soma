# Motor do painel SOMA

Gera `index.html` (oficial) e `teste.html` (teste) na raiz do repositório a partir de `template.html` e dos dados desta pasta.

## Atualização de vendas e estoque (automática a cada 5 h, ou à mão)

1. `python3 motor/atualizar.py --consultas` imprime as consultas Shopify já com as datas.
2. Rodar cada consulta no conector da Shopify (`run-analytics-query` / `graphql_query`) e copiar os números, exatamente como vieram, para `motor/entrada.json` no formato descrito no topo de `atualizar.py`.
3. `python3 motor/atualizar.py motor/entrada.json`
   - valida (dias contíguos, dias fechados que mudaram demais, SKUs e bodegas faltando, faixas normais) e só grava se tudo passar;
   - atualiza `rows.json`, `estoque.json`, `links.json`, `dist.json` (uma vez por dia) e `meta.json`;
   - regenera `index.html` e `teste.html`.
4. Se a saída terminar com `OK PARA PUBLICAR`: `git add -A && git commit && git pull --rebase && git push`.
   Se terminar com `ERRO`, não publicar: refazer a consulta indicada e tentar de novo.

## O que continua manual

- `melonn.json`: leitura do Reporte inventario da Melonn (disponible, esperada, reservada, alistada). Só muda quando chegam prints novos.
- `fechs.json`: fechamentos das faturas Melonn.
- `lotes_embed.json`, `ocs.json`, `tk_data.json`: lotes, ordens de compra e tickets (a planilha "Painel SOMA — dados" é lida ao vivo pelo painel).
- Layout: `template.html`; abas de teste: `oc_addon.py`, `tk_parts.py`, `prev_parts.py`.
