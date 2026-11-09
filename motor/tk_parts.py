# Aba de EXEMPLO: "Ticket · BioNutriLab" — ambiente compartilhado de produção, entregas e pagamentos por ticket.
NAV = '''<button id="tab-tk" role="tab" data-tab="tk"><svg viewBox="0 0 24 24"><path d="M4 7a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v2a2 2 0 0 0 0 4v2a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-2a2 2 0 0 0 0-4z"/><path d="M10 9h4M10 13h4"/></svg>Ticket BNL<span class="badge tst">teste</span></button>'''

CSS = '''
/* ---------- aba de exemplo: Ticket · BioNutriLab ---------- */
.tk-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:6px 20px;font-size:12.5px}
.tk-grid div{display:flex;justify-content:space-between;gap:12px;border-bottom:1px dashed var(--line);padding:5px 0}
.tk-link{color:var(--muted);font-size:16px}
#tk-lote,#tk-tkt{min-width:150px}
.tk-h1{margin:0}
.tk-h1 select{font:inherit;font-size:var(--fs-h1);font-weight:600;letter-spacing:-.02em;color:var(--fg);background:transparent;border:0;border-bottom:2px dashed var(--line-strong);border-radius:0;height:auto;padding:2px 34px 4px 0;cursor:pointer;max-width:100%;appearance:none;-webkit-appearance:none;
  background-image:linear-gradient(45deg,transparent 50%,currentColor 50%),linear-gradient(135deg,currentColor 50%,transparent 50%);background-position:calc(100% - 14px) 55%,calc(100% - 8px) 55%;background-size:6px 6px,6px 6px;background-repeat:no-repeat}
.tk-h1 select:hover{border-bottom-color:var(--accent)}
.tk-h1 select:focus-visible{outline:none;border-bottom-color:var(--accent);box-shadow:0 3px 0 -1px color-mix(in srgb,var(--accent) 35%,transparent)}
.tk-h1 option,.tk-h1 optgroup{font-size:14px;font-weight:400;color:var(--fg);background:var(--surface)}
.tk-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
@media (max-width:520px){.tk-h1 select{font-size:19px}}
.tk-grid span{color:var(--muted)}.tk-grid b{text-align:right}
.tk-grid div.empty{display:block;text-align:center;border:1px dashed var(--line-strong);padding:18px}
.tk-rule{border:1px solid color-mix(in srgb,var(--accent) 30%,transparent);background:var(--accent-soft);border-radius:var(--r);padding:12px 14px;font-size:13px;display:grid;gap:4px}
.tk-rule b{color:var(--fg)}
.tk-steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:6px}
.tk-steps div{border:1px solid var(--line);border-radius:8px;padding:8px 10px;background:var(--surface-2);font-size:12px;display:grid;gap:2px;position:relative}
.tk-steps div.ok{border-color:color-mix(in srgb,var(--good) 45%,transparent)}
.tk-steps div.now{border-color:var(--accent);box-shadow:0 0 0 2px color-mix(in srgb,var(--accent) 25%,transparent)}
.tk-steps span{font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:600}
.tk-steps b{font-family:var(--mono);font-size:12.5px;font-weight:500}
.tk-wk{border:1px solid var(--line);border-radius:var(--r);background:var(--surface);overflow:hidden}
.tk-wk>summary{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;padding:10px 12px;border-radius:0}
.tk-wk>summary .t{font-weight:600}
.tk-wk>summary .s{margin-left:auto;display:flex;gap:6px;flex-wrap:wrap}
.tk-wk[open]>summary{border-bottom:1px solid var(--line)}
.tk-wk .tbl{border:0;border-radius:0}
.tk-wk td.neg{color:var(--crit)}.tk-wk td.pos{color:var(--good)}
.tk-tree{display:grid;gap:8px}
.tk-tree .fd{border:1px solid var(--line);border-radius:var(--r);background:var(--surface-2);padding:10px 12px;display:grid;gap:6px}
.tk-tree .fd>b{display:flex;align-items:center;gap:8px;font-size:13px}
.tk-tree .fd>b::before{content:"";width:14px;height:11px;border-radius:2px;background:var(--warn);opacity:.75;flex:none}
.tk-tree ul{margin:0;padding-left:22px;display:grid;gap:4px;font-size:12.5px}
.tk-tree li{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}
'''

