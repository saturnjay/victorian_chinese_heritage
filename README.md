# Victorian Chinese Heritage Map

An interactive research map documenting places connected with Chinese migration, work, community life, religion, burial, commemoration and heritage interpretation across Victoria.

- **Evidence reviewed through:** 30 July 2026
- **Mapped findings:** 86
- **Heritage Victoria 2022 core selection:** 19
- **Documentary verification:** 79 verified, 1 documentary-only, 6 requiring field verification
- **Findings with registered photographs:** 41

The project is a working compilation of publicly documented heritage, not a statutory register, heritage certificate or physical inspection of every site. Coordinates are research and visitor-orientation points rather than cadastral or statutory boundaries.

## Latest research update

The map began this review with 73 records. Two Chinese funerary-burner leads from the University of Idaho census were added as VCH-074 and VCH-075, bringing the interim total to 75.

A subsequent comparison with [Scattered Legacy](https://www.scatteredlegacy.org.au) examined 112 Victorian catalogue records:

- 45 were already represented by a map finding or an equivalent feature;
- 11 were assessed as the strongest potential additions;
- 24 were retained as documentary leads requiring more evidence before mapping;
- the remaining records primarily provide collection, object or historical context, with four excluded or questioned because of uncertain attribution, location or Victorian relevance.

All 11 strongest candidates have now been added as VCH-076–VCH-086. Eight have sufficient evidence for verified public-heritage status. Three are mapped cautiously as documentary leads with generalised coordinates and field-verification warnings.

| ID | Added finding | Current assessment |
|---|---|---|
| VCH-076 | Avoca Chinese Garden | Verified public heritage |
| VCH-077 | Creswick Chinese Camp site at Calembeen Park | Verified public heritage |
| VCH-078 | Kong Meng Historic Reserve | Verified public heritage |
| VCH-079 | Thomas Coto gravestone, Sale Cemetery | Verified public heritage |
| VCH-080 | Bowmans Forest Cemetery Chinese and Strangers section | Verified public heritage |
| VCH-081 | Chiltern Cemetery Chinese section | Verified public heritage |
| VCH-082 | Myrtleford Pioneer Cemetery Chinese section and memorial | Verified public heritage |
| VCH-083 | Stanley Chinese alluvial goldfields | Documentary lead — field verification required |
| VCH-084 | Stanley Pioneer Cemetery Chinese burials | Documentary lead — field verification required |
| VCH-085 | Wangaratta Cemetery Chinese and Strangers section | Verified public heritage |
| VCH-086 | Harry Goon's Hut and Chinese market garden camp, Wodonga | Documentary lead — field verification required |

The Peter Ah Sen Saw Mill record, VCH-004, also now includes the Victorian Heritage Database photograph supplied for the project.

## Current coverage

### Verification status

- **Verified:** 79
- **Documentary only:** 1
- **Field verification required:** 6

Verification here means that the place identity, association or published evidence was matched to the cited documentary sources. It does not mean that the site was physically inspected in 2026.

### Inclusion tiers

- **Core statutory — Heritage Victoria 2022 selection:** 19
- **Verified public heritage:** 53
- **Verified public heritage / modern interpretation:** 1
- **Documented former / reconstructed heritage:** 6
- **Documented former / unlocated heritage:** 1
- **Documentary lead — field verification required:** 5
- **Reported / field verification needed:** 1

### Findings by region

- **Goldfields:** 40
- **High Country:** 19
- **Metropolitan Melbourne:** 17
- **Gippsland:** 4
- **Grampians:** 4
- **Murray:** 1
- **Wimmera Mallee:** 1

### Findings by map group

- **Cemeteries & funerary heritage:** 32
- **Mining & archaeology:** 13
- **Built heritage:** 9
- **Temples & religion:** 9
- **Market gardens & industry:** 7
- **Memorials & public art:** 6
- **Museums, collections & interpretation:** 5
- **Urban precincts & community places:** 4
- **Industry & work:** 1

## What the map includes

The inventory brings together:

- all 19 places and objects identified on Heritage Victoria's 2022 Chinese-heritage selection page;
- Victorian Heritage Register places, Victorian Heritage Inventory archaeology and local heritage evidence;
- Chinese cemetery sections, separate burial grounds, funerary burners, headstones, memorials and documented unmarked graves;
- temples, churches, missions, association premises, residences, shops and urban precincts;
- mining camps, landscapes, tunnels, pig ovens, kilns, market gardens and industrial sites;
- museums, archives, public monuments, reconstructed places and well-documented former sites.

Heritage Victoria states that its published Chinese-heritage selection is not exhaustive. Historical archaeological places may also be protected even when they have not yet been entered in the Victorian Heritage Inventory.

## Repository contents

- `index.html` — the current interactive map and embedded 86-record research dataset.
- `assets/heritage-images/` — images used in the historical overview and featured interpretation.
- `assets/verified-findings/` — local research copies of finding photographs used by the map.
- `research_outputs/scattered_legacy_victorian_map_audit_2026-07-30.xlsx` — the Scattered Legacy comparison workbook, including the 75-record pre-addition map baseline, 112-record Victorian audit, candidate assessment, image metadata, key photographs and methodology.
- `research_outputs/scattered_legacy_key_photos/` — research-reference copies of selected Scattered Legacy images.
- `cemetery_records/` — source captures, extracted cemetery data, name tables and supporting scripts for the cemetery research stream.
- `scripts/build_scattered_legacy_audit.py` — reproducible workbook-generation script for the Scattered Legacy audit.
- `leaflet-1.9.4.js`, `leaflet-1.9.4.css`, `leaflet.markercluster-1.5.3.js` and `MarkerCluster-1.5.3.css` — pinned local mapping and marker-clustering libraries.

The Scattered Legacy workbook is an audit snapshot created before VCH-076–VCH-086 were added. It intentionally retains the earlier 75-record baseline so the evidence and selection process remain traceable.

## Using the webpage

Open `index.html` in a modern browser or serve the repository through GitHub Pages or another HTTPS static host. The research records, filters and detail panels are embedded in the HTML. Background map tiles and external source links require an internet connection.

Visitors can:

- search names, locations, histories and register identifiers;
- filter by heritage group, region, inclusion tier and confidence;
- select markers or use the chronological finding index;
- review historical summaries, surviving evidence, protection, access and sensitivity notes;
- inspect source links, verification notes and photograph attribution.

The map offsets markers that share the same visitor point by a few metres so that each record remains clickable. The stored coordinates shown in the record are not changed.

## Coordinate method

Every finding records WGS84 latitude and longitude together with:

- **Coordinate precision** — for example, published point, visitor point, site vicinity, landscape vicinity or generalised sensitive location.
- **Coordinate basis / note** — an explanation of what the point represents and what it does not represent.

Sensitive archaeology, burial places, uncertain former sites and private-property leads are generalised where appropriate. Do not use the points as survey coordinates, property boundaries or locations for ground disturbance.

## Source grading

- **A:** statutory register, government dataset or official custodian/operator.
- **B:** council, cemetery trust, museum, academic source or specialist heritage project.
- **C:** local history, historical society, architectural guide or visitor source that should be corroborated for legal or parcel-level use.
- **D:** community report or field lead requiring professional verification.

A record may use a combined grade where, for example, an authoritative place identity is paired with a secondary visitor coordinate.

## Photographs and rights

The map currently registers photographs for 41 findings. Each displayed photograph includes its source, stated creator or courtesy, relevance and available licence information.

Some files are reusable under an identified open licence; others are research-reference copies for which reuse permission has not been established. In particular, inclusion in Scattered Legacy or another catalogue does not by itself establish permission to republish an image. Check the original source, named photographer, institution or rights holder before public reuse.

The map's image record for each Scattered Legacy addition explicitly states **“Reuse permission not established.”**

## Responsible and lawful use

A public map point does not grant public access. Confirm ownership, opening hours, closures, cultural protocols and permit requirements before visiting. Do not:

- trespass on private or restricted land;
- disturb graves, headstones, funerary structures or memorials;
- enter mine shafts, unstable workings or fenced archaeological areas;
- dig, probe, metal-detect, remove pottery or collect artefacts;
- treat a reconstructed museum feature as original nineteenth-century fabric;
- rely on this project as a heritage certificate or statutory boundary.

For statutory decisions, consult [Heritage Victoria](https://www.heritage.vic.gov.au), the [Victorian Heritage Database](https://vhd.heritagecouncil.vic.gov.au), the relevant council planning scheme, land manager, cemetery trust or community custodian.

## Known limitations and next research priorities

- Public registers, local studies, access conditions and site condition continue to change.
- Several former places require archival mapping, landowner consultation or archaeological survey before an exact parcel or surviving feature can be identified.
- Some cemetery burial counts are historical estimates, and many burials have no visible marker.
- VCH-083, VCH-084 and VCH-086 use cautious or generalised points pending field and custodian verification.
- Three earlier findings also remain field-verification records, and one former place is retained for documentary value without a verified surviving feature.
- The 24 Scattered Legacy documentary leads—many of them former joss houses—require stronger location and survival evidence before they should become separate map points.
- Image permissions must be resolved individually before photographs without a confirmed reuse licence are republished outside the research context.

## Suggested citation

Jian Chen and the Chinese Community Council of Australia (Victoria), *Victorian Chinese Heritage Map: A History Measured in Generations*, 86 mapped findings, documentary evidence reviewed through 30 July 2026. Cite the primary and additional source URLs attached to an individual finding when referring to that place. See [www.cccav.org.au](https://www.cccav.org.au).
