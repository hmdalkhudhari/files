/* Preview ideas layer — bznstatus (toggle each idea live) */
(function(){
var S=document.currentScript, PAGE=S.getAttribute('data-page'), H=document.documentElement;
var IDEAS={
 home:[['A','السهم المتحرك تحت','بكل الصفحات، يختفي بعد أول سكرول'],['H','لمعة تروح وترد على الأزرار المهمة','الأزرار الذهبية بكل الصفحات'],['L','افتتاحية: الشعار ينرسم + «بزنس ستيتس»','ونفس الشعار يتحرك عند أي انتظار أو انتقال'],['1','«BUSINESS STATUS» ضخم شفاف ورا الهيدر','يتحرك عكس السكرول'],['M','شريط لوجوات العملاء يتحرك','١٧ شركة، يوقف لما تمر عليه'],['3','ساعة الكويت الحية','بالهيدر على الكمبيوتر، وفوق العنوان بالجوال'],['4','كلمة وحدة ذهبية بالعنوان','«سوّق أذكى، مو أكثر»']],
 consult:[['M','شريط لوجوات العملاء يتحرك','١٧ شركة، يوقف لما تمر عليه'],['A','السهم المتحرك تحت','بكل الصفحات، يختفي بعد أول سكرول'],['H','لمعة تروح وترد على الأزرار المهمة','الأزرار الذهبية بكل الصفحات'],['B','خلفية الرئيسية (الخطوط الصغيرة)','نفس خلفية الهوم بكل الصفحات'],['L','افتتاحية: الشعار ينرسم + «بزنس ستيتس»','ونفس الشعار يتحرك عند أي انتظار أو انتقال'],['6','أرقامك بزوايا [ ] تعدّ','بدل الكروت العادية'],['7','الأقسام تتراكب مثل كروت','وأنت تنزل بالصفحة'],['8','زرين + شريط «احجز» ثابت','الشريط بالجوال فقط'],['K','ستايل الكت كامل','كرات ضوء بالخلفية، كروت الكت، أشرطة ذهبية، عناوين لامعة'],['F','توحيد الخط (IBM Plex)','بدل Tajawal']],
 system:[['M','شريط لوجوات العملاء يتحرك','١٧ شركة، يوقف لما تمر عليه'],['A','السهم المتحرك تحت','بكل الصفحات، يختفي بعد أول سكرول'],['H','لمعة تروح وترد على الأزرار المهمة','الأزرار الذهبية بكل الصفحات'],['B','خلفية الرئيسية (الخطوط الصغيرة)','نفس خلفية الهوم بكل الصفحات'],['G','كرة أرضية ليلية 3D','الخليج يضوي ذهبي وتغطس مع السكرول'],['3','ساعة حية فوق الكرة','توقيت الكويت بالثواني'],['L','افتتاحية: الشعار ينرسم + «بزنس ستيتس»','ونفس الشعار يتحرك عند أي انتظار أو انتقال'],['9','خريطة الخليج تنبض بالخلفية','تغطس شوي مع السكرول'],['10','إضاءة الصفحة تتغير مع كل قسم','ذهبي / أزرق / أبيض'],['11','الأقسام كبطاقات مرقمة DEPT_01','تطلع وحدة وحدة بلمعة'],['12','زر الشراء يفتح واتساب','مؤقت لين رابط الدفع'],['F','توحيد الخط (IBM Plex)','بدل Tajawal']],
 kit:[['M','شريط لوجوات العملاء يتحرك','١٧ شركة، يوقف لما تمر عليه'],['A','السهم المتحرك تحت','بكل الصفحات، يختفي بعد أول سكرول'],['H','لمعة تروح وترد على الأزرار المهمة','الأزرار الذهبية بكل الصفحات'],['B','خلفية الرئيسية (الخطوط الصغيرة)','نفس خلفية الهوم بكل الصفحات'],['L','افتتاحية: الشعار ينرسم + «بزنس ستيتس»','ونفس الشعار يتحرك عند أي انتظار أو انتقال'],['13','أشرطة ضوء ذهبية سائلة ورا جسمك','بدل الدائرة، تتبع الماوس'],['14','شبكة خطوط رفيعة مثل مجلة','٦ أعمدة'],['15','«حمد الخضري» ضخم ينزل حرف حرف','+ سطر إنجليزي رفيع'],['16','الباقة اللي تضغطها تلوّن الصفحة','والباقي يخفت'],['F','توحيد الخط (IBM Plex)','بدل Tajawal + Poppins']]
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
if(PAGE!=='home'){ document.body.insertBefore(el('div','ix-bg'),document.body.firstChild); }
/* M: marquee */
var LOGOS=[['dozzie.webp','Dozzie'],['ghrelin.webp','Ghrelin'],['hair-affair.webp','Hair Affair'],['kham.webp','Kham'],['liva.webp','Liva'],['loyac.webp','LOYAC'],['mushtari.webp','Mushtari'],['noun-line.webp','Noun Line'],['pine-wood.webp','Pine Wood'],['positive-coffee.webp','Positive Coffee'],['selvix.webp','Selvix'],['skala-spa.webp','Skála Spa'],['ymh-trading.webp','YMH Trading'],['a7rf.webp','لعبة أحرف'],['bravo.webp','Bravo'],['jakh.webp','Jakh Fabrics'],[null,'Lumen Pro'],[null,'Miel Salon']];
var tiles=LOGOS.map(function(l){ return l[0]? '<span class="t"><img src="../assets/logos/'+l[0]+'" alt="'+l[1]+'" loading="lazy"></span>' : '<span class="t txt">'+l[1]+'</span>'; }).join('');
var mq=el('section','ix-mq','<div class="lbl">اشتغلنا مع</div><div class="track">'+tiles+tiles+'</div>');
var anchor=document.querySelector('.hero, header.hero'); if(PAGE==='kit') anchor=document.querySelector('.stats')||anchor;
if(anchor) anchor.insertAdjacentElement('afterend',mq);
/* ================= HOME ================= */
if(PAGE==='home'){
  var hero=document.querySelector('.hero');
  if(hero){ hero.appendChild(el('div','ix-wm','BUSINESS STATUS'));
    addEventListener('scroll',function(){ H.style.setProperty('--ixs', (-scrollY*0.35)+'px'); },{passive:true}); }
  var t=el('section','ix-trust','<div class="in"><span class="stars"><b>★★★★★</b> خبرة أكثر من ١٠ سنوات</span><span class="lbl">اشتغلنا مع</span><span class="logos"><span><img src="../assets/lumen.jpg" alt="">Lumen Pro</span><span><img src="../assets/bravo.jpg" alt="">Bravo</span><span><img src="../assets/jakh.jpg" alt="">Jakh Fabrics</span></span></div>');
  if(hero) hero.insertAdjacentElement('afterend',t);
  var end=document.querySelector('.bsn-end');
  if(end){ var c=el('span','ix-clock','<i></i>الكويت <b>--:--</b>'); end.insertBefore(c,end.firstChild);
    var c2=el('div','ix-clock2','<i></i>الكويت الحين <b>--:--</b>'); var ht=document.querySelector('.hero .htext'); if(ht) ht.insertBefore(c2,ht.firstChild);
    function tick(){ try{ var v=new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Kuwait',hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false}).format(new Date()); c.querySelector('b').textContent=v; c2.querySelector('b').textContent=v; }catch(e){} } tick(); setInterval(tick,1000); }
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
  /* S: scroll story */
  if(img){ var story=el('section','ix-story','<div class="st"><div class="sc sc1"><img alt=""><h2>ساعة وحدة <em>معي</em></h2></div><div class="sc sc2"><div class="nums"><div><b>+٣٩</b><span>ألف متابع</span></div><div><b>+١٠</b><span>سنوات خبرة</span></div><div><b>٦٠</b><span>دقيقة أونلاين</span></div></div></div><div class="sc sc3"><h2>تطلع <em>بحلول تطبّقها</em></h2><p>مو كلام عام. خطة لمشروعك أنت.</p><a class="cta" href="#book">احجز موعدك المجاني ←</a></div><div class="bar"><i></i></div></div>');
    story.querySelector('img').src=img.src; var hdr=document.querySelector('header.hero'); if(hdr) hdr.insertAdjacentElement('afterend',story);
    function st(){ if(!H.classList.contains('iS')) return; var r=story.getBoundingClientRect(); var p=Math.min(1,Math.max(0,-r.top/(r.height-innerHeight))); story.style.setProperty('--p',p); story.classList.toggle('s1',p<.33); story.classList.toggle('s2',p>=.33&&p<.66); story.classList.toggle('s3',p>=.66); }
    addEventListener('scroll',st,{passive:true}); st(); }
  /* K: kit style */
  var orbs=el('div','ix-orbs','<i></i><i></i><i></i>'); document.body.insertBefore(orbs,document.body.firstChild);
  if(ph){ var rib2=el('div','ix-rib','<svg viewBox="0 0 600 700" preserveAspectRatio="none"><defs><linearGradient id="ixrg2" x1="0" x2="1"><stop offset="0" stop-color="#F2C230" stop-opacity="0"/><stop offset=".35" stop-color="#F2C230"/><stop offset=".65" stop-color="#FFE58A"/><stop offset="1" stop-color="#F2C230" stop-opacity="0"/></linearGradient></defs><path class="r1" d="M-60,420 C120,300 220,520 380,400 C500,310 560,360 680,300"/><path class="r2" d="M-60,520 C100,420 260,600 400,470 C520,360 580,420 680,380"/><path class="r3" d="M-60,330 C140,250 240,430 400,330 C520,260 580,300 680,240"/></svg>'); ph.insertBefore(rib2,ph.firstChild);
    addEventListener('pointermove',function(e){ H.style.setProperty('--ixx',((e.clientX/innerWidth-.5)*40)+'px'); H.style.setProperty('--ixy',((e.clientY/innerHeight-.5)*30)+'px'); },{passive:true}); }
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
  var hv=document.querySelector('.hero-visual'); if(hv){ var gl=el('div','ix-globe'); hv.appendChild(gl); var started=false;
    var gc=el('div','ix-gclock','<i></i>لايف · الكويت <b>--:--:--</b>'); gl.appendChild(gc); (function tk(){ try{ gc.querySelector('b').textContent=new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Kuwait',hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false}).format(new Date()); }catch(e){} setTimeout(tk,1000); })();
    function startGlobe(){ if(started||!H.classList.contains('iG')) return; started=true; var sc=document.createElement('script'); sc.src='https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js'; sc.onload=function(){ var T=window.THREE; var W=gl.clientWidth||520, Hh=gl.clientHeight||520;
      var ren=new T.WebGLRenderer({antialias:true,alpha:true}); ren.setPixelRatio(Math.min(2,devicePixelRatio)); ren.setSize(W,Hh); gl.appendChild(ren.domElement);
      var scene=new T.Scene(), cam=new T.PerspectiveCamera(38,W/Hh,.1,100); cam.position.set(0,0.3,4.9);
      scene.add(new T.AmbientLight(0x6f80d0,.9)); var dl=new T.DirectionalLight(0xdfe6ff,.9); dl.position.set(-3,2,4); scene.add(dl); var gd=new T.PointLight(0xF2C230,.8,7); gd.position.set(1.6,1.0,1.8); scene.add(gd);
      var grp=new T.Group(); scene.add(grp);
      var tex=new T.TextureLoader(); tex.crossOrigin='anonymous';
      var mat=new T.MeshStandardMaterial({color:0x0b1540,roughness:.9,metalness:.05,emissive:new T.Color(0xF2C230),emissiveIntensity:0});
      tex.load('https://cdn.jsdelivr.net/npm/three-globe@2.24.6/example/img/earth-night.jpg',function(t){ mat.map=t; mat.emissiveMap=t; mat.emissive.set(0xFFE2A0); mat.emissiveIntensity=.75; mat.color.set(0x3a4a9c); mat.needsUpdate=true; });
      var earth=new T.Mesh(new T.SphereGeometry(1.5,96,96),mat); grp.add(earth);
      var wire=new T.Mesh(new T.SphereGeometry(1.503,36,24),new T.MeshBasicMaterial({color:0xF2C230,wireframe:true,transparent:true,opacity:.02})); grp.add(wire);
      var atm=new T.Mesh(new T.SphereGeometry(1.56,64,64),new T.MeshBasicMaterial({color:0x5b74ff,transparent:true,opacity:.10,side:T.BackSide})); grp.add(atm);
      var glow=new T.Mesh(new T.SphereGeometry(1.68,48,48),new T.MeshBasicMaterial({color:0xF2C230,transparent:true,opacity:.035,side:T.BackSide})); grp.add(glow);
      function ll(lat,lon,r){ var ph=(90-lat)*Math.PI/180, th=(lon+180)*Math.PI/180; return new T.Vector3(-r*Math.sin(ph)*Math.cos(th), r*Math.cos(ph), r*Math.sin(ph)*Math.sin(th)); }
      var cities=[[29.37,47.98,1],[25.2,55.27,.6],[24.7,46.7,.6],[25.28,51.53,.5],[26.4,50.1,.5]]; var pins=[];
      cities.forEach(function(c){ var m=new T.Mesh(new T.SphereGeometry(.012+.01*c[2],12,12),new T.MeshBasicMaterial({color:0xF2C230})); m.position.copy(ll(c[0],c[1],1.505)); grp.add(m);
        var ring=new T.Mesh(new T.RingGeometry(.02,.03,32),new T.MeshBasicMaterial({color:0xF2C230,transparent:true,opacity:.8,side:T.DoubleSide})); ring.position.copy(ll(c[0],c[1],1.51)); ring.lookAt(new T.Vector3(0,0,0)); grp.add(ring); pins.push({r:ring,t:Math.random()*3,s:c[2]}); });
      // face the Gulf (lon ~50) toward camera
      grp.rotation.y=-(50+180)*Math.PI/180+Math.PI/2; grp.rotation.x=.25;
      var t0=performance.now();
      (function loop(now){ var dt=(now-t0)/1000; grp.rotation.y+=0.0012; pins.forEach(function(p){ var k=((dt+p.t)%3)/3; p.r.scale.setScalar(1+k*4*p.s); p.r.material.opacity=.6*(1-k); }); var sy=Math.min(1,scrollY/600); grp.position.y=-sy*1.4; grp.rotation.x=.25+sy*.5; ren.render(scene,cam); requestAnimationFrame(loop); })(t0);
      addEventListener('resize',function(){ var W=gl.clientWidth, Hh=gl.clientHeight; cam.aspect=W/Hh; cam.updateProjectionMatrix(); ren.setSize(W,Hh); }); }; document.head.appendChild(sc); }
    startGlobe(); document.addEventListener('ix-change',startGlobe); }
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
/* ================= A: arrow ================= */
document.body.appendChild(el('div','ix-arrow','<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M6 9l6 6 6-6"/></svg>'));
addEventListener('scroll',function(){ H.classList.toggle('ix-scrolled',scrollY>160); },{passive:true});
/* ================= L: intro + transitions ================= */
var intro=el('div','ix-intro','<svg viewBox="0 0 64 64"><path class="p1" d="M17 19h10a3 3 0 013 3v4a12 12 0 0012 12h3a3 3 0 013 3v4a11 11 0 01-11 11H17A11 11 0 016 45V30a11 11 0 0111-11z"/><rect class="p2" x="31" y="8" width="25" height="25" rx="8"/></svg><div class="w">Business Status</div><div class="w2">بزنس ستيتس</div><i></i>');
document.body.appendChild(intro);
var seen=false; try{ seen=sessionStorage.getItem('ix-intro')==='1'; }catch(e){}
if(H.classList.contains('iL') && !seen){ intro.classList.add('play'); try{ sessionStorage.setItem('ix-intro','1'); }catch(e){} setTimeout(function(){ intro.classList.remove('play'); intro.classList.add('done'); },2100); } else { intro.classList.add('done'); }
H.classList.add('ix-ready');
document.addEventListener('click',function(e){ var a=e.target.closest&&e.target.closest('a[href]'); if(!a||!H.classList.contains('iL')) return; var href=a.getAttribute('href'); if(!href||href.charAt(0)==='#'||a.target==='_blank'||/^(https?:|mailto:|tel:|wa\.me)/.test(href)&&!/hmdalkhudhari\.github\.io\/files\/preview/.test(href)) return; e.preventDefault(); intro.classList.remove('done'); intro.classList.add('out'); setTimeout(function(){ location.href=a.href; },700); });
addEventListener('pageshow',function(ev){ if(ev.persisted||intro.classList.contains('out')){ intro.classList.remove('out'); intro.classList.add('done'); } });
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
