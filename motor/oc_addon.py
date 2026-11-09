# Página de TESTE: duplica o Controle de lotes como aba "Lotes · OC" com ordens de compra,
# conferência contratado × entregue, sinalizador de pagamento, anexos e relatório semanal.
# Uso: python3 motor/oc_addon.py  -> gera teste.html e index.html (raiz do repositório) a partir de motor/_build/painel_ruptura_soma.html
import json, re, sys, os
BASE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(BASE); BUILD = os.path.join(BASE, "_build")
sys.path.insert(0, BASE)
import tk_parts

SRC = os.path.join(BUILD, "painel_ruptura_soma.html")
OUT = os.path.join(REPO, "teste.html")
OCS = json.load(open(os.path.join(BASE, "ocs.json"), encoding="utf-8"))

NAV = '''<button id="tab-oc" role="tab" data-tab="oc"><svg viewBox="0 0 24 24"><path d="M9 4h6v3H9z"/><path d="M15 5h3v16H6V5h3"/><path d="M9 13l2 2 4-4"/></svg>Lotes · OC<span class="badge tst">teste</span></button>'''

CSS = '''
/* ---------- aba de teste: Lotes · OC ---------- */
:root{--frutos:#c0265e}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--frutos:#f06292}}
:root[data-theme="dark"]{--frutos:#f06292}
.sw.f{background:var(--frutos)}
.tabs .badge.tst{background:var(--accent-soft);color:var(--accent)}
.oc-flags{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.oc-lot{display:grid;gap:6px;justify-items:start}
.oc-lot .nm{font-weight:600;display:flex;align-items:center;gap:6px}
.oc-btn{font:inherit;font-size:12px;font-weight:500;height:26px;padding:0 10px;border-radius:999px;border:1px solid var(--line-strong);background:var(--surface);color:var(--fg-2);cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.oc-btn:hover{background:var(--soft);color:var(--fg)}
.oc-btn[aria-expanded="true"]{background:var(--accent);border-color:var(--accent);color:var(--accent-fg)}
.oc-btn::after{content:"";width:6px;height:6px;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:rotate(45deg) translateY(-2px)}
.oc-btn[aria-expanded="true"]::after{transform:rotate(-135deg) translateY(-1px)}
.prog{display:grid;grid-template-columns:minmax(70px,1fr) 50px;gap:8px;align-items:center;min-width:130px}
.prog .b{height:8px;border-radius:999px;background:var(--soft);overflow:hidden;display:flex}
.prog .b i{display:block;height:100%}
.prog .b i.ok{background:var(--good)}.prog .b i.go{background:var(--accent)}.prog .b i.tr{background:color-mix(in srgb,var(--accent) 35%,transparent)}.prog .b i.ov{background:var(--warn)}
.prog span{font-family:var(--mono);font-size:12px;text-align:right}
tr.oc-det>td{background:var(--surface-2);padding:14px 16px;white-space:normal}
tr.oc-det:hover>td{background:var(--surface-2)}
.oc-panel{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(220px,1fr);gap:16px}
.oc-panel .blk{border:1px solid var(--line);border-radius:var(--r);background:var(--surface);padding:12px 14px;display:grid;gap:10px;align-content:start;min-width:0}
.oc-panel .blk h3{margin:0;font-size:13px;font-weight:600}
.oc-panel table th,.oc-panel table td{padding:6px 7px;font-size:12px}
.oc-panel .prog{min-width:104px;grid-template-columns:minmax(50px,1fr) 46px}
.ring{--p:0;--c:var(--accent);width:118px;height:118px;border-radius:50%;background:conic-gradient(var(--c) calc(var(--p)*1%),var(--soft) 0);display:grid;place-items:center;margin:auto}
.ring>div{width:88px;height:88px;border-radius:50%;background:var(--surface);display:grid;place-items:center;text-align:center;line-height:1.1}
.ring b{font-family:var(--mono);font-size:20px}.ring small{font-size:10.5px;color:var(--muted)}
.tl{display:grid;grid-template-columns:repeat(auto-fit,minmax(118px,1fr));gap:8px}
.tl div{border:1px solid var(--line);border-radius:8px;padding:8px 10px;background:var(--surface-2);min-width:0}
.tl span{display:block;font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:600}
.tl b{font-family:var(--mono);font-size:13px;font-weight:500}
.fin{display:grid;grid-template-columns:1fr auto;gap:6px 12px;font-size:12.5px;align-items:center}
.fin>span:nth-child(odd){color:var(--muted)}
.fin>span:nth-child(even){font-family:var(--mono);text-align:right}
.docs{display:flex;flex-wrap:wrap;gap:6px}
.tag-ex{display:inline-flex;align-items:center;padding:1px 7px;border-radius:999px;font-size:10.5px;font-weight:700;letter-spacing:.06em;background:var(--warnbg);color:var(--warn);border:1px dashed color-mix(in srgb,var(--warn) 55%,transparent)}
.rep-out{font-family:var(--mono);font-size:12.5px;white-space:pre-wrap;background:var(--surface-2);border:1px solid var(--line);border-radius:var(--r);padding:14px 16px;margin:0;max-height:520px;overflow:auto;line-height:1.55}
.ocfields{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:6px 18px;font-size:12.5px}
.ocfields div{display:flex;justify-content:space-between;gap:10px;border-bottom:1px dashed var(--line);padding:4px 0}
.ocfields span{color:var(--muted)}
@media (max-width:760px){.oc-panel{grid-template-columns:1fr;position:sticky;left:0;width:calc(100vw - 86px)}tr.oc-det>td{padding:10px}}
#oc-lotes td{vertical-align:top}#oc-lotes td.num{padding-top:12px}
'''

