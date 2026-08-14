# Copyright and image-rights audit

Audit updated: 13 August 2026  
Previous audit: 30 July 2026  
Scope: all files currently present in this repository, including public webpages, standalone and embedded images, proposal documents, research workbooks, cemetery source captures and extracts, third-party code, hosted map services, and CCCAV branding.

This is a practical rights-risk review, not legal advice or a legal determination. Copyright is assessed item by item. A citation, source link, catalogue listing, photographer credit, or public availability is not by itself a licence or permission.

## Executive finding

**Do not publish or distribute the repository as a whole in its current local state.**

The current repository contains **83 standalone raster image files**. The public website uses 47 local heritage/content images:

- **19** have a plausible open-licence or public-domain basis but still require complete, durable attribution records and source rechecking;
- **28** have no documented republication permission or applicable open licence and must be licensed, removed, or replaced before public release.

The homepage also publishes a project-generated animated GIF. It is derived from a proposal screenshot and a CC BY-SA photograph, so its constituent map, image, attribution, and share-alike obligations must be resolved rather than treating the GIF as wholly unrestricted project artwork.

The repository now also contains eight full-page proposal screenshots, two byte-identical proposal DOCX files containing an embedded interface image, 16 Scattered Legacy research images embedded again in an XLSX workbook, five Monument Australia photographs, and extensive source captures. Screenshots and composite files inherit rights issues in visible source photographs, map tiles, logos, and interface assets.

The cemetery stream now publishes a browser package of **720 records**. It is derived partly from a 544-row CAFHOV dataset in which 537 rows carry CC BY-NC 4.0 notices and seven have blank rights fields. The package also exposes 768 photograph-link fields representing 690 unique external URLs. This material must not be represented as unrestricted MIT data or assumed cleared for commercial reuse.

The top-level MIT licence remains too broad and ambiguous for this mixed repository. It should apply only to identified project-owned software code and must expressly exclude third-party images, branding, source captures, institutional publications, embedded media, and third-party-derived datasets.

## Audit method and limits

This update:

- enumerated every standalone JPG, PNG, and GIF in the working tree;
- matched local image paths against public HTML, CSS, JavaScript, and proposal files;
- inspected embedded media inside DOCX and XLSX containers;
- compared current source and extracted cemetery-file counts;
- counted CAFHOV rights statements and published photograph links;
- reviewed the licence labels, creators, and source URLs embedded in `places.html`;
- checked the current Git status, remote, top-level licence, and absence of a `.gitignore` file.

It did not obtain new permissions, authenticate ownership, examine private correspondence, or perform a line-by-line substantial-similarity review of all prose. Live source terms can change and must be rechecked immediately before release.

## Standalone picture inventory — 83 files

| Category | Files | Current status |
|---|---:|---|
| Public heritage/content images | 47 | 19 provisional open/public-domain; 28 unresolved |
| Homepage animated map preview | 1 | Project-generated composite; constituent rights review required |
| Proposal screenshots | 8 | Project screenshots containing third-party/interface elements |
| Scattered Legacy research copies | 16 | Research-only; republication permission not documented |
| Monument Australia research copies | 5 | Research-only; express source copyright and no open licence recorded |
| Leaflet interface images | 5 | Reusable under Leaflet’s BSD-2-Clause licence with notice obligations |
| CCCAV logo | 1 | Organisational branding; ownership/authorisation not documented here |
| **Total** | **83** | Embedded copies in DOCX/XLSX are additional reproductions, not additional standalone files |

## Public heritage and content images

### A. Provisionally reusable images — 19

These files have a stated Creative Commons, CC0, public-domain, or no-known-restrictions basis linked to a source page. They are not automatically covered by this repository’s MIT licence.

