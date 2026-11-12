/* v2 (Hamad 11-10 notes) */
(function(){
var H=document.documentElement;
setTimeout(function(){ H.classList.remove('ix-pre'); },4500); /* safety */
function isGold(el){ var c=getComputedStyle(el).backgroundColor, m=c.match(/\d+(\.\d+)?/g); if(!m||m.length<3) return false; var r=+m[0],g=+m[1],b=+m[2],a=m.length>3?+m[3]:1; return a>.6&&r>225&&g>170&&g<215&&b<90; }
function shine(){ document.querySelectorAll('a,button').forEach(function(el){ if(el.classList.contains('ix-gs')||el.closest('.ixp')) return; if(isGold(el)){ var r=el.getBoundingClientRect(); if(r.width<30||el.matches('.bsn-burger,.chip,.lang button')) return; el.classList.add('ix-gs'); } }); }
function init(){ shine(); setTimeout(shine,1200); setTimeout(shine,3500); document.addEventListener('ix-change',shine);
  /* system: the buy buttons blink */
  if(H.classList.contains('pg-system')) document.querySelectorAll('a.cta[href="#buy"],a.cta[href="#"],.bsn-cta.ix-topcta').forEach(function(a){ a.classList.add('ix-blink'); });
  /* rating link under the reviews block (consult) */
}
if(document.readyState!=='loading') init(); else document.addEventListener('DOMContentLoaded',init);
})();