HTML = '''
  <div class="page-h" data-tab="oc">
    <div><div class="eyebrow">Compras · ordem de compra por lote · versão de teste</div><h1>Lotes e ordens de compra</h1><p>Cada lote = uma OC (ticket do time de compras). Conferência entregue × contratado por referência; o saldo de 50% só é liberado com o lote 100% entregue e vence 30 dias depois da finalização.</p></div>
    <span class="pill warn">Página de teste · não altera o painel oficial</span>
  </div>
  <div class="alerts" id="oc-alerts" data-tab="oc"></div>
  <div class="kpis five" id="oc-kpis" data-tab="oc"></div>

  <section class="card" data-tab="oc">
    <div class="sec-h">
      <h2>Total por lote · conferência com a OC</h2>
      <div class="oc-flags">
        <label class="chk"><input type="checkbox" id="oc-ex"> Mostrar OC de exemplo (#223492)</label>
        <label class="chk"><input type="checkbox" id="oc-sim"> Simular conclusão do exemplo</label>
      </div>
      <p>Use o botão abaixo de cada lote para ver contratado × entregue × faltante por referência, datas, pagamentos e documentos. Lotes 1–8 são anteriores ao controle por OC: mostram só o entregue.</p>
    </div>
    <div class="tbl"><table id="oc-lotes"></table></div>
    <div class="note">Entregue = despachos com estado <b>Entregado</b>; em trânsito aparece à parte (barra clara). Início da entrega = primeiro despacho do lote; finalização = despacho que completa 100% de todas as referências. Entrega acima do contratado gera alerta de divergência, sem bloquear o 100%.</div>
  </section>

  <section class="card" data-tab="oc">
    <div class="sec-h"><h2>Progresso das ordens de compra (%)</h2><p>Entregue ÷ contratado por referência, por OC.</p></div>
    <div class="chart" style="height:220px"><canvas id="cOC"></canvas></div>
    <div class="note" id="oc-chart-note"></div>
  </section>

  <section class="card" data-tab="oc">
    <div class="sec-h"><h2>Despachos por ticket</h2><p>Mesmas linhas do Controle de lotes (todas as abas: produção total), com ticket/OC e Frutos Rojos.</p></div>
    <div class="tbl"><table id="oc-desp" class="sheet"></table></div>
  </section>

  <section class="card" data-tab="oc">
    <div class="sec-h"><h2>Relatório da semana</h2><p>Formato WhatsApp · copie e cole.</p></div>
    <div class="bar">
      <label class="chk">Semana <select id="oc-wk"></select></label>
      <label class="chk"><input type="checkbox" id="oc-wk-ex"> incluir OC de exemplo</label>
      <button class="btn ghost" id="oc-copy" type="button">Copiar relatório</button>
      <span class="note" id="oc-copy-st"></span>
    </div>
    <pre class="rep-out" id="oc-rep"></pre>
  </section>

  <section class="card" data-tab="oc">
    <details><summary>Como lançar uma OC nova</summary>
      <div class="howto" style="margin-top:8px">
        <div>1. Envie no chat o PDF da OC (formato Grax Digital): número, emissão, itens por SKU com quantidade e valor unitário, IVA, data de entrega acordada e condição de pagamento. O lote recebe o número da OC como ticket.</div>
        <div>2. Os despachos continuam vindo da planilha de controle de despacho (print ou arquivo no chat), com o número do lote.</div>
        <div>3. PDF da OC e comprovantes de pagamento vão para a pasta do lote no Drive: <a id="oc-drive" href="#" target="_blank" rel="noopener">Painel SOMA — Lotes (ordens de compra e comprovantes) ↗</a>. Avise no chat quando subir um comprovante (antecipo ou saldo) para marcar como pago.</div>
        <div>4. Regras: saldo de 50% só libera quando todas as referências do lote chegam a 100%; vence 30 dias depois da finalização. Se uma OC nova começa e a anterior não está 100%, o painel sinaliza o pagamento travado.</div>
      </div>
    </details>
  </section>
'''

