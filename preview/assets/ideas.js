/* Preview ideas layer — bznstatus (toggle each idea live) */
(function(){
var S=document.currentScript, PAGE=S.getAttribute('data-page'), H=document.documentElement;
var IDEAS={
 home:[['1','«BUSINESS STATUS» ضخم شفاف ورا الهيدر','يتحرك عكس السكرول'],['2','شريط «اشتغلنا مع» + نجوم','Lumen Pro · Bravo · Jakh Fabrics'],['3','ساعة الكويت الحية بالهيدر','تطلع بالكمبيوتر فقط'],['4','كلمة وحدة ذهبية بالعنوان','«سوّق أذكى، مو أكثر»']],
 consult:[['5','صورتك تنكشف وين ما يمر الإصبع','طبقة ذهبية تنمسح وترجع'],['6','أرقامك بزوايا [ ] تعدّ','بدل الكروت العادية'],['7','الأقسام تتراكب مثل كروت','وأنت تنزل بالصفحة'],['8','زرين + شريط «احجز» ثابت','الشريط بالجوال فقط'],['F','توحيد الخط (IBM Plex)','بدل Tajawal']],
 system:[['9','خريطة الخليج تنبض بالخلفية','تغطس شوي مع السكرول'],['10','إضاءة الصفحة تتغير مع كل قسم','ذهبي / أزرق / أبيض'],['11','الأقسام كبطاقات مرقمة DEPT_01','تطلع وحدة وحدة بلمعة'],['12','زر الشراء يفتح واتساب','مؤقت لين رابط الدفع'],['F','توحيد الخط (IBM Plex)','بدل Tajawal']],
 kit:[['13','أشرطة ضوء ذهبية سائلة ورا جسمك','بدل الدائرة، تتبع الماوس'],['14','شبكة خطوط رفيعة مثل مجلة','٦ أعمدة'],['15','«حمد الخضري» ضخم ينزل حرف حرف','+ سطر إنجليزي رفيع'],['16','الباقة اللي تضغطها تلوّن الصفحة','والباقي يخفت'],['F','توحيد الخط (IBM Plex)','بدل Tajawal + Poppins']]
};
var list=IDEAS[PAGE]||[], KEY='ix-'+PAGE, state={};
try{state=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
list.forEach(function(it){ if(!(it[0] in state)) state[it[0]]=true; });
function apply(){ list.forEach(function(it){ H.classList.toggle('i'+it[0], !!state[it[0]]); }); try{localStorage.setItem(KEY,JSON.stringify(state))}catch(e){} }
apply();
function el(tag,cls,html){var e=document.createElement(tag); if(cls)e.className=cls; if(html!=null)e.innerHTML=html; return e;}
var AR=['٠','١','٢','٣','٤','٥','٦','٧','٨','٩']; function ar(n){return String(n).replace(/\d/g,function(d){return AR[d]})}
function ready(fn){ if(document.readyState!=='loading') fn(); else document.addEventListener('DOMContentLoaded',fn); }

ready(function(){
/* ================= HOME ================= */
if(PAGE==='home'){
  var hero=document.querySelector('.hero');
  if(hero){ hero.appendChild(el('div','ix-wm','BUSINESS STATUS'));
    addEventListener('scroll',function(){ H.style.setProperty('--ixs', (-scrollY*0.35)+'px'); },{passive:true}); }
  var t=el('section','ix-trust','<div class="in"><span class="stars"><b>★★★★★</b> خبرة أكثر من ١٠ سنوات</span><span class="lbl">اشتغلنا مع</span><span class="logos"><span><img src="../assets/lumen.jpg" alt="">Lumen Pro</span><span><img src="../assets/bravo.jpg" alt="">Bravo</span><span><img src="../assets/jakh.jpg" alt="">Jakh Fabrics</span></span></div>');
  if(hero) hero.insertAdjacentElement('afterend',t);
  var end=document.querySelector('.bsn-end');
  if(end){ var c=el('span','ix-clock','<i></i>الكويت <b>--:--</b>'); end.insertBefore(c,end.firstChild);
    function tick(){ try{ c.querySelector('b').textContent=new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Kuwait',hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false}).format(new Date()); }catch(e){} } tick(); setInterval(tick,1000); }
  var h1=document.querySelector('.hero h1 .ar');
  if(h1){ var orig=h1.innerHTML; var alt='سوّق <em class="ix-gw">أذكى</em>، مو أكثر.';
    function setH(){ h1.innerHTML = H.classList.contains('i4')?alt:orig; } setH(); document.addEventListener('ix-change',setH); }
}
/* ================= CONSULT ================= */
if(PAGE==='consult'){
  var ph=document.querySelector('.hero-photo'), img=ph&&ph.querySelector('img');
  if(img){ var cv=el('canvas','ix-grain'); ph.appendChild(cv); var ctx=cv.getContext('2d'), noise;
    function fit(){ var r=img.getBoundingClientRect(), p=ph.getBoundingClientRect(); cv.width=Math.max(1,r.width|0); cv.height=Math.max(1,r.height|0); cv.style.left=(r.left-p.left)+'px'; cv.style.top=(r.top-p.top)+'px'; cv.style.width=r.width+'px'; cv.style.height=r.height+'px';
      noise=document.createElement('canvas'); noise.width=cv.width; noise.height=cv.height; var nc=noise.getContext('2d'), id=nc.createImageData(noise.width,noise.height), d=id.data;
      for(var i=0;i<d.length;i+=4){ var v=180+Math.random()*75; d[i]=v; d[i+1]=v*0.78; d[i+2]=v*0.2; d[i+3]=40+Math.random()*70; } nc.putImageData(id,0,0); var hole=nc.createRadialGradient(noise.width/2,noise.height*0.3,0,noise.width/2,noise.height*0.3,noise.width*0.55); hole.addColorStop(0,'rgba(0,0,0,1)'); hole.addColorStop(1,'rgba(0,0,0,0)'); nc.globalCompositeOperation='destination-out'; nc.fillStyle=hole; nc.fillRect(0,0,noise.width,noise.height); ctx.globalCompositeOperation='source-over'; ctx.drawImage(noise,0,0); }
    img.complete?fit():img.addEventListener('load',fit); addEventListener('resize',fit);
    function wipe(e){ var r=cv.getBoundingClientRect(); var x=(e.clientX-r.left)*cv.width/r.width, y=(e.clientY-r.top)*cv.height/r.height; ctx.globalCompositeOperation='destination-out'; var g=ctx.createRadialGradient(x,y,0,x,y,70); g.addColorStop(0,'rgba(0,0,0,1)'); g.addColorStop(1,'rgba(0,0,0,0)'); ctx.fillStyle=g; ctx.beginPath(); ctx.arc(x,y,70,0,7); ctx.fill(); }
    cv.addEventListener('pointermove',wipe); cv.addEventListener('pointerdown',wipe);
    setInterval(function(){ if(!noise||!H.classList.contains('i5')) return; ctx.globalCompositeOperation='source-over'; ctx.globalAlpha=.035; ctx.drawImage(noise,0,0); ctx.globalAlpha=1; },90); }
  /* 6: count-up on .stats b (Arabic digits) */
  var io=new IntersectionObserver(function(es){ es.forEach(function(en){ if(!en.isIntersecting) return; io.unobserve(en.target); var b=en.target, tn=b.firstChild; if(!tn||tn.nodeType!==3) return; var txt=tn.nodeValue, m=txt.match(/[٠-٩\d]+/); if(!m) return; var target=parseInt(m[0].replace(/[٠-٩]/g,function(c){return AR.indexOf(c)}),10), t0=performance.now();
    (function f(now){ var k=Math.min(1,(now-t0)/1400), e=1-Math.pow(1-k,3); tn.nodeValue=txt.replace(m[0],ar(Math.round(target*e))); if(k<1) requestAnimationFrame(f); })(t0); }); },{threshold:.4});
  document.querySelectorAll('.stats b').forEach(function(b){ io.observe(b); });
  /* 8: sticky bar */
  var bar=el('div','ix-bar','<a href="#book">احجز الحين <span>←</span></a>'); document.body.appendChild(bar);
  var hh=document.querySelector('.hero'), bk=document.getElementById('book');
  function barChk(){ var past=hh? (hh.getBoundingClientRect().bottom<0):(scrollY>500); var inb=bk? (bk.getBoundingClientRect().top<innerHeight*0.6):false; bar.classList.toggle('on',past&&!inb); }
  addEventListener('scroll',barChk,{passive:true}); barChk();
}
/* ================= SYSTEM ================= */
if(PAGE==='system'){
  var map=el('div','ix-map','<svg viewBox="0 0 1000 700" preserveAspectRatio="xMidYMid slice">'+
   (function(){var g='';for(var x=0;x<=1000;x+=100)g+='<line class="grid" x1="'+x+'" y1="0" x2="'+x+'" y2="700"/>';for(var y=0;y<=700;y+=100)g+='<line class="grid" x1="0" y1="'+y+'" x2="1000" y2="'+y+'"/>';return g})()+
   '<path class="coast" d="M120,120 C200,140 260,170 300,240 C330,290 360,330 420,360 C480,390 540,400 600,440 C650,470 700,520 760,560 C820,600 900,620 980,640"/>'+
   '<path class="coast" d="M380,60 C420,120 440,180 470,230 C500,280 560,300 610,340 C660,380 700,420 740,470 C780,520 830,540 900,560"/>'+
   '<path class="kw" d="M300,235 L345,215 L380,235 L372,262 L385,290 L352,300 L318,292 L302,268 Z"/>'+
   '<path class="coast" d="M352,245 C362,255 368,262 360,274 C350,280 340,272 338,262 C338,254 345,248 352,245Z"/>'+
   '<g><circle class="ring" cx="340" cy="258" r="7" style="--d:0s"/><circle class="ping" cx="340" cy="258" r="4"/><text class="lbl" x="352" y="252">KUWAIT</text></g>'+
   '<g><circle class="ring" cx="560" cy="330" r="6" style="--d:.8s"/><circle class="ping" cx="560" cy="330" r="3"/><text class="lbl" x="570" y="326">DAMMAM</text></g>'+
   '<g><circle class="ring" cx="640" cy="400" r="6" style="--d:1.5s"/><circle class="ping" cx="640" cy="400" r="3"/><text class="lbl" x="650" y="396">DOHA</text></g>'+
   '<g><circle class="ring" cx="800" cy="560" r="6" style="--d:2.1s"/><circle class="ping" cx="800" cy="560" r="3"/><text class="lbl" x="810" y="556">DUBAI</text></g>'+
   '<g><circle class="ring" cx="430" cy="470" r="6" style="--d:.4s"/><circle class="ping" cx="430" cy="470" r="3"/><text class="lbl" x="440" y="466">RIYADH</text></g>'+
   '</svg>');
  document.body.insertBefore(map,document.body.firstChild);
  addEventListener('scroll',function(){ H.style.setProperty('--ixm',(scrollY*0.12)+'px'); },{passive:true});
  var glow=el('div','ix-glow'); document.body.insertBefore(glow,document.body.firstChild);
  var cols=['rgba(242,194,48,.22)','rgba(80,110,255,.26)','rgba(255,255,255,.14)'];
  var secs=[].slice.call(document.querySelectorAll('header.hero, body>section')); var io2=new IntersectionObserver(function(es){ es.forEach(function(en){ if(en.isIntersecting){ var k=secs.indexOf(en.target); H.style.setProperty('--ixc',cols[k%3]); } }); },{threshold:.35}); secs.forEach(function(s){io2.observe(s)});
  var lis=document.querySelectorAll('.steps li'); lis.forEach(function(li,k){ li.style.setProperty('--k',k); var d=el('span','ix-dep','DEPT_'+String(k+1).padStart(2,'0')); li.appendChild(d); });
  var io3=new IntersectionObserver(function(es){ es.forEach(function(en){ if(en.isIntersecting){ en.target.classList.add('ix-in'); io3.unobserve(en.target);} }); },{threshold:.2}); lis.forEach(function(li){io3.observe(li)});
  var cta=document.querySelector('a.cta[href="#"]'); if(cta){ var waurl='https://wa.me/96590000937?text='+encodeURIComponent('السلام عليكم، أبي أشتري نظام التسويق الذكي ($75)'); function setC(){ cta.setAttribute('href', H.classList.contains('i12')?waurl:'#'); cta.target=H.classList.contains('i12')?'_blank':''; } setC(); document.addEventListener('ix-change',setC); }
}
/* ================= KIT ================= */
if(PAGE==='kit'){
  var photo=document.querySelector('.photo');
  if(photo){ var rib=el('div','ix-rib','<svg viewBox="0 0 600 700" preserveAspectRatio="none"><defs><linearGradient id="ixrg" x1="0" x2="1"><stop offset="0" stop-color="#F2C230" stop-opacity="0"/><stop offset=".35" stop-color="#F2C230"/><stop offset=".65" stop-color="#FFE58A"/><stop offset="1" stop-color="#F2C230" stop-opacity="0"/></linearGradient></defs><path class="r1" d="M-60,420 C120,300 220,520 380,400 C500,310 560,360 680,300"/><path class="r2" d="M-60,520 C100,420 260,600 400,470 C520,360 580,420 680,380"/><path class="r3" d="M-60,330 C140,250 240,430 400,330 C520,260 580,300 680,240"/></svg>');
    photo.insertBefore(rib,photo.firstChild);
    addEventListener('pointermove',function(e){ var x=(e.clientX/innerWidth-.5)*40, y=(e.clientY/innerHeight-.5)*30; H.style.setProperty('--ixx',x+'px'); H.style.setProperty('--ixy',y+'px'); },{passive:true});
    addEventListener('scroll',function(){ H.style.setProperty('--ixy',(scrollY*0.08)+'px'); },{passive:true}); }
  document.body.appendChild(el('div','ix-lines'));
  var txt=document.querySelector('.hero .txt'), h1k=document.querySelector('.hero h1');
  if(txt&&h1k){ var nm=el('div','ix-name'); 'حمد الخضري'.split(' ').forEach(function(w,k){ var s=el('span',null,w); s.style.setProperty('--k',k); nm.appendChild(s); if(k===0) nm.appendChild(document.createTextNode(' ')); }); nm.appendChild(el('small',null,'HAMAD ALKHUDHARI · MEDIA KIT 2026')); h1k.insertAdjacentElement('beforebegin',nm); }
  document.body.appendChild(el('div','ix-pkglow'));
  document.querySelectorAll('.pk').forEach(function(pk){ pk.addEventListener('click',function(e){ if(e.target.closest('a')) return; var on=pk.classList.contains('ix-on'); document.querySelectorAll('.pk').forEach(function(p){p.classList.remove('ix-on')}); if(on){ H.classList.remove('ix-focus'); } else { pk.classList.add('ix-on'); H.classList.add('ix-focus'); } }); });
}
/* ================= PANEL ================= */
var pages=[['home','الرئيسية'],['consult','الاستشارة'],['system','النظام'],['kit','الكت']];
var btn=el('button','ixp-btn','✦ الأفكار <span>('+list.length+')</span>'); btn.type='button';
var p=el('div','ixp'); p.innerHTML='<div class="nav">'+pages.map(function(q){return '<a href="../'+q[0]+'/" class="'+(q[0]===PAGE?'cur':'')+'">'+q[1]+'</a>'}).join('')+'</div><h4>أفكار هالصفحة</h4><p>شغّل وطفّي وشوف الفرق على طول. اللي يعجبك خلّه شغال، وبعدين اضغط «انسخ اختياري» ودزه لي.</p>'+
 list.map(function(it){return '<label><span>'+it[1]+'<small>'+it[2]+'</small></span><input type="checkbox" data-k="'+it[0]+'"'+(state[it[0]]?' checked':'')+'><span class="sw"></span></label>'}).join('')+
 '<div class="row"><button type="button" data-a="all">شغّل الكل</button><button type="button" data-a="none">طفّي الكل</button><button type="button" class="g" data-a="copy">انسخ اختياري</button></div><div class="out"></div>';
document.body.appendChild(btn); document.body.appendChild(p);
btn.addEventListener('click',function(){ p.classList.toggle('open'); });
document.addEventListener('click',function(e){ if(p.classList.contains('open') && !p.contains(e.target) && e.target!==btn && !btn.contains(e.target)) p.classList.remove('open'); });
p.addEventListener('change',function(e){ var k=e.target.getAttribute('data-k'); if(!k) return; state[k]=e.target.checked; apply(); document.dispatchEvent(new Event('ix-change')); });
p.addEventListener('click',function(e){ var a=e.target.getAttribute&&e.target.getAttribute('data-a'); if(!a) return;
  if(a==='all'||a==='none'){ list.forEach(function(it){ state[it[0]]=(a==='all'); }); p.querySelectorAll('input').forEach(function(i){ i.checked=(a==='all'); }); apply(); document.dispatchEvent(new Event('ix-change')); }
  if(a==='copy'){ var name={home:'الرئيسية',consult:'الاستشارة',system:'النظام',kit:'الكت'}[PAGE]; var on=list.filter(function(it){return state[it[0]]}).map(function(it){return it[0]}); var off=list.filter(function(it){return !state[it[0]]}).map(function(it){return it[0]});
    var s=name+': أبي '+(on.length?on.join('، '):'ولا شي')+(off.length?' | لا أبي '+off.join('، '):''); var out=p.querySelector('.out');
    (navigator.clipboard&&navigator.clipboard.writeText?navigator.clipboard.writeText(s):Promise.reject()).then(function(){ out.textContent='انسخ وأرسله: '+s; }).catch(function(){ out.textContent=s; }); }
});
});
})();
