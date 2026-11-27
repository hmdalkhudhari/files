#!/usr/bin/env python3
"""Anthropic official plugins page: reuses the approved mowjaz-shortcuts layout (css/js/footer) with plugin content."""
import re, html, pathlib
R = pathlib.Path(__file__).resolve().parents[1]
E_ = lambda s: html.escape(s, quote=True)
src = (R/'mowjaz-shortcuts/index.html').read_text(encoding='utf8')
CP = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h8"/></svg>'
MKT = 'knowledge-work-plugins'
# id, name, group, ar, en, extra commands, connectors
P = [
 ('productivity','Productivity','a','يرتب مهامك وتقويمك وإيميلك، ويحفظ سياق شغلك عشان ما تعيد الشرح كل مرة. يربط Slack وNotion وAsana وJira وMicrosoft 365.','Manages your tasks, calendar and email, and keeps context about your work so you stop repeating yourself. Connects Slack, Notion, Asana, Jira, Microsoft 365.',''),
 ('enterprise-search','Enterprise Search','a','تسأل سؤال واحد ويدوّر لك بالإيميل والشات والملفات والويكي كلها.','One question searches your email, chat, documents and wikis at once.',''),
 ('pdf-viewer','PDF Viewer','a','تفتح الـPDF وتعلّق عليه وتعبّي النماذج وتوقّع وتنزّله.','View, annotate, fill forms, sign and download PDFs.',''),
 ('marketing','Marketing','b','يكتب المحتوى، يخطط الحملة بالأهداف والقنوات والتقويم، يراجع صوت البراند، يقارن المنافسين، ويطلع تقرير الأداء. يربط Canva وHubSpot وNotion وFigma.','Drafts content, plans campaigns with objectives, channels and a calendar, reviews brand voice, briefs you on competitors, and reports performance. Connects Canva, HubSpot, Notion, Figma.','/draft-content · /campaign-plan · /brand-review · /competitive-brief · /performance-report · /seo-audit · /email-sequence'),
 ('sales','Sales','b','يبحث عن العميل، يجهزك للمكالمة، يلخص الاجتماع ويكتب المتابعة، يراجع الصفقات والبايبلاين، ويكتب التوقعات. يشتغل على CRM مالك (HubSpot، Close، Salesforce) وإيميلك.','Researches prospects, preps your calls, summarizes meetings and drafts follow-ups, reviews deals and pipeline, and writes the forecast. Works with your CRM (HubSpot, Close, Salesforce) and your email.',''),
 ('customer-support','Customer Support','b','يصنّف التكتات، يكتب الردود، يرفع المشاكل الكبيرة، ويحوّل المشكلة المحلولة لمقال بقاعدة المعرفة. يربط Intercom وHubSpot وJira.','Triages tickets, drafts replies, packages escalations, and turns resolved issues into knowledge-base articles. Connects Intercom, HubSpot, Jira.',''),
 ('product-management','Product Management','c','يكتب مواصفات الميزة، يخطط خارطة الطريق، يلخص أبحاث المستخدمين، ويحدّث أصحاب المصلحة.','Writes feature specs, plans roadmaps, synthesizes user research, and updates stakeholders.',''),
 ('design','Design','c','نقد التصميم، إدارة نظام التصميم، نصوص الواجهة، فحص الوصولية، وتسليم المطور. يربط Figma.','Design critique, design-system management, UX copy, accessibility audits, and developer handoff. Connects Figma.','/critique · /design-system · /handoff · /ux-copy · /accessibility · /research-synthesis'),
 ('engineering','Engineering','c','ستاند أب، مراجعة كود، قرارات معمارية، استجابة للأعطال، وتوثيق تقني.','Standups, code review, architecture decisions, incident response, and technical documentation.',''),
 ('finance','Finance','c','قيود اليومية، تسوية الحسابات، القوائم المالية، تحليل الفروقات، إقفال الشهر، وتجهيز التدقيق. يربط Snowflake وBigQuery وMicrosoft 365.','Journal entries, reconciliations, financial statements, variance analysis, month-end close, and audit prep. Connects Snowflake, BigQuery, Microsoft 365.',''),
 ('data','Data','c','يكتب SQL، يحلل البيانات، يبني داشبوردات، ويحوّل الأرقام لقصة واضحة.','Writes SQL, analyzes datasets, builds dashboards, and turns numbers into a clear story.',''),
 ('legal','Legal','c','مراجعة العقود، فرز اتفاقيات عدم الإفصاح (NDA)، الامتثال، تقييم المخاطر، وردود قانونية بقوالب.','Contract review, NDA triage, compliance, risk assessment, and templated legal responses.',''),
 ('human-resources','Human Resources','c','التوظيف، التعيين، تقييم الأداء، تحليل الرواتب، والسياسات.','Recruiting, onboarding, performance reviews, compensation analysis, and policies.',''),
 ('operations','Operations','c','إدارة الموردين، توثيق العمليات، إدارة التغيير، تخطيط السعة، ومتابعة الامتثال.','Vendor management, process documentation, change management, capacity planning, and compliance tracking.',''),
 ('small-business','Small Business','d','شغل المشروع الصغير كله: فواتير، فلوس، عملاء، تسويق، توظيف. كل خطوة تلمس فلوس أو عملاء تنطر موافقتك.','Runs the whole small business: invoices, cash, customers, marketing, hiring. Every step that touches money or customers waits for your approval.',''),
 ('bio-research','Bio Research','d','يربط أدوات البحث قبل السريري: البحث العلمي، تحليل الجينات، وتحديد الأهداف الدوائية.','Connects preclinical research tools: literature search, genomics analysis, target prioritization.',''),
 ('cowork-plugin-management','Cowork Plugin Management','d','تسوي بلوجن خاص بشركتك أو تعدّل الموجود على أدواتك وطريقتك.','Build your company\'s own plugin or customize an existing one for your tools and workflow.',''),
]
GROUPS = [('a','الشغل اليومي','Everyday work'),('b','التسويق والمبيعات والعملاء','Marketing, sales, customers'),('c','الأقسام الداخلية','Internal departments'),('d','متخصصة','Specialized')]
def rw(n,p):
    pid,name,g,ar,en,cmds=p
    cmd=f'claude plugin install {pid}@{MKT}'
    ex = f'<p class="hint" style="margin:6px 0 0;font-size:12.5px;color:var(--soft);direction:ltr;text-align:left">{E_(cmds)}</p>' if cmds else ''
    s = f'{name} {ar} {en} {pid}'.lower()
    return (f'<li class="rw" data-s="{E_(s)}"><div class="rt"><bdi class="cd" dir="ltr">{n}. {E_(name)}</bdi>'
            f'<button class="cp" type="button" data-t="{E_(cmd)}">{CP}<span>انسخ أمر التثبيت</span></button></div>'
            f'<div class="bi one"><span class="a">{E_(ar)}</span><span class="e" dir="ltr" style="display:block;margin-top:4px">{E_(en)}</span></div>{ex}</li>')