JS = r'''
/* ===================== TESTE · Lotes · OC ===================== */
const OCS0=__OCS__;
const OCDRIVE="https://drive.google.com/drive/folders/1TtIACsKnXLv3WbfxFI-Hpez4rDkzMRua";
const REFS=[["p","Piña","pina"],["n","Naranja","naranja"],["f","Frutos Rojos","frutos"],["s","Shaker","shaker"]];
const REFNOME={p:"Soma Sculpt Piña",n:"Soma Sculpt Naranja",f:"Soma Sculpt Frutos Rojos",s:"Shaker Termo"};
const ocEsc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const cop=v=>"COP "+fmt(v||0);
const refOf=n=>{const k=String(n||"").toLowerCase();return /frutos|rojo|berry/.test(k)?"f":/pi[ñn]a/.test(k)?"p":/naranja|laranja/.test(k)?"n":/shaker/.test(k)?"s":null};
const estOC=e=>{const k=String(e||"").toLowerCase();return /tr[aá]nsito/.test(k)?"tr":/pendiente|produzid/.test(k)?"pd":"ok"};
const dfull=s=>s?dm(s)+"/"+s.slice(0,4):"—";
let ocStore={};try{ocStore=JSON.parse(localStorage.getItem("soma-oc-teste")||"{}")}catch(_){}
if(ocStore.ex===undefined)ocStore.ex=true;
const ocSave=()=>{try{localStorage.setItem("soma-oc-teste",JSON.stringify(ocStore))}catch(_){}};
const ocOpen=new Set();

function ocDespachos(){
  const real=(typeof LOTES0!=="undefined"?LOTES0:[]).map(r=>({id:r.id,aba:r["Aba"]||"",fecha:gvDate(r["Fecha Despacho"]),lote:r["Lote"]==null||r["Lote"]===""?null:+r["Lote"],ref:refOf(r["Producto"]),prod:r["Producto"]||"",qtd:+r["Cantidad"]||0,promessa:gvDate(r["Promesa de Entrega"]),est:estOC(r["Estado"]),estTxt:r["Estado"]||"",bodega:r["Bodega"]||"",nota:r["Nota"]||"",ex:false})).filter(r=>r.ref);
  const ex=[];OCS0.filter(o=>o.exemplo).forEach(o=>{if(!ocStore.ex)return;(o.demo_despachos||[]).forEach((d,i)=>ex.push({id:"ex-"+i,aba:"Soma CO",fecha:d.fecha,lote:o.lote,ref:d.ref,prod:REFNOME[d.ref],qtd:d.qtd,promessa:d.promessa||null,est:(ocStore.sim&&d.est==="tr")?"ok":(d.est||"ok"),estTxt:d.est==="tr"&&!ocStore.sim?"En tránsito":"Entregado a Melonn",bodega:"",nota:"EXEMPLO",ex:true}));
    if(ocStore.sim)(o.demo_conclusao||[]).forEach((d,i)=>ex.push({id:"exs-"+i,aba:"Soma CO",fecha:d.fecha,lote:o.lote,ref:d.ref,prod:REFNOME[d.ref],qtd:d.qtd,promessa:d.promessa||null,est:"ok",estTxt:"Entregado a Melonn",bodega:"",nota:"EXEMPLO · simulação",ex:true}))});
  return real.concat(ex);
}
function ocList(){return OCS0.filter(o=>!o.exemplo||ocStore.ex)}

/* estado de um lote: contratado (OC) × entregue (despachos) */
function lotState(L,D){
  const rows=D.filter(d=>d.lote===L);const oc=ocList().find(o=>o.lote===L)||null;
  const refs=[...new Set([...(oc?oc.itens.map(i=>i.ref):[]),...rows.map(r=>r.ref)])].sort((a,b)=>REFS.findIndex(x=>x[0]===a)-REFS.findIndex(x=>x[0]===b));
  const per=refs.map(k=>{const it=oc?oc.itens.find(i=>i.ref===k):null;const con=it?it.qtd:null;
    const ent=rows.filter(r=>r.ref===k&&r.est==="ok").reduce((a,r)=>a+r.qtd,0);const tr=rows.filter(r=>r.ref===k&&r.est==="tr").reduce((a,r)=>a+r.qtd,0);
    // data em que esta referência atingiu 100% (pela Fecha Despacho, só entregues)
    let fin=null;if(con){let acc=0;for(const r of rows.filter(r=>r.ref===k&&r.est==="ok").sort((a,b)=>(a.fecha||"").localeCompare(b.fecha||""))){acc+=r.qtd;if(acc>=con){fin=r.fecha;break}}}
    return {k,con,ent,tr,falt:con!=null?Math.max(0,con-ent):null,exc:con!=null?Math.max(0,ent-con):0,pct:con?ent/con*100:null,unit:it?it.unit:null,fin}});
  const fechas=rows.map(r=>r.fecha).filter(Boolean).sort();
  const inicio=fechas[0]||null;
  const con=oc?per.reduce((a,x)=>a+(x.con||0),0):null;const ent=per.reduce((a,x)=>a+x.ent,0);const tr=per.reduce((a,x)=>a+x.tr,0);
  const done=oc?per.filter(x=>x.con).every(x=>x.ent>=x.con):false;
  const final=done?per.filter(x=>x.con).map(x=>x.fin).sort().at(-1):null;
  let pay=null;
  if(oc){const bruto=oc.itens.reduce((a,i)=>a+i.qtd*i.unit,0);const total=bruto*(1+(oc.iva||0));const ant=total*(oc.antecipo_pct??.5);const saldo=total-ant;
    const pAnt=(oc.pagamentos||[]).find(p=>/antecip/i.test(p.tipo));const pSal=(oc.pagamentos||[]).find(p=>/saldo/i.test(p.tipo));
    const vence=final?iso(addD(pd(final),oc.prazo_saldo_dias??30)):null;const dias=vence?Math.round((pd(vence)-HOJE)/864e5):null;
    const valEnt=per.reduce((a,x)=>a+Math.min(x.ent,x.con||0)*(x.unit||0),0)*(1+(oc.iva||0));
    let st,cls;if(pSal){st=`pago ${dm(pSal.data)}`;cls="good"}else if(!done){st="travado";cls="crit"}else if(dias<0){st=`vencido há ${-dias} d`;cls="crit"}else{st=`liberado · vence ${dm(vence)}`;cls=dias<=7?"warn":"good"}
    pay={bruto,total,ant,saldo,pAnt,pSal,vence,dias,st,cls,valEnt}}
  return {L,rows,oc,per,inicio,final,con,ent,tr,done,pay,pct:con?Math.min(ent,con)/con*100:null};
}

function ocProg(x){if(!x.con)return `<span class="note">sem OC</span>`;const w=v=>Math.max(0,Math.min(100,v));const pe=w(Math.min(x.ent,x.con)/x.con*100),pt=w(x.tr/x.con*100);
  return `<div class="prog"><div class="b" role="img" aria-label="${f1(x.ent/x.con*100)}% entregue"><i class="${x.ent>=x.con?"ok":"go"}" style="width:${pe}%"></i><i class="tr" style="width:${Math.min(pt,100-pe)}%"></i></div><span>${f1(x.ent/x.con*100)}%</span></div>`}

function renderOC(){
  if(!$("#oc-lotes"))return;
  $("#oc-ex").checked=!!ocStore.ex;$("#oc-sim").checked=!!ocStore.sim;$("#oc-sim").disabled=!ocStore.ex;$("#oc-drive").href=OCDRIVE;
  const D=ocDespachos();const lots=[...new Set(D.map(d=>d.lote).filter(v=>v!=null))].sort((a,b)=>a-b);
  const S=lots.map(L=>lotState(L,D));const withOC=S.filter(s=>s.oc);

  // ---- alertas / sinalizador ----
  const al=[];
  const ocs=[...withOC].sort((a,b)=>(a.oc.emissao||"").localeCompare(b.oc.emissao||""));
  ocs.forEach((s,i)=>{const nx=ocs[i+1];const falt=s.per.filter(x=>x.con&&x.ent<x.con).map(x=>`${fmt(x.con-x.ent)} ${REFS.find(r=>r[0]===x.k)[1]}`).join(" · ");
    if(!s.done&&nx)al.push(["crit",`<b>OC #${ocEsc(s.oc.numero)}</b> (lote ${s.L}) ainda ${f1(s.pct)}% e a OC #${ocEsc(nx.oc.numero)} já começou — saldo da anterior travado. Faltam ${falt}.`]);
    else if(!s.done)al.push(["warn",`<b>OC #${ocEsc(s.oc.numero)}</b> (lote ${s.L}) em entrega: ${f1(s.pct)}% · faltam ${falt}. Saldo de 50% travado até 100%.`]);
    s.per.filter(x=>x.exc>0).forEach(x=>al.push(["warn",`<b>OC #${ocEsc(s.oc.numero)}</b> · ${REFS.find(r=>r[0]===x.k)[1]}: entregue ${fmt(x.exc)} acima do contratado — divergência com o documento.`]));
    if(s.pay&&!s.pay.pAnt)al.push(["warn",`<b>OC #${ocEsc(s.oc.numero)}</b>: antecipo de 50% (${cop(s.pay.ant)}) sem comprovante anexado.`]);
    if(s.done&&!s.pay.pSal)al.push([s.pay.cls==="crit"?"crit":s.pay.dias<=7?"warn":"good",`<b>OC #${ocEsc(s.oc.numero)}</b> 100% entregue em ${dm(s.final)} · saldo ${cop(s.pay.saldo)} ${s.pay.dias<0?"vencido há "+(-s.pay.dias)+" dias":"vence "+dmw(s.pay.vence)+" ("+s.pay.dias+" dias)"}.`]);
  });
  if(!withOC.length)al.push(["warn","Nenhuma OC registrada ainda — o controle por OC começa no próximo lote. Ative “Mostrar OC de exemplo” para testar o fluxo."]);
  $("#oc-alerts").innerHTML=al.map(([c,t])=>`<div class="alert ${c}" role="status"><span class="dot"></span><span>${c==="crit"?"Atenção: ":c==="good"?"OK: ":"Aviso: "}${t}</span></div>`).join("");

  // ---- KPIs ----
  const abertas=withOC.filter(s=>!s.done);const conAb=abertas.reduce((a,s)=>a+s.con,0),entAb=abertas.reduce((a,s)=>a+Math.min(s.ent,s.con),0);
  const lib=withOC.filter(s=>s.done&&!s.pay.pSal).reduce((a,s)=>a+s.pay.saldo,0);const trav=abertas.reduce((a,s)=>a+s.pay.saldo,0);
  const K=[["OCs em aberto",String(abertas.length),`${withOC.length} OC${withOC.length===1?"":"s"} registrada${withOC.length===1?"":"s"}`],
    ["Contratado em aberto",fmt(conAb)+" un.",`entregue ${fmt(entAb)} · falta ${fmt(conAb-entAb)}`],
    ["Entregue / contratado",conAb?f1(entAb/conAb*100)+"%":"—","das OCs em aberto"],
    ["Saldo liberado a pagar",lib?cop(lib):"—","lotes 100% · vence 30 d após finalização"],
    ["Saldo travado",trav?cop(trav):"—","aguardando entrega 100%"]];
  $("#oc-kpis").innerHTML=K.map(([a,b,c])=>`<div class="kpi"><div class="eyebrow">${a}</div><div class="v">${b}</div><div class="s">${c}</div></div>`).join("");

  // ---- tabela Total por lote com botão de conferência ----
  const hasF=S.some(s=>s.per.some(x=>x.k==="f"));const NC=hasF?8:7;
  const head=`<tr><th>Lote · ticket / OC</th><th>Piña</th><th>Naranja</th>${hasF?"<th>Frutos Rojos</th>":""}<th>Entregue total</th><th>% da OC</th><th>Entrega · início → 100%</th><th>Saldo 50%</th></tr>`;
  const cell=(s,k)=>{const x=s.per.find(p=>p.k===k);if(!x)return `<td class="num">—</td>`;return `<td class="num">${fmt(x.ent)}${x.tr?`<br><span class="note">+${fmt(x.tr)} trânsito</span>`:""}${x.con?`<br><span class="note">de ${fmt(x.con)}</span>`:""}</td>`};
  const body=S.map(s=>{const open=ocOpen.has(s.L);const ex=s.oc&&s.oc.exemplo;
    const tot=s.per.filter(x=>x.k!=="s").reduce((a,x)=>a+x.ent,0);
    const row=`<tr style="--lc:${lcol(s.L)}"><td><div class="oc-lot"><span class="nm"><span class="sw" style="background:${lcol(s.L)}"></span>Lote ${s.L}${s.oc?` · <span class="num">#${ocEsc(s.oc.numero)}</span>`:""}${ex?' <span class="tag-ex">EXEMPLO</span>':""}</span>${s.oc?`<span class="note">OC emitida ${dfull(s.oc.emissao)}</span>`:'<span class="note">anterior ao controle por OC</span>'}<button class="oc-btn" type="button" data-oc="${s.L}" aria-expanded="${open}" aria-controls="oc-det-${s.L}">Conferência</button></div></td>
      ${cell(s,"p")}${cell(s,"n")}${hasF?cell(s,"f"):""}<td class="num"><b>${fmt(tot)}</b>${s.per.find(x=>x.k==="s")?`<br><span class="note">+${fmt(s.per.find(x=>x.k==="s").ent)} shaker</span>`:""}</td>
      <td>${s.oc?ocProg({con:s.con,ent:Math.min(s.ent,s.con),tr:s.tr}):'<span class="note">—</span>'}</td>
      <td class="num">${s.inicio?dm(s.inicio):"—"} → ${s.final?dm(s.final):s.oc?'<span class="note">em aberto</span>':"—"}</td>
      <td>${s.pay?`<span class="pill ${s.pay.cls}">${s.pay.cls==="crit"?"🔒 ":""}${s.pay.st}</span>`:'<span class="note">—</span>'}</td></tr>`;
    return row+`<tr class="oc-det" id="oc-det-${s.L}" ${open?"":"hidden"}><td colspan="${NC}">${open?ocPanel(s):""}</td></tr>`}).join("");
  $("#oc-lotes").innerHTML=head+(body||`<tr><td colspan="${NC}" class="empty">Sem despachos.</td></tr>`);
  $("#oc-lotes").querySelectorAll("button[data-oc]").forEach(b=>b.onclick=()=>{const L=+b.dataset.oc;ocOpen.has(L)?ocOpen.delete(L):ocOpen.add(L);renderOC()});

  // ---- gráfico % por OC ----
  const cats=withOC.map(s=>`Lote ${s.L} · #${s.oc.numero}${s.oc.exemplo?" (ex.)":""}`);
  const refsUsed=REFS.filter(([k])=>withOC.some(s=>s.per.some(x=>x.k===k&&x.con)));
  mk("cOC",{type:"bar",data:{labels:cats,datasets:refsUsed.map(([k,nome,tok])=>({label:nome,data:withOC.map(s=>{const x=s.per.find(p=>p.k===k);return x&&x.con?Math.round(x.ent/x.con*1000)/10:null}),backgroundColor:css("--"+tok),borderRadius:4,maxBarThickness:22}))},
    options:baseOpts({indexAxis:"y",plugins:{tooltip:{callbacks:{label:c=>{const s=withOC[c.dataIndex];const x=s.per.find(p=>REFS.find(r=>r[1]===c.dataset.label)[0]===p.k);return ` ${c.dataset.label}: ${f1(c.parsed.x)}% · ${fmt(x.ent)} de ${fmt(x.con)}`}}}},scales:{x:{min:0,suggestedMax:100,ticks:{color:css("--muted"),callback:v=>v+"%"},grid:{color:css("--line")},border:{display:false}},y:{ticks:{color:css("--fg")},grid:{display:false}}}})});
  $("#oc-chart-note").textContent=withOC.length?"100% = quantidade do documento. Barras acima de 100% indicam entrega maior que o contratado.":"Sem OCs registradas — o gráfico aparece quando a primeira OC for lançada (ou ative o exemplo).";

  // ---- despachos ----
  const ocNum=L=>{const o=ocList().find(o=>o.lote===L);return o?"#"+o.numero:"—"};
  const srt=[...D].sort((a,b)=>(a.lote??1e9)-(b.lote??1e9)||(a.fecha||"").localeCompare(b.fecha||""));
  const ESTB={ok:'<span class="est ok">Entregado</span>',tr:'<span class="est go">En tránsito</span>',pd:'<span class="est wait">Pendiente</span>'};
  $("#oc-desp").innerHTML=`<tr><th>Fecha Despacho</th><th>Lote</th><th>Ticket / OC</th><th>Producto</th><th>Cantidad</th><th>Promesa de Entrega</th><th>Estado</th><th>Aba</th><th>Bodega</th><th>Nota</th></tr>`+
    srt.map(r=>`<tr style="--lc:${lcol(r.lote)}"><td class="lt num">${dfull(r.fecha)}</td><td class="lt num">${r.lote??"—"}</td><td class="num">${ocNum(r.lote)}</td><td class="lt">${ocEsc(REFNOME[r.ref]||r.prod)}${/usa/i.test(r.prod)?' <span class="note">USA</span>':""}</td><td class="lt num">${fmt(r.qtd)}</td><td class="num">${r.promessa?dm(r.promessa):"—"}</td><td>${ESTB[r.est]}</td><td>${ocEsc(r.aba)}</td><td>${ocEsc(r.bodega)||"—"}</td><td class="note">${r.ex?'<span class="tag-ex">EXEMPLO</span>':ocEsc(r.nota)}</td></tr>`).join("");

  renderOCRep(S);
}

function ocPanel(s){
  const R=k=>REFS.find(r=>r[0]===k);
  if(!s.oc){
    return `<div class="oc-panel"><div class="blk"><h3>Lote ${s.L} · entregue por referência</h3>
      <div class="note">Lote anterior ao controle por OC: não há quantidade contratada para conferir. Mostra o que foi despachado.</div>
      <div class="tbl"><table><tr><th>Referência</th><th>Entregue</th><th>Em trânsito</th><th>Despachos</th></tr>${s.per.map(x=>`<tr><td><span class="sw ${x.k}"></span>${R(x.k)[1]}</td><td class="num">${fmt(x.ent)}</td><td class="num">${x.tr?fmt(x.tr):"—"}</td><td class="num">${s.rows.filter(r=>r.ref===x.k).length}</td></tr>`).join("")}</table></div></div>
      <div class="blk"><h3>Datas</h3><div class="tl"><div><span>Início entrega</span><b>${s.inicio?dfull(s.inicio):"—"}</b></div><div><span>Último despacho</span><b>${s.rows.length?dfull(s.rows.map(r=>r.fecha).filter(Boolean).sort().at(-1)):"—"}</b></div></div>
      <div class="docs"><a class="btn ghost" href="${OCDRIVE}" target="_blank" rel="noopener">Pasta de documentos ↗</a></div></div></div>`;
  }
  const o=s.oc,p=s.pay;const pct=Math.min(100,s.pct||0);
  const rows=s.per.filter(x=>x.con||x.ent).map(x=>`<tr><td><span class="sw ${x.k}"></span>${R(x.k)[1]}${x.con?`<br><span class="note">${ocEsc((o.itens.find(i=>i.ref===x.k)||{}).sku||"")}</span>`:""}</td><td class="num">${x.con?fmt(x.con):"—"}</td><td class="num">${fmt(x.ent)}</td><td class="num">${x.tr?fmt(x.tr):"—"}</td><td class="num">${x.con==null?"—":x.exc?`<span style="color:var(--warn)">+${fmt(x.exc)}</span>`:x.falt?fmt(x.falt):'<span style="color:var(--good)">0</span>'}</td><td>${x.con?ocProg(x):'<span class="pill warn">fora da OC</span>'}</td><td class="num">${x.fin?dm(x.fin):x.con?"—":""}</td></tr>`).join("");
  const tot=`<tr class="tot"><td>Total</td><td class="num">${fmt(s.con)}</td><td class="num">${fmt(s.ent)}</td><td class="num">${s.tr?fmt(s.tr):"—"}</td><td class="num">${fmt(Math.max(0,s.con-s.per.reduce((a,x)=>a+Math.min(x.ent,x.con||0),0)))}</td><td>${ocProg({con:s.con,ent:Math.min(s.ent,s.con),tr:s.tr})}</td><td class="num">${s.final?dm(s.final):"—"}</td></tr>`;
  const st=s.done?`<span class="pill good">100% entregue · conforme documento</span>`:`<span class="pill warn">Em entrega · ${f1(s.pct)}%</span>`;
  const docs=[o.doc_oc?`<a class="btn ghost" href="${ocEsc(o.doc_oc)}" target="_blank" rel="noopener">OC #${ocEsc(o.numero)} (PDF) ↗</a>`:`<span class="pill">PDF da OC: anexar na pasta</span>`]
    .concat((o.pagamentos||[]).map(x=>x.comprovante?`<a class="btn ghost" href="${ocEsc(x.comprovante)}" target="_blank" rel="noopener">Comprovante ${ocEsc(x.tipo)} ↗</a>`:`<span class="pill">Comprovante ${ocEsc(x.tipo)}: anexar</span>`))
    .concat([`<a class="btn ghost" href="${ocEsc(o.pasta||OCDRIVE)}" target="_blank" rel="noopener">Pasta do lote ↗</a>`]).join("");
  return `<div class="oc-panel">
    <div class="blk"><div class="sec-h"><h3>Lote ${s.L} · OC #${ocEsc(o.numero)} ${o.exemplo?'<span class="tag-ex">EXEMPLO</span>':""}</h3>${st}</div>
      <div class="tbl"><table><tr><th>Referência</th><th>Contratado</th><th>Entregue</th><th>Trânsito</th><th>Faltante</th><th>%</th><th>100% em</th></tr>${rows}${tot}</table></div>
      <div class="tl"><div><span>Emissão OC</span><b>${dfull(o.emissao)}</b></div><div><span>Entrega acordada</span><b>${dfull(o.entrega_acordada)}</b></div><div><span>Início entrega</span><b>${s.inicio?dfull(s.inicio):"—"}</b></div><div><span>Finalização 100%</span><b>${s.final?dfull(s.final):"em aberto"}</b></div><div><span>Saldo vence</span><b>${p.vence?dfull(p.vence):"após 100%"}</b></div></div>
      <div class="ocfields"><div><span>Fornecedor</span><b>${ocEsc(o.fornecedor)}</b></div><div><span>Condição</span><b>${ocEsc(o.condicao)}</b></div><div><span>Comprador</span><b>${ocEsc(o.comprador||"—")}</b></div><div><span>Modalidade</span><b>${ocEsc(o.modalidade||"—")}</b></div></div>
    </div>
    <div class="blk"><div class="ring" style="--p:${pct};--c:${s.done?"var(--good)":"var(--accent)"}" role="img" aria-label="${f1(s.pct)}% entregue"><div><span><b>${f1(s.pct)}%</b><br><small>entregue</small></span></div></div>
      <h3>Pagamento</h3>
      <div class="fin"><span>Total OC (c/ IVA ${Math.round((o.iva||0)*100)}%)</span><span>${cop(p.total)}</span>
        <span>Antecipo ${Math.round((o.antecipo_pct??.5)*100)}%</span><span>${cop(p.ant)}</span>
        <span>Status antecipo</span><span>${p.pAnt?`<span class="pill good">pago ${dm(p.pAnt.data)}</span>`:'<span class="pill warn">sem comprovante</span>'}</span>
        <span>Saldo ${100-Math.round((o.antecipo_pct??.5)*100)}%</span><span>${cop(p.saldo)}</span>
        <span>Status saldo</span><span><span class="pill ${p.cls}">${p.cls==="crit"&&!s.done?"🔒 ":""}${p.st}</span></span>
        <span>Valor já entregue (c/ IVA)</span><span>${cop(p.valEnt)}</span></div>
      <h3>Documentos</h3><div class="docs">${docs}</div>
    </div></div>`;
}

/* ---------- relatório semanal ---------- */
function ocWeeks(){const out=[];const mon=d=>{const x=new Date(d);const wd=(x.getDay()+6)%7;x.setDate(x.getDate()-wd);return x};let w=mon(HOJE);for(let i=0;i<8;i++){const a=addD(w,-7*i),b=addD(a,6);out.push([iso(a),iso(b),i===0])}return out}
function renderOCRep(S){
  const sel=$("#oc-wk");if(!sel.options.length){sel.innerHTML=ocWeeks().map(([a,b,cur],i)=>`<option value="${a}|${b}">${dm(a)} → ${dm(b)}${cur?" (atual)":""}</option>`).join("");sel.value=ocStore.wk||sel.options[0].value;sel.onchange=()=>{ocStore.wk=sel.value;ocSave();renderOC()}}
  $("#oc-wk-ex").checked=!!ocStore.wkex;
  const [a,b]=sel.value.split("|");const D=ocDespachos().filter(d=>ocStore.wkex||!d.ex);const St=S.filter(s=>ocStore.wkex||!(s.oc&&s.oc.exemplo));
  const wk=D.filter(d=>d.fecha&&d.fecha>=a&&d.fecha<=b);const N=k=>REFS.find(r=>r[0]===k)[1];
  const byLot={};wk.forEach(d=>{const L=d.lote??"sem nº";(byLot[L]=byLot[L]||{n:0,r:{}}).n++;byLot[L].r[d.ref]=(byLot[L].r[d.ref]||0)+d.qtd});
  const sumRef=k=>wk.filter(d=>d.ref===k).reduce((x,d)=>x+d.qtd,0);
  const L=[];const SEP="━━━━━━━━━━━━━━";
  L.push("📦 *RELATÓRIO SEMANAL · LOTES E COMPRAS*",`Semana ${dm(a)} → ${dm(b)}${b>META.hoje?" (parcial, até "+dm(META.hoje)+")":""}`,"",SEP,"🚚 *DESPACHOS DA SEMANA*");
  if(!wk.length)L.push("• Nenhum despacho na semana");
  Object.entries(byLot).forEach(([lt,v])=>L.push(`• Lote ${lt}: ${Object.entries(v.r).map(([k,q])=>`${N(k)} ${fmt(q)}`).join(" · ")} (${v.n} despacho${v.n>1?"s":""})`));
  if(wk.length)L.push(`Total: ${REFS.filter(([k])=>sumRef(k)).map(([k,n])=>`${n} ${fmt(sumRef(k))}`).join(" · ")}`);
  const trn=D.filter(d=>d.est==="tr");L.push("",SEP,"🛣️ *EM TRÂNSITO HOJE*");
  if(!trn.length)L.push("• Nada em trânsito");else{const g={};trn.forEach(d=>{const k=(d.lote??"sem nº")+"|"+d.ref;g[k]=(g[k]||0)+d.qtd});Object.entries(g).forEach(([k,q])=>{const[lt,r]=k.split("|");L.push(`• Lote ${lt} · ${N(r)} ${fmt(q)}`)})}
  const oc=St.filter(s=>s.oc);L.push("",SEP,"📋 *ORDENS DE COMPRA*");
  if(!oc.length)L.push("• Nenhuma OC registrada (controle por OC começa no próximo lote)");
  oc.forEach(s=>{L.push(`• OC #${s.oc.numero} · Lote ${s.L}${s.oc.exemplo?" (exemplo)":""}: ${s.per.filter(x=>x.con).map(x=>`${N(x.k)} ${f1(x.ent/x.con*100)}%`).join(" · ")}`);const f=s.per.filter(x=>x.con&&x.ent<x.con);L.push(f.length?`  Falta: ${f.map(x=>`${fmt(x.con-x.ent)} ${N(x.k)}`).join(" · ")}`:`  ✅ 100% entregue em ${dm(s.final)}`)});
  L.push("",SEP,"💰 *PAGAMENTOS*");
  if(!oc.length)L.push("• Sem pagamentos de OC no controle");
  oc.forEach(s=>{const p=s.pay;L.push(`• OC #${s.oc.numero}: antecipo ${p.pAnt?"pago "+dm(p.pAnt.data):"sem comprovante"} · saldo ${cop(p.saldo)} ${p.pSal?"pago "+dm(p.pSal.data):s.done?(p.dias<0?"VENCIDO há "+(-p.dias)+" d":"liberado, vence "+dm(p.vence)):"🔒 travado até 100%"}`)});
  const att=[];oc.forEach((s,i)=>{if(!s.done&&oc[i+1])att.push(`OC #${s.oc.numero} incompleta com OC #${oc[i+1].oc.numero} já iniciada`);s.per.filter(x=>x.exc).forEach(x=>att.push(`OC #${s.oc.numero}: ${N(x.k)} +${fmt(x.exc)} acima do documento`));if(s.done&&!s.pay.pSal&&s.pay.dias<=7)att.push(`Saldo OC #${s.oc.numero} vence ${dm(s.pay.vence)}`)});
  L.push("",SEP,"⚠️ *PONTOS DE ATENÇÃO*");L.push(att.length?att.map(t=>"• "+t).join("\n"):"• Nenhum");
  $("#oc-rep").textContent=L.join("\n");
}
$("#oc-ex").onchange=e=>{ocStore.ex=e.target.checked;if(!ocStore.ex)ocStore.sim=false;ocSave();renderOC()};
$("#oc-sim").onchange=e=>{ocStore.sim=e.target.checked;ocSave();renderOC()};
$("#oc-wk-ex").onchange=e=>{ocStore.wkex=e.target.checked;ocSave();renderOC()};
$("#oc-copy").onclick=async()=>{const t=$("#oc-rep").textContent;try{await navigator.clipboard.writeText(t);$("#oc-copy-st").textContent="Copiado."}catch(_){const r=document.createRange();r.selectNodeContents($("#oc-rep"));const s=getSelection();s.removeAllRanges();s.addRange(r);$("#oc-copy-st").textContent="Selecionado — use Ctrl+C."}};
{const _rl=renderLotes;renderLotes=function(){_rl.apply(this,arguments);try{renderOC()}catch(e){console.error(e)}}}
try{renderOC()}catch(e){console.error(e)}
'''

