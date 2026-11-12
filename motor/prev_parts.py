# Aba de TESTE "Previsão · Produção": previsão de pedidos (histórico × rampa manual editável),
# projeção diária de estoque por produto com zonas (ruptura / vermelho / amarelo / verde),
# sugestão de produção e tabela editável "Produção em andamento".
# Usa os dados que já alimentam a aba Ruptura e vendas (ROWS, STOCK, MEL) — não altera nada dela.
# Parâmetros: aba "Controle de produção" da planilha do painel (gviz); lotes: aba "Produção em andamento".

NAV = '''<button id="tab-rup2" role="tab" data-tab="rup2"><svg viewBox="0 0 24 24"><path d="M3 17l5-6 4 3 5-7 4 4"/><path d="M3 21h18"/></svg>Ruptura e vendas<span class="badge tst">teste</span></button>'''

PAGEH = '''
  <div class="page-h" data-tab="rup2">
    <div><div class="eyebrow">Shopify · Melonn · Piña, Naranja e Shaker · cópia de teste</div><h1>Ruptura e vendas · teste</h1><p>Cópia da aba Ruptura e vendas com a previsão de estoque e produção incluída (marcada como <b>novo</b>) logo abaixo do Ponto de ruptura. A aba original Ruptura e vendas continua igual.</p></div>
    <span class="pill warn">Cópia de teste · a aba original não foi alterada</span>
  </div>
'''

CSS = '''
/* ---------- aba de teste: Previsão · Produção ---------- */
.pv-ctl{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:end}
.pv-ctl label{display:grid;gap:4px;font-size:12px;color:var(--muted);font-weight:500}
.pv-ctl input[type=number]{width:120px;height:var(--ctl-h)}
.pv-ctl input[disabled]{opacity:.75}
.pv-ctl .chk{display:flex;align-items:center;gap:6px;color:var(--fg-2);font-size:12.5px;height:var(--ctl-h)}
.pv-ghost{font:inherit;font-size:12.5px;font-weight:500;height:var(--ctl-h);padding:0 12px;border-radius:var(--r-sm);border:1px solid var(--line-strong);background:var(--surface);color:var(--fg-2);cursor:pointer;display:inline-flex;align-items:center;gap:6px;white-space:nowrap}
.pv-ghost:hover{background:var(--soft);color:var(--fg)}a.pv-ghost{text-decoration:none}
.pv-ghost.danger{color:var(--crit)}
.pv-info{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:12.5px;color:var(--muted)}
.pv-info b{color:var(--fg);font-family:var(--mono);font-weight:500}
.pv-drag canvas{touch-action:none;cursor:ns-resize}
.pv-zone{display:inline-flex;align-items:center;gap:6px;padding:2px 9px;border-radius:999px;font-size:11.5px;font-weight:600;white-space:nowrap}
.pv-zone::before{content:"";width:7px;height:7px;border-radius:50%;background:currentColor}
.pv-zone.rup,.pv-zone.red{background:var(--critbg);color:var(--crit)}
.pv-zone.yel{background:var(--warnbg);color:var(--warn)}
.pv-zone.grn{background:var(--goodbg);color:var(--good)}
.pv-zone.rup{outline:1px solid var(--crit)}
#pv-tab td{white-space:nowrap}#pv-tab th{white-space:normal;line-height:1.25;vertical-align:bottom}#pv-tab td,#pv-tab th{padding-left:10px;padding-right:10px}
#pv-tab td.prod{font-weight:600}
#pv-tab td.sug{font-family:var(--mono);font-weight:700}
.pv-charts{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(360px,100%),1fr));gap:var(--sp-4)}
.pv-charts .chart{height:260px}
#pv-lots input[type=number]{width:82px;height:var(--ctl-h-sm)}
#pv-lots input[type=date]{height:var(--ctl-h-sm);font-size:12px;padding:0 4px;width:128px}
#pv-lots input[type=text]{height:var(--ctl-h-sm);font-size:12px;width:96px}
#pv-lots select{height:var(--ctl-h-sm);font-size:12.5px;width:auto;min-width:0}
#pv-lots td,#pv-lots th{white-space:nowrap;vertical-align:middle;padding-left:6px;padding-right:6px;text-align:left}
#pv-lots td.calc{font-family:var(--mono);font-size:12.5px}
#pv-lots button.x{font:inherit;border:1px solid var(--line);background:var(--surface);color:var(--crit);border-radius:var(--r-sm);height:28px;width:28px;cursor:pointer;line-height:1}
#pv-lots button.x:hover{background:var(--critbg)}
.pv-bar{display:flex;flex-wrap:wrap;gap:8px 10px;align-items:center}
.pv-new{display:inline-flex;align-items:center;padding:1px 8px;border-radius:999px;font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;background:var(--accent-soft);color:var(--accent);vertical-align:middle;margin-left:6px}
.pv-ex{display:inline-flex;align-items:center;padding:1px 7px;border-radius:999px;font-size:10.5px;font-weight:700;letter-spacing:.06em;background:var(--warnbg);color:var(--warn);border:1px dashed color-mix(in srgb,var(--warn) 55%,transparent)}
@media (max-width:760px){.pv-ctl input[type=number]{width:100%}.pv-ctl label{flex:1 1 140px}}
'''

