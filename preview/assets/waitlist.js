/* waitlist (system): CTAs -> #buy, submit to the Apps Script endpoint (fallback: Netlify Forms) */
(function(){
 var ENDPOINT=""; /* ضع رابط Apps Script (قائمة الانتظار) هنا بعد النشر */
 var box=document.getElementById('wl'); if(!box) return;
 var f=document.getElementById('wlf'), err=box.querySelector('.err');
 function retarget(){document.querySelectorAll('a.cta[href="#"],a.cta[href="#buy"],.bsn-cta.ix-topcta').forEach(function(a){
   a.setAttribute('href','#buy'); var arr=a.querySelector('.arr'); if(arr){a.firstChild.nodeValue='سجّل اسمك بقائمة الانتظار ';} else {a.textContent=a.closest('.bar')?'سجّل اسمك':'قائمة الانتظار';}
 });}
 retarget(); setTimeout(retarget,1200); setTimeout(retarget,3500);
 f.addEventListener('submit',function(e){
  e.preventDefault(); err.hidden=true;
  var n=f.elements.name, p=f.elements.phone, m=f.elements.email, bad=null;
  [n,p].forEach(function(x){var ok=x.value.trim().length>0&&(x!==p||/^[0-9\s-]{6,15}$/.test(x.value.trim()));x.setAttribute('aria-invalid',ok?'false':'true');if(!ok&&!bad)bad=x;});
  if(m.value.trim()&&!/\S+@\S+\.\S+/.test(m.value)){m.setAttribute('aria-invalid','true');if(!bad)bad=m;}else m.setAttribute('aria-invalid','false');
  if(bad){err.textContent='كمّل الاسم ورقم الواتساب بشكل صحيح';err.hidden=false;bad.focus();return;}
  if(f.elements.company.value) return; /* honeypot */
  var d=new FormData(f); d.set('page','system-waitlist'); d.set('form-name','system-waitlist'); d.set('whatsapp',f.elements.cc.value+p.value.replace(/\D/g,'').replace(/^0+/,''));
  var btn=f.querySelector('button'); btn.disabled=true;
  function ok(){try{gtag('event','generate_lead',{form:'system_waitlist'})}catch(_){}box.classList.add('done');}
  function fail(){btn.disabled=false;err.textContent='صار خطأ بالإرسال. جرّب مرة ثانية أو كلمنا واتساب';err.hidden=false;}
  if(ENDPOINT){fetch(ENDPOINT,{method:'POST',mode:'no-cors',body:new URLSearchParams(d)}).then(ok).catch(fail);}
  else if(/netlify|bznstatus\.com$/.test(location.hostname)){fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(d).toString()}).then(function(r){r.ok?ok():fail()}).catch(fail);}
  else {ok(); box.querySelector('.ok small').hidden=false;} /* معاينة: ما يرسل شي */
 });
})();