- `assets/heritage-images/era-arrival.jpg` — stated public domain
- `assets/heritage-images/era-community.jpg` — stated public domain/no known restrictions
- `assets/heritage-images/era-endurance.jpg` — stated public domain
- `assets/heritage-images/era-recognition.jpg` — CC BY-SA 4.0
- `assets/heritage-images/finding-beechworth-cemetery.jpg` — CC BY-SA 3.0
- `assets/heritage-images/finding-golden-dragon.jpg` — stated public domain
- `assets/heritage-images/finding-melbourne-chinatown.jpg` — stated public domain
- `assets/heritage-images/finding-see-yup-temple.jpg` — stated public domain
- `assets/verified-findings/VCH-007-white-hills-cemetery.jpg` — CC BY-SA 4.0
- `assets/verified-findings/VCH-009-maldon-cemetery-burner.jpg` — CC BY-SA 3.0
- `assets/verified-findings/VCH-010-st-andrews-beechworth.jpg` — CC BY-SA 3.0
- `assets/verified-findings/VCH-014-bendigo-joss-house.jpg` — CC BY-SA 3.0
- `assets/verified-findings/VCH-016-num-pon-soon.jpg` — stated public domain
- `assets/verified-findings/VCH-017-066-chinese-mission-church.jpg` — CC BY-SA 4.0
- `assets/verified-findings/VCH-044-castlemaine-diggings.jpg` — CC BY-SA 3.0
- `assets/verified-findings/VCH-047-hepburn-blowhole.jpg` — CC BY 2.5
- `assets/verified-findings/VCH-062-sovereign-hill-chinese-camp.jpg` — CC BY 3.0
- `assets/verified-findings/VCH-069-celestial-avenue-context.jpg` — stated public domain
- `assets/verified-findings/VCH-073-sun-yat-sen-statue.jpg` — CC0

Before release, create a durable attribution record for every retained image containing, where supplied: title, creator, source page, exact licence and version, licence URL, copyright notice, download/check date, and a statement of cropping, resizing, recompression, or other modification. Check public-domain claims against the source record and applicable term, not only the label copied into the webpage. CC BY-SA derivatives must comply with the relevant share-alike conditions.

### B. Images requiring permission, removal, or replacement — 28

#### University of Idaho funerary-burner census — 10

The page identifies photographers but supplies no open-reuse licence. “Photo by” is attribution, not permission.

- `assets/verified-findings/VCH-003-castlemaine-cemetery-burner.jpg`
- `assets/verified-findings/VCH-007-white-hills-burner-idaho.jpg`
- `assets/verified-findings/VCH-008-beechworth-burners-idaho.jpg`
- `assets/verified-findings/VCH-009-maldon-cemetery-burner-idaho.jpg`
- `assets/verified-findings/VCH-022-dunolly-cemetery-burner.jpg`
- `assets/verified-findings/VCH-025-ballarat-new-cemetery-burner.jpg`
- `assets/verified-findings/VCH-026-ballarat-old-cemetery-burner.jpg`
- `assets/verified-findings/VCH-028-maryborough-cemetery-burner.jpg`
- `assets/verified-findings/VCH-074-glenpatrick-cemetery-burner.jpg`
- `assets/verified-findings/VCH-075-bendigo-cemetery-burner.jpg`

Required action: obtain written web-republication permission from the photographer or authorised rightsholder, or replace the file with a CCCAV-owned or verified open-licence photograph.

#### Scattered Legacy photographs — 11

The public data correctly labels these “Reuse permission not established,” but the webpage still loads and displays them. A catalogue credit does not establish that the catalogue can grant republication rights.

- `assets/verified-findings/VCH-076-avoca-chinese-garden.jpg`
- `assets/verified-findings/VCH-077-creswick-chinese-camp.jpg`
- `assets/verified-findings/VCH-078-kong-meng-historic-reserve.jpg`
- `assets/verified-findings/VCH-079-thomas-coto-gravestone.jpg`
- `assets/verified-findings/VCH-080-bowmans-forest-cemetery.jpg`
- `assets/verified-findings/VCH-081-chiltern-cemetery.jpg`
- `assets/verified-findings/VCH-082-myrtleford-cemetery.jpg`
- `assets/verified-findings/VCH-083-stanley-alluvial-goldfields.jpg`
- `assets/verified-findings/VCH-084-stanley-pioneer-cemetery.jpg`
- `assets/verified-findings/VCH-085-wangaratta-cemetery.jpg`
- `assets/verified-findings/VCH-086-harry-goons-hut.jpg`

Required action: obtain written permission from each named photographer/rightsholder or courtesy organisation. Identify the photographers for VCH-083 and VCH-084 before seeking permission.

#### Other institutions and websites — 5

- `assets/verified-findings/VCH-004-peter-ah-sen-saw-mill.jpg` — Victorian Heritage Database image; image-specific reuse terms are not recorded. General Victorian Government CC terms exclude images and third-party content unless stated otherwise.
- `assets/verified-findings/VCH-019-georgies-hut.jpg` — Victorian Collections object photograph; no republication terms documented.
- `assets/verified-findings/VCH-021-avoca-cemetery-burner.jpg` — Avoca and District Historical Society image; no republication terms documented.
- `assets/verified-findings/VCH-035-whroo-cemetery.jpg` — Whroo Cemetery Trust image; no republication terms documented.
- `assets/verified-findings/VCH-038-echuca-cemetery-burner.jpg` — Find a Grave image URL; contributor identity and permission are not documented.

