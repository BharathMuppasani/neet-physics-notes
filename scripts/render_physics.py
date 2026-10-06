"""Render authored lessons and syllabus into static pages. No network required."""
import html, json, pathlib, re, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from content.physics_lessons import CHAPTERS
from content import deep as deep_layer
deep_layer.apply(CHAPTERS)
from content.visual_lessons import LABS
from content.problem_briefs import BRIEFS
from content.exemplar_practice import QUESTIONS
from content.challenge_practice import QUESTIONS as CHALLENGES
SITE=ROOT/'site'
syllabus=json.loads((ROOT/'content/syllabus.json').read_text())
escape=html.escape
banks=['q-test05','q-test06','q-solids','q-fluids-extra','q-completion','q-class11']
base=(SITE/'solids.html').read_text().split('<head>')[1].split('</head>')[0]
base=base[:base.index('<script')]
base=re.sub(r'<title>.*?</title>','<title>{title}</title>',base)
head=base+'<script src="assets/catalog.js"></script>\n<script src="assets/site.js"></script>\n'+''.join(f'<script src="assets/{b}.js"></script>\n' for b in banks)+'<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg-full.js" defer></script>\n'
def page(name,key,title,body,toc=False,scripts=''):
    (SITE/name).write_text('<!doctype html>\n<html lang="en"><head>'+head.replace('{title}',escape(title))+'</head>\n'+f'<body class="ch-mechanics" data-page="{key}"><div class="frame'+(' with-toc' if toc else '')+'">'+('<aside class="toc" aria-label="Sections"></aside>' if toc else '')+'<main class="content">'+body+'<footer class="footer">Class 11 Physics · Read the assumptions, check the units, and explain the result. Progress is saved in this browser.</footer></main></div>'+scripts+'</body></html>\n')
def hero(eyebrow,title,intro):
    return f'<header class="hero"><span class="eyebrow">{eyebrow}</span><h1>{escape(title)}</h1><p class="lede">{intro}</p></header>'
def formula(s):
    return '<div class="formula"><div class="f-title">'+escape(s['title'])+'</div><div class="f-main">\\[ '+s['formula']+' \\]</div><div class="f-where"><strong>Symbols and assumptions:</strong> '+s['symbols']+'</div></div>'
TYPES={'numerical','concept','ar','statement','multi','match','graph'}
def deep_notes(d):
    out=''
    for heading,html_body in d.get('notes',[]):
        out+=f'<div class="lesson-note"><h3>{escape(heading)}</h3><div class="prose">{html_body}</div></div>'
    return out
def deep_formulas(s,d):
    cards=[s]+list(d.get('formulas',[]))
    if len(cards)==1:
        return formula(s)
    return formula(s)+'<details class="lesson-depth"><summary>Other useful formulas</summary><div class="formula-grid">'+''.join(formula(x) for x in cards[1:])+'</div></details>'
def deep_figure(d):
    f=d.get('figure')
    if not f:
        return ''
    return '<figure class="fig">'+f['svg']+'<figcaption>'+f['caption']+'</figcaption></figure>'
def deep_examples(d):
    out=''
    for e in d.get('examples',[]):
        steps=''.join(f'<li>{x}</li>' for x in e['steps'])
        out+=('<div class="eg"><div class="eg-q"><span class="eg-tag">Worked example · '+escape(e.get('tag','Numerical'))+'</span><p>'+e['q']+'</p></div>'
              '<details><summary>Show solution</summary><div class="eg-a"><ol class="steps">'+steps+'</ol><p class="answer">Answer: '+e['answer']+'</p></div></details></div>')
    return out
