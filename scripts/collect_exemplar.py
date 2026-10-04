"""Collect public NCERT Exemplar PDFs and index question numbers, never import keys.

Run manually: python3 scripts/collect_exemplar.py
Raw reference files stay in ignored papers/references. Public output contains
URLs, checksums and question identifiers only. Authored adaptations are reviewed
separately in content/exemplar_practice.json.
"""
import concurrent.futures, hashlib, json, pathlib, re, urllib.request
from pypdf import PdfReader

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEST = ROOT / 'papers/references/ncert-exemplar'
DEST.mkdir(parents=True, exist_ok=True)
NAMES = ['Units and Measurements', 'Motion in a Straight Line', 'Motion in a Plane',
         'Laws of Motion', 'Work, Energy and Power', 'Rotational Motion', 'Gravitation',
         'Solids', 'Fluids', 'Thermal Properties', 'Thermodynamics', 'Kinetic Theory',
         'Oscillations', 'Waves']

def collect(item):
    number, title = item
    url = f'https://ncert.nic.in/pdf/publication/exemplarproblem/classXI/physics/keep3{number:02}.pdf'
    target = DEST / f'keep3{number:02}.pdf'
    if not target.exists():
        with urllib.request.urlopen(url, timeout=35) as response:
            target.write_bytes(response.read())
    data = target.read_bytes()
    reader = PdfReader(target)
    text = '\n'.join(page.extract_text() for page in reader.pages)
    (target.with_suffix('.txt')).write_text(text)
    ids = sorted(set(re.findall(rf'\b{number}\.\d+\b', text)), key=lambda s: int(s.split('.')[1]))
    print(f'{title}: {len(ids)} question identifiers', flush=True)
    return dict(chapter=number, title=title, url=url, sha256=hashlib.sha256(data).hexdigest(),
                pages=len(reader.pages), question_ids=ids, collected='2026-10-04')

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    records = list(pool.map(collect, enumerate(NAMES, 2)))
(ROOT / 'content/exemplar_sources.json').write_text(json.dumps(records, indent=2) + '\n')
