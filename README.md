# Victorian Chinese Heritage Research Package

**Documentary evidence reviewed:** 28 July 2026  
**Inventory size:** 73 mapped findings  
**Heritage Victoria 2022 core:** 19 findings

The current evidence audit reviewed all 73 findings and live-checked 131 distinct cited URLs. Seventy-one findings are verified against current documentary evidence; one is retained as documentary history without a verified surviving feature, and one remains a field-verification lead. Reusable, human-reviewed photographs were located for 18 findings (17 unique image files). This is source verification, not a statutory certificate or physical site inspection.

## Files

- `victorian_chinese_heritage_map.html` — interactive searchable Leaflet map with clickable histories, protection notes, access cautions and source links.
- `victorian_chinese_heritage_inventory.xlsx` — polished 39-field research workbook with Overview, Inventory, Sources, Methodology, Data Dictionary and Map Legend sheets.
- `victorian_chinese_heritage_inventory.csv` — UTF-8 version of the complete inventory.
- `victorian_chinese_heritage.geojson` — point layer for GIS and web-mapping use, retaining all research fields as properties.
- `victorian_chinese_heritage_sources.csv` — normalised one-URL-per-row source register showing every linked finding.
- `verification/` — per-finding verification outcomes, full URL response audit, corrected-link log, image metadata, rights information and machine-readable summaries.
- `assets/verified-findings/` — locally saved, reusable finding photographs with attribution recorded in `verification/image_metadata.csv`.
- `victorian_chinese_heritage_verified_package_2026-07-28.zip` — portable evidence package containing the verified data, photographs, metadata and updated map.
- `qa_report.txt` — automated validation summary generated with this release.
- `leaflet-1.9.4.js` and `leaflet-1.9.4.css` — pinned local map engine files, allowing the explorer itself to start without a CDN.
- `leaflet.markercluster-1.5.3.js` and `MarkerCluster-1.5.3.css` — pinned local clustering files for dense groups of findings.

## Coverage

The inventory is a comprehensive working compilation of publicly documented Chinese heritage in Victoria, not a legal or final exhaustive register. It includes:

- all 19 places and objects on Heritage Victoria's 2022 Chinese-heritage selection page;
- state-registered buildings, objects, cemeteries, landscapes and archaeological places;
- Victorian Heritage Inventory and other documented historical archaeology;
- Chinese cemetery sections, separate burial grounds, funerary burners, headstones, memorials and documented unmarked graves;
- temples, churches, missions, association premises, residences, commercial buildings and urban precincts;
- mining camps, villages, tunnels, pig ovens, kilns, market gardens and industrial sites;
- museums, archives, public monuments, reconstructed places and well-documented former sites.

Heritage Victoria states that its 2022 selection is not exhaustive. The Victorian Heritage Inventory likewise notes that its archaeological listing is not comprehensive and that historical archaeological sites can be protected whether or not they are already listed.

## Location and coordinate method

Every record has decimal-degree WGS84 latitude and longitude plus two explanatory fields:

- **Coordinate precision** — published point, address/visitor point, precinct centroid, landscape vicinity, former-site vicinity, generalised sensitive location, and similar wording.
- **Coordinate basis / note** — what the point represents and what it does not represent.

Coordinates are orientation points, not survey or statutory boundaries. Sensitive archaeology, burial grounds and reports of exposed artefacts are deliberately generalised where appropriate. Multiple records at the same visitor destination can be offset by a few metres on the HTML map solely so every marker can be clicked; pop-ups report the stored coordinates.

## Inclusion tiers

- **Core statutory — Heritage Victoria 2022 selection:** 19
- **Documented former / reconstructed heritage:** 6
- **Documented former / unlocated heritage:** 1
- **Reported / field verification needed:** 1
- **Verified public heritage:** 45
- **Verified public heritage / modern interpretation:** 1

## Findings by region

- **Gippsland:** 3
- **Goldfields:** 35
- **Grampians:** 4
- **High Country:** 12
- **Metropolitan Melbourne:** 17
- **Murray:** 1
- **Wimmera Mallee:** 1

## Findings by map group

- **Built heritage:** 9
- **Cemeteries & funerary heritage:** 24
- **Industry & work:** 1
- **Market gardens & industry:** 6
- **Memorials & public art:** 5
- **Mining & archaeology:** 11
- **Museums, collections & interpretation:** 5
- **Temples & religion:** 9
- **Urban precincts & community places:** 3

## Source grading

- **A:** statutory register, government dataset or official custodian/operator.
- **B:** council, cemetery trust, museum database, academic or specialist heritage project.
- **C:** local history, architectural guide, visitor guide or historical society; useful but should be cross-checked for legal or parcel-level use.
- **D:** community report or field lead requiring professional verification.

The source-grade wording in each record may combine grades when, for example, a statutory identity is paired with a secondary coordinate.

## Responsible and lawful use

A public point does not grant public access. Confirm current ownership, opening hours, closures, cultural protocols and permit requirements before visiting. Do not:

- trespass on private or restricted land;
- disturb graves, headstones, funerary structures or memorials;
- enter mine shafts, unstable workings or fenced archaeological areas;
- dig, probe, metal-detect, remove pottery or collect artefacts;
- treat a reconstructed museum feature as original nineteenth-century fabric;
- rely on this package as a heritage certificate or cadastral boundary.

For statutory decisions, consult Heritage Victoria, the Victorian Heritage Database, the relevant council planning scheme, the land manager, cemetery trust or community custodian.

## Using the webpage

Keep the four local Leaflet files beside `victorian_chinese_heritage_map.html`, then open the HTML file in a modern browser. For the most dependable background-map loading, publish the folder to an HTTPS website or open it through a local static web server.

The page is designed as an educational journey through Chinese Victorian history. Begin with the four era cards, or use the Previous and Next controls above the map to move through the findings in chronological order. When focus is not inside a form field, the Left and Right Arrow keys provide the same navigation. The chronological index, filters and map remain coordinated, while each detail panel explains the date, historical significance, evidence quality and source links for the selected place.

Before the Learning Path, a visual history overview combines a documentary photo mosaic, three evidence milestones and a five-part timeline from the pre-gold-rush presence to contemporary Victoria. Its research trail is recorded in `verification/history_overview_sources.csv`.

The research data, filters and detail panels are embedded in the HTML and remain usable offline. Background tiles require an internet connection. If both providers are unavailable, the explorer automatically retains its markers on a neutral background and offers a retry action. Search covers all fields, including place names, locations, histories and register identifiers; map position changes only when a visitor chooses a finding, Home or Fit results.

## Known limitations

- Public registers and local heritage studies continue to change.
- Several former sites require archival mapping or professional archaeological survey before a parcel or feature can be located precisely.
- Some cemetery counts are historical estimates and many burials have no visible marker.
- Operating hours and restoration status can change after 28 July 2026.
- A small number of community-reported or local-memory sites are retained as clearly labelled verification leads rather than confirmed archaeology.

## Suggested citation

Jian Chen and the Chinese Community Council of Australia (Victoria), *Victorian Chinese Heritage: A History Measured in Generations*, 73 mapped findings, documentary evidence reviewed 28 July 2026. Use the primary and additional source URLs attached to each finding when citing an individual place. See [www.cccav.org.au](https://www.cccav.org.au).
