# Aba de TESTE "Ruptura · esgotados" (só em teste.html):
# ponto de ruptura por referência e por bodega com a conta aberta:
# disponível Shopify − esgotados Melonn = livre; + esperada Melonn = base; ritmo do período; data de chegada editável.
import re

NAV = '''<button id="tab-rupesg" role="tab" data-tab="rupesg"><svg viewBox="0 0 24 24"><path d="M12 3v12"/><path d="M8 11l4 4 4-4"/><path d="M4 21h16"/></svg>Ruptura · esgotados<span class="badge tst">teste</span></button>'''

BLOCK = '''
  <div class="page-h" data-tab="rupesg">
    <div><div class="eyebrow">Shopify · Melonn · esgotados e esperada · teste</div><h1>Ruptura com esgotados e trânsito</h1><p>A conta do ponto de ruptura aberta, referência por referência e bodega por bodega: <b>disponível na Shopify − pedidos esgotados na Melonn = livre</b>; <b>livre + esperada na Melonn = base</b>; base ÷ venda por dia = dias até a ruptura. Informe a data de chegada da esperada para ver se a bodega fica sem estoque antes de ela chegar.</p></div>
    <span class="pill warn">Aba de teste · as outras abas não mudam</span>
  </div>
  <div class="alerts" id="re-alerts" data-tab="rupesg"></div>
  <section class="card" data-tab="rupesg">
    <div class="sec-h"><h2>Ponto de ruptura por referência</h2><p id="re-src"></p></div>
    <div class="re-grid" id="re-cards"></div>
  </section>
  <section class="card" data-tab="rupesg">
    <div class="sec-h"><h2>Por bodega</h2><p>Cada bodega atende os departamentos mais próximos. Preencha a <b>chegada prevista</b> das esperadas: a data fica salva neste navegador.</p></div>
    <div class="tbl"><table class="re-tab" id="re-bod"></table></div>
  </section>
  <section class="card" data-tab="rupesg">
    <div class="sec-h"><h2>Como a conta é feita</h2></div>
    <div class="re-how" id="re-how"></div>
  </section>
'''

CSS = '''
.re-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--sp-3)}
@media (max-width:1100px){.re-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.re-grid{grid-template-columns:1fr}}
.re-card{border:1px solid var(--line);border-radius:12px;padding:14px;background:var(--surface);display:flex;flex-direction:column;gap:10px;min-width:0}
.re-card h3{margin:0;font-size:15px;display:flex;align-items:center;gap:8px}
.re-card .re-big{font-size:22px;font-weight:650;line-height:1.15}
.re-card .re-sub{font-size:var(--fs-xs);color:var(--muted)}
.re-eq{display:grid;grid-template-columns:1fr auto;gap:3px 12px;font-size:13px}
.re-eq span:nth-child(even){text-align:right;font-variant-numeric:tabular-nums}
.re-eq .op{color:var(--muted)}
.re-eq .tot{font-weight:650;border-top:1px solid var(--line);padding-top:3px}
.re-eq .neg{color:var(--crit)}
.re-dates{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.re-dates div{border-radius:8px;padding:8px;background:var(--bg)}
.re-dates b{display:block;font-size:14px}
.re-tab th,.re-tab td{white-space:nowrap}
.re-tab tr.re-sku td{background:var(--bg);font-weight:650}
.re-tab input[type=date]{font:inherit;font-size:12px;padding:3px 6px;border:1px solid var(--line);border-radius:6px;background:var(--surface);color:var(--fg)}
.re-tab .neg{color:var(--crit);font-weight:600}
.re-how{font-size:13px;line-height:1.6;color:var(--fg-2)}
.re-how ul{margin:6px 0 0;padding-left:18px}
'''