s = open(SRC, encoding="utf-8").read()
# título e noindex
s = s.replace("<title>Ruptura SOMA</title>", "<title>Ruptura SOMA · teste</title>\n<meta name=\"robots\" content=\"noindex\">", 1)
# nav
anchor = re.search(r'<button id="tab-lotes"[^\n]*?</button>', s)
assert anchor
s = s[:anchor.end()] + "\n      " + NAV + "\n      " + tk_parts.NAV + s[anchor.end():]
# css
i = s.index("</style>"); s = s[:i] + CSS + tk_parts.CSS + s[i:]
# html: logo depois da seção de lotes
m = re.search(r'<section class="card" id="lotes-sec" data-tab="lotes">.*?</section>', s, re.S)
assert m
s = s[:m.end()] + "\n" + HTML + tk_parts.HTML + s[m.end():]
# rota por hash (abre na aba de teste por padrão)
old = 'showTab(h0==="lotes"?"lotes":"ruptura");'
assert old in s
s = s.replace(old, 'showTab(["ruptura","lotes","oc","tk","cedi","dist","faturas"].includes(h0)?h0:"oc");')
# js no fim do último <script> inline
j = s.rindex("</script>")
TKD = json.load(open(os.path.join(BASE, "tk_data.json"), encoding="utf-8"))
TKJS = tk_parts.JS.replace("__OCST__", json.dumps(TKD["ocs"], ensure_ascii=False)).replace("__COMP__", json.dumps(TKD["comp"], ensure_ascii=False)).replace("__TKDRIVE__", json.dumps(TKD["drive"], ensure_ascii=False))
s = s[:j] + JS.replace("__OCS__", json.dumps(OCS, ensure_ascii=False)) + TKJS + s[j:]
# ---- aba de teste "Previsão · Produção" só na página de teste (index.html continua igual) ----
import prev_parts
def add_prev(src):
    # 1) nav: duplicata "Ruptura e vendas · teste" logo depois da aba original
    a = re.search(r'<button id="tab-ruptura"[^\n]*?</button>', src); assert a
    src = src[:a.end()] + "\n      " + prev_parts.NAV + src[a.end():]
    i = src.index("</style>"); src = src[:i] + prev_parts.CSS + src[i:]
    # 2) a aba duplicada mostra as MESMAS seções da Ruptura e vendas (sem alterar a original)
    ph = '<div class="page-h" data-tab="ruptura">'
    k0 = src.index(ph); k1 = src.index("</div>\n  </div>", k0) + len("</div>\n  </div>")
    body = src[k1:]
    body = re.sub(r'data-tab="([^"]*)"', lambda m: 'data-tab="%s"' % (m.group(1) + ",rup2") if "ruptura" in m.group(1).split(",") else m.group(0), body)
    src = src[:k1] + "\n" + prev_parts.PAGEH + body
    # 3) seções novas (prompt) logo depois do "Ponto de ruptura por SKU"
    r = src.index('<div class="rup" id="rup"></div>'); e = src.index("</section>", r) + len("</section>")
    src = src[:e] + "\n" + prev_parts.HTML + src[e:]
    # 4) rota por hash: aceita #rup2; padrão continua o original da página de teste
    o2 = 'showTab(["ruptura","lotes","oc","tk","cedi","dist","faturas"].includes(h0)?h0:"oc");'
    assert o2 in src
    src = src.replace(o2, 'showTab(["ruptura","rup2","lotes","oc","tk","cedi","dist","faturas"].includes(h0)?h0:"oc");')
    j2 = src.rindex("</script>")
    js = prev_parts.JS + '\n{const _st=showTab;showTab=function(t){_st(t);if(t==="rup2")Object.values(CH).forEach(c=>{try{c.resize()}catch(_){}})}}\n'
    return src[:j2] + js + src[j2:]
