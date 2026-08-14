#!/usr/bin/env python3
"""Build normalized cemetery-register exports and a conservative Chinese-name index."""

from __future__ import annotations

import csv
import html
import json
import re
import sys
from pathlib import Path

try:
    import xlrd
except ImportError:
    raise SystemExit(
        "xlrd is required for the two legacy .xls files. "
        "Install it or run with PYTHONPATH pointing to an xlrd installation."
    )


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
OUT = ROOT / "extracted"
OUT.mkdir(exist_ok=True)

FIELDS = [
    "finding_ids",
    "cemetery",
    "recorded_name",
    "chinese_characters",
    "year_or_date",
    "age",
    "plot_or_location",
    "origin_or_birthplace",
    "evidence_basis",
    "confidence",
    "source_url",
    "source_record_url",
    "source_file",
    "notes",
    "gender",
    "pronunciation",
    "other_names",
    "maiden_name",
    "birth_date",
    "death_date",
    "province",
    "county",
    "district",
    "township",
    "village",
    "plot_number",
    "latitude",
    "longitude",
    "photo_1",
    "photo_2",
    "photo_3",
    "community_notes",
    "related_story_url",
]


def clean(value) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return re.sub(r"\s+", " ", str(value)).strip()


def clean_markup(value) -> str:
    """Convert the small HTML fragments in the source notes to readable text."""
    return clean(html.unescape(re.sub(r"<[^>]+>", " ", str(value or ""))))


def first_link(value) -> str:
    match = re.search(r'href=["\']?([^"\' >]+)', str(value or ""), re.IGNORECASE)
    return html.unescape(match.group(1)) if match else ""


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


names: list[dict] = []


def add(**row) -> None:
    normalized = {field: clean(row.get(field, "")) for field in FIELDS}
    names.append(normalized)


# Melbourne General Cemetery: the source dataset is specifically a survey of
# Chinese graves, so no ethnicity inference is necessary.
mgc_path = RAW / "cafhov_mgc_collection.csv"
with mgc_path.open(encoding="utf-8-sig", newline="") as handle:
    mgc_rows = list(csv.DictReader(handle))

mgc_normalized = []
for row in mgc_rows:
    title = clean(row.get("title"))
    # One photographed grave (object 400) has no title, but is identified in
    # CAFHOV's Other names field as Lee Kee Yook. Preserve that named record.
    if not title:
        title = clean(row.get("othernames"))
    # The first row describes the collection rather than a person/grave.
    if (
        not title
        or title.lower() in {"melbourne general cemetery", "empty"}
        or re.match(r"^\d+\s+unknown\b", title, re.IGNORECASE)
    ):
        continue
    # Split only the final spaced separator before the Chinese inscription;
    # two English names legitimately contain an internal slash.
    parts = [p.strip() for p in title.rsplit(" / ", 1)]
    latin_name = parts[0]
    chinese = parts[1] if len(parts) > 1 else ""
    normalized = {
        "recorded_name": latin_name,
        "chinese_characters": chinese,
        "date": clean(row.get("date")),
        "description": clean(row.get("description")),
        "plot": clean(row.get("plot")),
        "origin": clean(row.get("location")),
        "latitude": clean(row.get("latitude")),
        "longitude": clean(row.get("longitude")),
        "identifier": clean(row.get("objectid")),
        "reference_url": (
            f"https://cafhov.github.io/chinesegraves/item.html?id={clean(row.get('objectid'))}"
        ),
        "gender": clean(row.get("gender")),
        "pronunciation": clean(row.get("pronounced")),
        "other_names": clean(row.get("othernames")),
        "maiden_name": clean(row.get("maidenname")),
        "birth_date": clean(row.get("birthdate")),
        "death_date": clean(row.get("deathdate")),
        "province": clean(row.get("province")),
        "county": clean(row.get("county")),
        "district": clean(row.get("district")),
        "township": clean(row.get("township")),
        "village": clean(row.get("village")),
        "plot_number": clean(row.get("plotnumber")),
        "photo_1": clean(row.get("Image1")),
        "photo_2": clean(row.get("Image2")),
        "photo_3": clean(row.get("Image3")),
        "community_notes": clean_markup(row.get("communitynotes")),
        "related_story_url": first_link(row.get("communitynotes")),
    }
    mgc_normalized.append(normalized)
    add(
        finding_ids="VCH-027",
        cemetery="Melbourne General Cemetery",
        recorded_name=latin_name,
        chinese_characters=chinese,
        year_or_date=row.get("date"),
        plot_or_location=row.get("plot"),
        origin_or_birthplace=row.get("location"),
        evidence_basis="Record is in the dedicated Chinese-graves survey dataset",
        confidence="High",
        source_url="https://cafhov.github.io/chinesegraves/data.html",
        source_record_url=(
            f"https://cafhov.github.io/chinesegraves/item.html?id={clean(row.get('objectid'))}"
        ),
        source_file=mgc_path.name,
        notes=row.get("description"),
        gender=row.get("gender"),
        pronunciation=row.get("pronounced"),
        other_names=row.get("othernames"),
        maiden_name=row.get("maidenname"),
        birth_date=row.get("birthdate"),
        death_date=row.get("deathdate"),
        province=row.get("province"),
        county=row.get("county"),
        district=row.get("district"),
        township=row.get("township"),
        village=row.get("village"),
        plot_number=row.get("plotnumber"),
        latitude=row.get("latitude"),
        longitude=row.get("longitude"),
        photo_1=row.get("Image1"),
        photo_2=row.get("Image2"),
        photo_3=row.get("Image3"),
        community_notes=clean_markup(row.get("communitynotes")),
        related_story_url=first_link(row.get("communitynotes")),
    )
