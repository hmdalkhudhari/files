#!/usr/bin/env python3
"""Builds /followers-7000/ and /claude-sales-employee/ people-file pages (AR+EN steps, copy buttons)."""
import re, pathlib, html, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build2 as B
E_ = html.escape
ROOT = pathlib.Path(__file__).parent.parent
AR = B.AR

def sec(i, title, inner):
    return f'<section id="s{i}"><h2>{AR(i)}. {E_(title)}</h2><div class="card">{inner}</div></section>'
def pr(label, text, hint=''):
    h = f'<p class="hint">{E_(hint)}</p>' if hint else ''
    return f'<div class="lab">{E_(label)}</div>{B.pbox(text)}{h}'
def go(url, txt):
    return f'<a class="go" href="{E_(url)}" target="_blank" rel="noopener">{E_(txt)}</a>'
def fin(pg, slug):
    pg = pg.replace('href="../../../library/"', 'href="../library/"')
    pg = re.sub(r'<a href="[^"]*\.pdf" download>PDF</a>', '', pg)
    out = ROOT / slug; out.mkdir(exist_ok=True); (out / 'index.html').write_text(pg, encoding='utf8'); print('wrote', out / 'index.html')

# ================= 7000 followers =================
S1 = [('افتح Claude: الإعدادات (Settings) ← الموصلات (Connectors)', 'Open Claude: Settings → Connectors'),
      ('اضغط تصفح الموصلات (Browse connectors) وابحث عن Metricool', 'Click Browse connectors and search for Metricool'),
      ('اضغط Connect وسجل دخول بحساب متريكول', 'Click Connect and sign in with your Metricool account')]
S2 = [('من نفس الصفحة اضغط إضافة موصل مخصص (Add custom connector)', 'On the same page click Add custom connector'),
      ('الصق رابط Meedro MCP اللي تلقاه داخل حسابك بميدرو', 'Paste the Meedro MCP link you find inside your Meedro account'),
      ('اضغط Connect وسجل دخول بميدرو', 'Click Connect and sign in to Meedro'),
      ('بمحادثة جديدة: زر الأدوات ← فعّل متريكول وميدرو الاثنين', 'In a new chat: tools button → turn on both Metricool and Meedro')]
P1 = ('شوف اللي منزله بحسابي بمتريكول وشنو يحتاج تعديل. عطني قائمة بالتعديلات وشلون أعدل كل وحدة.\n'
      'Look at what I have posted on my Metricool account and tell me what needs fixing. Give me a list of changes and how to make each one.')
P2 = ('من ميدرو شوف مجالي والفيديوات اللي راحت فايرال بالضبط، وهوكاتها وقوالبها. بعدين سوّ لي خطة شهر كاملة، ورجع لمتريكول وسوّ جدول الفيديوات، وحط خطة نعيد فيها الفيديوات الفايرال اللي جابت مشاهدات مرة ثانية.\n'
      'Use Meedro to look at my niche and the videos that went viral, with their hooks and templates. Then build me a full 30-day plan, go back to Metricool and set up the posting schedule, and add a plan to repost the viral ones that already performed.')
body1 = (
 '<p class="lead" style="margin-top:22px">الطريقة اللي زدت فيها ٧ آلاف متابع بأقل من شهر: تربط Claude بأداتين (ميدرو ومتريكول) وتعطيه جملتين. ٤ خطوات.</p>'
 + sec(1, 'اربط متريكول بـClaude', B.steps(S1) + go('https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities', 'دليل الموصلات من Claude ←'))
 + sec(2, 'اربط ميدرو بـClaude', B.steps(S2) + go('https://meedro.ai', 'افتح ميدرو ←'))
 + sec(3, 'الأمر الأول: متريكول يفحص حسابك', pr('الصق هذا لـClaude · Paste to Claude', P1, 'يعطيك قائمة بالتعديلات وشلون تسويها.'))
 + sec(4, 'الأمر الثاني: ميدرو يطلع لك خطة شهر', pr('الصق هذا لـClaude · Paste to Claude', P2, 'بعدها يرجع لمتريكول ويسوي الجدول وخطة إعادة الفايرال.')))
sects1 = [('s1', '١. اربط متريكول'), ('s2', '٢. اربط ميدرو'), ('s3', '٣. الأمر الأول'), ('s4', '٤. الأمر الثاني')]
pg = B.page('٧٠٠٠ متابع بأقل من شهر بالـAI', 'ملف مجاني', 'زدت <em>٧٠٠٠ متابع</em> بأقل من شهر',
            'اربط ميدرو ومتريكول بـClaude وانسخ الأمرين. الخطوات عربي وإنجليزي.', sects1, body1,
            'خطوات الربط من دليل Claude الرسمي. © حمد الخضري @hmdalkhudhari', slug='followers-7000', cprompt=B.CPR('followers-7000'))
fin(pg, 'followers-7000')

# ================= sales employee =================
T1 = [('اربط Gmail بـClaude: الإعدادات (Settings) ← الموصلات (Connectors) ← تصفح ← Gmail ← Connect', 'Connect Gmail: Settings → Connectors → Browse → Gmail → Connect'),
      ('اربط Google Sheets بنفس الطريقة (لتسجيل كل إيميل بجدول)', 'Connect Google Sheets the same way (to log every email in a sheet)'),
      ('سوّ جدول فاضي بأعمدة: الشركة، الإيميل، التاريخ، الحالة، الرد', 'Make an empty sheet with columns: Company, Email, Date, Status, Reply')]