Required action: obtain written permission from the authorised rightsholder or replace each image.

#### Walk from Robe illustrations — 2

- `assets/heritage-images/robe-pai-fang-welcoming-gate.jpg` — ABC photograph credited to Sam Bradbrook, 2024; no project-held republication permission is documented.
- `assets/heritage-images/walk-from-robe-route.png` — derived from Samuel Charles Brees, *Flemington, Melbourne*, c.1856. The underlying work is likely public domain, but the exact collection record, download terms, copyright-duration basis, and project modifications are not documented.

Required action: obtain ABC/rightsholder permission or replace the contemporary photograph. Complete and retain the public-domain and modification record for the historical route artwork.

## Generated preview and proposal materials

### Homepage animated preview — 1 file

- `media/map-interaction-demo.gif`

The GIF is generated by `scripts/build_map_interaction_gif.swift` from `proposal/screenshots/03-explorer-map.png` and `assets/verified-findings/VCH-007-white-hills-cemetery.jpg`. It reproduces a map/interface screenshot and a CC BY-SA 4.0 photograph. The animation is publicly displayed on `index.html` but has no adjacent creator, source, licence, or modification statement.

Required action: document the screenshot’s tile/source attribution, comply with the photograph’s CC BY-SA terms, identify the GIF as modified/composited, and determine the appropriate share-alike treatment. Regenerate it without any uncleared constituent element if needed.

### Proposal screenshots — 8 files

- `proposal/screenshots/01-hero.png`
- `proposal/screenshots/02-history-overview.png`
- `proposal/screenshots/03-explorer-map.png`
- `proposal/screenshots/04-detail-bendigo-joss-house.png`
- `proposal/screenshots/05-detail-castlemaine-burner.png`
- `proposal/screenshots/06-filters.png`
- `proposal/screenshots/07-era-timeline.png`
- `proposal/screenshots/08-evidence-about.png`

These are project-made screenshots but may reproduce third-party photographs, map tiles, institutional text, logos, and interface assets. A screenshot is a new file, not a clean grant of rights over everything visible inside it. Screenshot 03 is published from `proposal/PROJECT_PROPOSAL.html` and Markdown, is used to build the public GIF, and is embedded in the proposal DOCX after resizing or recomposition.

Two byte-identical copies of the proposal document exist:

- `PROJECT_PROPOSAL.docx`
- `proposal/PROJECT_PROPOSAL.docx`

Each DOCX contains one embedded interface image. Distribution of either document reproduces that image. Remove duplicate deliverables and use a cleared, attribution-complete demonstration image before external distribution.

## Research-only image collections

### Scattered Legacy copies — 16 files

All files in `research_outputs/scattered_legacy_key_photos/` lack documented republication permission. The same 16 pictures are embedded in `research_outputs/scattered_legacy_victorian_map_audit_2026-07-30.xlsx`.

Status: **keep private**. Do not publish the folder or distribute the workbook until permission is documented, or regenerate the workbook without embedded images. Also review whether copied catalogue prose or substantial metadata should remain in a public version.

### Monument Australia copies — 5 files

- `cemetery_records/raw/linton_memorial_0.jpg`
- `cemetery_records/raw/linton_memorial_1.jpg`
- `cemetery_records/raw/linton_memorial_2.jpg`
- `cemetery_records/raw/linton_memorial_3.jpg`
- `cemetery_records/raw/linton_memorial_4.jpg`

The captured source page carries an express copyright notice and no open licence is recorded. Status: **keep private or obtain written permission**.

## Interface assets and branding

### Leaflet images — 5 files

- `images/layers-2x.png`
- `images/layers.png`
- `images/marker-icon-2x.png`
- `images/marker-icon.png`
- `images/marker-shadow.png`

These are Leaflet distribution assets covered by Leaflet’s BSD-2-Clause licence. They can be redistributed if the required copyright, licence conditions, and disclaimer are retained. The repository does not currently include a complete Leaflet notice file.

### CCCAV logo — 1 file

- `cccav-logo.png`

Confirm in writing that CCCAV owns the logo or has authorised this project to display it. Treat it as protected branding/trademark material excluded from the MIT licence and from downstream reuse, even if the project is authorised to use it.

## Text, code, datasets, and source captures