mgc_fields = [
    "recorded_name", "chinese_characters", "date", "description", "plot", "origin",
    "latitude", "longitude", "identifier", "reference_url", "gender",
    "pronunciation", "other_names", "maiden_name", "birth_date", "death_date",
    "province", "county", "district", "township", "village", "plot_number",
    "photo_1", "photo_2", "photo_3",
    "community_notes", "related_story_url",
]
write_csv(OUT / "melbourne_general_chinese_graves.csv", mgc_normalized, mgc_fields)


# Yackandandah: official database query restricted to the cemetery's Chinese section.
yack_path = RAW / "yackandandah_chinese_section_query.json"
yack = json.loads(yack_path.read_text(encoding="utf-8"))
yack_rows = list(yack["burials"].values())
yack_export = []
for row in yack_rows:
    person = clean(" ".join(filter(None, [clean(row.get("givenNames")), clean(row.get("surname"))])))
    out = {
        "id": clean(row.get("id")),
        "recorded_name": person,
        "burial_year": clean(row.get("burialYear")),
        "section": clean(row.get("sectionName")),
    }
    yack_export.append(out)
    add(
        finding_ids="VCH-024",
        cemetery="Yackandandah Cemetery",
        recorded_name=person,
        year_or_date=row.get("burialYear"),
        plot_or_location=row.get("sectionName"),
        evidence_basis="Official burial database result in section named Chinese",
        confidence="High",
        source_url="https://cemetery.yackandandah.com/burial-search/",
        source_record_url=f"https://cemetery-db.yackandandah.com/Search.aspx?id={row.get('id')}",
        source_file=yack_path.name,
    )
write_csv(
    OUT / "yackandandah_chinese_section.csv",
    yack_export,
    ["id", "recorded_name", "burial_year", "section"],
)


# Creswick: preserve the entire official public export, then make only a
# conservative candidate subset from historical Compartment 6. That compartment
# is mixed, so these rows remain medium-confidence even when names look Chinese.
creswick_path = RAW / "creswick_new_cemetery_public_query.json"
creswick_payload = json.loads(creswick_path.read_text(encoding="utf-8"))
creswick_rows = creswick_payload["data"]["data"]
creswick_fields = [
    "deceasedHashId", "cemetery", "location", "firstName", "middleName",
    "lastName", "dob", "dod", "doi",
]
write_csv(OUT / "creswick_new_cemetery_full_register.csv", creswick_rows, creswick_fields)