s_test = add_prev(s)
open(os.path.join(BUILD, "painel_teste.html"), "w", encoding="utf-8").write(s_test)

# embrulha: teste.html (abre na aba OC) e index.html oficial (abre em Ruptura, com a aba OC disponível)
def wrap(src, path):
    head = []
    for pat in [r'<title>.*?</title>\n?', r'<meta name="robots"[^>]*>\n?', r'<meta name="claude:viewport-fit-sides"[^>]*>\n?', r'<meta name="viewport"[^>]*>\n?', r'<link rel="stylesheet"[^>]*>\n?']:
        mm = re.search(pat, src, re.S)
        if mm: head.append(mm.group(0).strip()); src = src.replace(mm.group(0), "", 1)
    out = '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">' + "".join(head) + '<style>[hidden]{display:none!important}</style></head><body>' + src + '</body></html>'
    open(path, "w", encoding="utf-8").write(out)
    print(path, len(out))
wrap(s_test, OUT)
off = s.replace('<title>Ruptura SOMA · teste</title>\n<meta name="robots" content="noindex">', '<title>Ruptura SOMA</title>', 1)
off = off.replace('includes(h0)?h0:"oc");', 'includes(h0)?h0:"ruptura");')
open(os.path.join(BUILD, "painel_oficial_oc.html"), "w", encoding="utf-8").write(off)
wrap(off, os.path.join(REPO, "index.html"))