OVERRIDE = """
:root{--navy:#1E2A66;--ink:#1E2A66;--y:#F2C230;--mint:#F2C230;--blue:#F2C230;--paper:#F6F5F1;--soft:#5B5F73;--line:#E4E2DC}
html,body{background:#F6F5F1!important}
header{background:#fff!important;color:#1E2A66;border-bottom:1px solid #E4E2DC}
header .logo{background:url('data:image/png;base64,LOGOB64') center/contain no-repeat;background-color:transparent;padding:0;border-radius:0;width:150px;height:42px;margin:0 auto 4px;box-sizing:border-box}
.tag{color:#5B5F73}.kick{background:#F2C230;color:#1E2A66}
h1{color:#1E2A66}h1 em{color:#1E2A66;background:linear-gradient(transparent 62%,#F2C230 62%);padding:0 4px;border-radius:0}
header p{color:#5B5F73}
.gl{background:#fff;border-color:#FF5A5F}.gl b{color:#1E2A66}.gl span{background:#1E2A66;color:#fff}
.sn{background:#F2C230;color:#1E2A66}
.cd{color:#C8323A}.pc{background:#F1F0EC}.pb{background:#F4F5FA}
.go{background:linear-gradient(135deg,#F2C230,#FFD966);animation:none}.go::after{display:none}
.big{background:#F2C230}
.tab.on{background:#1E2A66;color:#fff}.chips a{background:#F2C230}
.btn.ig{background:#fff;color:#1E2A66}.btn.wa{background:#1FA855;color:#fff}
footer{background:#fff;color:#1E2A66;border-top:1px solid #E4E2DC}footer h2,footer p{color:#1E2A66}.fine{color:#5B5F73}.btn.ig{border:1.5px solid #1E2A66}
.scrl,.fab{background:rgba(30,42,102,.92);border-color:rgba(242,194,48,.75)}
.sec,.st,.rw,.cm{border-color:#E4E2DC}
.rw .cp,.cp{background:#F2C230;color:#1E2A66}.cp.ok{background:#1FA855;color:#fff}
"""
panels=''; n=0
tabs=''
for gi,(g,ar,en) in enumerate(GROUPS):
    items=[p for p in P if p[2]==g]
    rows=''
    for p in items:
        n+=1; rows+=rw(n,p)
    panels+=f'<div class="panel{"" if gi==0 else " hide"}" id="g{g}"><p class="tip">{E_(ar)} · {E_(en)}</p><ul>{rows}</ul></div>'
    tabs+=f'<button type="button" class="tab{" on" if gi==0 else ""}" data-p="g{g}">{E_(ar)} ({len(items)})</button>'
