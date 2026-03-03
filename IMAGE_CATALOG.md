# Nancy Image Asset Catalog

> Last updated: 2026-03-03
> Total tagged images: 102+ (growing as loox download completes)

## Summary

| Source | Count | Notes |
|--------|-------|-------|
| Ad Creatives (Glued) | 50 | Top-performing last 90 days by spend + ROAS |
| Loox Review Photos | 10 local + ~450 downloading | Real customer photos from CSV export |
| Product Photography | 23 | PDP shots, gallery, hero images |
| AI-Generated | 3 | Lifestyle renders — QC for artifacts |
| UGC Branded Posters | 4 | **CAUTION**: Have visible name text, cause mismatches |
| UGC TikTok | 3 | Real TikTok screenshots — good for UGC grids |
| Media Logos | 5 | TimeOut, Tatler, Zenify, Vice, Vocal |
| Brand Logos | 3 | Nancy full logo, pink variants (SVG + PNG) |

## File Structure

```
nancy-landing-pages/
├── assets/
│   ├── loox-reviews/           ← Downloaded from Loox CSV (452 images)
│   │   ├── lem/                ← ~138 images
│   │   ├── uno/                ← (downloading)
│   │   ├── berri/              ← (downloading)
│   │   ├── other/              ← ~30 images
│   │   └── loox-metadata.json  ← Review text, rating, date, verified
│   ├── winning-ads/            ← Top 50 from Glued MCP (last 90 days)
│   │   └── winning-ads-metadata.json ← ROAS, spend, conversions, entity name
│   ├── IMAGE_TAGS.json         ← Structured tags for every image
│   ├── generate_tags.py        ← Re-run to regenerate tags
│   ├── download_loox_images.py
│   └── download_winning_ads.py
├── images/                     ← Shared images (loox-review1-10, pdp shots)
├── lem/images/                 ← Lem-specific assets
│   ├── product/                ← Product photos, GIFs, lifestyle
│   ├── ugc/                    ← Branded poster cards (use with caution)
│   ├── winning/                ← Comparison/winning ad reference
│   ├── media/                  ← Press logos
│   └── logos/                  ← Nancy brand logos
└── IMAGE_CATALOG.md            ← This file
```

## Top 10 Winning Ad Creatives (Last 90 Days by Spend)

| # | Name | Spend (HKD) | ROAS | Conv | Type |
|---|------|-------------|------|------|------|
| 1 | NAN_JULW2_377A (manus.space LP) | 1,965K | 2.12x | 6,599 | image |
| 2 | Elevate Your Me-Time to Next Level | 940K | 2.03x | 3,057 | video |
| 3 | This New Year, Lem Ends the Guessing | 734K | 2.17x | 2,479 | image |
| 4 | Lem Video ACH DYLE 85 (Valentines) | 605K | 2.47x | 2,423 | video |
| 5 | This Valentine's, You Win | 579K | 2.03x | 1,904 | image |
| 6 | NAN_NOVW2_114C (Dutch) | 530K | 1.68x | 1,415 | image |
| 7 | This Toy Broke the Internet | 481K | 1.73x | 1,323 | video |
| 8 | Best Relaxation Devices of 2025 | 478K | 1.97x | 1,517 | image |
| 9 | Lem Video 4v3 (Valentines) | 454K | 1.93x | 1,366 | video |
| 10 | Lem Video ACH DYLE 67 | 444K | 2.70x | 1,914 | video |

Files: `assets/winning-ads/01_2.1x_1965k_image_e0eaacf8.jpg` through `50_*.jpg`

## Loox Review Images

Downloaded from `/Users/rahul/Downloads/Loox Reviews for Nancy.csv` (22,303 total reviews, 452 with images).

### By Product
- **Lem**: ~138 images (majority 5-star)
- **Other**: ~30 images
- **Uno/Berri**: In progress

### Best Use Cases
- **Review avatars**: Small 48px circles — use any organic customer photo
- **UGC grids**: Mix with TikTok screenshots for authentic social proof
- **Full-width features**: High-quality unboxing/product shots from reviewers

### Known Issues
- `loox-review10.jpg` in `/images/` may be AI-generated (different quality from others)
- Some review images are low-resolution phone photos

