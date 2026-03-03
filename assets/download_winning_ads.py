#!/usr/bin/env python3
"""Download top winning ad creatives from Glued MCP query results."""
import json
import os
import time
import urllib.request
import ssl

TOOL_RESULTS_DIR = "/Users/rahul/.claude/projects/-Users-rahul-Downloads/0145dc3a-765c-490d-a067-1d01a5643da7/tool-results"
OUTPUT_DIR = "/Users/rahul/Downloads/nancy-landing-pages/assets/winning-ads"

# SSL workaround for macOS
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def load_glued_results():
    """Load both result files and merge creatives."""
    all_creatives = {}

    for fname in os.listdir(TOOL_RESULTS_DIR):
        if not fname.startswith('toolu_01') or not fname.endswith('.json'):
            continue
        fpath = os.path.join(TOOL_RESULTS_DIR, fname)
        try:
            with open(fpath, 'r') as f:
                data = json.load(f)
            if isinstance(data, list) and len(data) > 0 and 'text' in data[0]:
                parsed = json.loads(data[0]['text'])
                if 'rows' in parsed:
                    for row in parsed['rows']:
                        key = row.get('image_hash') or row.get('video_id') or row.get('entity_id')
                        if key and key not in all_creatives:
                            all_creatives[key] = row
        except Exception as e:
            print(f"  Skipping {fname}: {e}")

    return all_creatives

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    creatives = load_glued_results()
    print(f"Found {len(creatives)} unique creatives across result files")

    # Filter to ones with asset_url and meaningful spend
    downloadable = []
    for key, c in creatives.items():
        url = c.get('asset_url', '')
        spend = c.get('metrics', {}).get('spend', 0)
        if url and spend > 1000:  # Min HK$1000 spend
            downloadable.append(c)

    # Sort by spend descending
    downloadable.sort(key=lambda x: x['metrics']['spend'], reverse=True)
    print(f"Downloadable (spend > HK$1000): {len(downloadable)}")

    # Take top 50
    downloadable = downloadable[:50]

    metadata = []
    downloaded = 0
    failed = 0

    for i, c in enumerate(downloadable):
        url = c['asset_url']
        m = c['metrics']
        roas = m.get('roas', 0)
        spend = m.get('spend', 0)
        ctype = c.get('creative_type', 'unknown')
        hash_short = (c.get('image_hash') or c.get('video_id') or 'unknown')[:8]

        ext = '.jpg'
        if '.png' in url:
            ext = '.png'

        filename = f"{i+1:02d}_{roas:.1f}x_{spend/1000:.0f}k_{ctype}_{hash_short}{ext}"
        filepath = os.path.join(OUTPUT_DIR, filename)

        if os.path.exists(filepath):
            downloaded += 1
            metadata.append({
                "rank": i + 1,
                "filename": filename,
                "entity_name": c.get('entity_name', ''),
                "creative_type": ctype,
                "spend_hkd": spend,
                "roas": roas,
                "conversions": m.get('conversions', 0),
                "cpa_hkd": m.get('cpa', 0),
                "impressions": m.get('impressions', 0),
                "image_hash": c.get('image_hash'),
                "video_id": c.get('video_id'),
                "asset_url": url,
                "status": c.get('status', ''),
                "ad_count": c.get('ad_count', 0)
            })
            continue

        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
            })
            with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
                with open(filepath, 'wb') as out:
                    out.write(resp.read())
            downloaded += 1
            print(f"  [{i+1}/{len(downloadable)}] {filename} ({spend/1000:.0f}k HKD, {roas:.1f}x)")
        except Exception as e:
            print(f"  FAILED [{i+1}]: {str(e)[:60]}")
            failed += 1

        metadata.append({
            "rank": i + 1,
            "filename": filename,
            "entity_name": c.get('entity_name', ''),
            "creative_type": ctype,
            "spend_hkd": spend,
            "roas": roas,
            "conversions": m.get('conversions', 0),
            "cpa_hkd": m.get('cpa', 0),
            "impressions": m.get('impressions', 0),
            "image_hash": c.get('image_hash'),
            "video_id": c.get('video_id'),
            "asset_url": url,
            "status": c.get('status', ''),
            "ad_count": c.get('ad_count', 0)
        })

        time.sleep(0.5)

    # Save metadata
    with open(os.path.join(OUTPUT_DIR, "winning-ads-metadata.json"), 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"\nDone! Downloaded: {downloaded}, Failed: {failed}")
    print(f"Metadata saved to winning-ads-metadata.json")

if __name__ == "__main__":
    main()