HTML = '''
  <div class="alerts" id="pv-alerts" data-tab="rup2"></div>

  <section class="card" data-tab="rup2">
    <div class="sec-h">
      <h2>Previsão manual de pedidos <span class="pv-new">novo</span></h2>
      <p id="pv-src">Lendo parâmetros da planilha…</p>
    </div>
    <div class="pv-ctl">
      <label>Total de pedidos no mês <input type="number" id="pv-total" min="0" step="1" placeholder="opcional"></label>
      <label>Média de pedidos/dia a alcançar <input type="number" id="pv-media" min="0" step="1"></label>
      <label>Crescimento da rampa (%/dia) <input type="number" id="pv-pct" min="0" step="1"></label>
      <label class="chk"><input type="checkbox" id="pv-move"> Ao arrastar, mover também os dias seguintes</label>
      <button type="button" class="pv-ghost" id="pv-undo">Desfazer edições</button>
    </div>
    <div class="pv-info" id="pv-info"></div>
    <div><div class="eyebrow">Pedidos por dia: histórico × manual</div><div class="chart tall pv-drag"><canvas id="cPvOrd"></canvas></div></div>
    <div class="note">Arraste um ponto da linha <b>Manual</b> para mudar a previsão daquele dia (com a opção acima, os dias seguintes acompanham). As edições e os controles ficam salvos neste navegador; “Desfazer edições” volta para os parâmetros da planilha.</div>
  </section>

  <section class="card" data-tab="rup2">
    <div class="sec-h">
      <h2>Estoque e produção por produto <span class="pv-new">novo</span></h2>
      <span class="seg" id="pv-scen"><button data-v="man">Cenário manual (rampa)</button><button data-v="hist">Cenário histórico (média 14 dias)</button></span>
    </div>
    <div class="tbl"><table id="pv-tab"></table></div>
    <div class="note" id="pv-tab-note"></div>
    <div class="pv-charts" id="pv-charts"></div>
    <div class="note">Linha cheia = estoque físico projetado · tracejada = posição (físico + programado que ainda não chegou) · faixas: <b style="color:var(--crit)">vermelha</b> até a demanda do tempo de transporte, <b style="color:var(--warn)">amarela</b> até transporte + segurança, <b style="color:var(--good)">verde</b> acima · linha vertical = ruptura.</div>
  </section>

  <section class="card" data-tab="rup2">
    <div class="sec-h">
      <h2>Produção em andamento <span class="pv-new">novo</span></h2>
      <p id="pv-lots-src"></p>
    </div>
    <div class="tbl"><table id="pv-lots"></table></div>
    <div class="pv-bar">
      <button type="button" class="btn" id="pv-add">+ Adicionar lote</button>
      <button type="button" class="pv-ghost" id="pv-copy">Copiar para a planilha</button>
      <a class="pv-ghost" href="https://docs.google.com/spreadsheets/d/1pb1Yk9Ewnfy5VYx29XGJ-JvQBPIOlD_E1QzAweiaE7Q/edit" target="_blank" rel="noopener">Abrir planilha ↗</a>
      <button type="button" class="pv-ghost danger" id="pv-reset-lots" hidden>Descartar edições locais</button>
      <span class="note" id="pv-copy-st"></span>
    </div>
    <div class="note">Entrada em estoque = envio estimado + tempo de transporte. Lotes “Recebido” saem da projeção. Para a equipe ver: <b>Copiar para a planilha</b> e colar na aba <b>Produção em andamento</b> a partir da célula A1 — o painel lê essa aba para todos. Quando há lotes aqui, eles substituem a lista de produções da aba Controle de produção.</div>
  </section>
'''

