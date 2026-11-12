# Motor do painel SOMA

Gera `index.html` (oficial) e `teste.html` (teste) na raiz do repositório a partir de `template.html` e dos dados desta pasta. SKUs: p = Piña (SOMAPINA), n = Naranja (SOMANARANJA), s = Shaker, r = Frutos Rojos (SOMAROJO, 4 produtos na Shopify com o mesmo SKU; desde 10/11/2026).

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
- `esgotados.json`: pedidos esgotados na Melonn (arquivo sell_orders, coluna Cantidad agotada) por SKU e bodega, com o disponível da bodega antes da leitura. O `gen.py` desconta esses esgotados do disponível de cada bodega, e o desconto de uma bodega para sozinho quando o disponível dela sobe mais de 20 un. acima da base, porque a Melonn recebeu mercadoria e atendeu a fila. Troque o arquivo quando chegar um sell_orders novo.
- `lotes_embed.json`, `ocs.json`, `tk_data.json`: lotes, ordens de compra e tickets (a planilha "Painel SOMA — dados" é lida ao vivo pelo painel).
- Layout: `template.html`; abas de teste: `oc_addon.py`, `tk_parts.py`, `prev_parts.py`.
