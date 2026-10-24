#!/usr/bin/env python3
"""Structural checker for translated adev markdown pages.

Compares each translated file against the English original on the `main` branch
(or UPSTREAM_REF) and reports anything that would break the adev build or silently
lose content:

  * heading count/levels must match, and every heading whose generated id differs
    from the English one must carry `{#english-id}`;
  * fenced code blocks must be identical (count and content);
  * link targets `](target)` and `href`/`path`/`imgSrc`/`src` attribute values
    must be the same multiset;
  * callout keywords (NOTE:, TIP:, ...) at line start must be preserved;
  * `<docs-step title>` count must match and translated step titles must carry `{#english-id}`;
  * in-page anchors (`#id`) must resolve to a heading or step id in the document.

Usage:
  python3 uz-tools/check-translation.py                 # all .md files changed vs main
  python3 uz-tools/check-translation.py path/to/a.md …  # specific files
Exit code 1 when a problem is found.
"""
import os
import re
import subprocess
import sys

REF = os.environ.get('UPSTREAM_REF', 'main')
CALLOUTS = ('NOTE:', 'TIP:', 'HELPFUL:', 'IMPORTANT:', 'CRITICAL:', 'TODO:', 'QUESTION:', 'TLDR:')
ATTR_RE = re.compile(r'\b(href|path|imgSrc|src)="([^"]*)"')
MDLINK_RE = re.compile(r'\]\(([^)\s]+)')
STEP_RE = re.compile(r'<docs-step[^>]*title="([^"]*)"')


def slug(heading: str) -> str:
    m = re.search(r'{#\s*([\w-]+)\s*}', heading)
    if m:
        return m.group(1)
    s = heading.lower()
    s = re.sub(r'\s|/', '-', s)
    s = re.sub(r'[^\w-]', '', s).replace('_', '')
    return s


def split(text: str):
    """Return (headings, code_blocks, prose_lines)."""
    headings, blocks, prose = [], [], []
    code, buf = False, []
    for line in text.split('\n'):
        t = line.strip()
        if t.startswith('```'):
            if code:
                blocks.append('\n'.join(buf))
                buf = []
            code = not code
            continue
        if code:
            buf.append(line)
            continue
        prose.append(line)
        m = re.match(r'^(#{2,6})\s+(.*)$', t)
        if m:
            headings.append((len(m.group(1)), m.group(2).strip()))
    return headings, blocks, prose


def multiset(items):
    d = {}
    for i in items:
        d[i] = d.get(i, 0) + 1
    return d


def diff_multiset(a, b):
    out = []
    for k in sorted(set(a) | set(b)):
        if a.get(k, 0) != b.get(k, 0):
            out.append(f'{k!r}: original×{a.get(k, 0)} translated×{b.get(k, 0)}')
    return out


def check(path: str) -> list:
    problems = []
    try:
        en = subprocess.run(['git', 'show', f'{REF}:{path}'], capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return [f'not found on {REF} (new file?) — skipped']
    uz = open(path, encoding='utf-8').read()
    eh, eb, ep = split(en)
    uh, ub, up = split(uz)

    if len(eh) != len(uh):
        problems.append(f'heading count differs: original {len(eh)}, translated {len(uh)}')
    else:
        for (el, et), (ul, ut) in zip(eh, uh):
            if el != ul:
                problems.append(f'heading level differs: "{et}" (H{el}) vs "{ut}" (H{ul})')
            eid, uid = slug(et), slug(ut)
            if eid != uid:
                problems.append(f'heading "{ut}" generates id "{uid}", expected "{eid}" — append {{#{eid}}}')

    if len(eb) != len(ub):
        problems.append(f'code block count differs: original {len(eb)}, translated {len(ub)}')
    else:
        for i, (a, b) in enumerate(zip(eb, ub)):
            if a.strip() != b.strip():
                problems.append(f'code block #{i + 1} was modified (must stay identical to the original)')

    for name, rx in (('attribute value', ATTR_RE), ('markdown link target', MDLINK_RE)):
        ea = multiset(m.group(2) if rx is ATTR_RE else m.group(1) for m in rx.finditer('\n'.join(ep)))
        ua = multiset(m.group(2) if rx is ATTR_RE else m.group(1) for m in rx.finditer('\n'.join(up)))
        for d in diff_multiset(ea, ua):
            problems.append(f'{name} changed: {d}')

    ec = multiset(l.strip().split(':')[0] + ':' for l in ep if l.strip().startswith(CALLOUTS))
    uc = multiset(l.strip().split(':')[0] + ':' for l in up if l.strip().startswith(CALLOUTS))
    for d in diff_multiset(ec, uc):
        problems.append(f'callout keyword changed/removed: {d}')

    es, us = STEP_RE.findall(en), STEP_RE.findall(uz)
    if len(es) != len(us):
        problems.append('<docs-step title=...> count differs')
    else:
        for et, ut in zip(es, us):
            if slug(et) != slug(ut):
                problems.append(f'docs-step title "{ut}" generates id "{slug(ut)}", expected "{slug(et)}" — append {{#{slug(et)}}} inside the title attribute')

    # In-page anchors (#id) must resolve to a heading or docs-step id in this document.
    ids = {slug(h) for _, h in uh} | {slug(t) for t in us}
    for m in re.finditer(r'(?:\]\(|href=")#([\w-]+)', '\n'.join(up)):
        if m.group(1) not in ids:
            problems.append(f'in-page anchor "#{m.group(1)}" has no matching heading/step id in this document')

    if uz.strip() == en.strip():
        problems.append('file is identical to the original (not translated)')
    return problems


def main(argv):
    files = argv[1:]
    if not files:
        out = subprocess.run(['git', 'diff', '--name-only', REF, '--', 'adev/src/content'],
                             capture_output=True, text=True, check=True).stdout.split()
        files = [f for f in out if f.endswith('.md') and os.path.exists(f)]
    bad = 0
    for f in files:
        probs = check(f)
        status = 'OK ' if not probs else 'ERR'
        print(f'[{status}] {f}')
        for p in probs:
            print(f'       - {p}')
        bad += bool(probs)
    print(f'\n{len(files) - bad}/{len(files)} files pass')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
