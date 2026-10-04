"""Deepening layer for the Class 11 lessons.

Each module content/deep/<chapter>.py may define
  DEEP = {section_id: {...}}   extra teaching attached to an existing or new section
  NEW_SECTIONS = [{...}]       whole new sections inserted after an existing one
See docs/deepening-schema.md for every field. scripts/check_deep.py validates them.
"""
import importlib
import os
import pkgutil

DEEP = {}
NEW_SECTIONS = []
_only = set(filter(None, os.environ.get('DEEP_ONLY', '').split(',')))  # limit imports while drafting
for _m in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
    if _only and _m.name not in _only:
        continue
    _mod = importlib.import_module(f'{__name__}.{_m.name}')
    for _k, _v in getattr(_mod, 'DEEP', {}).items():
        assert _k not in DEEP, f'duplicate DEEP entry {_k}'
        DEEP[_k] = _v
    NEW_SECTIONS += getattr(_mod, 'NEW_SECTIONS', [])


def apply(chapters):
    """Insert NEW_SECTIONS into chapters (after their anchor) and attach DEEP dicts."""
    by_key = {c['key']: c for c in chapters}
    for s in NEW_SECTIONS:
        chapter = by_key[s['chapter']]
        ids = [x['id'] for x in chapter['sections']]
        assert s['id'] not in ids, f'duplicate section {s["id"]}'
        pos = ids.index(s['after']) + 1 if s.get('after') else len(ids)
        entry = dict(s)
        entry['options'] = s['options'].split('|') if isinstance(s['options'], str) else list(s['options'])
        chapter['sections'].insert(pos, entry)
    known = {x['id'] for c in chapters for x in c['sections']}
    for sid, d in DEEP.items():
        assert sid in known, f'DEEP entry for unknown section {sid}'
    for c in chapters:
        for x in c['sections']:
            merged = dict(x.get('deep') or {})
            merged.update(DEEP.get(x['id'], {}))
            x['deep'] = merged
    return chapters
