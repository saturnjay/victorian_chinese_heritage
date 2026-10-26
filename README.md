# Victorian Chinese Heritage website

## Repository layout

```text
.
├── index.html                 # Homepage
├── pages/                     # People, places, stories, research, donation, cemetery pages
├── assets/
│   ├── css/                   # Shared site styles
│   ├── js/                    # Site behaviour and translation runtime
│   │   └── i18n/              # Simplified and Traditional Chinese catalogues
│   ├── images/                # Logo, heritage illustrations and finding photographs
│   ├── media/                 # Animated map preview
│   └── vendor/                # Leaflet, its icons, and marker clustering
├── data/                      # Generated public browser datasets
├── .nojekyll
├── .gitignore
├── LICENSE
└── README.md
```

All paths are relative, including navigation, dataset images, and vendor icons, so the site can run under a GitHub repository subpath.

## Contents

- Eight HTML pages, with `index.html` as the homepage.
- Shared styles and scripts, translations, and generated heritage/cemetery datasets.
- Local Leaflet and marker-clustering libraries and icon images.
- Referenced images and the map preview animation, retaining relative paths.
- Original project `LICENSE`, `.nojekyll` to bypass Jekyll, and `.gitignore`.

## Updates

This is a deployment snapshot. Maintain content and rebuild the generated website in the original research project, then refresh the corresponding files here using the layout above. Generated HTML must retain the updated relative paths; copying the original root-level files directly will undo this organisation. The database, editable CSV files, templates, local editor, scripts, backups, review exports, source captures, research documents, and original Git history are excluded.

Map tiles, external sources, and external fonts require internet access. The contribution form opens the visitor's email application and does not require a backend.

## Attribution and existing publication limits

Retain on-page sources, captions, and credits. Existing project documentation identifies photographs whose reuse permission has not been established. This snapshot preserves the referenced images and their current notices; packaging the site does not resolve those permissions. The project code licence does not grant rights to third-party images or source material.