steps = [
 ('افتح claude.com/plugins واختر البلوجن وثبّته (لـClaude Cowork)','Open claude.com/plugins, pick the plugin and install it (for Claude Cowork)',('https://claude.com/plugins','claude.com/plugins ←')),
 ('لـClaude Code: أضف مستودع Anthropic مرة وحدة بالترمنال','For Claude Code: add Anthropic\'s marketplace once, in the terminal',None),
 ('بعدها ثبّت أي بلوجن بزر «انسخ أمر التثبيت» تحت','Then install any plugin with the "copy install command" button below',None),
 ('يشتغل تلقائي، والأوامر تطلع عندك مثل /sales:call-prep','It works automatically, and its commands appear like /sales:call-prep',None)]
st=''
for i,(a,e,l) in enumerate(steps,1):
    extra = f'<a class="go" href="{l[0]}" target="_blank" rel="noopener">{l[1]}</a>' if l else ''
    if i==2: extra = f'<div class="pr code"><p dir="ltr">claude plugin marketplace add anthropics/{MKT}</p></div><div class="pa"><button class="cp" type="button" data-t="claude plugin marketplace add anthropics/{MKT}">{CP}<span>انسخ الأمر</span></button></div>'
    st+=f'<li class="st"><b class="sn">{i}</b><div class="sb"><span class="a">{E_(a)}</span><span class="e" dir="ltr">{E_(e)}</span>{extra}</div></li>'
header='''<header><div class="wrap">
<div class="logo" role="img" aria-label="Hamad Alkhudhari"></div><div class="tag">Business &amp; AI</div>
<span class="kick">ملف مجاني</span>
<h1><em dir="ltr" data-n="17">17</em> بلوجن رسمي<br>من <em dir="ltr">Anthropic</em> لـClaude</h1>
<p>شنو يسوي كل واحد، وكيف تثبته بدقيقتين.</p>
<a class="gl" href="https://bznstatus.com/consult/"><b>لكم خصم خاص<i>٢٥٪</i></b><span>اضغط هنا ←</span></a>
</div></header>'''
main=f'''<main class="wrap">
<section class="how"><h2 style="margin:0">٤ خطوات بس</h2><ol class="steps">{st}</ol></section>
<hr class="sdiv">
<div class="tools"><input id="q" type="search" placeholder="دوّر: sales أو مبيعات…" autocomplete="off"><div class="tabs" role="tablist">{tabs}</div></div>
{panels}
</main>'''
b0=src.index('<header>'); b1=src.index('</main>')+len('</main>')
out=src[:b0]+header+'\n'+main+src[b1:]
last=out.index('</style>'); out=out[:last]+OVERRIDE.replace('LOGOB64',(R/'file-page-kit/logo-navy.b64').read_text().strip())+out[last:]
T='١٧ بلوجن رسمي من Anthropic لـClaude | حمد الخضري'
out=re.sub(r'<title>.*?</title>',f'<title>{T}</title>',out,count=1)
out=re.sub(r'<meta property="og:title" content="[^"]*">',f'<meta property="og:title" content="{T}">',out)
out=re.sub(r'<meta property="og:image"[^>]*>','',out)
out=re.sub(r'<meta property="og:description" content="[^"]*">','<meta property="og:description" content="شنو يسوي كل بلوجن رسمي من Anthropic وكيف تثبته">',out)
out=re.sub(r'<p class="fine">.*?</p>','<p class="fine">المصدر الرسمي: github.com/anthropics/knowledge-work-plugins وclaude.com/plugins (٢٦ نوفمبر ٢٠٢٦). البلوجنز مفتوحة المصدر وتحتاج اشتراك Claude. الصفحة الرئيسية بالمستودع تقول ١١، بس الملف الرسمي فيه ١٧ من Anthropic نفسها.</p>',out,count=1,flags=re.S)
(R/'anthropic-plugins'/'index.html').write_text(out,encoding='utf8'); print('wrote',len(out))