def deep_practice(key,i,s,d):
    out=[]
    for n,p in enumerate(d.get('practice',[]),1):
        opts=p['options'].split('|') if isinstance(p['options'],str) else list(p['options'])
        assert len(opts)==4 and 0<=p['answer']<4 and p.get('type','numerical') in TYPES, s['id']
        out.append(dict(id=f"c11-{s['id']}-p{n}",src='c11',qno=f'{key} · {i}.{n}',topic=s['id'],type=p.get('type','numerical'),q=p['q'],opts=opts,ans=p['answer'],sol='<p>'+p['explanation']+'</p>'))
    return out

def visual_lab(lab):
    key=lab['key'];p=lab['predict']
    steps=''.join(f'<li><span class="equation-step-number">{i}</span><div><h4>{escape(s["title"])}</h4><div class="equation-step-math">\\[ {s["equation"]} \\]</div><p>{escape(s["text"])}</p></div></li>' for i,s in enumerate(lab['steps'],1))
    choices=''.join(f'<button class="btn" data-predict-choice="{i}" aria-pressed="false">{escape(t)}</button>' for i,t in enumerate(p['options']))
    recipe=''.join(f'<li>{escape(t)}</li>' for t in lab['problem_steps'])
    return f'''<figure class="physics-lab" id="lab-{key}" data-physics-lab="{key}" data-prediction-answer="{p['answer']}">
      <figcaption class="lab-heading"><span class="eyebrow">Visual experiment</span><h3>{escape(lab['title'])}</h3><p>{escape(lab['intro'])}</p></figcaption>
      <div class="lab-workbench"><div class="lab-stage"><p class="muted">The equation walkthrough below explains this experiment. Interactive controls load when JavaScript is available.</p></div><dl class="lab-metrics"></dl></div>
      <div class="lab-controls"></div><div class="lab-toolbar"><button class="btn primary" data-lab-play aria-pressed="false" hidden>Play motion</button><button class="btn" data-lab-reset>Reset experiment</button><p class="small muted" data-lab-status></p></div>
      <details class="lab-prediction"><summary>Predict before you change an input</summary><p>{escape(p['question'])}</p><div class="row">{choices}</div><p class="lab-prediction-feedback" role="status" hidden><strong></strong> {escape(p['explanation'])}</p></details>
      <div class="lab-problem-guide"><span class="eyebrow">Use this in a question</span><p>{escape(lab['use_when'])}</p><ol>{recipe}</ol></div>
      <details class="lab-equation-depth"><summary>Why the equation works · optional</summary><div class="equation-story"><ol>{steps}</ol></div></details>
      <p class="lab-assumptions"><strong>Model and symbols:</strong> {escape(lab['assumptions'])}</p>
    </figure>'''

def chapter_overview(c):
    labs=[lab for s in c['sections'] for lab in LABS.get(s['id'],[])]
    n_examples=len(c['sections'])+sum(len(s.get('deep',{}).get('examples',[])) for s in c['sections'])
    links=''.join(f'<a href="#lab-{lab["key"]}">{escape(lab["title"])}</a>' for lab in labs)
    return f'<div class="lesson-overview"><div class="lesson-overview-stats"><span><strong>{len(c["sections"])}</strong> concepts</span><span><strong>{n_examples}</strong> worked examples</span><span><strong>{len(labs)}</strong> visual experiments</span></div><p>Understand the idea → see it move → solve a question. Extra theory is there when you need it.</p><div class="experiment-links" aria-label="Jump to an experiment">{links}</div></div>'
old={}
engine=(SITE/'assets/site.js').read_text()
for k,f,label in [('solids','solids.html','Mechanical Properties of Solids'),('fluids1','fluids-1.html','Fluids I · Pressure & Flow'),('fluids2','fluids-2.html','Fluids II · Viscosity & Surface Tension')]:
    text=(SITE/f).read_text()
    old[k]=dict(key=k,page=f,label=label,volume=3,sections=re.findall(r'<section\b[^>]*\bid="([^"]+)"',text))