JS = r'''
/* ===================== Previsão · Produção (teste) ===================== */
const PV_DEF={transp:7,seg:5,totalMes:null,media:350,pct:0.30,horiz:45,estoque:{p:null,n:null,s:null,r:null}};
const PV_SKU=[["p","Piña","SOMAPINA","pina"],["n","Naranja","SOMANARANJA","naranja"],["s","Shaker","Shaker","shaker"],["r","Frutos Rojos","SOMAROJO","rojo"]];
const PV_KEY="soma-prev-v1";
const PV_SIT=["Em produção","Enviado","Recebido"];
let PV_SHEET={params:null,prog:[],andamento:null,st:"lendo a planilha…",ok:false};
let PVS=(()=>{try{return JSON.parse(localStorage.getItem(PV_KEY))||{}}catch(_){return{}}})();
PVS.ctl=PVS.ctl||{};PVS.edits=PVS.edits||{};PVS.scen=PVS.scen||"man";
const pvSave=()=>{try{localStorage.setItem(PV_KEY,JSON.stringify(PVS))}catch(_){}};
const pvAdd=(s,n)=>iso(addD(pd(s),n));
const pvDiff=(a,b)=>Math.round((pd(a)-pd(b))/864e5);
const pvNum=v=>{if(v==null||v==="")return null;if(typeof v==="number")return isFinite(v)?v:null;let s=String(v).trim();const pc=/%$/.test(s);s=s.replace("%","").replace(/\s/g,"");if(/,\d{1,2}$/.test(s))s=s.replace(/\./g,"").replace(",",".");else s=s.replace(/,/g,"");const x=parseFloat(s);return isFinite(x)?(pc?x/100:x):null};
const pvProdKey=s=>{s=String(s||"").toLowerCase();return /pi[nñ]a|somapina/.test(s)?"p":/naranja/.test(s)?"n":/shaker/.test(s)?"s":/rojo|frutos/.test(s)?"r":null};
const pvRGBA=(hex,a)=>{const h=String(hex).replace("#","");if(h.length<6)return hex;const n=parseInt(h.slice(0,6),16);return `rgba(${n>>16&255},${n>>8&255},${n&255},${a})`};
const pvEsc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const pvDm=s=>s?dm(s):"—";
const pvMerge=(a,b)=>{for(const k in b){const v=b[k];if(v&&typeof v==="object"&&!Array.isArray(v)&&a[k]&&typeof a[k]==="object"&&!Array.isArray(a[k]))pvMerge(a[k],v);else a[k]=v}return a};
const pvOpts=x=>pvMerge(baseOpts(),x);
const pvWd=s=>s?WD[pd(s).getDay()]+" "+dm(s):"—";

function pvParseParams(rows){
  const P={...PV_DEF,estoque:{...PV_DEF.estoque}};let hit=0;
  rows.forEach(o=>{const ks=Object.keys(o);if(ks.length<2)return;const lab=String(o[ks[0]]??"").toLowerCase().trim();if(!lab)return;const n=pvNum(o[ks[1]]);
    if(/transporte/.test(lab)){if(n!=null){P.transp=Math.max(0,Math.round(n));hit++}}
    else if(/seguran/.test(lab)){if(n!=null){P.seg=Math.max(0,Math.round(n));hit++}}
    else if(/total/.test(lab)&&/m[eê]s/.test(lab)){P.totalMes=n;hit++}
    else if(/m[eé]dia/.test(lab)){if(n!=null){P.media=n;hit++}}
    else if(/aumento|rampa|crescimento/.test(lab)){if(n!=null){P.pct=n>1?n/100:n;hit++}}
    else if(/horizonte/.test(lab)){if(n!=null){P.horiz=Math.max(7,Math.min(180,Math.round(n)));hit++}}
    else if(/estoque/.test(lab)){const k=pvProdKey(lab);if(k){P.estoque[k]=n;hit++}}});
  return hit?P:null;
}
function pvParseProg(rows){return rows.map(o=>({prod:pvProdKey(o["Produto"]),lote:"",qtd:pvNum(o["Quantidade"]),ini:null,ent:null,envio:gvDate(o["Data de embarque"]),sit:o["Situação"]||"Em produção"})).filter(x=>x.prod&&x.qtd)}
async function pvLoad(){
  const st=[];
  try{const r=await gv("Controle de produção");const P=pvParseParams(r);if(P){PV_SHEET.params=P;PV_SHEET.prog=pvParseProg(r);st.push("parâmetros: aba <b>Controle de produção</b>")}else st.push("aba <b>Controle de produção</b> não encontrada — usando os valores padrão (7 dias de transporte, 5 de segurança, 350 pedidos/dia, rampa 30%, 45 dias)")}
  catch(e){st.push("aba <b>Controle de produção</b> não encontrada — usando os valores padrão (7 dias de transporte, 5 de segurança, 350 pedidos/dia, rampa 30%, 45 dias)")}
  try{const r=await gv("Produção em andamento");if(r.length&&("Envio estimado" in r[0]))PV_SHEET.andamento=r.map(o=>({prod:pvProdKey(o["Produto"]),lote:o["Lote"]??"",qtd:pvNum(o["Quantidade"]),ini:gvDate(o["Início da produção"]),ent:gvDate(o["Entrega estimada"]),envio:gvDate(o["Envio estimado"]),sit:o["Situação"]||"Em produção"})).filter(x=>x.prod&&x.qtd)}catch(e){}
  PV_SHEET.st=st.join(" · ");PV_SHEET.ok=true;renderPrev();
}
function pvParams(){const B=PV_SHEET.params||{...PV_DEF,estoque:{...PV_DEF.estoque}};const c=PVS.ctl;
  return {...B,totalMes:("totalMes" in c)?c.totalMes:B.totalMes,media:("media" in c)?c.media:B.media,pct:("pct" in c)?c.pct:B.pct}}
const pvMed=a=>{const s=[...a].sort((x,y)=>x-y);if(!s.length)return 0;const m=s.length>>1;return s.length%2?s[m]:(s[m-1]+s[m])/2};
function pvHist(){
  const full=ROWS.filter(r=>r.d!==META.parcial);const last7=full.slice(-7),last14=full.slice(-14);
  const start=last7.reduce((a,r)=>a+r.o,0)/Math.max(1,last7.length);
  const mo=pvMed(last14.map(r=>r.o));const norm=last14.filter(r=>r.o>=0.5*mo&&r.o<=1.6*mo);
  const upo={},hu={};
  PV_SKU.forEach(([k])=>{const nb=k==="r"?full.filter(r=>(r.r||0)>=50).slice(-14):norm;const mr=pvMed(nb.map(r=>(r[k]||0)/r.o));const ok=nb.filter(r=>(r[k]||0)/r.o>=0.5*mr);const O=ok.reduce((a,r)=>a+r.o,0),U=ok.reduce((a,r)=>a+(r[k]||0),0);upo[k]=O?U/O:0;hu[k]=ok.length?U/ok.length:0});
  const ho=norm.reduce((a,r)=>a+r.o,0)/Math.max(1,norm.length);
  return {full,start,upo,hu,ho,norm,last7,last14,excl:last14.length-norm.length};
}
function pvRamp(start,target,pct,n){const out=[];let v=start;for(let k=1;k<=n;k++){if(pct>0){if(v<target)v=Math.min(target,v*(1+pct));else if(v>target)v=Math.max(target,v/(1+pct))}out.push(v)}return out}
function pvSolve(start,pct,need,rem){if(rem<=0)return null;if(need<=0)return {t:0,ok:true};let lo=0,hi=Math.max(start,need)*20+1000;const f=t=>pvRamp(start,t,pct,rem).reduce((a,b)=>a+b,0);
  if(f(hi)<need)return {t:hi,ok:false};for(let i=0;i<70;i++){const m=(lo+hi)/2;if(f(m)<need)lo=m;else hi=m}return {t:(lo+hi)/2,ok:true}}
function pvExample(){const h=META.hoje;return[
  {prod:"p",lote:"EXEMPLO-01",qtd:8000,ini:pvAdd(h,-6),ent:pvAdd(h,4),envio:pvAdd(h,5),sit:"Em produção",ex:true},
  {prod:"n",lote:"EXEMPLO-01",qtd:8000,ini:pvAdd(h,-6),ent:pvAdd(h,4),envio:pvAdd(h,5),sit:"Em produção",ex:true},
  {prod:"s",lote:"EXEMPLO-02",qtd:10000,ini:pvAdd(h,1),ent:pvAdd(h,22),envio:pvAdd(h,23),sit:"Em produção",ex:true}]}
function pvLots(){
  if(Array.isArray(PVS.lots))return {src:"local",lots:PVS.lots};
  if(PV_SHEET.andamento&&PV_SHEET.andamento.length)return {src:"sheet-and",lots:PV_SHEET.andamento};
  if(PV_SHEET.prog.length)return {src:"sheet-prog",lots:PV_SHEET.prog};
  return {src:"exemplo",lots:pvExample()};
}
function pvStock0(k,P){const m=P.estoque&&P.estoque[k];if(m!=null)return {v:m,src:"manual (planilha)"};
  const sh=Object.values(STOCK[k].bod).reduce((a,[x])=>a+x,0);const tr=(typeof melEspTotal==="function")?melEspTotal(k):0;return {v:sh+tr,src:"estimado",sh,tr}}

function pvModel(){
  const P=pvParams(),H=pvHist();const hoje=META.hoje;const N=P.horiz+P.transp+P.seg+31;
  const dates=[];for(let i=1;i<=N;i++)dates.push(pvAdd(hoje,i));
  // meta do mês (rampa que fecha o total)
  const mon=hoje.slice(0,7);const done=ROWS.filter(r=>r.d.slice(0,7)===mon).reduce((a,r)=>a+r.o,0);
  const eom=iso(new Date(pd(hoje).getFullYear(),pd(hoje).getMonth()+1,0));const rem=pvDiff(eom,hoje);
  let target=P.media,solve=null;
  if(P.totalMes){solve=pvSolve(H.start,P.pct,P.totalMes-done,rem);if(solve)target=solve.t}
  const ramp=pvRamp(H.start,target,P.pct,N);
  const man=dates.map((d,i)=>{const e=PVS.edits[d];return (e!=null&&isFinite(e))?Math.max(0,e):ramp[i]});
  const hist=dates.map(()=>H.ho);
  const lotsInfo=pvLots();
  const dem={man:{},hist:{}};PV_SKU.forEach(([k])=>{dem.man[k]=man.map(o=>o*H.upo[k]);dem.hist[k]=dates.map(()=>H.hu[k])});
  return {P,H,hoje,N,dates,done,rem,eom,target,solve,ramp,man,hist,dem,lotsInfo};
}
function pvProj(M,k,scen){
  const P=M.P,T=P.transp,S=P.seg,Hz=P.horiz,dem=M.dem[scen][k];const st=pvStock0(k,P);
  const L=M.lotsInfo.lots.filter(l=>l.prod===k&&!/receb/i.test(l.sit||"")).map(l=>{const a=l.envio?pvAdd(l.envio,T):null;let i=a?pvDiff(a,M.hoje):null;const late=i!=null&&i<1;if(late)i=1;return {...l,arr:a,i,late}});
  const prog=L.reduce((a,l)=>a+(+l.qtd||0),0);
  const pend=t=>L.filter(l=>l.i==null||l.i>t).reduce((a,l)=>a+(+l.qtd||0),0);
  const sumD=(t,n)=>{let s=0;for(let j=t;j<t+n&&j<dem.length;j++)s+=dem[j];return s};
  const fis=[st.v];for(let t=1;t<=Hz;t++){const arr=L.filter(l=>l.i===t).reduce((a,l)=>a+(+l.qtd||0),0);fis.push(fis[t-1]-dem[t-1]+arr)}
  const out=[];for(let t=0;t<=Hz;t++){const pos=fis[t]+pend(t),lr=sumD(t,T),la=sumD(t,T+S);const z=fis[t]<=0?"rup":pos<lr?"red":pos<la?"yel":"grn";out.push({t,date:pvAdd(M.hoje,t),fis:fis[t],pos,lr,la,z})}
  const first=f=>{const x=out.find(f);return x?x:null};
  const yel=first(o=>o.z!=="grn"),red=first(o=>o.z==="red"||o.z==="rup"),rup=first(o=>o.fis<=0);
  const need=sumD(0,T+S+30)-out[0].pos;const sug=need>0?Math.ceil(need/100)*100:0;
  const ud=dem[0]||0;
  return {k,st,L,prog,out,yel,red,rup,sug,ud,cov:ud>0?st.v/ud:Infinity};
}
const PV_ZL={rup:"Ruptura",red:"Vermelho",yel:"Amarelo",grn:"Verde"};
const pvZone=z=>`<span class="pv-zone ${z}">${PV_ZL[z]}</span>`;
const pvWhen=(o,hoje)=>o?(o.t===0?"<b>já hoje</b>":pvWd(o.date)):"—";

let PV_DRAG=null;
const pvRampVLine={id:"pvVLine",afterDatasetsDraw(ch,_a,opt){const i=ch.options.plugins.pvVLine&&ch.options.plugins.pvVLine.index;if(i==null||i<0)return;const x=ch.scales.x.getPixelForValue(i);const {top,bottom}=ch.chartArea;const c=ch.ctx;c.save();c.strokeStyle=ch.options.plugins.pvVLine.color;c.lineWidth=1.5;c.setLineDash([4,3]);c.beginPath();c.moveTo(x,top);c.lineTo(x,bottom);c.stroke();c.setLineDash([]);c.fillStyle=ch.options.plugins.pvVLine.color;c.font="600 11px "+css("--font");c.textAlign=x>ch.chartArea.right-80?"right":"left";c.fillText(ch.options.plugins.pvVLine.label,x+(c.textAlign==="left"?5:-5),top+12);c.restore()}};

function renderPrev(){
  if(!$("#pv-tab"))return;
  const M=pvModel(),P=M.P,H=M.H;
  // controles
  const ti=$("#pv-total"),mi=$("#pv-media"),pi=$("#pv-pct");
  if(document.activeElement!==ti)ti.value=P.totalMes??"";
  if(document.activeElement!==mi)mi.value=Math.round(P.totalMes&&M.solve?M.target:P.media);
  mi.disabled=!!(P.totalMes&&M.solve);mi.title=mi.disabled?"Calculada pelo total do mês":"";
  if(document.activeElement!==pi)pi.value=Math.round(P.pct*1000)/10;
  $("#pv-move").checked=!!PVS.move;
  $("#pv-src").innerHTML=`${PV_SHEET.st} · Hoje = <b>${pvWd(M.hoje)}</b> (último dia com dados; o histórico usa só dias completos) · horizonte ${P.horiz} dias · transporte ${P.transp} d · segurança ${P.seg} d.`;
  const nEd=Object.keys(PVS.edits).length;
  const mtxt=P.totalMes?(M.solve?(M.solve.ok?`Total do mês <b>${fmt(P.totalMes)}</b>: já feitos ${fmt(M.done)} até hoje, faltam ${fmt(Math.max(0,P.totalMes-M.done))} em ${M.rem} dias → média de chegada da rampa <b>${fmt(M.target)}</b>/dia`:`Total do mês <b>${fmt(P.totalMes)}</b> não fecha com essa rampa em ${M.rem} dias (aumente o crescimento)`):"Último dia do mês: o total não se aplica"):`Média a alcançar <b>${fmt(M.target)}</b>/dia`;
  const upo=PV_SKU.map(([k,n])=>`${n} <b>${H.upo[k].toLocaleString("pt-BR",{maximumFractionDigits:2})}</b>`).join(" · ");
  $("#pv-info").innerHTML=`<span>Partida: <b>${fmt(H.start)}</b> pedidos/dia (média ${dm(H.last7[0].d)}–${dm(H.last7.at(-1).d)})</span><span>Histórico 14 dias: <b>${fmt(H.ho)}</b> pedidos/dia${H.excl?` (${H.excl} dia(s) fora do normal excluídos)`:""}</span><span>${mtxt}</span><span>Unidades por pedido (14 dias): ${upo}</span>${nEd?`<span><b>${nEd}</b> dia(s) editado(s) à mão</span>`:""}`;
  // gráfico de pedidos
  const past=H.full.slice(-21);const labels=[...past.map(r=>r.d),...M.dates.slice(0,P.horiz)];const np=past.length;
  const real=labels.map((d,i)=>i<np?past[i].o:null);
  const hist=labels.map((d,i)=>i<np-1?null:i===np-1?past[i].o:M.hist[i-np]);
  const man=labels.map((d,i)=>i<np-1?null:i===np-1?past[i].o:M.man[i-np]);
  const edited=labels.map((d,i)=>i>=np&&PVS.edits[d]!=null);
  const acc=css("--accent"),mut=css("--muted"),wr=css("--warn");
  mk("cPvOrd",{type:"line",data:{labels:labels.map(dm),datasets:[
    {label:"Real (dias completos)",data:real,borderColor:acc,backgroundColor:acc,borderWidth:2,pointRadius:2,tension:.2},
    {label:"Histórico (média 14 dias)",data:hist,borderColor:mut,backgroundColor:mut,borderDash:[5,4],borderWidth:2,pointRadius:0,tension:0},
    {label:"Manual (rampa · arraste os pontos)",data:man,borderColor:wr,backgroundColor:wr,borderWidth:2.2,pointRadius:labels.map((d,i)=>i<np?0:edited[i]?5:3),pointHoverRadius:7,pointBackgroundColor:labels.map((d,i)=>edited[i]?css("--surface"):wr),pointBorderColor:wr,pointBorderWidth:2,tension:.15}]},
    options:pvOpts({plugins:{tooltip:{callbacks:{label:c=>c.parsed.y==null?null:` ${c.dataset.label.split(" (")[0]}: ${fmt(c.parsed.y)} pedidos`}}},scales:{y:{beginAtZero:true,ticks:{color:mut,callback:v=>fmt(v)},grid:{color:css("--line")}},x:{ticks:{color:mut,maxRotation:0,autoSkip:true,maxTicksLimit:window.innerWidth<760?6:14},grid:{display:false}}}})});
  {const cv=$("#cPvOrd");cv._pvLabels=labels;cv._pvNp=np;}
  pvBindDrag(np,labels);
  // tabela por produto
  const scen=PVS.scen;document.querySelectorAll("#pv-scen button").forEach(b=>b.classList.toggle("on",b.dataset.v===scen));
  const R=PV_SKU.map(([k])=>pvProj(M,k,scen));
  $("#pv-tab").innerHTML=`<tr><th>Produto</th><th>Estoque hoje</th><th>Programado</th><th>Un./dia</th><th>Cobertura</th><th>Zona hoje</th><th>Entra no amarelo<br><span class="note">(enviar até)</span></th><th>Entra no vermelho</th><th>Ruptura</th><th>Sugerido produzir</th></tr>`+
    R.map((r,i)=>{const [k,nome,sku]=PV_SKU[i];return `<tr><td class="prod">${nome} <span class="note">${sku}</span></td><td class="num" title="${r.st.src==="estimado"?`Shopify disponível ${fmt(r.st.sh)} + em trânsito Melonn ${fmt(r.st.tr)}`:"Estoque manual da planilha"}">${fmt(r.st.v)}</td><td class="num">${fmt(r.prog)}</td><td class="num">${fmt(r.ud)}</td><td class="num">${isFinite(r.cov)?f1(r.cov)+" d":"—"}</td><td>${pvZone(r.out[0].z)}</td><td>${pvWhen(r.yel)}</td><td>${pvWhen(r.red)}</td><td>${r.rup?(r.rup.t===0?"<b style='color:var(--crit)'>hoje</b>":`<b style="color:var(--crit)">${pvWd(r.rup.date)}</b>`):`sem ruptura em ${P.horiz} d`}</td><td class="num sug">${r.sug?fmt(r.sug):"0"}</td></tr>`}).join("");
  const li=M.lotsInfo;const late=R.flatMap(r=>r.L.filter(l=>l.late));
  $("#pv-tab-note").innerHTML=`Cenário <b>${scen==="man"?"manual":"histórico"}</b>. Estoque hoje = ${PV_SKU.map(([k,n])=>`${n}: ${pvStock0(k,P).src==="estimado"?"Shopify + trânsito Melonn":"manual"}`).join(" · ")}. Programado = lotes não recebidos (${li.src==="exemplo"?"<span class='pv-ex'>LOTES DE EXEMPLO</span>":li.src==="local"?"tabela Produção em andamento · edições deste navegador":"planilha"}). Sugerido = demanda de ${P.transp} d de transporte + ${P.seg} d de segurança + 30 d − posição atual, arredondado para cima em centenas.${late.length?` <b style="color:var(--warn)">${late.length} lote(s) com entrada já vencida e não marcados como Recebido — contados como chegando amanhã.</b>`:""}`;
  // alertas
  const al=R.filter(r=>r.out[0].z!=="grn"||r.rup).map(r=>{const nome=PV_SKU.find(x=>x[0]===r.k)[1];const z=r.out[0].z;
    const nx=r.rup?r.L.filter(l=>l.i!=null&&l.i>r.rup.t).sort((a,b)=>a.i-b.i)[0]:null;
    const gap=nx?` · próximo lote entra ${pvWd(nx.arr)} (${nx.i-r.rup.t} dia(s) sem estoque)`:(r.rup?" · nenhum lote programado depois da ruptura":"");
    const cls=(z==="rup"||z==="red"||(r.rup&&r.rup.t<=M.P.transp))?"crit":"warn";
    return `<div class="alert ${cls}"><span class="dot"></span><span><b>${nome}</b> · zona ${PV_ZL[z].toLowerCase()} hoje${r.rup?` · ruptura ${r.rup.t===0?"hoje":pvWd(r.rup.date)}`:""}${gap}${r.sug?` · sugerido produzir ${fmt(r.sug)} un.`:""}</span></div>`});
  $("#pv-alerts").innerHTML=al.join("");
  // gráficos por produto
  const box=$("#pv-charts");if(!box.dataset.ok){box.innerHTML=PV_SKU.map(([k,n])=>`<div><div class="eyebrow">${n} · estoque projetado</div><div class="chart"><canvas id="cPv_${k}"></canvas></div></div>`).join("");box.dataset.ok=1}
  const cR=css("--crit"),cY=css("--warn"),cG=css("--good");
  R.forEach(r=>{const tok=PV_SKU.find(x=>x[0]===r.k)[3];const col=css("--"+tok);const o=r.out;const lab=o.map(x=>dm(x.date));
    const top=Math.max(...o.map(x=>Math.max(x.fis,x.pos,x.la)))*1.12||1;
    mk("cPv_"+r.k,{type:"line",data:{labels:lab,datasets:[
      {label:"Faixa vermelha",data:o.map(x=>x.lr),borderWidth:0,pointRadius:0,fill:"origin",backgroundColor:pvRGBA(cR,.16),order:5},
      {label:"Faixa amarela",data:o.map(x=>x.la),borderWidth:0,pointRadius:0,fill:"-1",backgroundColor:pvRGBA(cY,.16),order:4},
      {label:"Faixa verde",data:o.map(x=>x.la),borderWidth:0,pointRadius:0,fill:"end",backgroundColor:pvRGBA(cG,.10),order:3},
      {label:"Posição",data:o.map(x=>Math.max(0,x.pos)),borderColor:col,borderDash:[5,4],borderWidth:1.6,pointRadius:0,fill:false,order:2},
      {label:"Estoque físico",data:o.map(x=>Math.max(0,x.fis)),borderColor:col,backgroundColor:col,borderWidth:2.4,pointRadius:0,pointHoverRadius:4,fill:false,order:1}]},
      options:pvOpts({plugins:{legend:{labels:{filter:i=>!/Faixa/.test(i.text)}},pvVLine:{index:r.rup?r.rup.t:-1,label:r.rup?"Ruptura "+dm(r.rup.date):"",color:cR},tooltip:{callbacks:{label:c=>/Faixa verde/.test(c.dataset.label)?null:` ${c.dataset.label.replace("Faixa vermelha","Limite vermelho").replace("Faixa amarela","Limite amarelo")}: ${fmt(c.parsed.y)}`}}},
        scales:{y:{beginAtZero:true,suggestedMax:top,ticks:{color:css("--muted"),callback:v=>fmt(v)},grid:{color:css("--line")}},x:{ticks:{color:css("--muted"),maxRotation:0,autoSkip:true,maxTicksLimit:window.innerWidth<760?5:9},grid:{display:false}}}}),plugins:[pvRampVLine]})});
  renderPvLots(M);
}
function pvBindDrag(np,labels){
  const cv=$("#cPvOrd");if(!cv||cv.dataset.pvb)return;cv.dataset.pvb=1;
  const ch=()=>CH["cPvOrd"];
  const near=e=>{const c=ch();if(!c)return null;const r=cv.getBoundingClientRect();const x=e.clientX-r.left,y=e.clientY-r.top;const meta=c.getDatasetMeta(2);let best=null,bd=1e9;
    meta.data.forEach((pt,i)=>{if(i<cv._pvNp)return;const d=Math.hypot(pt.x-x,pt.y-y);if(d<bd){bd=d;best=i}});return bd<=16?best:null};
  cv.addEventListener("pointerdown",e=>{const i=near(e);if(i==null)return;e.preventDefault();cv.setPointerCapture(e.pointerId);PV_DRAG={i,lab:cv._pvLabels,base:{...PVS.edits}}});
  cv.addEventListener("pointermove",e=>{const c=ch();if(!c)return;if(!PV_DRAG){cv.style.cursor=near(e)!=null?"ns-resize":"default";return}
    const r=cv.getBoundingClientRect();let v=c.scales.y.getValueForPixel(e.clientY-r.top);v=Math.max(0,Math.round(v));
    const M=pvModel();const L=PV_DRAG.lab;const di=PV_DRAG.i-cv._pvNp;const d0=L[PV_DRAG.i];
    const cur=k=>{const d=M.dates[k];return (PV_DRAG.base[d]!=null)?PV_DRAG.base[d]:M.ramp[k]};
    const delta=v-cur(di);const ed={...PV_DRAG.base};ed[d0]=v;
    if(PVS.move)for(let k=di+1;k<M.dates.length;k++)ed[M.dates[k]]=Math.max(0,Math.round(cur(k)+delta));
    PVS.edits=ed;const ds=c.data.datasets[2];for(let i=cv._pvNp;i<ds.data.length;i++){const d=L[i];ds.data[i]=ed[d]!=null?ed[d]:ds.data[i]}c.update("none")});
  const end=()=>{if(!PV_DRAG)return;PV_DRAG=null;pvSave();renderPrev()};
  cv.addEventListener("pointerup",end);cv.addEventListener("pointercancel",end);
}
function renderPvLots(M){
  const li=M.lotsInfo,T=M.P.transp,tb=$("#pv-lots");
  const srcTxt={local:"Fonte: <b>edições deste navegador</b> (ainda não estão na planilha — use “Copiar para a planilha”)","sheet-and":"Fonte: aba <b>Produção em andamento</b> da planilha (vale para toda a equipe)","sheet-prog":"Fonte: lista de produções da aba <b>Controle de produção</b>",exemplo:"<span class='pv-ex'>EXEMPLO</span> Nenhum lote cadastrado ainda: estes lotes são só para mostrar a tela funcionando. Edite, exclua ou adicione os reais."}[li.src];
  $("#pv-lots-src").innerHTML=srcTxt;$("#pv-reset-lots").hidden=li.src!=="local";
  const opt=(v,arr)=>arr.map(([a,b])=>`<option value="${a}"${a===v?" selected":""}>${b}</option>`).join("");
  tb.innerHTML=`<tr><th>Produto</th><th>Lote</th><th>Quantidade</th><th>Início da produção</th><th>Entrega estimada</th><th>Envio estimado</th><th>Entrada em estoque</th><th>Situação</th><th></th></tr>`+
    (li.lots.length?li.lots.map((l,i)=>`<tr data-i="${i}"><td><select data-f="prod">${opt(l.prod,PV_SKU.map(x=>[x[0],x[1]]))}</select></td><td><input type="text" data-f="lote" value="${pvEsc(l.lote)}">${l.ex?' <span class="pv-ex">EX</span>':""}</td><td><input type="number" data-f="qtd" min="0" step="100" value="${l.qtd??""}"></td><td><input type="date" data-f="ini" value="${l.ini||""}"></td><td><input type="date" data-f="ent" value="${l.ent||""}"></td><td><input type="date" data-f="envio" value="${l.envio||""}"></td><td class="calc">${l.envio?pvWd(pvAdd(l.envio,T)):"—"}</td><td><select data-f="sit">${opt(l.sit||"Em produção",PV_SIT.map(x=>[x,x]))}</select></td><td><button class="x" data-del="${i}" title="Excluir lote" aria-label="Excluir lote">×</button></td></tr>`).join(""):`<tr><td colspan="9" class="note">Nenhum lote. Use “+ Adicionar lote”.</td></tr>`);
  const own=()=>{if(!Array.isArray(PVS.lots))PVS.lots=pvLots().lots.map(l=>{const c={...l};delete c.ex;return c});return PVS.lots};
  tb.querySelectorAll("[data-f]").forEach(el=>el.onchange=()=>{const i=+el.closest("tr").dataset.i;const L=own();const f=el.dataset.f;L[i][f]=f==="qtd"?pvNum(el.value):(el.value||null);pvSave();renderPrev()});
  tb.querySelectorAll("[data-del]").forEach(b=>b.onclick=()=>{const L=own();L.splice(+b.dataset.del,1);pvSave();renderPrev()});
}
function pvTSV(){const L=pvLots().lots;return ["Produto\tLote\tQuantidade\tInício da produção\tEntrega estimada\tEnvio estimado\tSituação",...L.map(l=>[PV_SKU.find(x=>x[0]===l.prod)[1],l.lote||"",l.qtd??"",l.ini||"",l.ent||"",l.envio||"",l.sit||""].join("\t"))].join("\n")}
(function(){
  const num=v=>v===""?null:pvNum(v);
  $("#pv-total").onchange=e=>{PVS.ctl.totalMes=num(e.target.value);pvSave();renderPrev()};
  $("#pv-media").onchange=e=>{const v=num(e.target.value);if(v!=null){PVS.ctl.media=v;pvSave();renderPrev()}};
  $("#pv-pct").onchange=e=>{const v=num(e.target.value);if(v!=null){PVS.ctl.pct=v/100;pvSave();renderPrev()}};
  $("#pv-move").onchange=e=>{PVS.move=e.target.checked;pvSave()};
  $("#pv-undo").onclick=()=>{PVS.edits={};PVS.ctl={};pvSave();renderPrev()};
  $("#pv-scen").onclick=e=>{const b=e.target.closest("button[data-v]");if(!b)return;PVS.scen=b.dataset.v;pvSave();renderPrev()};
  $("#pv-add").onclick=()=>{if(!Array.isArray(PVS.lots))PVS.lots=pvLots().lots.filter(l=>!l.ex).map(l=>({...l}));PVS.lots.push({prod:"p",lote:"",qtd:null,ini:META.hoje,ent:null,envio:null,sit:"Em produção"});pvSave();renderPrev()};
  $("#pv-reset-lots").onclick=()=>{if(!confirm("Descartar as edições de lotes deste navegador e voltar para a planilha?"))return;delete PVS.lots;pvSave();renderPrev()};
  $("#pv-copy").onclick=async()=>{const t=pvTSV();try{await navigator.clipboard.writeText(t);$("#pv-copy-st").textContent="Copiado (com cabeçalho). Cole na aba Produção em andamento, célula A1."}catch(_){$("#pv-copy-st").textContent="Não consegui copiar automaticamente; selecione a tabela e copie."}};
  new MutationObserver(()=>{try{renderPrev()}catch(e){console.error(e)}}).observe(document.documentElement,{attributes:true,attributeFilter:["data-theme"]});
  try{renderPrev()}catch(e){console.error(e)}
  pvLoad();
})();
'''
