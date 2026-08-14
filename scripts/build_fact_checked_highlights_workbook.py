#!/usr/bin/env python3
"""Build a fact-check workbook from the map data embedded in index.html.

Uses only the Python standard library so the workbook is reproducible in this
repository without installing packages. With --live, cited web pages are
retrieved and their response metadata is included in the Source Audit sheet.
"""

import argparse
import concurrent.futures
import datetime as dt
import html
import json
import mimetypes
import re
import ssl
import urllib.error
import urllib.request
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
OUTPUT = ROOT / "victorian_chinese_heritage_fact_checked_highlights.xlsx"
CHECKED_ON = dt.date.today().isoformat()
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
)


def between(text, start, end):
    return text.split(start, 1)[1].split(end, 1)[0]


def extract_map_data():
    source = INDEX.read_text(encoding="utf-8")
    records = json.loads(between(source, "const DATA = ", ";\n    DATA.push("))
    additions = json.loads(
        "["
        + between(source, "    DATA.push(", ");\n    const GROUP_COLORS").replace(
            ");\n    DATA.push(", ","
        )
        + "]"
    )
    records.extend(additions)
    photos = json.loads(
        "{"
        + between(
            source,
            "      const PHOTO_BY_ID = {",
            "\n      };\n      const BURNER_CENSUS_PHOTO_BY_ID",
        )
        + "}"
    )
    burner_photos = json.loads(
        "{"
        + between(
            source,
            "      const BURNER_CENSUS_PHOTO_BY_ID = {",
            "\n      };\n      [\"VCH-003\"",
        )
        + "}"
    )
    for record_id in [
        "VCH-003",
        "VCH-022",
        "VCH-025",
        "VCH-026",
        "VCH-028",
        "VCH-074",
        "VCH-075",
    ]:
        photos[record_id] = burner_photos[record_id]
    verification = json.loads(
        "{"
        + between(
            source,
            "      const VERIFICATION_BY_ID = {",
            "\n      };\n      const chronologyYear",
        )
        + "}"
    )
    if len(records) != len({r["ID"] for r in records}):
        raise ValueError("Duplicate highlight IDs found")
    return records, photos, burner_photos, verification


def split_urls(value):
    return [item.strip() for item in (value or "").split(";") if item.strip()]


def collect_url_uses(records, photos, burner_photos):
    uses = defaultdict(list)
    for record in records:
        rid = record["ID"]
        for field, role in [
            ("Primary source URL", "Primary factual source"),
            ("Finding / register link", "Finding/register page"),
            ("Additional source URLs", "Additional factual source"),
            ("Map link", "Map/location link"),
        ]:
            for url in split_urls(record.get(field, "")):
                uses[url].append((rid, role))
        seen = set()
        for photo_role, photo in [
            ("Primary map picture source", photos.get(rid)),
            ("Additional map picture source", burner_photos.get(rid)),
        ]:
            if photo and photo.get("source") and photo["source"] not in seen:
                uses[photo["source"]].append((rid, photo_role))
                seen.add(photo["source"])
    return uses


class TitleParser:
    def __init__(self):
        self.in_title = False
        self.parts = []

    def feed(self, text):
        match = re.search(r"<title\b[^>]*>(.*?)</title\s*>", text, re.I | re.S)
        if match:
            self.parts.append(html.unescape(re.sub(r"<[^>]+>", " ", match.group(1))))

    @property
    def title(self):
        return re.sub(r"\s+", " ", " ".join(self.parts)).strip()


def check_url(url):
    checked_at = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    result = {
        "Requested URL": url,
        "Final URL": "",
        "HTTP status": "",
        "Accessible": "No",
        "Content type": "",
        "Page title": "",
        "Checked at (UTC)": checked_at,
        "Error / note": "",
    }
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/pdf,image/*,*/*;q=0.8",
        },
    )
    try:
        context = ssl.create_default_context()
        with urllib.request.urlopen(request, timeout=15, context=context) as response:
            body = response.read(600_000)
            status = getattr(response, "status", 200)
            ctype = response.headers.get_content_type()
            charset = response.headers.get_content_charset() or "utf-8"
            result.update(
                {
                    "Final URL": response.geturl(),
                    "HTTP status": status,
                    "Accessible": "Yes" if 200 <= status < 400 else "No",
                    "Content type": ctype,
                }
            )
            if "html" in ctype:
                text = body.decode(charset, errors="replace")
                parser = TitleParser()
                parser.feed(text)
                result["Page title"] = parser.title
    except urllib.error.HTTPError as exc:
        result.update(
            {
                "Final URL": exc.geturl(),
                "HTTP status": exc.code,
                "Content type": exc.headers.get_content_type() if exc.headers else "",
                "Error / note": f"HTTP {exc.code}: access failure does not by itself disprove the map claim",
            }
        )
    except Exception as exc:
        result["Error / note"] = (
            f"{type(exc).__name__}: {str(exc)[:240]}; "
            "access failure does not by itself disprove the map claim"
        )
    return result