T2 = [('افتح محادثة جديدة وفعّل Gmail وSheets من زر الأدوات', 'Open a new chat and turn on Gmail and Sheets from the tools button'),
      ('الصق الأمر تحت وخلّه يسوي أول دفعة كمسودات (Drafts) عشان تراجعها', 'Paste the command below and let it make the first batch as drafts so you can review them'),
      ('إذا عجبتك المسودات، خله يرسل ويسجل بالجدول', 'If the drafts look good, tell it to send and log them in the sheet')]
T3 = [('حط الأمر كمهمة مجدولة (Scheduled task) بـClaude: كل يوم ٩ الصبح', 'Save the command as a Scheduled task in Claude: every day at 9 AM'),
      ('كل يوم راجع الردود بنفسك وردّ على المهم', 'Check the replies yourself every day and answer the important ones')]
C1 = ('كل يوم الساعة ٩ الصبح سوّ التالي:\n'
      '١. دور على ١٠ شركات [بلدك/مجالك] جديدة غير الموجودة بجدول [اسم الجدول].\n'
      '٢. ادخل موقع كل شركة والتقط الإيميل الرسمي لها (من صفحة تواصل معنا فقط).\n'
      '٣. اكتب لكل شركة إيميل قصير فيه فكرة على شغلهم هم، مو قالب واحد للكل.\n'
      '٤. أرفق إحصائيات حسابي [ملف/رابط] وأرسل من إيميلي.\n'
      '٥. سجل كل شركة بالجدول: الاسم، الإيميل، التاريخ، الحالة.\n'
      '٦. إذا ما لقيت إيميل رسمي، تخطى الشركة ولا تخمن.\n\n'
      'Every day at 9 AM: 1) find 10 new [country/industry] companies not already in [sheet name]; 2) open each website and take the official email from the contact page only; '
      '3) write each one a short email with an idea based on their own business, not one template; 4) attach my account stats and send from my email; '
      '5) log each company in the sheet: name, email, date, status; 6) if there is no official email, skip it, never guess.')
C2 = ('Subject: [Company] x @[your handle]: [your best number] in 30 days, let\'s work together\n\n'
      'Hi [Company] team,\n\n'
      "I'm [your name], a [country] [your niche] content creator (@[your handle]). In the last 30 days my reels reached [views] views and [viewers] viewers, with [shares] shares and [saves] saves. [One line about your audience, e.g. its location.]\n\n"
      '[One sentence about their product and why your audience wants it.]\n\n'
      "I'd love to create something that gets your product in front of this audience: an Arabic tutorial reel, a collab post and a story, with a direct link to you.\n\n"
      'Attached: my official Instagram insights (last 30 days). My Media Kit with formats and past work: [your media kit link]\n\n'
      'If you prefer another way of collaborating, just let us know and we will make it work.\n\n'
      'If it sounds interesting, reply with a good time for a quick call and I will send a concrete idea for [Company].\n\n'
      'Best regards,\n[Your name] | @[your handle]\n\n'
      '---\n\n'
      'الموضوع: [الشركة] × [اسمك]: [أفضل رقم] بـ٣٠ يوم، خلنا نشتغل مع بعض\n\n'
      'هلا فريق [الشركة]،\n\n'
      'أنا [اسمك]، صانع محتوى [مجالك] من [بلدك] (@[حسابك]). آخر ٣٠ يوم وصلت ريلاتي [عدد] مشاهدة و[عدد] شخص، مع [عدد] مشاركة و[عدد] حفظ. [جملة عن جمهورك.]\n\n'
      '[جملة تناسب الشركة: ليش جمهوري يبي منتجكم.]\n\n'
      'أبي أسوي لكم شي يوصّل منتجكم لهالجمهور: ريل شرح، وCollab وستوري فيها رابط مباشر لكم.\n\n'
      'مرفق ملف إحصائيات انستقرام الرسمي (آخر ٣٠ يوم)، وهذا الميديا كت فيه الصيغ وشغلنا السابق: [رابط الميديا كت]\n\n'
      'إذا تبون طريقة تعاون ثانية قولوا لنا ونرتبها.\n\n'
      'إذا عجبتكم الفكرة، عطونا وقت لمكالمة قصيرة وأرسل لكم فكرة جاهزة خاصة بـ[الشركة].\n\n'
      'تحياتي،\n[اسمك] | @[حسابك]')
body2 = (
 '<p class="lead" style="margin-top:22px">خليت Claude موظف مبيعات: يلقط الشركات والإيميلات ويكتب ويرسل ويسجل بجدول. ٣ خطوات وقالب إيميل.</p>'
 + sec(1, 'جهّز الموصلات والجدول', B.steps(T1) + go('https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities', 'دليل الموصلات من Claude ←'))
 + sec(2, 'جرب أول دفعة', B.steps(T2) + pr('الأمر · The command', C1, 'بدّل اللي بين [ ] بمعلوماتك. ابدأ بمسودات وراجعها قبل الإرسال.'))
 + sec(3, 'خلّه يشتغل كل يوم', B.steps(T3))
 + sec(4, 'قالب الإيميل (إنجليزي + عربي)', pr('القالب · Email template', C2, 'بدّل اللي بين [ ] بأرقامك ومعلوماتك، وجملة واحدة تناسب كل شركة.')))
sects2 = [('s1', '١. الموصلات والجدول'), ('s2', '٢. أول دفعة'), ('s3', '٣. كل يوم'), ('s4', '٤. قالب الإيميل')]
pg = B.page('خليت Claude موظف مبيعات بدالي', 'ملف مجاني', 'خليت Claude <em>موظف مبيعات</em> بدالي',
            'الخطوات الثلاث وقالب الإيميل. عربي وإنجليزي وزر نسخ.', sects2, body2,
            'خطوات الربط من دليل Claude الرسمي. © حمد الخضري @hmdalkhudhari', slug='claude-sales-employee', cprompt=B.CPR('claude-sales-employee'))
fin(pg, 'claude-sales-employee')