HTML = '''
  <div class="page-h" data-tab="tk">
    <div><div class="eyebrow" id="tk-eyebrow">Ambiente compartilhado SOMA × BioNutriLab</div><h1 id="tk-title">Ticket</h1><p>Uma visão por ticket: acordo comercial, programação semanal de produção, conferência, entregas, pagamentos e documentos. Quantidades e datas vêm do <b>controle de lote</b> (todas as linhas com o mesmo nº de ticket = 1 ticket); comprovantes vêm da pasta do ticket no Drive.</p></div>
    <span class="pill" id="tk-pill"></span>
  </div>
  <div class="bar" data-tab="tk" role="group" aria-label="Selecionar lote ou ticket">
    <label class="chk">Lote <select id="tk-lote"></select></label>
    <span class="tk-link" aria-hidden="true">⇄</span>
    <label class="chk">Ticket <select id="tk-tkt"></select></label>
    <span class="note" id="tk-src"></span>
  </div>

  <div class="alerts" id="tk-alerts" data-tab="tk"></div>
  <div class="kpis five" id="tk-kpis" data-tab="tk"></div>

  <section class="card" data-tab="tk">
    <div class="sec-h"><h2>Linha do tempo do ticket</h2><p>Do orçamento ao pagamento final.</p></div>
    <div class="tk-steps" id="tk-steps"></div>
  </section>

  <section class="card" data-tab="tk">
    <div class="sec-h"><h2>1 · Acordo comercial</h2><p>Copiado do orçamento da BioNutriLab e da ordem de compra. É a única base para valores, quantidades e forma de pagamento.</p></div>
    <div class="tk-grid" id="tk-acordo"></div>
    <div class="tbl"><table id="tk-itens"></table></div>
    <div class="tk-rule" id="tk-regras"></div>
  </section>

  <section class="card" data-tab="tk">
    <div class="sec-h"><h2>2 · Programação semanal de produção</h2><p>Nós enviamos a proposta (programado); a BioNutriLab devolve no fim da semana com produzido real, desvio e causa. A semana só conta quando está <b>Fechada</b> (conferida pelas duas partes).</p></div>
    <div id="tk-semanas" style="display:grid;gap:10px"></div>
  </section>

  <section class="card" data-tab="tk">
    <div class="sec-h"><h2>3 · Conferência por referência</h2><p>Contratado × programado × produzido (semanas fechadas) × entregue.</p></div>
    <div class="tbl"><table id="tk-conf"></table></div>
  </section>

  <section class="card" data-tab="tk">
    <div class="sec-h"><h2>4 · Entregas</h2><p>Despachos do ticket para a Melonn, com o documento de cada entrega.</p></div>
    <div class="tbl"><table id="tk-ent" class="sheet"></table></div>
  </section>

  <section class="card" data-tab="tk">
    <div class="sec-h"><h2>5 · Pagamentos</h2><p>Cada comprovante numa linha — antecipo pode ser dividido em parcelas. Data do pagamento final calculada pela regra do acordo.</p></div>
    <div class="tbl" id="tk-pag-wrap"><table id="tk-pag"></table></div>
  </section>

  <section class="card" data-tab="tk">
    <div class="sec-h"><h2>6 · Solicitações e alterações</h2><p>Qualquer pedido fora do acordo é registrado aqui e só vale com documento assinado pelas duas partes.</p></div>
    <div class="tbl" id="tk-sol-wrap"><table id="tk-sol"></table></div>
  </section>

  <section class="card" data-tab="tk">
    <div class="sec-h"><h2>7 · Documentos do ticket (Drive)</h2><p>Uma pasta por ticket, com subpastas fixas. Link único para Grax, SOMA e BioNutriLab.</p></div>
    <div class="tk-tree" id="tk-docs"></div>
  </section>

  <section class="card" data-tab="tk">
    <details id="tk-ins-wrap"><summary>Verificação de insumos / embalagem (opcional)</summary>
      <div class="tbl" style="margin-top:8px"><table id="tk-ins"></table></div>
    </details>
    <details id="tk-all-wrap"><summary>Todos os tickets lidos do controle de lote</summary>
      <div class="note" style="margin:8px 0">Agrupado por nº de ticket (linhas com o mesmo nº = 1 ticket). Início = primeira data · fechamento = última data · pagamento final = fechamento + 30 dias.</div>
      <div class="tbl"><table id="tk-all"></table></div>
    </details>
    <details><summary>Como funciona na versão real</summary>
      <div class="howto" style="margin-top:8px">
        <div>• A versão real fica numa <b>planilha Google</b> compartilhada por e-mail (não neste painel, que é link aberto), com uma pasta no Drive por ticket.</div>
        <div>• BioNutriLab: comenta na planilha e edita só as colunas de produzido real, desvio e causa; sobe arquivos na pasta 02 · Produção.</div>
        <div>• Grax/SOMA: lança acordo, programação proposta, entregas e comprovantes.</div>
        <div>• Toda sexta: fechamento da semana → relatório semanal gerado a partir da planilha.</div>
      </div>
    </details>
  </section>
'''

