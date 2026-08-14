# Victorian cemetery record search

This folder records the website/register search for all 26 cemetery and funerary findings in the project map. It contains the downloaded source material, normalized full-register exports, and a conservative index of Chinese names or likely Chinese-name candidates.

## Main result

`extracted/chinese_names.csv` contains **720 sourced rows** from 10 cemetery/object sources:

- 657 high-confidence rows: an explicit Chinese-grave dataset, Chinese cemetery section, source annotation, Chinese characters, or recorded China/Canton/Hong Kong birthplace.
- 63 medium-confidence rows: the source context and a historical Chinese-form name support the match, but the register does not explicitly record ethnicity.
- 694 distinct displayed name strings. This is not necessarily 694 distinct individuals because spelling variants, aliases, and duplicate historical registrations may exist.

The largest sets are Melbourne General Cemetery (534 rows), Ballarat Old/early Ballarat records (82), Echuca (47), Yackandandah (25), Creswick (14), and Whroo (12). Individual named evidence was also found for Beechworth, Linton, Moliagul/Inkerman, and the Bi Jiang tombstone. The Melbourne total includes Lee Kee Yook, whose CAFHOV record has no title but identifies the person in its “Other names” field.

No person has been classified from a modern surname alone. Medium-confidence rows should be verified against the original record before publication as Chinese biographical data.

## Folder guide

- `cemetery_source_manifest.csv` — one row for every cemetery finding, with the website attempted, access outcome, files saved, and recommended next route.
- `raw/` — source files as downloaded: official spreadsheets and JSON queries, website pages, reports, and memorial photographs.
- `raw/cafhov_mgc_collection.csv` — CAFHOV’s complete Melbourne General Cemetery metadata, including name variants, pronunciation, ancestral-origin fields, dates, plots, notes and photograph links.
- `extracted/chinese_names.csv` — combined, source-attributed name index.
- `extracted/*full_register.csv` and cemetery-specific CSV files — convenient UTF-8 conversions of the downloaded data.
- `scripts/extract_names.py` — reproducible extraction and normalization code.

## Important limitations

“Chinese” in the output means that the historical source explicitly says so or that the row is a candidate supported by the documented evidence basis. It does not establish a person's identity by itself. Cemetery registers can contain errors, Anglicised spellings, reversed name order, aliases, and repeated entries.

Creswick Compartment 6 is historically associated mainly with Chinese burials, but it is a mixed compartment. Its name-pattern matches are therefore marked medium confidence. The Whroo and non-explicit Echuca matches are marked the same way.

The early Ballarat transcription preserves an offensive historical classification in some source cells. The combined CSV mentions that term only when explaining the verbatim evidence used for selection; it is not present-day language endorsed by this project.

Several custodians expose only individual searches or paid/manual research services. No attempt was made to bypass access controls or scrape a service that did not offer a supported public export. These unresolved sites are clearly identified in the manifest.

## Principal online sources

- [Chinese Graves at Melbourne General Cemetery](https://cafhov.github.io/chinesegraves/data.html)
- [Yackandandah Cemetery burial search](https://cemetery.yackandandah.com/burial-search/)
- [Creswick Cemetery deceased search](https://apps.byond.cloud/deceased-search/dba1e99a-efb0-4f4d-e4eb-aeee2f7d77c3)
- [Creswick Chinese cemetery history](https://www.creswickcemetery.com.au/history/chinese/)
- [Echuca Cemetery records](https://www.echucacemetery.com/cemetery-records/)
- [Whroo Cemetery interment register](https://whroocemeterytrust.org/)
- [Ballarat early burial spreadsheet catalogue record](https://victoriancollections.net.au/items/5badd55821ea690b78bf2a48)
- [Beechworth Cemetery family research](https://beechworthcemetery.com.au/family-research/)
- [Linton Chinese Pioneers memorial](https://www.monumentaustralia.org/themes/landscape/settlement/display/95588-chinese-pioneers-of-linton)
- [Dunolly Museum: Inkerman Cemetery inside Moliagul Cemetery](https://dunollymuseumsite.wordpress.com/inkerman-cemetery-inside-the-moliagul-cemetery/)

## Rebuilding the extracts

The script uses Python's standard library plus `xlrd` for the two legacy `.xls` workbooks:

```sh
python3 -m pip install -r cemetery_records/scripts/requirements.txt
python3 cemetery_records/scripts/extract_names.py
```

The source files are retained, so every selected row can be independently checked and the matching policy can be made broader or narrower later.