JS = r'''
/* ===================== Ruptura · esgotados e trânsito (teste) ===================== */
const RE_KEY="soma-rupesg-v1";
let RES=(()=>{try{return JSON.parse(localStorage.getItem(RE_KEY))||{}}catch(_){return{}}})();RES.eta=RES.eta||{};
const reSave=()=>{try{localStorage.setItem(RE_KEY,JSON.stringify(RES))}catch(_){}};
const RE_B=["Bogotá","Medellín","Cali","Barranquilla"];
const reEsg=(k,b)=>+((typeof ESG!=="undefined"&&ESG.aplicado?.[k]?.[b])||0);
// divisão por bodega: vendas por departamento (janela da aba Distribuição), cada departamento atendido pela bodega mais próxima
function reShare(k){const src=DIST[dBase]||DIST.d7||{};const o={};RE_B.forEach(b=>o[b]=0);let t=0;
  for(const[reg,v]of Object.entries(src)){const u=+v[k]||0;const g=DIST.geo?.[reg]||"Bogotá";o[RE_B.includes(g)?g:"Bogotá"]+=u;t+=u}
  if(t<=0)return k==="p"?Object.fromEntries(RE_B.map(b=>[b,1/RE_B.length])):reShare("p");RE_B.forEach(b=>o[b]/=t);return o}
const reDays=s=>s?Math.round((pd(s)-new Date(HOJE.toDateString()))/864e5):null;
function reWhen(d){if(!isFinite(d))return "sem ruptura";if(d<=0)return "já em ruptura";const f=Math.floor(d);return f===0?"HOJE":WD[addD(HOJE,f).getDay()]+" "+dm(iso(addD(HOJE,f)))}
const reCls=d=>!isFinite(d)?"good":d<=3?"crit":d<=7?"warn":"good";
const reF=d=>!isFinite(d)?"—":d<=0?"0 d":f1(d)+" d";
function reCalc(){
  const out={};SK.forEach(([k,nome])=>{const sh=reShare(k);const rate=+PER.avg[k]||0;const bods={};
    RE_B.forEach(b=>{const net=(STOCK[k].bod[b]||[0])[0];const esg=reEsg(k,b);const disp=net+esg;const E=melEsp(k,b);const D=rate*sh[b];
      const eta=RES.eta[k+"|"+b]||"";const t=eta?Math.max(0,reDays(eta)):null;
      const sem=D>0?net/D:(net>0?Infinity:0),com=D>0?(net+E)/D:Infinity;
      let gap=null;if(E>0&&t!=null&&D>0){const ini=Math.max(0,sem);if(ini<t)gap={ini,fim:t,un:Math.round(D*(t-ini)+Math.max(0,-net))}}
      bods[b]={disp,esg,net,E,D,eta,t,sem,com,gap}});
    const tot=x=>RE_B.reduce((a,b)=>a+bods[b][x],0);const net=tot("net"),E=tot("E");
    out[k]={nome:STOCK[k].nome,sku:STOCK[k].sku,rate,bods,disp:tot("disp"),esg:tot("esg"),net,E,sem:rate>0?net/rate:Infinity,com:rate>0?(net+E)/rate:Infinity}});
  return out}
function renderRupEsg(){
  if(!PER||!$("#re-cards"))return;const C=reCalc();
  // cards por referência
  $("#re-cards").innerHTML=SK.map(([k,nome,tok])=>{const c=C[k];
    return `<div class="re-card"><h3><span class="sw ${k}"></span>${c.nome}</h3>
      <div><div class="re-big ${reCls(c.com)==="crit"?"neg":""}">${reWhen(c.com)}</div><div class="re-sub">ruptura com a esperada · ${reF(c.com)} de cobertura</div></div>
      <div class="re-eq"><span class="op">Disponível Shopify</span><span>${fmt(c.disp)}</span>
        <span class="op">− Esgotados na Melonn</span><span class="${c.esg?"neg":""}">${c.esg?"−"+fmt(c.esg):"0"}</span>
        <span class="tot">= Livre hoje</span><span class="tot ${c.net<0?"neg":""}">${fmt(c.net)}</span>
        <span class="op">+ Esperada na Melonn</span><span>${c.E?"+"+fmt(c.E):"0"}</span>
        <span class="tot">= Base para ruptura</span><span class="tot">${fmt(c.net+c.E)}</span>
        <span class="op">Venda por dia</span><span>${fmt(c.rate)}</span></div>
      <div class="re-dates"><div><span class="re-sub">Sem a esperada</span><b class="${reCls(c.sem)}">${reWhen(c.sem)}</b><span class="re-sub">${reF(c.sem)}</span></div><div><span class="re-sub">Com a esperada</span><b class="${reCls(c.com)}">${reWhen(c.com)}</b><span class="re-sub">${reF(c.com)}</span></div></div></div>`}).join("");
  // tabela por bodega
  const H=`<tr><th>Bodega</th><th>Disp. Shopify</th><th>Esgotados</th><th>Livre</th><th>Esperada</th><th>Chegada prevista</th><th>Venda/dia</th><th>Acaba sem esperada</th><th>Acaba com esperada</th><th>Antes da chegada</th></tr>`;
  let h=H;SK.forEach(([k])=>{const c=C[k];h+=`<tr class="re-sku"><td colspan="10"><span class="sw ${k}"></span>${c.nome} <span class="note">${c.sku}</span></td></tr>`;
    RE_B.forEach(b=>{const x=c.bods[b];const key=k+"|"+b;
      const antes=x.E<=0?`<span class="note">sem esperada</span>`:!x.eta?`<span class="note">informe a chegada</span>`:x.gap?`<span class="pill crit">sem estoque ${x.gap.ini<1?"já":"de "+reWhen(x.gap.ini)} até ${dm(x.eta)}</span> <span class="note">~${fmt(x.gap.un)} un. em espera</span>`:`<span class="pill good">chega a tempo</span>`;
      h+=`<tr><td>${b}</td><td class="num">${fmt(x.disp)}</td><td class="num ${x.esg?"neg":""}">${x.esg?"−"+fmt(x.esg):"—"}</td><td class="num ${x.net<0?"neg":""}">${fmt(x.net)}</td><td class="num">${x.E?"+"+fmt(x.E):"—"}</td>
        <td>${x.E>0?`<input type="date" data-k="${key}" value="${x.eta}" min="${iso(HOJE)}">`:`<span class="note">—</span>`}</td>
        <td class="num">${fmt(x.D)}</td><td class="num ${reCls(x.sem)}">${reWhen(x.sem)} <span class="note">${reF(x.sem)}</span></td><td class="num ${reCls(x.com)}">${reWhen(x.com)} <span class="note">${reF(x.com)}</span></td><td>${antes}</td></tr>`})});
  $("#re-bod").innerHTML=h;
  $("#re-bod").querySelectorAll("input[type=date]").forEach(inp=>inp.onchange=e=>{const k=e.target.dataset.k;if(e.target.value)RES.eta[k]=e.target.value;else delete RES.eta[k];reSave();renderRupEsg()});
  // alertas
  const al=[];SK.forEach(([k])=>{const c=C[k];RE_B.forEach(b=>{const x=c.bods[b];if(x.D<=0)return;
    if(x.net<=0)al.push(["crit",`${c.nome} · <b>${b}</b>: já em ruptura${x.net<0?` (${fmt(-x.net)} un. em pedidos esgotados)`:""}${x.E?` · esperada ${fmt(x.E)}${x.eta?` chega ${dm(x.eta)}`:" sem data"}`:" · sem esperada"}`]);
    else if(x.sem<=3)al.push(["warn",x.E?`${c.nome} · <b>${b}</b>: acaba ${reWhen(x.sem)} se a esperada não chegar antes (${fmt(x.E)} un.${x.eta?`, chegada ${dm(x.eta)}`:", sem data"})`:`${c.nome} · <b>${b}</b>: acaba ${reWhen(x.sem)} e não há esperada a caminho`])})});
  $("#re-alerts").innerHTML=al.map(([c,t])=>`<div class="alert ${c}"><span class="dot"></span><span>${t}</span></div>`).join("");
  // fontes e método
  const melT=Object.values(MEL).map(m=>m.lido_em).filter(Boolean).sort().pop();const dt=s=>s?new Date(s).toLocaleString("pt-BR",{day:"2-digit",month:"2-digit",hour:"2-digit",minute:"2-digit"}):"—";
  $("#re-src").innerHTML=`Shopify ${META.atualizado} · esgotados ${dt(ESG?.lido_em)} · esperada Melonn ${dt(melT)} · venda/dia: período ${$("#per-lbl")?.textContent||""}`;
  const abs=Object.entries(ESG?.absorvido||{}).flatMap(([k,o])=>Object.entries(o).map(([b,q])=>`${STOCK[k]?.nome||k} ${b}: ${fmt(q)}`));
  const fix=Object.entries(ESG?.fixo||{}).flatMap(([k,o])=>Object.entries(o).map(([b,q])=>`${b} ${fmt(q)}`));
  $("#re-how").innerHTML=`<ul>
    <li><b>Disponível Shopify:</b> o que a Melonn informa como disponível em cada bodega, lido na Shopify (${META.atualizado}, atualização automática a cada 5 h).</li>
    <li><b>Esgotados:</b> pedidos pagos parados na Melonn por falta de estoque (arquivo de pedidos de ${dt(ESG?.lido_em)}). Eles consomem a próxima mercadoria que chegar, por isso saem do disponível.${abs.length?` Já atendidos com a mercadoria que entrou depois do arquivo, e por isso não descontados: ${abs.join(" · ")}.`:""}${fix.length?` Frutos Rojos do Limitado com código SOMAROJOS (${fix.join(" · ")}): descontados até a Melonn ligar o código ao estoque SOMAROJO.`:""}</li>
    <li><b>Esperada:</b> mercadoria anunciada para entrar em cada bodega (Reporte inventario da Melonn, ${dt(melT)}). "Com a esperada" supõe que ela chega antes de o livre acabar; com a data de chegada preenchida, a tabela mostra o buraco quando não chega a tempo.</li>
    <li><b>Venda por dia:</b> média do período escolhido na aba Ruptura e vendas (${$("#per-lbl")?.textContent||""}). Frutos Rojos conta só a partir do lançamento (${dm(R0)}). A venda de cada bodega é a fatia dos departamentos que ela atende (bodega mais próxima), pelas vendas por departamento da janela escolhida na aba Distribuição.</li>
    <li>A conta por referência soma as quatro bodegas como se o estoque pudesse atender qualquer região; a conta por bodega é a mais realista quando uma bodega zera antes das outras.</li></ul>`;
}
{const _rr=render;render=function(){_rr.apply(this,arguments);try{renderRupEsg()}catch(e){console.error(e)}}}
{const _st=showTab;showTab=function(t){_st(t);if(t==="rupesg")try{renderRupEsg()}catch(e){console.error(e)}}}
try{renderRupEsg()}catch(e){console.error(e)}
'''


def apply(src):
    # nav: logo depois da aba "Ruptura e vendas · teste"
    a = re.search(r'<button id="tab-rup2"[^\n]*?</button>', src); assert a
    src = src[:a.end()] + "\n      " + NAV + src[a.end():]
    i = src.index("</style>"); src = src[:i] + CSS + src[i:]
    # conteúdo: antes do cabeçalho da aba Ruptura e vendas (só aparece na aba rupesg)
    ph = '<div class="page-h" data-tab="ruptura">'
    k = src.index(ph); src = src[:k] + BLOCK.lstrip() + "\n  " + src[k:]
    # rota por hash
    o = 'showTab(["ruptura","rup2","lotes","oc","tk","cedi","dist","faturas"].includes(h0)?h0:"oc");'
    assert o in src
    src = src.replace(o, 'showTab(["ruptura","rup2","rupesg","lotes","oc","tk","cedi","dist","faturas"].includes(h0)?h0:"oc");')
    j = src.rindex("</script>")
    return src[:j] + JS + src[j:]
