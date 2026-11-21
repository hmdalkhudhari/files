// node pdf.js <index.html> <out.pdf>  — يطلع PDF من الصفحة (يحتاج playwright)
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+require('path').resolve(process.argv[2]));await p.waitForTimeout(1500);
await p.pdf({path:process.argv[3],format:'A4',printBackground:true,margin:{top:'10mm',bottom:'10mm',left:'8mm',right:'8mm'}});await b.close()})()