strict_creswick = re.compile(
    r"(^|\s)AH(\s|$)|\bCHIN HON\b|\bQUANCHI\b|\bQUANG SHUNG\b|\bLEE YOU\b",
    re.IGNORECASE,
)
for row in creswick_rows:
    location = clean(row.get("location"))
    date = clean(row.get("doi"))
    if not location.startswith("6-") or (date and date[:4] > "1923"):
        continue
    person = clean(" ".join(clean(row.get(k)) for k in ("firstName", "middleName", "lastName")))
    if not strict_creswick.search(person):
        continue
    add(
        finding_ids="VCH-023",
        cemetery="Creswick Cemetery",
        recorded_name=person,
        year_or_date=row.get("doi") or row.get("dod"),
        death_date=row.get("dod"),
        plot_or_location=location,
        evidence_basis="Historical Compartment 6 location plus conservative Chinese-form name match",
        confidence="Medium",
        source_url="https://www.creswickcemetery.com.au/history/chinese/",
        source_record_url="https://apps.byond.cloud/deceased-search/dba1e99a-efb0-4f4d-e4eb-aeee2f7d77c3",
        source_file=creswick_path.name,
        notes="Compartment 6 also contains non-Chinese burials; verify before treating ethnicity as certain.",
    )


# Echuca: export every row. Select only explicit Chinese annotations (high) and
# the historically common standalone Ah name element (medium).
echuca_path = RAW / "echuca_burials_1857_2017.xls"
book = xlrd.open_workbook(str(echuca_path))
echuca_all = []
seen_echuca = set()
for sheet in book.sheets():
    for row_num in range(1, sheet.nrows):
        values = [clean(v) for v in sheet.row_values(row_num)]
        values.extend([""] * (5 - len(values)))
        if not any(values):
            continue
        row = {
            "surname": values[0],
            "given_name": values[1],
            "age": values[2],
            "year_of_death": values[3],
            "notes": values[4],
            "source_sheet": sheet.name,
        }
        echuca_all.append(row)
        combined = clean(" ".join(values))
        dedupe = (values[0].casefold(), values[1].casefold(), values[2], values[3])
        explicit = bool(re.search(r"\bchinese\b", combined, re.IGNORECASE))
        ah_name = bool(re.search(r"(^|\s)ah(\s|$)", f"{values[1]} {values[0]}", re.IGNORECASE))
        if not (explicit or ah_name) or dedupe in seen_echuca:
            continue
        seen_echuca.add(dedupe)
        add(
            finding_ids="VCH-038",
            cemetery="Echuca Cemetery",
            recorded_name=clean(f"{values[1]} {values[0]}"),
            year_or_date=values[3],
            death_date=values[3],
            age=values[2],
            evidence_basis=(
                "Register explicitly annotates the person as Chinese"
                if explicit
                else "Historical standalone 'Ah' name element; ethnicity not explicit in register"
            ),
            confidence="High" if explicit else "Medium",
            source_url="https://www.echucacemetery.com/cemetery-records/",
            source_file=echuca_path.name,
            notes=values[4],
        )
write_csv(
    OUT / "echuca_burials_1857_2017.csv",
    echuca_all,
    ["surname", "given_name", "age", "year_of_death", "notes", "source_sheet"],
)


