#!/usr/bin/env python3
"""Builds /nine-employees/ people-file page (AR+EN steps, copy buttons). Run: python3 build_nine.py"""
import re, pathlib, html, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build2 as B
E_ = html.escape
ROOT = pathlib.Path(__file__).parent.parent

def sec(i, title, inner):
    return f'<section id="s{i}"><h2>{B.AR(i)}. {E_(title)}</h2><div class="card">{inner}</div></section>'
def pr(label, text, hint=''):
    h = f'<p class="hint">{E_(hint)}</p>' if hint else ''
    return f'<div class="lab">{E_(label)}</div>{B.pbox(text)}{h}'
def go(url, txt):
    return f'<a class="go" href="{E_(url)}" target="_blank" rel="noopener">{E_(txt)}</a>'

S1 = [('افتح تطبيق Claude على الكمبيوتر (Claude Desktop) وروح لوضع Cowork', 'Open the Claude desktop app and switch to Cowork'),
      ('من القائمة اليسار اضغط Projects ثم زر +', 'In the left panel click Projects, then the + button'),
      ('اختر Start from scratch، واكتب اسم المشروع (مثلا: شركتي) ووصف قصير', 'Choose Start from scratch, then type a project name (for example: My Company) and a short description')]
S2 = [('داخل المشروع افتح خانة التعليمات (Instructions)', 'Inside the project, open the Instructions field'),
      ('الصق الأمر تحت وبدّل اللي بين [ ] بمعلومات شركتك', 'Paste the prompt below and replace what is inside [ ] with your company details'),
      ('احفظ، وهذي التعليمات تنطبق على كل مهمة داخل المشروع', 'Save it: these instructions apply to every task inside the project')]
S3 = [('داخل المشروع اكتب /schedule بأي مهمة، أو اضغط Scheduled من القائمة اليسار', 'Inside the project type /schedule in any task, or click Scheduled in the left panel'),
      ('الصق الأمر تحت، واختر التكرار: يوميا الساعة ٧ الصبح', 'Paste the prompt below and set the repeat to: daily at 7 AM'),
      ('احفظ المهمة. تشتغل بالسحابة وما يحتاج جهازك يكون شغال', 'Save the task. It runs in the cloud, so your computer does not need to be on')]
S4 = [('سوّ مهمة مجدولة ثانية بنفس الطريقة', 'Create a second scheduled task the same way'),
      ('الصق الأمر تحت، واختر التكرار: كل أحد الساعة ٧ مساء', 'Paste the prompt below and set the repeat to: every Sunday at 7 PM')]

P1 = ('أنت المدير العام لشركتي [اسم الشركة] ([وصف قصير عن مجالها]). أنا ما أتواصل مع أي موظف غيرك، وأنت توزع الشغل وترجع لي بالنتيجة.\n\n'
      'عندك ٨ موظفين، لكل واحد وصف وظيفي مكتوب:\n'
      '١. المصمم: يصمم الكاروسيل والكفرات والستوريز.\n'
      '٢. المونتير: يكتب خطة المونتاج ويراجع الفيديوهات.\n'
      '٣. الكاتب: يكتب السكربتات والكابشنات.\n'
      '٤. الناشر: يرتب الجدول وينشر بالسوشال ميديا.\n'
      '٥. الباحث: يدور عن منافسيني ومجالي ويطلع الأشياء الفايرال والمنتشرة أكثر.\n'
      '٦. المساعد اليومي: يلخص لي المهام والأخبار.\n'
      '٧. مسؤول الردود: يكتب ردود التعليقات والرسائل.\n'
      '٨. محلل الأرقام: يقرأ الإحصائيات ويقول شنو نحسن.\n'
      '(غيّر الأدوار حسب شغلك.)\n\n'
      'نظام الترقيات: كل موظف يجمع نقاط. اللي يسوي الشي صح بشكل متكرر يترقى، واللي يغلط يتعدل وصفه الوظيفي.\n\n'
      'قبل أي إرسال أو نشر لازم تعرض علي الشي وتنتظر موافقتي.\n\n'
      'You are the general manager of my company [company name] ([short description of the field]). I talk only to you; you assign the work and report back to me.\n\n'
      'You manage 8 employees, each with a written job description: designer, video editor, writer, publisher, researcher (my competitors and my field, and what is going viral), daily assistant, replies agent, and numbers analyst. (Change the roles to fit your business.)\n\n'
      'Promotion system: every employee earns points. Whoever does things right repeatedly gets promoted; whoever gets it wrong has their job description corrected.\n\n'
      'Before anything is sent or published, show it to me and wait for my approval.')