new={c['key']:dict(key=c['key'],page=c['key']+'.html',label=c['title'],volume=c['volume'],sections=[s['id'] for s in c['sections']]) for c in CHAPTERS}
ordered=[(new|old)[key] for v in syllabus['physics'] for row in v['chapters'] for key in row[2:]]
card_details=json.loads((ROOT/'content/chapter_cards.json').read_text())
volume_titles={1:'Foundations & Motion',2:'Forces, Energy & Rotation',3:'Gravity, Materials & Oscillations',4:'Waves & Thermal Physics'}
def chapter_card(meta, module_pages, progress=False):
    key=meta['key']
    detail=card_details[key]
    colour=detail['color']
    title={'fluids1':'Fluids I: Pressure to Bernoulli','fluids2':'Fluids II: Viscosity & Surface Tension'}.get(key,meta['label'])
    contents=f'<span class="card-k">Volume {meta["volume"]} · Module pp. {module_pages}</span><h3>{escape(title)}</h3><p>{escape(detail["description"])}</p><div class="chips">'+''.join(f'<span class="chip {colour}">{escape(label)}</span>' for label in detail['chips'])+'</div>'
    attrs=f'class="card ch-card'+(' study-card' if progress else '')+f'" style="--c: var(--{colour})"'
    if not progress:
        return f'<a {attrs} href="{meta["page"]}">{contents}</a>'
    return f'<article {attrs} data-study-chapter="{key}"><a class="chapter-card-link" href="{meta["page"]}">{contents}</a><div class="chapter-card-progress"><p data-study-summary></p><progress data-study-meter max="{len(meta["sections"])}" value="0" aria-label="{escape(title)} sections studied"></progress><p class="small" data-practice-summary></p><a data-continue-study></a><p class="small"><a href="practice.html?chapter={key}">Chapter practice →</a></p></div></article>'

def chapter_volumes(progress=False):
    body=''
    heading='h2' if progress else 'h3'
    for vol in syllabus['physics']:
        number=vol['volume']
        body+=f'<section class="chapter-volume" id="volume-{number}"><{heading} class="volume-heading">Volume {number} · {volume_titles[number]}</{heading}><div class="grid-cards">'
        for row in vol['chapters']:
            for key in row[2:]:
                body+=chapter_card((new|old)[key],row[1],progress)
        body+='</div></section>'
    return body