## Google Drive Asset Links (from Slack #static-studio-ner-nancy)

### Permanent Reference
| Folder | URL | Notes |
|--------|-----|-------|
| Best Performer Reference | [Drive](https://drive.google.com/drive/folders/1c4rl2aGyT0GajpYAd3s9TsaCayVWb4FJ) | Curated best performers |
| UGC Assets (288) | [Drive](https://drive.google.com/drive/folders/1B3sIIunp9UX_e_tDAAsn80Guz2Mz75Qn) | UGC creative assets |
| Master Drive Folder | [Drive](https://drive.google.com/drive/folders/1HMApskXsDIypMfSoWFeHBPuPnQLSK5XC) | Root folder |

### Weekly Creative Drops (2026)
| Week | Count | URL | Notes |
|------|-------|-----|-------|
| Feb W4 | 1,209 statics | [Drive](https://drive.google.com/drive/folders/1O8rP2j2V7PKL-Dt6rUBPnK3NNkcP-sFY) | Latest weekly drop |
| Feb W4 | 140 clone ads | [Drive](https://drive.google.com/drive/folders/181P--Q6xBr5g673SX1LedpDRCm3kY8QH) | Clone variants |
| Feb W1+W2 | 186 winners | [Drive](https://drive.google.com/drive/folders/1E2ajEVJ2jvZaap0Mf-e2rcibs1XYOuOv) | Weekly winners |
| Feb W1+W2 | 206 translations | [Drive](https://drive.google.com/drive/folders/1w2pxNoFcXyT9ZbuKt_yCt-id9NkAQ0LV) | Localized variants |
| Jan W4 | winners | [Drive](https://drive.google.com/drive/folders/1n2GcqHKkuUIPQVB6ZcSoL9_U3bry9Edn) | Winning creatives |
| Dec W4 | 405 assets | [Drive](https://drive.google.com/drive/folders/1wSZS2txM9bTplkKtpXDbyfP1NC8RDuGj) | Large batch |

## Known Issues & Cautions

### Branded Poster Cards (DO NOT use as avatars)
These files have visible name text — using them as avatars for different reviewers creates name mismatches:
- `lem/images/ugc/alyssa-g.png` — Shows "Alyssa Grenfell" (1.4MB)
- `lem/images/ugc/jordan-t.png` — Shows "Jordan Theresa" (1.2MB)
- `lem/images/ugc/daliza.png` — Shows "Daliza" (1.0MB)
- `lem/images/ugc/deliza.png` — Shows "Deliza" (1.0MB)

**Instead**: Use `images/loox-review*.jpg` (13-40KB each, no text overlay, organic look).

### AI-Generated Images (QC for Broken Nail Rule)
- `lem/images/product/lem-lifestyle-bathroom.png`
- `lem/images/product/lem-lifestyle-nightstand.png`
- `lem/images/product/lem-lifestyle-travel.png`

Check for: distorted nails, extra fingers, wrong product shape, text artifacts.

## Querying IMAGE_TAGS.json

```bash
# Find all 5-star loox images for Lem
python3 -c "
import json
tags = json.load(open('assets/IMAGE_TAGS.json'))
lem_5star = [t for t in tags if t['source']=='loox' and t['product']=='lem' and t.get('rating')==5]
print(f'{len(lem_5star)} images')
for t in lem_5star[:5]: print(f\"  {t['path']} ({t['size_kb']}KB)\")
"

# Find top winning ads by ROAS
python3 -c "
import json
tags = json.load(open('assets/IMAGE_TAGS.json'))
ads = [t for t in tags if t['source']=='ad-creative' and t.get('ad_roas')]
ads.sort(key=lambda x: x['ad_roas'], reverse=True)
for t in ads[:10]: print(f\"  {t['ad_roas']:.1f}x ROAS | {t['path']}\")
"

# Find organic images suitable for UGC grids
python3 -c "
import json
tags = json.load(open('assets/IMAGE_TAGS.json'))
ugc = [t for t in tags if t['organic_score'] >= 4 and 'ugc-grid' in t.get('best_use', [])]
print(f'{len(ugc)} images suitable for UGC grids')
"
```
