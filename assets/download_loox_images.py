#!/usr/bin/env python3
"""Download all Loox review images from CSV export."""
import csv
import json
import os
import time
import urllib.request
import ssl
import re

CSV_PATH = "/Users/rahul/Downloads/Loox Reviews for Nancy.csv"
OUTPUT_DIR = "/Users/rahul/Downloads/nancy-landing-pages/assets/loox-reviews"

# SSL workaround for macOS
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def sanitize(s):
    return re.sub(r'[^a-zA-Z0-9_-]', '', s.replace(' ', '-').replace('.', ''))[:30]

def main():
    metadata = []
    stats = {"total_with_images": 0, "downloaded": 0, "failed": 0, "by_product": {}, "by_rating": {}}

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows_with_images = [r for r in reader if r.get('img', '').strip()]

    print(f"Found {len(rows_with_images)} reviews with images")
    stats["total_with_images"] = len(rows_with_images)

    for i, row in enumerate(rows_with_images):
        handle = (row.get('handle') or 'other').strip().lower()
        rating = row.get('rating', '0')
        review_id = row.get('id', f'unknown_{i}')
        nickname = sanitize(row.get('nickname', 'anon'))
        img_urls = [u.strip() for u in row['img'].split(',') if u.strip()]

        # Determine output subfolder
        if handle in ('lem', 'uno', 'berri'):
            subfolder = handle
        else:
            subfolder = 'other'

        # Stats
        stats["by_product"][handle] = stats["by_product"].get(handle, 0) + 1
        stats["by_rating"][rating] = stats["by_rating"].get(rating, 0) + 1

        out_dir = os.path.join(OUTPUT_DIR, subfolder)
        os.makedirs(out_dir, exist_ok=True)

        downloaded_paths = []
        for j, url in enumerate(img_urls):
            suffix = f"_{j}" if len(img_urls) > 1 else ""
            ext = ".jpg"
            if ".png" in url.lower():
                ext = ".png"
            elif ".webp" in url.lower():
                ext = ".webp"

            filename = f"{handle}_{rating}star_{nickname}_{review_id}{suffix}{ext}"
            filepath = os.path.join(out_dir, filename)

            if os.path.exists(filepath):
                downloaded_paths.append(f"loox-reviews/{subfolder}/{filename}")
                stats["downloaded"] += 1
                continue

            try:
                req = urllib.request.Request(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
                })
                with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
                    with open(filepath, 'wb') as out:
                        out.write(resp.read())
                downloaded_paths.append(f"loox-reviews/{subfolder}/{filename}")
                stats["downloaded"] += 1
                if (stats["downloaded"] % 50) == 0:
                    print(f"  Downloaded {stats['downloaded']}/{stats['total_with_images']}...")
            except Exception as e:
                print(f"  FAILED: {url[:60]}... - {e}")
                stats["failed"] += 1

            time.sleep(0.3)

        metadata.append({
            "id": review_id,
            "nickname": row.get('nickname', ''),
            "rating": int(rating) if rating.isdigit() else 0,
            "review": row.get('review', ''),
            "date": row.get('date', ''),
            "product": handle,
            "verified_purchase": row.get('verified_purchase', '') == 'true',
            "image_paths": downloaded_paths,
            "original_urls": img_urls
        })

    # Save metadata
    meta_path = os.path.join(OUTPUT_DIR, "loox-metadata.json")
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"\nDone!")
    print(f"  Total with images: {stats['total_with_images']}")
    print(f"  Downloaded: {stats['downloaded']}")
    print(f"  Failed: {stats['failed']}")
    print(f"  By product: {json.dumps(stats['by_product'], indent=2)}")
    print(f"  By rating: {json.dumps(stats['by_rating'], indent=2)}")

    # Save stats
    with open(os.path.join(OUTPUT_DIR, "download-stats.json"), 'w') as f:
        json.dump(stats, f, indent=2)

if __name__ == "__main__":
    main()