### Project-authored webpage, prose, translations, and scripts

Likely project-owned material includes the portal HTML/CSS/JavaScript, project prose, research notes, translation catalogues, extraction/build scripts, and original analytical selection. Facts, names, dates, and coordinates are generally not protected as facts, but source prose, photographs, database structure, and original selection or arrangement may be protected.

The 86 place summaries appear primarily project-authored or paraphrased, but no sentence-by-sentence source comparison has been completed. Preserve item-level citations and avoid copying distinctive source language. Community submissions also need contributor terms covering permission, attribution, privacy, correction, withdrawal, and the project’s right to edit and publish.

Recommended licence structure:

- MIT only for specifically identified project-owned software;
- a separate content/data licence for project-owned prose and original compilation, if desired;
- explicit exclusions for all third-party images, source captures, logos, embedded media, community submissions, and third-party-derived datasets;
- a clear rights notice on the public website and in downloadable packages.

### Third-party software

- `leaflet-1.9.4.js`, `leaflet-1.9.4.css`, and `images/*` — Leaflet, BSD-2-Clause
- `leaflet.markercluster-1.5.3.js` and `MarkerCluster-1.5.3.css` — Leaflet.markercluster, MIT

The repository must ship the relevant upstream notices. Add a `THIRD_PARTY_NOTICES.md` file or the upstream licence files. Do not imply that third-party software is licensed by the project’s own MIT grant.

### Hosted maps and tiles

The explorer uses OpenStreetMap-derived and third-party tile services and displays attribution in the map interface. Before release:

- retain visible attribution for every basemap and screenshot;
- verify each provider’s current usage and screenshot/publication terms;
- use the correct OpenStreetMap tile endpoint, allow a valid browser referrer, honour caching, and do not bulk-download or prefetch tiles;
- verify that CARTO and Esri layers are permitted for the intended traffic and use;
- do not describe hosted tiles or screenshots of tiles as covered by the repository’s MIT licence.

### Cemetery source captures — 27 files

`cemetery_records/raw/` currently contains:

- 12 captured HTML pages;
- 3 JSON downloads;
- 2 CSV metadata downloads;
- 3 PDFs;
- 2 XLS workbooks;
- 5 JPG photographs.

These are source copies, not project-owned publications. Private research retention and public redistribution are different acts. Keep the raw directory out of public deployment unless a source-specific licence, permission, public-domain basis, or applicable legal exception is documented.

The complete `cafhov_mgc_collection.csv` and the older Melbourne metadata export each contain 544 rows. In each file, 537 rows state CC BY-NC 4.0 and require attribution to Chinese Australian Family Historians of Victoria; seven rows have blank rights fields. The blank rows must not be assumed licensed. CC BY-NC permits sharing and adaptation only subject to attribution and noncommercial conditions and does not grant unrelated privacy, publicity, trademark, or moral rights.

The Ballarat, Creswick, Echuca, Whroo, and Yackandandah bulk exports or transcriptions have no repository-level redistribution permission on record. Individual factual entries may be unprotected as facts, but the compilation, copied expression, access terms, and contractual restrictions still require source-specific review.

### Extracted and browser-packaged cemetery data

`cemetery_records/extracted/` contains seven CSV files. `chinese_names.csv` contains 720 displayed records, including 534 derived from CAFHOV. The public `cemetery-records-data.js` packages all 720 records directly into the website and includes:

- names and Chinese characters;
- dates, locations, plots, notes, pronunciations, aliases, and other source-derived metadata where available;
- 768 photograph-link fields representing 690 unique external photograph URLs;
- source and source-record links.

Linking to an external photograph is not the same as storing a local copy, but packaging and republishing source metadata and deep links still requires compliance with the source licence and applicable terms. The detail page currently gives CAFHOV attribution and links CC BY-NC 4.0, which is helpful but does not resolve the seven blank-rights rows or permissions for the other bulk datasets.

Status: **do not license the extracted CSVs or browser package under MIT**. Record a source-by-source data basis, keep required attribution with the records, restrict CAFHOV-derived material to compliant noncommercial use unless further permission is obtained, and consider publishing analytical summaries or a reproducible extraction method instead of unrestricted bulk data.

### Scattered Legacy workbook and build script

- `research_outputs/scattered_legacy_victorian_map_audit_2026-07-30.xlsx` contains catalogue text/metadata and 16 embedded third-party images.
- `research_outputs/scattered_legacy_key_photos/` contains the same images separately.
- `scripts/build_scattered_legacy_audit.py` downloads, resizes, and embeds those images.

