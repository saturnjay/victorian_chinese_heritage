#!/usr/bin/env python3
"""Regenerate TRANSLATION_AUDIT.md from the two i18n catalogues.

Each catalogue entry (text, attributes, values) becomes one register row, in
file order. English is the canonical source key; the two Chinese columns are
read from i18n-zh-hans.js and i18n-zh-hant.js respectively. Run from the
repository root:

    python3 scripts/build_translation_audit.py
"""
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HANS = ROOT / 'i18n-zh-hans.js'
HANT = ROOT / 'i18n-zh-hant.js'
OUTPUT = ROOT / 'TRANSLATION_AUDIT.md'

ENTRY_LINE = re.compile(r"^\s*,?'(.*)':\s*'(.*)'\s*,?\s*$")
SECTION_OPEN = re.compile(r'^\s*(text|attributes|values): \{')
SECTION_CLOSE = re.compile(r'^\s*\}\s*,?\s*$')
AUDIT_ROW = re.compile(
    r'^\| T\d+ \| ([^|]*) \| ([^|]*) \| [^|]* \| [^|]* '
    r'\| ([^|]*) \| ([^|]*) \| ([^|]*) \| ([^|]*) \|$'
)


def parse_catalog(path):
    """Return {section: [(english, translated), ...]} in file order."""
    sections = {}
    current = None
    for line in path.read_text(encoding='utf-8').splitlines():
        if current is None:
            match = SECTION_OPEN.match(line)
            if match:
                current = match.group(1)
                sections[current] = []
            continue
        if SECTION_CLOSE.match(line):
            current = None
            continue
        match = ENTRY_LINE.match(line)
        if match:
            key = match.group(1).replace("\\'", "'")
            value = match.group(2).replace("\\'", "'")
            sections[current].append((key, value))
    return sections


def parse_existing_reviews(path):
    """Retain human review fields when the generated register is refreshed."""
    if not path.exists():
        return {}
    reviews = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        match = AUDIT_ROW.match(line)
        if not match:
            continue
        section, english, status, reviewer, review_date, notes = (
            value.strip() for value in match.groups()
        )
        reviews[(section, english)] = (status, reviewer, review_date, notes)
    return reviews


def main():
    hans = parse_catalog(HANS)
    hant = parse_catalog(HANT)
    existing_reviews = parse_existing_reviews(OUTPUT)

    for section in ('text', 'attributes', 'values'):
        hans_keys = [key for key, _ in hans[section]]
        hant_keys = [key for key, _ in hant[section]]
        if hans_keys != hant_keys:
            raise SystemExit(
                f'Key mismatch in "{section}": '
                f'{HANS.name} has {len(hans_keys)} entries, {HANT.name} has {len(hant_keys)}.\n'
                + '\n'.join(
                    f'  - {HANS.name}: {key}'
                    for key in set(hans_keys) - set(hant_keys)
                )
                + '\n'.join(
                    f'  - {HANT.name}: {key}'
                    for key in set(hant_keys) - set(hans_keys)
                )
            )

    rows = []
    row_id = 0
    for section in ('text', 'attributes', 'values'):
        for (english, zh_hans), (_, zh_hant) in zip(hans[section], hant[section]):
            row_id += 1
            status, reviewer, review_date, notes = existing_reviews.get(
                (section, english), ('Human review required', '', '', '')
            )
            rows.append(
                f'| T{row_id:03d} | {section} | {english} | {zh_hans} | {zh_hant}'
                f' | {status} | {reviewer} | {review_date} | {notes} |'
            )

    totals = {section: len(hans[section]) for section in ('text', 'attributes', 'values')}

    header = f"""# Translation Audit — Victorian Chinese Heritage Explorer

Last generated: {date.today().strftime('%-d %B %Y')}

## Scope and provenance

This register covers every localised interface entry in `i18n-zh-hans.js` and `i18n-zh-hant.js` — the Simplified and Traditional Chinese catalogues used by the interactive map (`places.html`) and by the portal site pages (`index.html`, `people.html`, `stories.html`, `portal.html`, `donation.html`, `cemetery-methodology.html`, `cemetery-records.html`) through the shared `i18n.js` runtime. Canonical place names and item-level research records intentionally remain in English and are outside this translation register.

- English is the canonical source text used by the HTML and JavaScript.
- Simplified Chinese (`zh-Hans`) is the pre-existing catalogue, with targeted wording corrections made during the Traditional Chinese implementation.
- Traditional Chinese (`zh-Hant`) was initially converted from the Simplified Chinese catalogue with OpenCC `s2t`. It is a draft until reviewed by a fluent Traditional Chinese editor.
- Portal site entries were added on 14 August 2026 so every page can switch language in place through the existing EN / 中文 header button. They carry the same review status and are signed off the same way as the map entries.
- Placeholder tokens such as `{{name}}`, `{{number}}`, `{{year}}`, `{{count}}`, `{{dated}}`, `{{position}}`, `{{total}}`, `{{label}}` and `{{basemap}}` must remain unchanged.
- To approve an entry, replace its status, add the reviewer and review date, and record any wording decision in Notes. Keep matching changes in the relevant JavaScript catalogue.

## Status definitions

- `Human review required`: automated or inherited wording that has not been signed off.
- `Reviewed`: checked for meaning, terminology, tone, and Traditional Chinese character usage.
- `Approved`: final wording accepted for publication.

## Coverage

- Text entries: {totals['text']}
- Attribute entries: {totals['attributes']}
- Canonical value entries: {totals['values']}
- Total entries: {sum(totals.values())}

## Entry register

| ID | Section | English source | Simplified Chinese (`zh-Hans`) | Traditional Chinese (`zh-Hant`) | Status | Reviewer | Review date | Notes |
|---|---|---|---|---|---|---|---|---|
"""

    OUTPUT.write_text(header + '\n'.join(rows) + '\n', encoding='utf-8')
    print(
        f'Wrote {OUTPUT.name}: {totals["text"]} text, {totals["attributes"]} attribute, '
        f'{totals["values"]} value entries ({sum(totals.values())} total).'
    )


if __name__ == '__main__':
    main()