# Ballarat Old Cemetery/death-register transcription, 1848–1856.
ballarat_path = RAW / "ballarat_old_burials_1848_1856.xls"
sheet = xlrd.open_workbook(str(ballarat_path)).sheet_by_index(0)
headers = [clean(v).lower() for v in sheet.row_values(0)]
ballarat_all = []
for row_num in range(1, sheet.nrows):
    row = dict(zip(headers, [clean(v) for v in sheet.row_values(row_num)]))
    if not any(row.values()):
        continue
    ballarat_all.append(row)
    given = row.get("given", "")
    birthplace = row.get("pob", "")
    burial = row.get("burial", "")
    explicit = bool(re.search(r"china(?:man|mna)", given, re.IGNORECASE))
    chinese_birthplace = birthplace.casefold() in {"china", "canton", "hong kong"}
    if not (explicit or chinese_birthplace):
        continue
    # One source row has its death date duplicated into GIVEN; do not present
    # that transcription error as part of the person's name.
    display_given = "" if re.fullmatch(r"\d{1,2}[A-Za-z]{3}\d{4}", given) else given
    display_given = re.sub(
        r"[-:]?\s*china(?:man|mna)\b", "", display_given, flags=re.IGNORECASE
    ).strip()
    is_linton = burial.casefold() == "linton"
    add(
        finding_ids="VCH-029" if is_linton else "VCH-026",
        cemetery="Linton Cemetery" if is_linton else "Ballarat Old Cemetery / early Ballarat register",
        recorded_name=clean(f"{display_given} {row.get('surname', '')}"),
        year_or_date=row.get("dod"),
        death_date=row.get("dod"),
        age=row.get("age"),
        plot_or_location=burial,
        origin_or_birthplace=birthplace,
        evidence_basis=(
            "Historical register explicitly labels the person with the period term 'Chinaman'"
            if explicit
            else "Historical register records birthplace as China, Canton, or Hong Kong"
        ),
        confidence="High",
        source_url="https://victoriancollections.net.au/items/5badd55821ea690b78bf2a48",
        source_file=ballarat_path.name,
        notes=f"Register page {row.get('page', '')}; registration {row.get('regno', '')}",
    )
write_csv(OUT / "ballarat_old_burials_1848_1856.csv", ballarat_all, headers)


# Whroo's official HTML table. Restrict extraction to names containing the
# standalone Ah element or a family/alias field beginning with Ah.
whroo_path = RAW / "whroo_interment_register.html"
whroo_text = whroo_path.read_text(encoding="utf-8", errors="replace")
table_match = re.search(r'<table id="interment".*?</table>', whroo_text, re.I | re.S)
whroo_rows = []
if table_match:
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", table_match.group(0), re.I | re.S):
        cells = [
            clean(html.unescape(re.sub(r"<[^>]+>", "", td)))
            for td in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.I | re.S)
        ]
        if len(cells) < 8 or cells[0].casefold() == "grave":
            continue
        row = dict(zip(
            ["grave", "given_name", "surname", "father", "mother", "date", "religion", "age"],
            cells[:8],
        ))
        whroo_rows.append(row)
        combined = " ".join([row["given_name"], row["surname"], row["father"]])
        if not re.search(r"(^|\s)Ah(\s|$)", combined, re.I):
            continue
        add(
            finding_ids="VCH-035",
            cemetery="Whroo Cemetery",
            recorded_name=clean(f"{row['given_name']} {row['surname']}"),
            year_or_date=row["date"],
            age=row["age"],
            plot_or_location=row["grave"],
            evidence_basis="Official online interment table plus Chinese-form name",
            confidence="Medium",
            source_url="https://whroocemeterytrust.org/",
            source_file=whroo_path.name,
            notes=clean(f"Father/alias: {row['father']}; religion: {row['religion']}"),
        )
write_csv(
    OUT / "whroo_interment_register.csv",
    whroo_rows,
    ["grave", "given_name", "surname", "father", "mother", "date", "religion", "age"],
)