def run_url_audit(urls, live):
    if not live:
        return {
            url: {
                "Requested URL": url,
                "Final URL": "",
                "HTTP status": "",
                "Accessible": "Not checked",
                "Content type": "",
                "Page title": "",
                "Checked at (UTC)": "",
                "Error / note": "Live checking disabled",
            }
            for url in urls
        }
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
        future_urls = {pool.submit(check_url, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_urls):
            url = future_urls[future]
            try:
                results[url] = future.result()
            except Exception as exc:
                results[url] = {
                    "Requested URL": url,
                    "Final URL": "",
                    "HTTP status": "",
                    "Accessible": "No",
                    "Content type": "",
                    "Page title": "",
                    "Checked at (UTC)": "",
                    "Error / note": f"Audit worker error: {exc}",
                }
    return results


def is_generalised(record):
    precision = (record.get("Coordinate precision") or "").lower()
    indicators = (
        "approx",
        "vicinity",
        "centroid",
        "general",
        "representative",
        "intersection",
        "locality",
        "sensitive",
        "former-site",
        "landscape",
    )
    return any(indicator in precision for indicator in indicators)


def factual_urls(record):
    values = []
    for field in ["Primary source URL", "Finding / register link", "Additional source URLs"]:
        values.extend(split_urls(record.get(field, "")))
    return list(dict.fromkeys(values))


def outcome_for(record, verification, audits):
    urls = factual_urls(record)
    accessible = sum(audits.get(url, {}).get("Accessible") == "Yes" for url in urls)
    failed = sum(audits.get(url, {}).get("Accessible") == "No" for url in urls)
    grade = verification.get("grade", "")
    status = verification.get("status", "")
    if "Field verification required" in grade or "Field verification required" in status:
        outcome = "Documentary lead — field verification required"
        note = (
            "The cited documentary trail was reviewed, but the mapped feature's "
            "present physical survival/location still requires on-site confirmation."
        )
    elif grade == "Verified" and accessible:
        outcome = "Documentary check passed — live source available"
        note = (
            "Existing manual evidence review retained; at least one cited factual "
            "source returned a successful response during this audit."
        )
    elif grade == "Verified":
        outcome = "Previously verified — live source access issue"
        note = (
            "Existing manual evidence review retained. No cited factual source returned "
            "a successful response in this automated check; this is an access warning, "
            "not a finding that the place claim is false."
        )
    else:
        outcome = "Review status retained"
        note = "Existing evidence-review status retained and URL availability recorded separately."
    return outcome, note, len(urls), accessible, failed


def photo_associations(records, photos, burner_photos):
    rows = []
    by_id = {r["ID"]: r for r in records}
    for rid in by_id:
        seen = set()
        candidates = [
            ("Primary", photos.get(rid)),
            ("Additional", burner_photos.get(rid)),
        ]
        for role, photo in candidates:
            if not photo or photo.get("src") in seen:
                continue
            seen.add(photo.get("src"))
            local = ROOT / photo["src"].removeprefix("./")
            rows.append(
                {
                    "Record ID": rid,
                    "Place name": by_id[rid]["Name"],
                    "Picture role": role,
                    "Caption": photo.get("caption", ""),
                    "Alternative text": photo.get("alt", ""),
                    "Creator / credit": photo.get("credit", ""),
                    "Rights / reuse": photo.get("license", ""),
                    "Source URL": photo.get("source", ""),
                    "Relevance note": photo.get("relevance", ""),
                    "Local path": str(local.relative_to(ROOT)),
                    "File status": "Present" if local.is_file() else "Missing",
                    "_path": local,
                }
            )
    return rows


def x(value):
    return escape(str(value if value is not None else ""), {'"': "&quot;"})


def col_letter(index):
    out = ""
    while index:
        index, rem = divmod(index - 1, 26)
        out = chr(65 + rem) + out
    return out


def worksheet_xml(rows, widths=None, row_heights=None, drawing=False, autofilter=True):
    max_cols = max((len(row) for row in rows), default=1)
    parts = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">',
        '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" '
        'activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>',
    ]
    if widths:
        parts.append("<cols>")
        for idx, width in enumerate(widths, 1):
            parts.append(f'<col min="{idx}" max="{idx}" width="{width}" customWidth="1"/>')
        parts.append("</cols>")
    parts.append("<sheetData>")
    for row_idx, row in enumerate(rows, 1):
        height = (row_heights or {}).get(row_idx)
        row_attr = f' ht="{height}" customHeight="1"' if height else ""
        parts.append(f'<row r="{row_idx}"{row_attr}>')
        for col_idx, value in enumerate(row, 1):
            ref = f"{col_letter(col_idx)}{row_idx}"
            style = 1 if row_idx == 1 else 2
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                parts.append(f'<c r="{ref}" s="{style}"><v>{value}</v></c>')
            else:
                text = x(value)
                preserve = ' xml:space="preserve"' if text.strip() != text else ""
                parts.append(
                    f'<c r="{ref}" s="{style}" t="inlineStr"><is><t{preserve}>'
                    f"{text}</t></is></c>"
                )
        parts.append("</row>")
    parts.append("</sheetData>")
    if autofilter and rows:
        parts.append(f'<autoFilter ref="A1:{col_letter(max_cols)}{len(rows)}"/>')
    if drawing:
        parts.append('<drawing r:id="rId1"/>')
    parts.append("</worksheet>")
    return "".join(parts)