topics={s['id']:dict(label=s['title'],page=c['key']+'.html') for c in CHAPTERS for s in c['sections']}
(SITE/'assets/catalog.js').write_text('/* Generated by scripts/render_physics.py */\nwindow.PHYSICS_CATALOG = '+json.dumps(ordered,ensure_ascii=False)+';\nwindow.PHYSICS_TOPICS = '+json.dumps(topics,ensure_ascii=False)+';\n')
# Chapters on this week's coaching syllabus link to the one-page weekly lesson.
WEEK_BANNER='<a class="quick-banner" href="this-week.html{anchor}"><span class="qb-tag">This week</span><span class="qb-text"><strong>{title}</strong><span>Interactive models, 28 practice problems and a 5-minute recap for Module Test 7</span></span><span class="qb-go" aria-hidden="true">→</span></a>'
WEEK_BANNERS={
    'thermal-properties':WEEK_BANNER.format(anchor='',title='10.1–10.3 and 10.5 on one page, with the laws of thermodynamics and Experiment 6'),
    'thermodynamics':WEEK_BANNER.format(anchor='#thermo-laws',title='The laws of thermodynamics are on this week’s one-page lesson'),
}
questions=[]
for chapter_index,c in enumerate(CHAPTERS):
    key=c['key']
    body=hero(f'Class 11 · Coaching volume {c["volume"]} · module pp. {c["module_pages"]}',c['title'],c['intro'])
    if key in WEEK_BANNERS:
        body=body.replace('<header class="hero">','<header class="hero">'+WEEK_BANNERS[key],1)
    body+=chapter_overview(c)
    body+='<div class="row"><a class="btn" href="chapters.html">← All chapters</a><a class="btn" href="practice.html?chapter='+key+'">Practise this chapter →</a></div>'
    if c['ncert']:
        part='1' if c['ncert']<=7 else '2'
        num=c['ncert'] if part=='1' else c['ncert']-7
        url=f'https://ncert.nic.in/textbook/pdf/keph{part}{num:02}.pdf'
        body+='<p class="small muted">Textbook alignment: <a href="'+url+'">NCERT Class 11 Physics · chapter '+str(c['ncert'])+'</a>. Coaching order and separate foundation modules follow your uploaded index.</p>'
    for i,s in enumerate(c['sections'],1):
        assert len(s['options'])==4 and 0<=s['answer']<4
        offset=sum(ord(ch) for ch in s['id'])%4
        options=s['options'][offset:]+s['options'][:offset]
        question=dict(id='c11-'+s['id'],src='c11',qno=f'{key} · {i}',topic=s['id'],type='concept' if not any(ch.isdigit() for ch in s['question']) else 'numerical',q=s['question'],opts=options,ans=(s['answer']-offset)%4,sol='<p>'+s['explanation']+'</p>')
        questions.append(question)
        d=s.get('deep') or {}
        level=d.get('level','core')
        reasoning=BRIEFS.get(s['id'],s['reasoning'])
        body+=f'<section id="{s["id"]}" data-num="{i}" data-toc="{escape(s["title"],quote=True)}"><div class="sec-head"><span class="num">{i} <span class="level {level}">{ {"basic":"Basics","core":"Core","exam":"Exam"}[level] }</span></span><h2>{escape(s["title"])}</h2></div><div class="prose"><p>{s["intro"]}</p><p>{reasoning}</p></div>'
        body+=deep_formulas(s,d)
        if not LABS.get(s['id']):
            body+=deep_figure(d)
        body+=''.join(visual_lab(lab) for lab in LABS.get(s['id'],[]))
        body+='<div class="callout trap"><span class="label">Watch the assumption</span><p>'+s['trap']+'</p></div>'
        if d.get('tip'):
            body+='<details class="lesson-depth"><summary>A useful shortcut</summary>'+d['tip']+'</details>'
        body+='<div class="eg"><div class="eg-q"><span class="eg-tag">Worked example</span><p>'+s['example']+'</p></div><details><summary>Show solution</summary><div class="eg-a"><p>'+s['solution']+'</p></div></details></div>'
        examples=d.get('examples',[])
        body+=deep_examples({'examples':examples[:1]})
        if len(examples)>1:
            body+='<details class="lesson-depth"><summary>More solved problem patterns</summary>'+deep_examples({'examples':examples[1:]})+'</details>'
        if d.get('notes') or d.get('exam') or d.get('traps'):
            body+='<details class="lesson-depth theory-depth"><summary>Go deeper · extra explanation and derivations</summary>'+(deep_figure(d) if LABS.get(s['id']) else '')+deep_notes(d)
            if d.get('exam'):
                body+='<div class="callout exam"><span class="label">Question patterns</span>'+d['exam']+'</div>'
            for extra in d.get('traps',[]):
                body+='<div class="callout trap"><span class="label">Another common mistake</span><p>'+extra+'</p></div>'
            body+='</details>'
        questions+=deep_practice(key,i,s,d)
        if not LABS.get(s['id']) and s['id'] == {'units':'units-propagation','vectors':'vectors-components','linear':'linear-graphs','plane':'plane-projectiles','work':'work-theorem','rotation':'rotation-momentum','gravitation':'gravitation-variation','oscillations':'oscillations-phase','waves':'waves-travelling','thermal-properties':'thermal-properties-conduction','kinetic-theory':'kinetic-theory-speeds','thermodynamics':'thermodynamics-isothermal'}.get(key):
            body+=f'<figure class="sim concept-model" data-model="{key}"><div class="sim-head"><span class="tag">Explore</span><h4>Change an input and explain the result</h4></div><div class="model-content"></div></figure>'
        body+=f'<div class="quiz" data-topic="{s["id"]}" data-limit="{3 if d.get("practice") else 2}"><h3>Check the idea</h3></div></section>'
    body+='<div class="callout tip"><span class="label">Chapter check</span><p>Explain each formula’s symbols and conditions without looking. Solve the examples before revealing their steps, then use <a href="practice.html?chapter='+key+'">chapter practice</a> to check what needs revision.</p></div>'
    page(key+'.html',key,c['title'],body,True,'<script src="assets/sims-class11.js"></script><script src="assets/physics-labs.js"></script>')
    lesson_file=SITE/(key+'.html')
    lesson_text=lesson_file.read_text().replace('<link rel="stylesheet" href="assets/style.css">','<link rel="stylesheet" href="assets/style.css">\n<link rel="stylesheet" href="assets/physics-labs.css">')
    lesson_file.write_text(lesson_text)