# Explicit names found on individual authoritative or specialist history pages.
manual_rows = [
    dict(
        finding_ids="VCH-008", cemetery="Beechworth Chinese Cemetery",
        recorded_name="Henry Ah Yett", year_or_date="1932",
        evidence_basis="Official cemetery historic-graves tour identifies him as the last Chinese person buried there",
        confidence="High",
        source_url="https://beechworthcemetery.com.au/history-tours/historic-graves-tour",
        source_file="beechworth_family_research.html",
    ),
    dict(
        finding_ids="VCH-029", cemetery="Linton Cemetery",
        recorded_name="Wot Tin", year_or_date="1921",
        evidence_basis="Chinese Pioneers memorial page identifies the final Chinese burial",
        confidence="High",
        source_url="https://www.monumentaustralia.org/themes/landscape/settlement/display/95588-chinese-pioneers-of-linton",
        source_file="linton_chinese_pioneers_memorial.html",
    ),
    dict(
        finding_ids="VCH-023", cemetery="Creswick Cemetery",
        recorded_name="Ah Chin", year_or_date="1858-12-28",
        evidence_basis="Specialist Creswick Chinese cemetery history explicitly names the first burials",
        confidence="High",
        source_url="https://chinese-heritage.tripod.com/Creswick%20Cemetery.htm",
    ),
    dict(
        finding_ids="VCH-023", cemetery="Creswick Cemetery",
        recorded_name="Ah Chung", year_or_date="1858-12-28",
        evidence_basis="Specialist Creswick Chinese cemetery history explicitly names the first burials",
        confidence="High",
        source_url="https://chinese-heritage.tripod.com/Creswick%20Cemetery.htm",
    ),
    dict(
        finding_ids="VCH-023", cemetery="Creswick Cemetery",
        recorded_name="Shong Yuang", year_or_date="1910-10-21",
        evidence_basis="Specialist Creswick Chinese cemetery history explicitly names the last burial in its list",
        confidence="High",
        source_url="https://chinese-heritage.tripod.com/Creswick%20Cemetery.htm",
    ),
    dict(
        finding_ids="VCH-036", cemetery="Inkerman Cemetery within Moliagul Cemetery",
        recorded_name="Ah Shee", year_or_date="1857",
        evidence_basis="Dunolly Museum burial list explicitly annotates the person as Chinese",
        confidence="High",
        source_url="https://dunollymuseumsite.wordpress.com/inkerman-cemetery-inside-the-moliagul-cemetery/",
        source_file="moliagul_inkerman_cemetery.html",
    ),
    dict(
        finding_ids="VCH-036", cemetery="Inkerman Cemetery within Moliagul Cemetery",
        recorded_name="Yong Show", year_or_date="1857",
        evidence_basis="Dunolly Museum burial list explicitly annotates the person as Chinese",
        confidence="High",
        source_url="https://dunollymuseumsite.wordpress.com/inkerman-cemetery-inside-the-moliagul-cemetery/",
        source_file="moliagul_inkerman_cemetery.html",
    ),
    dict(
        finding_ids="VCH-037", cemetery="Bi Jiang tombstone (Victorian Collections object record)",
        recorded_name="Bi Jiang",
        evidence_basis="Name appears in the catalogued tombstone object title",
        confidence="High",
        source_url="https://victoriancollections.net.au/items/5e77f1d621ea670f84f8594e",
    ),
]
for row in manual_rows:
    add(**row)


# Keep source rows distinct but remove exact accidental duplicates.
deduped = []
seen = set()
for row in names:
    key = (
        row["cemetery"].casefold(),
        row["recorded_name"].casefold(),
        row["year_or_date"].casefold(),
        row["source_url"].casefold(),
        row["source_record_url"].casefold(),
    )
    if key not in seen:
        seen.add(key)
        deduped.append(row)

deduped.sort(key=lambda r: (r["cemetery"], r["recorded_name"], r["year_or_date"]))
write_csv(OUT / "chinese_names.csv", deduped, FIELDS)

print(f"Wrote {len(deduped)} candidate/name rows to {OUT / 'chinese_names.csv'}")
for confidence in ("High", "Medium", "Low"):
    print(f"  {confidence}: {sum(r['confidence'] == confidence for r in deduped)}")
for cemetery in sorted({r["cemetery"] for r in deduped}):
    print(f"  {cemetery}: {sum(r['cemetery'] == cemetery for r in deduped)}")