def styles_xml():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
 <fonts count="2"><font><sz val="11"/><name val="Aptos"/></font>
 <font><b/><color rgb="FFFFFFFF"/><sz val="11"/><name val="Aptos"/></font></fonts>
 <fills count="3"><fill><patternFill patternType="none"/></fill>
 <fill><patternFill patternType="gray125"/></fill>
 <fill><patternFill patternType="solid"><fgColor rgb="FF1F4E78"/><bgColor indexed="64"/></patternFill></fill></fills>
 <borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
 <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
 <cellXfs count="3"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
 <xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf>
 <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf></cellXfs>
 <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>"""


def drawing_xml(picture_rows):
    anchors = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<xdr:wsDr xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">',
    ]
    for image_no, (excel_row, photo) in enumerate(picture_rows, 1):
        zero_row = excel_row - 1
        name = x(f"{photo['Record ID']} {photo['Picture role']} picture")
        descr = x(photo["Alternative text"] or photo["Caption"])
        anchors.append(
            f'<xdr:oneCellAnchor><xdr:from><xdr:col>0</xdr:col><xdr:colOff>0</xdr:colOff>'
            f'<xdr:row>{zero_row}</xdr:row><xdr:rowOff>0</xdr:rowOff></xdr:from>'
            '<xdr:ext cx="2286000" cy="1371600"/>'
            f'<xdr:pic><xdr:nvPicPr><xdr:cNvPr id="{image_no}" name="{name}" descr="{descr}"/>'
            '<xdr:cNvPicPr><a:picLocks noChangeAspect="1"/></xdr:cNvPicPr></xdr:nvPicPr>'
            f'<xdr:blipFill><a:blip r:embed="rId{image_no}"/><a:stretch><a:fillRect/></a:stretch></xdr:blipFill>'
            '<xdr:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="2286000" cy="1371600"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></xdr:spPr></xdr:pic>'
            '<xdr:clientData/></xdr:oneCellAnchor>'
        )
    anchors.append("</xdr:wsDr>")
    return "".join(anchors)


def build_workbook(records, photos, burner_photos, verification, url_uses, audits):
    photo_rows = photo_associations(records, photos, burner_photos)
    grade_counts = Counter((verification.get(r["ID"], {}).get("grade") or "Not graded") for r in records)
    outcome_counts = Counter()
    accessible_urls = sum(a["Accessible"] == "Yes" for a in audits.values())
    failed_urls = sum(a["Accessible"] == "No" for a in audits.values())

    summary = [
        ["Fact-check workbook", "Victorian Chinese Heritage Map highlights"],
        ["Generated", CHECKED_ON],
        ["Scope", f"{len(records)} map highlights; all fields shown in the click panel are exported"],
        ["Method", "Existing manual evidence decisions + automated live availability check of every cited URL"],
        ["Important limitation", "This is a documentary fact-check, not a field inspection, title search, boundary survey, or statutory heritage certificate."],
        ["URL interpretation", "An inaccessible/blocked URL is an access warning only; it is not proof that a map claim is false."],
        ["Coordinates", "Approximate/generalised points must not be used as cadastral boundaries or exact feature locations."],
        ["Image rights", "Credits, source links, and reuse notes are preserved. Embedding an image does not grant additional reuse rights."],
        ["Highlights", len(records)],
        ["Distinct cited URLs", len(audits)],
        ["URLs accessible in automated check", accessible_urls],
        ["URLs blocked/failed in automated check", failed_urls],
        ["Embedded picture associations", sum(row["File status"] == "Present" for row in photo_rows)],
    ]
    for grade, count in sorted(grade_counts.items()):
        summary.append([f"Evidence grade: {grade}", count])
    summary.append(["Sheet guide", "Highlights = click metadata and per-place conclusion; Source Audit = URL response evidence; Key Pictures = embedded map images and rights metadata."])

    base_fields = list(records[0].keys())
    extra_fields = [
        "Verification grade",
        "Verification status",
        "Verification note",
        "Verification reviewed on",
        "Heritage Victoria core",
        "Approximate / generalised point",
        "Register IDs shown",
        "Fact-check outcome",
        "Fact-check note",
        "Factual source count",
        "Accessible factual sources",
        "Failed factual sources",
        "Fact-checked on",
        "Primary picture path",
        "Additional picture path(s)",
    ]
    highlights = [base_fields + extra_fields]
    for record in records:
        rid = record["ID"]
        ver = verification.get(rid, {})
        outcome, note, total, accessible, failed = outcome_for(record, ver, audits)
        outcome_counts[outcome] += 1
        pictures = [row for row in photo_rows if row["Record ID"] == rid]
        primary = next((p["Local path"] for p in pictures if p["Picture role"] == "Primary"), "")
        additional = "; ".join(p["Local path"] for p in pictures if p["Picture role"] == "Additional")
        register_ids = "; ".join(
            f"{label}: {record.get(field)}"
            for label, field in [
                ("VHR", "VHR number"),
                ("Inventory", "Heritage Inventory number"),
                ("VHD place", "VHD place ID"),
            ]
            if record.get(field)
        )
        extras = [
            ver.get("grade", ""),
            ver.get("status", ""),
            ver.get("note", ""),
            ver.get("reviewed", ""),
            record.get("Official Heritage Victoria Chinese selection (2022)", ""),
            "Yes" if is_generalised(record) else "No",
            register_ids,
            outcome,
            note,
            total,
            accessible,
            failed,
            CHECKED_ON,
            primary,
            additional,
        ]
        highlights.append([record.get(field, "") for field in base_fields] + extras)

    source_headers = [
        "Requested URL",
        "Used by record IDs",
        "Source roles",
        "Final URL",
        "HTTP status",
        "Accessible",
        "Content type",
        "Page title",
        "Checked at (UTC)",
        "Error / note",
    ]
    source_rows = [source_headers]
    for url in sorted(audits):
        audit = audits[url]
        uses = url_uses[url]
        source_rows.append(
            [
                url,
                "; ".join(sorted({rid for rid, _ in uses})),
                "; ".join(sorted({role for _, role in uses})),
                audit["Final URL"],
                audit["HTTP status"],
                audit["Accessible"],
                audit["Content type"],
                audit["Page title"],
                audit["Checked at (UTC)"],
                audit["Error / note"],
            ]
        )

    photo_headers = [
        "Key picture",
        "Record ID",
        "Place name",
        "Picture role",
        "Caption",
        "Alternative text",
        "Creator / credit",
        "Rights / reuse",
        "Source URL",
        "Relevance note",
        "Local path",
        "File status",
    ]
    picture_sheet = [photo_headers]
    picture_embed = []
    for photo in photo_rows:
        excel_row = len(picture_sheet) + 1
        picture_sheet.append(
            ["", *[photo[key] for key in photo_headers[1:]]]
        )
        if photo["File status"] == "Present":
            picture_embed.append((excel_row, photo))

    sheets = [
        ("Summary", summary, [28, 115], {}, False),
        ("Highlights", highlights, [15, 34] + [24] * (len(highlights[0]) - 2), {}, False),
        ("Source Audit", source_rows, [52, 25, 32, 52, 12, 13, 20, 44, 25, 55], {}, False),
        (
            "Key Pictures",
            picture_sheet,
            [34, 14, 32, 15, 44, 44, 28, 32, 52, 48, 45, 13],
            {row_num: 115 for row_num, _ in picture_embed},
            True,
        ),
    ]

    content_types = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Default Extension="jpg" ContentType="image/jpeg"/>',
        '<Default Extension="jpeg" ContentType="image/jpeg"/>',
        '<Default Extension="png" ContentType="image/png"/>',
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
    ]
    for idx in range(1, len(sheets) + 1):
        content_types.append(
            f'<Override PartName="/xl/worksheets/sheet{idx}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    content_types.append(
        '<Override PartName="/xl/drawings/drawing1.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.drawing+xml"/>'
    )
    content_types.append("</Types>")

    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets>'
        + "".join(
            f'<sheet name="{x(name)}" sheetId="{idx}" r:id="rId{idx}"/>'
            for idx, (name, *_rest) in enumerate(sheets, 1)
        )
        + "</sheets></workbook>"
    )
    workbook_rels = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
    ]
    for idx in range(1, len(sheets) + 1):
        workbook_rels.append(
            f'<Relationship Id="rId{idx}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
            f'Target="worksheets/sheet{idx}.xml"/>'
        )
    workbook_rels.append(
        f'<Relationship Id="rId{len(sheets)+1}" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
        'Target="styles.xml"/></Relationships>'
    )
    root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""

    drawing_rels = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
    ]
    media = []
    for image_no, (_excel_row, photo) in enumerate(picture_embed, 1):
        data = photo["_path"].read_bytes()
        if data.startswith(b"\x89PNG"):
            ext = "png"
        elif data.startswith(b"\xff\xd8"):
            ext = "jpg"
        else:
            ext = mimetypes.guess_extension(mimetypes.guess_type(str(photo["_path"]))[0] or "") or ".jpg"
            ext = ext.lstrip(".")
        target = f"image{image_no}.{ext}"
        media.append((target, data))
        drawing_rels.append(
            f'<Relationship Id="rId{image_no}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
            f'Target="../media/{target}"/>'
        )
    drawing_rels.append("</Relationships>")
    picture_sheet_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/drawing" Target="../drawings/drawing1.xml"/>
</Relationships>"""

    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", "".join(content_types))
        archive.writestr("_rels/.rels", root_rels)
        archive.writestr("xl/workbook.xml", workbook_xml)
        archive.writestr("xl/_rels/workbook.xml.rels", "".join(workbook_rels))
        archive.writestr("xl/styles.xml", styles_xml())
        for idx, (_name, rows, widths, heights, has_drawing) in enumerate(sheets, 1):
            archive.writestr(
                f"xl/worksheets/sheet{idx}.xml",
                worksheet_xml(rows, widths, heights, drawing=has_drawing, autofilter=idx != 1),
            )
        archive.writestr("xl/worksheets/_rels/sheet4.xml.rels", picture_sheet_rels)
        archive.writestr("xl/drawings/drawing1.xml", drawing_xml(picture_embed))
        archive.writestr("xl/drawings/_rels/drawing1.xml.rels", "".join(drawing_rels))
        for target, data in media:
            archive.writestr(f"xl/media/{target}", data)
    return {
        "records": len(records),
        "urls": len(audits),
        "accessible_urls": accessible_urls,
        "failed_urls": failed_urls,
        "pictures": len(picture_embed),
        "grades": dict(grade_counts),
        "outcomes": dict(outcome_counts),
        "output": str(OUTPUT),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Perform live checks of cited URLs")
    args = parser.parse_args()
    records, photos, burner_photos, verification = extract_map_data()
    url_uses = collect_url_uses(records, photos, burner_photos)
    audits = run_url_audit(sorted(url_uses), args.live)
    result = build_workbook(records, photos, burner_photos, verification, url_uses, audits)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