questions+=CHALLENGES+QUESTIONS
(SITE/'assets/q-class11.js').write_text('/* Original concept checks + reviewed NCERT Exemplar adaptations. */\nwindow.QBANK = window.QBANK || [];\nwindow.QBANK.push(...'+json.dumps(questions,ensure_ascii=False,indent=2)+');\n')
# Make data loading identical on every existing learning page, preserving old IDs.
for f in ['index.html','solids.html','fluids-1.html','fluids-2.html','practice.html','revise.html']:
    text=(SITE/f).read_text()
    if 'assets/catalog.js' not in text:
        text=text.replace('<script src="assets/site.js">','<script src="assets/catalog.js"></script>\n<script src="assets/site.js">')
    if 'assets/q-class11.js' not in text:
        text=text.replace('<script src="assets/q-completion.js"></script>','<script src="assets/q-completion.js"></script>\n<script src="assets/q-class11.js"></script>')
        if f=='revise.html':
            text=text.replace('<script src="assets/site.js"></script>','<script src="assets/site.js"></script>\n'+''.join(f'<script src="assets/{b}.js"></script>\n' for b in banks))
    (SITE/f).write_text(text)
body=hero('Your uploaded sequence','Physics chapters','Work through four volumes in order, or return to a section you need. Fluids keeps its two-part layout; maths, vectors and friction remain separate coaching modules.')
body+=chapter_volumes(progress=True)
body+='<p><a href="syllabus.html">View the organised syllabus and source notes →</a></p>'
page('chapters.html','chapters','Physics chapters',body)
body=hero('Syllabus library','Organised syllabus','The uploaded contents pages cover Class 11: four physics volumes, three chemistry volumes and five biology units. This catalogue transcribes those books; use an official exam notice to establish current examinable scope.')
body+='<p>Images remain organised locally under <code>papers/syllabus/</code>. Their original filenames and checksums are preserved in the file manifest. One exact chemistry-volume-3 duplicate is retained separately. Physics lessons follow the uploaded chapter order.</p>'
for subject in ['physics','chemistry','biology']:
    body+=f'<section id="{subject}"><h2>{subject.title()}</h2>'
    for v in syllabus[subject]:
        title='Volume '+str(v['volume']) if 'volume' in v else 'Unit '+v['unit']
        body+='<h3>'+escape(title)+'</h3><div class="table-wrap"><table><thead><tr><th>Chapter</th><th>'+('Starts on p.' if subject=='biology' else 'Module pages')+'</th></tr></thead><tbody>'
        for row in v['chapters']:
            label=escape(row[0])
            if subject=='physics':
                label=' · '.join(f'<a href="{(new|old)[k]["page"]}">{escape((new|old)[k]["label"])}</a>' for k in row[2:])
            body+='<tr><td>'+label+'</td><td>'+str(row[1])+'</td></tr>'
        body+='</tbody></table></div>'
    body+='</section>'