JS = r'''
/* ===================== EXEMPLO · Ticket BioNutriLab ===================== */
const TK0={ticket:"234422",tkLabel:"Ticket #234422",titulo:"Ticket #234422 · OC #223492",lote:null,oc:"223492",orc:"COT-BNL-0912",fornecedor:"BioNutriLab (BELAB) · NIT 901611009",cliente:"SOMA GROUP S.A.S · NIT 902061730-1",
 emissao_orc:"2026-07-20",emissao_oc:"2026-07-27",entrega_acordada:"2026-09-25",modalidade:"Recogida en proveedor (EXW)",comprador:"Leonan",
 condicao:"50% antecipado + 50% em 30 dias após a finalização 100% da entrega",antecipo_pct:.5,prazo_saldo:30,iva:.19,
 itens:[{sku:"SOM-PRD-001",ref:"n",nome:"Soma Sculpt Naranja",qtd:25000,unit:21449},{sku:"SOM-PRD-002",ref:"p",nome:"Soma Sculpt Piña",qtd:25000,unit:21449}],
 semanas:[
  {n:1,ini:"2026-08-31",fim:"2026-09-04",status:"Fechada",conf:"2026-09-05",dias:[["Lunes","2026-08-31","n",5000,5000,"",""],["Martes","2026-09-01","n",5000,4800,"Linha de produção","Parada de 1 h para ajuste da envasadora"],["Miércoles","2026-09-02","p",5000,5000,"",""],["Jueves","2026-09-03","p",5000,5000,"",""],["Viernes","2026-09-04","n",5000,5000,"",""]]},
  {n:2,ini:"2026-09-07",fim:"2026-09-11",status:"Fechada",conf:"2026-09-12",dias:[["Lunes","2026-09-07","p",5000,5000,"",""],["Martes","2026-09-08","n",5000,5000,"",""],["Miércoles","2026-09-09","p",5000,4500,"Insumo / embalagem","Doypack chegou com atraso"],["Jueves","2026-09-10","n",5000,5000,"",""],["Viernes","2026-09-11","p",5000,5000,"",""]]},
  {n:3,ini:"2026-09-14",fim:"2026-09-18",status:"Aguardando fechamento",conf:null,dias:[["Lunes","2026-09-14","n",200,null,"",""],["Lunes","2026-09-14","p",500,null,"",""]]}],
 entregas:[{fecha:"2026-09-07",ref:"n",qtd:14800,est:"ok",doc:"Remisión 4471"},{fecha:"2026-09-07",ref:"p",qtd:10000,est:"ok",doc:"Remisión 4471"},{fecha:"2026-09-14",ref:"n",qtd:10000,est:"ok",doc:"Remisión 4502"},{fecha:"2026-09-14",ref:"p",qtd:14500,est:"ok",doc:"Remisión 4502"}],
 pagamentos:[{tipo:"Antecipo",parcela:"1/2",valor:400000000,data:"2026-07-28",comp:true},{tipo:"Antecipo",parcela:"2/2",valor:238107750,data:"2026-08-05",comp:true},{tipo:"Saldo",parcela:"1/1",valor:638107750,data:null,comp:false}],
 solicitacoes:[{data:"2026-09-15",por:"BioNutriLab",pedido:"Pagamento do saldo proporcional às entregas semanais",doc:"Nenhum",status:"Não aprovado",motivo:"Fora do acordo: orçamento e OC preveem saldo em 30 dias após a finalização 100%."},
   {data:"2026-09-10",por:"Grax",pedido:"Adiantar 500 un. de Piña para a semana 2",doc:"Programação S2 revisada",status:"Aprovado",motivo:"Ajuste de programação, sem impacto no valor."}],
 insumos:[["Doypack Naranja",25000,25000,"OK"],["Doypack Piña",25000,24500,"Faltam 500 — chegada 14/09"],["Tampa / zip",50000,50000,"OK"],["Etiqueta lote/validade",50000,50000,"OK"],["Caixa master (50 un.)",1000,1000,"OK"]]};

/* ---- leitura por ticket a partir do controle de lote ---- */
const OCS_T=__OCST__;   // ordens de compra por ticket (planilha "Ordens de compra")
const COMP0=__COMP__;   // comprovantes lidos das pastas Comprovantes de pagamento / Ticket NN
const TKDRIVE=__TKDRIVE__;
const normT=v=>{const m=String(v??"").match(/\d+/);return m?+m[0]:null};
const pad2=n=>String(n).padStart(2,"0");
function tkRows(){
  return (typeof LOTES0!=="undefined"?LOTES0:[]).map(r=>{const tc=Object.keys(r).find(k=>/ticket/i.test(k));const m=String(tc?r[tc]??"":"").match(/\d+/);
    return {tnum:m?String(+m[0]):null,lote:normT(r["Lote"]),fecha:gvDate(r["Fecha Despacho"]),ref:refOf(r["Producto"]),prod:r["Producto"]||"",qtd:+r["Cantidad"]||0,promessa:gvDate(r["Promesa de Entrega"]),est:estOC(r["Estado"]),aba:r["Aba"]||"",bodega:r["Bodega"]||"",nota:r["Nota"]||""}}).filter(r=>r.ref&&(r.tnum||r.lote!=null));
}
function tkHasCol(){return (typeof LOTES0!=="undefined"?LOTES0:[]).some(r=>Object.keys(r).some(k=>/ticket/i.test(k)))}
/* resumo de um conjunto de linhas (por ticket ou por lote) */
function tkSum(rows,by,v){
  const ds=rows.map(r=>r.fecha).filter(Boolean).sort();
  const refs=[...new Set(rows.map(r=>r.ref))].sort((a,b)=>REFS.findIndex(x=>x[0]===a)-REFS.findIndex(x=>x[0]===b));
  const ent=k=>rows.filter(r=>r.ref===k&&r.est==="ok").reduce((a,r)=>a+r.qtd,0),tr=k=>rows.filter(r=>r.ref===k&&r.est!=="ok").reduce((a,r)=>a+r.qtd,0);
  const tks=[...new Set(rows.map(r=>r.tnum).filter(Boolean))],lotes=[...new Set(rows.map(r=>r.lote).filter(x=>x!=null))].sort((a,b)=>a-b);
  const ini=ds[0]||null,fim=ds.at(-1)||null,aberto=rows.some(r=>r.est!=="ok");
  const tk1=tks.length===1?tks[0]:null;const key=by==="t"?v:(tk1||"L"+v);
  const oc=(tk1&&OCS_T[tk1])||(by==="l"&&OCS_T["L"+v])||null;
  const comps=(tk1&&COMP0[tk1])||(by==="l"&&COMP0["L"+v])||[];
  const folder=(tk1&&TKDRIVE.tickets[tk1])||(by==="l"&&TKDRIVE.tickets[String(v)])||null;
  const tkLabel=tk1?"Ticket #"+tk1:tks.length>1?"Tickets "+tks.map(x=>"#"+x).join(", "):"Lote "+lotes.join(", ");
  return {by,v,key,rows,refs,ent,tr,ini,fim,aberto,pagFinal:fim?iso(addD(pd(fim),30)):null,tks,lotes,tk1,oc,comps,folder,tkLabel,legacy:!tks.length};
}
/* seleção integrada: escolher um lote mostra o(s) ticket(s) dele e vice-versa */
let tkState={by:"ex"};try{tkState=JSON.parse(localStorage.getItem("soma-tk3"))||{by:"ex"}}catch(_){}
const tkSave=()=>{try{localStorage.setItem("soma-tk3",JSON.stringify(tkState))}catch(_){}};
function renderTK(){
  if(!$("#tk-kpis"))return;
  const R=tkRows();
  const lotes=[...new Set(R.map(r=>r.lote).filter(x=>x!=null))].sort((a,b)=>b-a);
  const tks=[...new Set(R.map(r=>r.tnum).filter(Boolean))];
  const sumT=t=>tkSum(R.filter(r=>r.tnum===t),"t",t),sumL=l=>tkSum(R.filter(r=>r.lote===l),"l",l);
  const ST=tks.map(sumT).sort((a,b)=>(b.fim||"").localeCompare(a.fim||""));
  if(tkState.by==="t"&&!tks.includes(tkState.v))tkState={by:"ex"};
  if(tkState.by==="l"&&!lotes.includes(+tkState.v))tkState={by:"ex"};
  const ex=tkState.by==="ex";
  const cur=ex?null:tkState.by==="t"?sumT(tkState.v):sumL(+tkState.v);

  // seletores (o outro campo acompanha automaticamente)
  const op=(v,l,sel)=>`<option value="${ocEsc(v)}" ${sel?"selected":""}>${ocEsc(l)}</option>`;
  let lv,tv,lExtra="",tExtra="";
  if(ex){lv="ex";tv="ex"}
  else if(tkState.by==="l"){lv=String(tkState.v);tv=cur.tk1||(cur.tks.length>1?"_multi":"_none");if(cur.tks.length>1)tExtra=op("_multi",`vários (${cur.tks.map(x=>"#"+x).join(", ")})`,true);}
  else{tv=tkState.v;lv=cur.lotes.length===1?String(cur.lotes[0]):(cur.lotes.length>1?"_multi":"_none");if(cur.lotes.length>1)lExtra=op("_multi",`vários (${cur.lotes.join(", ")})`,true);}
  $("#tk-lote").innerHTML=op("_none","— sem lote —",lv==="_none")+lExtra+op("ex","Lote 9 (modelo)",lv==="ex")+lotes.map(l=>op(String(l),"Lote "+l,lv===String(l))).join("");
  $("#tk-tkt").innerHTML=op("_none","— sem ticket —",tv==="_none")+tExtra+op("ex","#234422 (modelo)",tv==="ex")+ST.map(t=>op(t.v,"#"+t.v+(t.oc?" · OC #"+t.oc.numero:""),tv===t.v)).join("");
  $("#tk-lote").onchange=e=>{const v=e.target.value;if(v==="_none"||v==="_multi")return renderTK();tkState=v==="ex"?{by:"ex"}:{by:"l",v:+v};tkSave();renderTK()};
  $("#tk-tkt").onchange=e=>{const v=e.target.value;if(v==="_none"||v==="_multi")return renderTK();tkState=v==="ex"?{by:"ex"}:{by:"t",v};tkSave();renderTK()};

  // tabela integrada no fim: tickets e lotes antigos
  const linhas=ST.concat(lotes.filter(l=>!R.some(r=>r.lote===l&&r.tnum)).map(sumL));
  $("#tk-all").innerHTML=`<tr><th>Ticket</th><th>Lote(s)</th><th>Linhas</th><th>Piña</th><th>Naranja</th><th>Frutos Rojos</th><th>Em trânsito</th><th>Início</th><th>Fechamento</th><th>Pagamento final</th><th>Comprovantes</th><th></th></tr>`+
    linhas.map(t=>`<tr><td><b>${t.tks.length?t.tks.map(x=>"#"+x).join(", "):"—"}</b></td><td>${t.lotes.length?t.lotes.map(l=>"Lote "+l).join(", "):"—"}</td><td class="num">${t.rows.length}</td>${["p","n","f"].map(k=>`<td class="num">${t.ent(k)?fmt(t.ent(k)):"—"}</td>`).join("")}<td class="num">${["p","n","f","s"].reduce((a,k)=>a+t.tr(k),0)?fmt(["p","n","f","s"].reduce((a,k)=>a+t.tr(k),0)):"—"}</td><td class="num">${t.ini?dm(t.ini):"—"}</td><td class="num">${t.fim?dm(t.fim):"—"}${t.aberto?'<br><span class="note">provisório</span>':""}</td><td class="num">${t.pagFinal?dfull(t.pagFinal):"—"}</td><td>${t.comps.length?`<span class="pill good">${t.comps.length}</span>`:'<span class="note">—</span>'}</td><td><button class="oc-btn" type="button" data-by="${t.by}" data-v="${ocEsc(t.v)}">Abrir</button></td></tr>`).join("")+
    `<tr><td colspan="12" class="note" style="white-space:normal">${tkHasCol()?"Lote e ticket vêm das colunas Lote e Ticket do controle de lote; linhas com o mesmo nº de ticket = 1 ticket.":"O controle de lote ainda não tem a coluna Ticket — por enquanto só aparecem os lotes. Quando a coluna existir, os tickets entram aqui ligados aos seus lotes."}</td></tr>`;
  $("#tk-all").querySelectorAll("button[data-by]").forEach(b=>b.onclick=()=>{tkState={by:b.dataset.by,v:b.dataset.by==="l"?+b.dataset.v:b.dataset.v};tkSave();renderTK();$("#tk-title").scrollIntoView({block:"start",behavior:"smooth"})});

  $("#tk-pill").className="pill "+(ex?"warn":"good");$("#tk-pill").textContent=ex?"Exemplo com dados fictícios":"Dados reais · controle de lote";
  $("#tk-eyebrow").textContent=ex?"Exemplo · ambiente compartilhado SOMA × BioNutriLab":"Ambiente compartilhado SOMA × BioNutriLab";
  $("#tk-src").textContent=ex?"Modelo para validar — dados fictícios.":`Fonte: controle de lote (${META.lotes_at||META.atualizado})`;
  if(ex){renderTKView(TK0,true);$("#tk-title").textContent="Ticket #234422 · Lote 9 · OC #223492"}
  else{const T=tkFromSummary(cur);renderTKView(T,false);
    $("#tk-title").textContent=[cur.tks.length?cur.tks.map(x=>"Ticket #"+x).join(" + "):null,cur.lotes.length?"Lote "+cur.lotes.join(", "):null,cur.oc?"OC #"+cur.oc.numero:null].filter(Boolean).join(" · ")}
}
/* converte o resumo real no mesmo formato do exemplo */
function tkFromSummary(t){
  const o=t.oc;const N={p:"Soma Sculpt Piña",n:"Soma Sculpt Naranja",f:"Soma Sculpt Frutos Rojos",s:"Shaker Termo"};
  const itens=o?o.itens:t.refs.map(k=>({sku:"",ref:k,nome:N[k],qtd:null,unit:null}));
  return {real:true,ticket:t.tk1||t.tkLabel,tkLabel:t.tkLabel,legacy:t.legacy,lote:t.lotes.join(", "),oc:o?o.numero:null,orc:o?o.orc:null,fornecedor:o?o.fornecedor:"BioNutriLab",cliente:"SOMA GROUP S.A.S",
    emissao_orc:o?o.emissao_orc:null,emissao_oc:o?o.emissao:null,entrega_acordada:o?o.entrega_acordada:null,modalidade:o?o.modalidade:null,comprador:o?o.comprador:null,
    condicao:o?o.condicao:null,antecipo_pct:o?o.antecipo_pct??.5:.5,prazo_saldo:30,iva:o?o.iva??.19:.19,itens:itens.map(i=>({...i,nome:i.nome||N[i.ref]})),
    semanas:[],entregas:t.rows.map(r=>({fecha:r.fecha,ref:r.ref,qtd:r.qtd,est:r.est,doc:[r.aba,r.bodega,r.nota].filter(Boolean).join(" · ")||"—"})),
    pagamentos:t.comps.map(c=>({tipo:c.tipo||"Comprovante",parcela:c.parcela||"—",valor:c.valor||0,data:c.data||null,comp:true,link:c.link,arquivo:c.arquivo})),
    solicitacoes:[],insumos:[],ini:t.ini,fim:t.fim,aberto:t.aberto,pagFinal:t.pagFinal,folder:t.folder||TKDRIVE.comprovantes};
}
function renderTKView(T,isEx){
  const N={p:"Piña",n:"Naranja",f:"Frutos Rojos",s:"Shaker"};const hasOC=T.itens.some(i=>i.qtd);
  const bruto=hasOC?T.itens.reduce((a,i)=>a+(i.qtd||0)*(i.unit||0),0):0,total=bruto*(1+T.iva),ant=total*T.antecipo_pct,saldo=total-ant;
  const con=hasOC?T.itens.reduce((a,i)=>a+(i.qtd||0),0):null;
  const prodRef=(k,onlyClosed)=>T.semanas.filter(w=>!onlyClosed||w.status==="Fechada").reduce((a,w)=>a+w.dias.filter(d=>d[2]===k).reduce((x,d)=>x+(+d[4]||0),0),0);
  const progRef=k=>T.semanas.reduce((a,w)=>a+w.dias.filter(d=>d[2]===k).reduce((x,d)=>x+d[3],0),0);
  const pendRef=k=>T.semanas.filter(w=>w.status!=="Fechada").reduce((a,w)=>a+w.dias.filter(d=>d[2]===k).reduce((x,d)=>x+d[3],0),0);
  const entRef=k=>T.entregas.filter(e=>e.ref===k&&e.est==="ok").reduce((a,e)=>a+e.qtd,0);
  const trRef=k=>T.entregas.filter(e=>e.ref===k&&e.est!=="ok").reduce((a,e)=>a+e.qtd,0);
  const ent=T.itens.reduce((a,i)=>a+entRef(i.ref),0),trn=T.itens.reduce((a,i)=>a+trRef(i.ref),0);
  const hasProd=T.semanas.length>0;const prodC=T.itens.reduce((a,i)=>a+prodRef(i.ref,true),0);
  // datas: exemplo usa semanas; real usa primeira/última data do controle de lote
  let ini,fim,vence,done;
  if(T.real){ini=T.ini;fim=T.fim;vence=T.pagFinal;done=!T.aberto&&(!hasOC||T.itens.every(i=>entRef(i.ref)>=(i.qtd||0)))}
  else{done=T.itens.every(i=>prodRef(i.ref,true)>=i.qtd)&&T.semanas.every(w=>w.status==="Fechada");ini=T.entregas.map(e=>e.fecha).sort()[0];const lc=T.semanas.map(w=>w.conf).filter(Boolean).sort().at(-1);fim=done?lc:null;vence=fim?iso(addD(pd(fim),T.prazo_saldo)):null}
  const pAnt=T.pagamentos.filter(p=>/antecip/i.test(p.tipo)&&p.data).reduce((a,p)=>a+p.valor,0);const pSal=T.pagamentos.filter(p=>/saldo/i.test(p.tipo)&&p.data).reduce((a,p)=>a+p.valor,0);
  const pTot=T.pagamentos.filter(p=>p.data||T.real).reduce((a,p)=>a+(p.valor||0),0);
  
  const empty=(sel,msg)=>{$(sel).innerHTML=`<div class="empty">${msg}</div>`};

  // alertas
  const al=[];
  if(T.real){
    if(!hasOC)al.push(["warn",`Sem OC deste ticket na planilha de ordens de compra — contratado, valores e forma de pagamento aparecem quando ela for lançada.`]);
    if(T.aberto)al.push(["warn",`${fmt(trn)} un. ainda em trânsito/pendentes — fechamento e pagamento final são provisórios até a última entrega.`]);
    if(!T.pagamentos.length)al.push(["warn",`Nenhum comprovante na pasta <a href="${T.folder}" target="_blank" rel="noopener">Comprovantes de pagamento / ${T.tkLabel}</a>.`]);
    if(hasOC)T.itens.filter(i=>i.qtd&&entRef(i.ref)>i.qtd).forEach(i=>al.push(["warn",`${N[i.ref]}: entregue ${fmt(entRef(i.ref)-i.qtd)} acima do contratado.`]));
  }else{
    const pend=T.semanas.find(w=>w.status!=="Fechada");
    if(pend)al.push(["warn",`Semana ${pend.n} (${dm(pend.ini)}–${dm(pend.fim)}) aguardando a BioNutriLab devolver a programação com o produzido real. Sem o fechamento dela o ticket não finaliza.`]);
    if(!done)al.push(["warn",`Saldo de ${cop(saldo)} travado: a data de pagamento final só existe depois da finalização 100% + ${T.prazo_saldo} dias.`]);
    T.solicitacoes.filter(s=>/não aprov/i.test(s.status)).forEach(s=>al.push(["crit",`Solicitação fora do acordo registrada em ${dm(s.data)} (${ocEsc(s.por)}): “${ocEsc(s.pedido)}” — não aprovada, sem documento.`]));
  }
  $("#tk-alerts").innerHTML=al.map(([c,t])=>`<div class="alert ${c}" role="status"><span class="dot"></span><span>${c==="crit"?"Atenção: ":"Aviso: "}${t}</span></div>`).join("");

  // KPIs
  const K=T.real?[
    ["Entregue",fmt(ent)+" un.",T.itens.map(i=>`${N[i.ref]} ${fmt(entRef(i.ref))}`).join(" · ")],
    ["Em trânsito / pendente",trn?fmt(trn)+" un.":"—",trn?T.itens.filter(i=>trRef(i.ref)).map(i=>`${N[i.ref]} ${fmt(trRef(i.ref))}`).join(" · "):"nada pendente"],
    ["Início",ini?dfull(ini):"—","primeira data do ticket"],
    ["Fechamento",fim?dfull(fim):"—",T.aberto?"provisório · última data até agora":"última data do ticket"],
    ["Pagamento final",vence?dfull(vence):"—",`fechamento + 30 dias${T.aberto?" · provisório":""}${hasOC?" · saldo "+cop(saldo-pSal):""}`]]
   :[["Contratado",fmt(con)+" un.",T.itens.map(i=>`${N[i.ref]} ${fmt(i.qtd)}`).join(" · ")],
    ["Produzido (semanas fechadas)",fmt(prodC)+" un.",`${f1(prodC/con*100)}% · ${fmt(con-prodC)} em conferência/faltante`],
    ["Entregue",fmt(ent)+" un.",`${f1(ent/con*100)}% do contratado`],
    ["Pago",cop(pAnt+pSal),`${f1((pAnt+pSal)/total*100)}% de ${cop(total)}`],
    ["Pagamento final",vence?dfull(vence):"após finalização",vence?`saldo ${cop(saldo)}`:`${cop(saldo)} · 30 d após 100%`]];
  $("#tk-kpis").innerHTML=K.map(([a,b,c])=>`<div class="kpi"><div class="eyebrow">${a}</div><div class="v">${b}</div><div class="s">${c}</div></div>`).join("");

  // linha do tempo
  const st=T.real?[["Ordem de compra",T.emissao_oc?dfull(T.emissao_oc):"sem OC",T.emissao_oc?"ok":""],["Antecipo",pAnt?cop(pAnt):"sem comprovante",pAnt?"ok":""],["Início entregas",ini?dfull(ini):"—",ini?"ok":""],["Fechamento",fim?dfull(fim)+(T.aberto?" (prov.)":""):"—",T.aberto?"now":"ok"],["Pagamento final",vence?dfull(vence):"—",pSal?"ok":""]]
   :[["Orçamento BNL",dfull(T.emissao_orc),"ok"],["Ordem de compra",dfull(T.emissao_oc),"ok"],["Antecipo 50%",pAnt>=ant?"pago "+dm(T.pagamentos.filter(p=>/antecip/i.test(p.tipo)).map(p=>p.data).sort().at(-1)):"pendente",pAnt>=ant?"ok":"now"]]
    .concat(T.semanas.map(w=>[`Produção S${w.n}`,w.status==="Fechada"?"fechada "+dm(w.conf):w.status.toLowerCase(),w.status==="Fechada"?"ok":"now"]))
    .concat([["Finalização 100%",fim?dfull(fim):"pendente",fim?"ok":""],["Saldo 50%",pSal?"pago":vence?"vence "+dm(vence):"travado",pSal?"ok":""]]);
  $("#tk-steps").innerHTML=st.map(([a,b,c])=>`<div class="${c}"><span>${a}</span><b>${b}</b></div>`).join("");

  // 1 · acordo
  if(hasOC){
    $("#tk-acordo").innerHTML=[["Ticket",T.tkLabel+(T.lote&&!T.legacy?" · lote "+T.lote:"")],["Orçamento BNL",(T.orc||"—")+(T.emissao_orc?" · "+dfull(T.emissao_orc):"")],["Ordem de compra","#"+T.oc+" · "+dfull(T.emissao_oc)],["Fornecedor",T.fornecedor],["Faturar a",T.cliente],["Entrega acordada",dfull(T.entrega_acordada)],["Modalidade",T.modalidade||"—"],["Comprador",T.comprador||"—"],["Condição de pagamento",T.condicao||"—"]].map(([a,b])=>`<div><span>${a}</span><b>${ocEsc(b)}</b></div>`).join("");
    $("#tk-itens").innerHTML=`<tr><th>SKU</th><th>Referência</th><th>Quantidade</th><th>Valor unitário</th><th>Subtotal (sem IVA)</th></tr>`+T.itens.map(i=>`<tr><td class="num">${ocEsc(i.sku)}</td><td><span class="sw ${i.ref}"></span>${i.nome}</td><td class="num">${fmt(i.qtd)}</td><td class="num">${fmt(i.unit)}</td><td class="num">${fmt(i.qtd*i.unit)}</td></tr>`).join("")+
      `<tr class="tot"><td>Total</td><td></td><td class="num">${fmt(con)}</td><td></td><td class="num">${fmt(bruto)}</td></tr><tr><td colspan="4">IVA ${Math.round(T.iva*100)}%</td><td class="num">${fmt(bruto*T.iva)}</td></tr><tr class="tot"><td colspan="4">Total geral (COP)</td><td class="num">${fmt(total)}</td></tr>`;
    $("#tk-regras").innerHTML=`<b>Regras deste ticket (do documento)</b><div>• Antecipo: ${cop(ant)} (${Math.round(T.antecipo_pct*100)}%) — pode ser pago em parcelas, cada uma com comprovante.</div><div>• Saldo: ${cop(saldo)}, vence 30 dias após o fechamento do ticket.</div><div>• Mudanças de valor, quantidade ou forma de pagamento só com documento aditivo assinado (aba 6).</div>`;$("#tk-regras").hidden=false;$("#tk-itens").parentElement.hidden=false;
  }else{$("#tk-acordo").innerHTML=`<div class="empty" style="grid-column:1/-1">Aguardando a OC deste ticket na planilha <b>Ordens de compra</b> (Drive · Painel SOMA — HTML / Ordens de compra).</div>`;$("#tk-itens").innerHTML="";$("#tk-itens").parentElement.hidden=true;$("#tk-regras").hidden=true}

  // 2 · programação semanal
  if(!hasProd)empty("#tk-semanas","Programação semanal ainda não lançada para este ticket.");
  else{const CAUSA=c=>c?`<span class="pill warn">${ocEsc(c)}</span>`:"—";
  $("#tk-semanas").innerHTML=T.semanas.map((w,i)=>{const tp=w.dias.reduce((a,d)=>a+d[3],0),tr=w.dias.reduce((a,d)=>a+(+d[4]||0),0),fechada=w.status==="Fechada";
    return `<details class="tk-wk" ${i===T.semanas.length-1||!fechada?"open":""}><summary><span class="t">Semana ${w.n} · ${dm(w.ini)} → ${dm(w.fim)}</span><span class="note">programado ${fmt(tp)} · real ${fechada?fmt(tr):"—"}</span>
      <span class="s"><span class="pill">📄 proposta enviada</span>${fechada?`<span class="pill">📄 devolvida BNL</span><span class="pill good">Fechada ${dm(w.conf)}</span>`:`<span class="pill warn">${w.status}</span>`}</span></summary>
      <div class="tbl"><table><tr><th>Día</th><th>Fecha</th><th>SKU</th><th>Programado</th><th>Producido real</th><th>Desvío</th><th>Causa del desvío</th><th>Observación</th></tr>${w.dias.map(d=>{const dv=d[4]==null?null:d[4]-d[3];return `<tr><td>${d[0]}</td><td class="num">${dm(d[1])}</td><td><span class="sw ${d[2]}"></span>${N[d[2]]}</td><td class="num">${fmt(d[3])}</td><td class="num">${d[4]==null?'<span class="note">aguardando BNL</span>':fmt(d[4])}</td><td class="num ${dv<0?"neg":dv>0?"pos":""}">${dv==null?"—":dv===0?"0":(dv>0?"+":"")+fmt(dv)}</td><td>${CAUSA(d[5])}</td><td class="note">${ocEsc(d[6])||"—"}</td></tr>`}).join("")}
      <tr class="tot"><td colspan="3">Total da semana</td><td class="num">${fmt(tp)}</td><td class="num">${fechada?fmt(tr):"—"}</td><td class="num">${fechada?(tr-tp===0?"0":fmt(tr-tp)):"—"}</td><td colspan="2"></td></tr></table></div></details>`}).join("")}

  // 3 · conferência
  $("#tk-conf").innerHTML=`<tr><th>Referência</th><th>Contratado</th>${hasProd?"<th>Programado</th><th>Produzido (fechado)</th><th>Em conferência</th>":""}<th>Entregue</th><th>Em trânsito</th><th>Faltante</th><th>% ${hasProd?"produzido":"entregue"}</th></tr>`+T.itens.map(i=>{const pc=prodRef(i.ref,true),pe=pendRef(i.ref),e=entRef(i.ref),t=trRef(i.ref);const base=hasProd?pc:e;
    return `<tr><td><span class="sw ${i.ref}"></span>${i.nome}</td><td class="num">${i.qtd?fmt(i.qtd):"—"}</td>${hasProd?`<td class="num">${fmt(progRef(i.ref))}</td><td class="num">${fmt(pc)}</td><td class="num">${pe?fmt(pe):"—"}</td>`:""}<td class="num">${fmt(e)}</td><td class="num">${t?fmt(t):"—"}</td><td class="num">${i.qtd?fmt(Math.max(0,i.qtd-base)):"—"}</td><td>${i.qtd?ocProg({con:i.qtd,ent:base,tr:hasProd?pe:t}):'<span class="note">sem OC</span>'}</td></tr>`}).join("");

  // 4 · entregas
  $("#tk-ent").innerHTML=`<tr><th>Fecha</th><th>Referência</th><th>Cantidad</th><th>Estado</th><th>${T.real?"Aba · bodega · nota":"Documento"}</th></tr>`+[...T.entregas].sort((a,b)=>(a.fecha||"").localeCompare(b.fecha||"")).map(e=>`<tr><td class="num">${dfull(e.fecha)}</td><td><span class="sw ${e.ref}"></span>${N[e.ref]}</td><td class="num">${fmt(e.qtd)}</td><td><span class="est ${e.est==="ok"?"ok":e.est==="tr"?"go":"wait"}">${e.est==="ok"?"Entregado":e.est==="tr"?"En tránsito":"Pendiente"}</span></td><td>${T.real?"":"📄 "}${ocEsc(e.doc)}</td></tr>`).join("")+`<tr class="tot"><td>Total</td><td></td><td class="num">${fmt(ent+trn)}</td><td colspan="2">${trn?fmt(trn)+" em trânsito/pendente":""}</td></tr>`;

  // 5 · pagamentos
  if(T.real&&!T.pagamentos.length)empty("#tk-pag-wrap",`Nenhum comprovante encontrado. Suba os arquivos em <a href="${T.folder}" target="_blank" rel="noopener">Comprovantes de pagamento / ${T.tkLabel}</a> — eu leio na próxima atualização.`);
  else{$("#tk-pag-wrap").innerHTML='<table id="tk-pag"></table>';
  $("#tk-pag").innerHTML=`<tr><th>Tipo</th><th>Parcela</th><th>Valor</th><th>Vencimento / regra</th><th>Data paga</th><th>Comprovante</th><th>Status</th></tr>`+T.pagamentos.map(p=>{const venc=/saldo/i.test(p.tipo)?(vence?dfull(vence):"30 d após fechamento"):"na emissão da OC";
    const stt=p.data?'<span class="pill good">Pago</span>':/saldo/i.test(p.tipo)&&!done?'<span class="pill crit">🔒 Travado</span>':'<span class="pill warn">A pagar</span>';
    return `<tr><td>${ocEsc(p.tipo)}</td><td class="num">${ocEsc(p.parcela)}</td><td class="num">${p.valor?cop(p.valor):"—"}</td><td>${venc}</td><td class="num">${p.data?dfull(p.data):"—"}</td><td>${p.link?`<a href="${ocEsc(p.link)}" target="_blank" rel="noopener">📎 ${ocEsc(p.arquivo||"abrir")}</a>`:p.comp?"📎 anexado":'<span class="note">—</span>'}</td><td>${stt}</td></tr>`}).join("")+
    `<tr class="tot"><td colspan="2">Total pago</td><td class="num">${cop(pTot)}</td><td colspan="2">${hasOC?"de "+cop(total):""}</td><td colspan="2">${hasOC?"Saldo em aberto "+cop(total-pTot):""}</td></tr>`}

  // 6 · solicitações
  if(!T.solicitacoes.length)empty("#tk-sol-wrap","Nenhuma solicitação registrada para este ticket.");
  else{$("#tk-sol-wrap").innerHTML='<table id="tk-sol"></table>';$("#tk-sol").innerHTML=`<tr><th>Data</th><th>Solicitado por</th><th>Pedido</th><th>Documento</th><th>Status</th><th>Motivo / base</th></tr>`+T.solicitacoes.map(s=>`<tr><td class="num">${dfull(s.data)}</td><td>${ocEsc(s.por)}</td><td style="white-space:normal;min-width:220px">${ocEsc(s.pedido)}</td><td>${ocEsc(s.doc)}</td><td><span class="pill ${/não/i.test(s.status)?"crit":"good"}">${ocEsc(s.status)}</span></td><td class="note" style="white-space:normal;min-width:240px">${ocEsc(s.motivo)}</td></tr>`).join("")}

  // 7 · documentos
  const folder=(t,items,link)=>`<div class="fd"><b>${t}${link?` · <a href="${link}" target="_blank" rel="noopener">abrir ↗</a>`:""}</b>${items.length?`<ul>${items.map(([n,ok,href])=>`<li><span>📄 ${href?`<a href="${ocEsc(href)}" target="_blank" rel="noopener">${ocEsc(n)}</a>`:ocEsc(n)}</span><span class="pill ${ok?"good":"warn"}">${ok?"anexado":"pendente"}</span></li>`).join("")}</ul>`:'<span class="note" style="padding-left:22px">vazia</span>'}</div>`;
  if(T.real){$("#tk-docs").innerHTML=`<div class="note">📁 Drive · <a href="${TKDRIVE.raiz}" target="_blank" rel="noopener">Painel SOMA — HTML ↗</a></div>`+
    folder(`Comprovantes de pagamento / ${T.tkLabel}`,T.pagamentos.map(p=>[p.arquivo||p.tipo,true,p.link]),T.folder)+
    folder("Ordens de compra",hasOC?[["OC #"+T.oc,true]]:[["OC do "+T.tkLabel,false]],TKDRIVE.ocs);}
  else{$("#tk-docs").innerHTML=`<div class="note">📁 SOMA × BioNutriLab — Produção e Pagamentos / <b>${T.tkLabel} · OC #${T.oc}</b> (exemplo)</div>`+
    folder("01 · Acordo comercial",[["Orçamento BioNutriLab "+T.orc,true],["Ordem de compra #"+T.oc,true],["Aditivos assinados",false]])+
    folder("02 · Produção",T.semanas.flatMap(w=>[[`Programação S${w.n} — proposta (Grax)`,true],[`Programação S${w.n} — fechada (BNL)`,w.status==="Fechada"]]))+
    folder("03 · Comprovantes de pagamento",T.pagamentos.map(p=>[`${p.tipo} ${p.parcela} — ${cop(p.valor)}`,p.comp]))+
    folder("04 · Entregas",[...new Set(T.entregas.map(e=>e.doc))].map(d=>[d,true]))}

  // insumos (só exemplo por enquanto)
  $("#tk-ins-wrap").hidden=!T.insumos.length;
  if(T.insumos.length)$("#tk-ins").innerHTML=`<tr><th>Insumo</th><th>Necessário</th><th>Disponível</th><th>Status</th></tr>`+T.insumos.map(r=>`<tr><td>${r[0]}</td><td class="num">${fmt(r[1])}</td><td class="num">${fmt(r[2])}</td><td><span class="pill ${r[3]==="OK"?"good":"warn"}">${r[3]}</span></td></tr>`).join("");
  try{tkAlign()}catch(_){}
}
function tkAlign(){document.querySelectorAll('section[data-tab="tk"] table').forEach(t=>{const rows=[...t.rows];const h=rows[0];if(!h)return;const n=h.cells.length;const d=rows.find((r,i)=>i>0&&r.cells.length===n);
  [...h.cells].forEach((th,i)=>{const num=!!(d&&d.cells[i]&&d.cells[i].classList.contains("num"));th.style.textAlign=num&&i>0?"right":"left";rows.slice(1).forEach(r=>{if(r.cells.length!==n)return;const c=r.cells[i];if(c&&!c.classList.contains("num"))c.style.textAlign="left"})})})}
try{renderTK()}catch(e){console.error(e)}
{const _rl2=renderLotes;renderLotes=function(){_rl2.apply(this,arguments);try{renderTK()}catch(e){console.error(e)}}}
'''