The script can be project-owned, but running it does not create republication rights. Keep the workbook private or regenerate a public version without embedded pictures and without substantial copied catalogue expression.

## Git and deployment status observed

The configured remote is `github.com/saturnjay/victorian_chinese_heritage`. At this update:

- the 19 provisionally reusable heritage images, CCCAV logo, Leaflet files, and Leaflet images are tracked;
- the 28 unresolved public-page images remain untracked;
- the proposal, research output, cemetery, media, and most rebuilt portal files are untracked;
- `index.html` and `README.md` have local modifications;
- no `.gitignore` is present;
- `.Rhistory` is present and untracked;
- the two proposal DOCX files are exact duplicates.

This remains a useful containment point. **Do not run a blanket `git add .` or deploy the repository root.** Use a deployment allowlist, add a rights-aware `.gitignore`, move private research evidence outside the public web root, remove incidental environment files, and commit only materials approved for release.

## Release gate

A public release should proceed only when all of the following are complete:

1. The 28 unresolved public heritage/content images have written permission, a verified applicable licence, or have been removed/replaced.
2. Every retained CC or public-domain image has a durable attribution and verification record, including modifications.
3. The animated GIF and externally distributed proposal screenshots/documents have been checked for all constituent image, map-tile, logo, and share-alike obligations.
4. Research-only source captures, Monument Australia images, Scattered Legacy images/workbook, and non-public proposal materials are excluded from the public repository and deployment.
5. The top-level licence is expressly limited to identified project-owned code and excludes all third-party and restricted material.
6. Complete Leaflet and Leaflet.markercluster notices are included.
7. CCCAV confirms logo authorisation and the logo is expressly excluded from downstream reuse.
8. A source-by-source data-rights register covers all seven cemetery extracts and the browser package, including CAFHOV attribution, CC BY-NC conditions, and the seven blank-rights records.
9. The public cemetery interface accurately communicates noncommercial/source restrictions and does not imply that linked grave photographs are project-owned.
10. OSM, CARTO, and Esri attribution and service policies are verified for the interactive map, screenshots, and GIF.
11. Community-contribution terms address rights, consent, privacy, attribution, editing, withdrawal, and culturally sensitive information.
12. A deployment allowlist or equivalent process prevents raw research files, workbooks, duplicate documents, `.Rhistory`, and uncleared media from being published accidentally.

## Authoritative guidance checked

- Australian Attorney-General’s Department, [Copyright basics](https://www.ag.gov.au/rights-and-protections/copyright/copyright-basics) and [For copyright users](https://www.ag.gov.au/rights-and-protections/copyright/copyright-users) — copyright protects photographs, maps, writing, software, and other original expression; use generally needs permission, an applicable licence, public-domain status, or a legal exception. Written permission is preferable where no licence applies.
- Creative Commons, [CC BY-NC 4.0 deed](https://creativecommons.org/licenses/by-nc/4.0/) and [legal code](https://creativecommons.org/licenses/by-nc/4.0/legalcode.en) — attribution, licence link, change indication, noncommercial use, and no additional restrictions are conditions; other rights may still apply.
- Victorian Government, [Copyright](https://www.vic.gov.au/copyright) — its general CC BY 4.0 statement excludes images, branding, and third-party material unless separately cleared.
- OpenStreetMap Foundation, [Tile Usage Policy](https://operations.osmfoundation.org/policies/tiles/) — requires visible attribution, the correct endpoint, valid identification/referrer behaviour, cache compliance, and no bulk download or prefetch.
- Leaflet, [BSD-2-Clause licence](https://github.com/Leaflet/Leaflet/blob/main/LICENSE), and Leaflet.markercluster, [MIT licence](https://github.com/Leaflet/Leaflet.markercluster) — redistribution requires retention of the relevant notices and conditions.
- ABC, [Terms of Use](https://help.abc.net.au/hc/en-us/articles/360001548096-ABC-Terms-of-Use) — no project-held permission for the Robe photograph is documented.
- University of Idaho, [Chinese Funerary Burners: A Census](https://www.lib.uidaho.edu/special-collections/t-abraham/burners.htm) — photographer credits are present, but no open-reuse licence is recorded in the project.

## Priority next action

Create a machine-readable rights register for every public image and dataset with fields for asset path, source, creator, rightsholder, licence/version, licence URL, permission evidence, permitted uses, attribution text, modification, review date, publication status, and replacement action. Use that register to generate both public attributions and the deployment allowlist.