body+='<section id="sources"><h2>Practice sources and review</h2><p>Original concept checks are labelled “Original NEET-style”. The source collector indexed question identifiers from the 14 official NCERT Exemplar PDFs. Selected patterns were rewritten with independent solutions and labelled “Adapted NCERT Exemplar”; they are not claimed to be NEET past-year questions.</p><p>Selection favours useful misconceptions, reasoning and numerical variety. The full collected collections are not automatically imported: source solutions can contain errors. For example, a descending lift above ground that slows has positive position, negative velocity and positive acceleration with an upward-positive axis.</p><ul>'
for source in json.loads((ROOT/'content/exemplar_sources.json').read_text()):
    body+='<li><a href="'+source['url']+'">NCERT Exemplar · '+escape(source['title'])+'</a></li>'
body+='</ul></section>'
page('syllabus.html','syllabus','Organised syllabus',body)
body=hero('Class 11 · revision','Formula reference','Read the symbols and limits alongside each relationship. Follow a chapter link if you cannot explain why the formula applies.')
body+='<div class="callout tip"><span class="label">Existing detailed reference</span><p><a href="revise.html">Solids and Fluids: formulas, ratio shortcuts and traps →</a></p></div>'
for meta in ordered:
    key=meta['key']
    body+='<section id="revision-'+key+'"><h2><a href="'+meta['page']+'">'+escape(meta['label'])+'</a></h2>'
    c=next((c for c in CHAPTERS if c['key']==key),None)
    if c:
        for entry in c['sections']:
            body+='<p class="small"><a href="'+meta['page']+'#'+entry['id']+'">Explanation and example →</a></p>'+formula(entry)+''.join(formula(x) for x in (entry.get('deep') or {}).get('formulas',[]))
    else:
        text=(SITE/meta['page']).read_text()
        for match in re.finditer(r'<div class="formula">',text):
            depth=0
            for token in re.finditer(r'<div\b[^>]*>|</div>',text[match.start():]):
                depth+= -1 if token.group().startswith('</') else 1
                if depth==0:
                    body+=text[match.start():match.start()+token.end()]
                    break
    body+='</section>'
page('formula-sheet.html','revise','Class 11 formula reference',body,True)
# Keep the approved homepage separate from lesson generation.
body=(SITE/'_home-body.html').read_text().replace('{{CHAPTER_CARDS}}',chapter_volumes())
page('index.html','home','NEET Physics Notes',body)
text=(SITE/'index.html').read_text().replace('class="ch-mechanics" data-page="home"','class="ch-home" data-page="home"')
text=text.replace('<link rel="stylesheet" href="assets/style.css">','<link rel="stylesheet" href="assets/style.css">\n<link rel="stylesheet" href="assets/home.css">')
(SITE/'index.html').write_text(text)
# Local index and a tracked public audit describe the source image organisation.
md=['# Uploaded Class 11 syllabus','',syllabus['scope'],'','Original images are preserved by filename mapping and SHA-256 in file-manifest.json. One exact chemistry volume 3 duplicate is in duplicates/.','']
for subject in ['physics','chemistry','biology']:
    md+=['## '+subject.title(),'']
    for v in syllabus[subject]:
        md+=['### '+('Volume '+str(v['volume']) if 'volume' in v else v['unit']),'']
        md += [f'- {r[0]} — '+('starts p. ' if subject=='biology' else 'pp. ')+str(r[1]) for r in v['chapters']]
        md+=['']
(ROOT/'papers/syllabus').mkdir(parents=True,exist_ok=True)
(ROOT/'papers/syllabus/README.md').write_text('\n'.join(md))
(ROOT/'docs/syllabus-catalogue.md').write_text('\n'.join(md)+'\n\nPublic catalogue: site/syllabus.html. Physics lessons: site/chapters.html. Original source images are not redistributed.\n')
print(f'Rendered {len(CHAPTERS)} new chapters, {sum(len(c["sections"]) for c in CHAPTERS)} new sections and {len(questions)} new practice questions.')