P2 = ('كل يوم الصبح اكتب لي تقرير قصير فيه:\n'
      '١. شنو لازم أسوي اليوم بالضبط (٣ مهام كحد أقصى).\n'
      '٢. أهم الأخبار بمجالي [مجالك] من آخر ٢٤ ساعة، مع مصدر كل خبر.\n'
      '٣. نقاط كل موظف وأي ترقية أو تعديل.\n\n'
      'Every morning write me a short report with: 1) exactly what I need to do today (max 3 tasks); '
      '2) the most important news in my field [your field] from the last 24 hours, with a source for each; '
      '3) each employee\'s points and any promotion or correction.')
P3 = ('كل أحد جهّز لنا اجتماع الفريق: لخص شنو صار هالأسبوع، شنو نجح وشنو لا، واقترح ٣ تحسينات على الأوصاف الوظيفية أو طريقة الشغل، وعطني القائمة أوافق عليها.\n\n'
      'Every Sunday prepare our team meeting: summarize what happened this week, what worked and what did not, '
      'and suggest 3 improvements to the job descriptions or the way we work, as a list for me to approve.')

body = (
 '<p class="lead" style="margin-top:22px">شركتي فيها ٩ موظفين كلهم داخل كلود: مدير عام وثمانية موظفين، أوصاف وظيفية ونقاط وتقرير يومي واجتماع أسبوعي. ٤ خطوات.</p>'
 + sec(1, 'سوّ مشروع للشركة', B.steps(S1) + go('https://support.claude.com/en/articles/14116274-organize-your-tasks-with-projects-in-claude-cowork', 'دليل المشاريع من Claude ←'))
 + sec(2, 'حط الفريق بالتعليمات', B.steps(S2) + pr('الصق هذا بالتعليمات · Paste into Instructions', P1, 'بدّل اللي بين [ ] بمعلومات شركتك. هذا هو المدير العام والموظفين.'))
 + sec(3, 'التقرير اليومي', B.steps(S3) + pr('الصق هذا بالمهمة · Paste into the task', P2, 'المهام المجدولة تحتاج خطة مدفوعة من Claude.') + go('https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork', 'دليل المهام المجدولة من Claude ←'))
 + sec(4, 'اجتماع الأحد', B.steps(S4) + pr('الصق هذا بالمهمة · Paste into the task', P3)))
sects = [('s1', '١. مشروع الشركة'), ('s2', '٢. الفريق'), ('s3', '٣. التقرير اليومي'), ('s4', '٤. اجتماع الأحد')]
pg = B.page('شركتي فيها ٩ موظفين ولا واحد إنسان', 'ملف مجاني', 'شركتي فيها <em>٩ موظفين</em> ولا واحد إنسان',
            'مشروع واحد بكلود، أمر واحد للفريق، ومهمتين مجدولتين. الخطوات عربي وإنجليزي وزر نسخ.', sects, body,
            'الخطوات من دليل Claude الرسمي. © حمد الخضري @hmdalkhudhari', slug='nine-employees', cprompt=B.CPR('nine-employees'))
pg = pg.replace('href="../../../library/"', 'href="../library/"')
pg = re.sub(r'<a href="[^"]*\.pdf" download>PDF</a>', '', pg)
out = ROOT / 'nine-employees'; out.mkdir(exist_ok=True); (out / 'index.html').write_text(pg, encoding='utf8'); print('wrote', out / 'index.html')
