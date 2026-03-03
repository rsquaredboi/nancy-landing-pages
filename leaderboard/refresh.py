#!/usr/bin/env python3
"""
Nancy Asset Leaderboard — refresh.py
Scores and ranks all tagged images by a composite formula mixing:
  - Ad performance (ROAS × log(spend) × conversions)
  - Conversion rate (conversions / impressions)
  - Quality score (organic_score + rating + verified + no issues)
  - Page usage (count of HTML pages referencing the asset)
  - Engagement proxy (page_count, upgradeable to Clarity later)

Reads from:
  - assets/IMAGE_TAGS.json (610+ tagged images)
  - assets/winning-ads/winning-ads-metadata.json (50 ad records)
  - assets/loox-reviews/loox-metadata.json (452 review records)
  - All *.html files (page scan for image references)

Outputs:
  - leaderboard/leaderboard.json (top 500 scored assets)
"""

import json
import os
import re
import glob
import math
import hashlib
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(BASE, "assets")
LEADERBOARD_DIR = os.path.join(BASE, "leaderboard")

# Scoring weights
WEIGHTS = {
    "ad_perf": 0.30,
    "conv_rate": 0.25,
    "quality": 0.20,
    "page_usage": 0.15,
    "engagement": 0.10,
}

TOP_N = 500


def load_json(path):
    """Load JSON file, return empty list/dict on failure."""
    if not os.path.exists(path):
        print(f"  [SKIP] {path} not found")
        return []
    with open(path) as f:
        return json.load(f)


def scan_html_pages():
    """Scan all HTML files for image src references. Returns {relative_path: [page_names]}."""
    usage = {}
    html_files = glob.glob(os.path.join(BASE, "**", "*.html"), recursive=True)
    # Exclude leaderboard itself
    html_files = [f for f in html_files if "/leaderboard/" not in f]

    src_re = re.compile(r'(?:src|href)=["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp|svg))["\']', re.IGNORECASE)

    for html_path in html_files:
        page_name = os.path.relpath(html_path, BASE)
        try:
            with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            continue

        for match in src_re.finditer(content):
            img_ref = match.group(1)
            # Normalize: strip leading ../ or ./ and resolve relative to page dir
            if img_ref.startswith("http"):
                continue  # skip external URLs

            page_dir = os.path.dirname(page_name)
            if img_ref.startswith("../"):
                resolved = os.path.normpath(os.path.join(page_dir, img_ref))
            elif img_ref.startswith("./"):
                resolved = os.path.normpath(os.path.join(page_dir, img_ref[2:]))
            elif img_ref.startswith("/"):
                resolved = img_ref.lstrip("/")
            else:
                resolved = os.path.normpath(os.path.join(page_dir, img_ref))

            resolved = resolved.replace("\\", "/")  # Windows compat

            if resolved not in usage:
                usage[resolved] = []
            if page_name not in usage[resolved]:
                usage[resolved].append(page_name)

    return usage


def build_ad_lookup(winning_ads):
    """Build lookup from filename → ad record."""
    lookup = {}
    for ad in winning_ads:
        fname = ad.get("filename", "")
        if fname:
            lookup[fname] = ad
            # Also key by full path
            lookup[f"assets/winning-ads/{fname}"] = ad
    return lookup


def compute_raw_scores(assets, ad_lookup, page_usage):
    """Compute raw score dimensions for each asset."""
    scored = []

    for asset in assets:
        path = asset.get("path", "")

        # --- Ad Performance ---
        ad = ad_lookup.get(path) or ad_lookup.get(os.path.basename(path))
        roas = 0
        spend_hkd = 0
        conversions = 0
        impressions = 0

        if ad:
            roas = ad.get("roas", 0) or 0
            spend_hkd = ad.get("spend_hkd", 0) or 0
            conversions = ad.get("conversions", 0) or 0
            impressions = ad.get("impressions", 0) or 0
        elif asset.get("ad_roas"):
            roas = asset.get("ad_roas", 0) or 0
            spend_hkd = asset.get("ad_spend_hkd", 0) or 0
            conversions = asset.get("ad_conversions", 0) or 0

        # Ad perf = ROAS × log(1 + spend) × sqrt(conversions)
        ad_perf_raw = roas * math.log1p(spend_hkd) * math.sqrt(max(conversions, 0))

        # --- Conversion Rate ---
        conv_rate_raw = (conversions / impressions * 100) if impressions > 0 else 0

        # --- Quality Score ---
        organic = asset.get("organic_score", 0) or 0
        rating = asset.get("rating", 0) or 0
        verified = 1 if asset.get("verified_purchase") else 0
        no_issues = 1 if not asset.get("issues") else 0
        quality_raw = (organic / 5.0) * 40 + (rating / 5.0) * 30 + verified * 15 + no_issues * 15

        # --- Page Usage ---
        pages = page_usage.get(path, [])
        page_count = len(pages)

        # --- Engagement (proxy = page_count for now) ---
        engagement_raw = page_count * 1.0  # Upgradeable with Clarity data

        scored.append({
            "path": path,
            "product": asset.get("product", "unknown"),
            "type": asset.get("type", "unknown"),
            "source": asset.get("source", "unknown"),
            "raw": {
                "ad_perf": ad_perf_raw,
                "conv_rate": conv_rate_raw,
                "quality": quality_raw,
                "page_usage": page_count,
                "engagement": engagement_raw,
            },
            "metrics": {
                "roas": round(roas, 2) if roas else None,
                "spend_hkd": round(spend_hkd, 0) if spend_hkd else None,
                "conversions": int(conversions) if conversions else None,
                "impressions": int(impressions) if impressions else None,
                "organic_score": organic,
                "rating": asset.get("rating"),
                "verified_purchase": asset.get("verified_purchase"),
                "page_count": page_count,
                "size_kb": asset.get("size_kb", 0),
            },
            "tags": asset.get("tags", []),
            "pages": pages,
            "best_use": asset.get("best_use", []),
            "review_text": asset.get("review_text", ""),
            "reviewer_name": asset.get("reviewer_name", ""),
            "entity_name": asset.get("entity_name", ""),
            "issues": asset.get("issues", []),
            "mood": asset.get("mood", ""),
            "has_text_overlay": asset.get("has_text_overlay", False),
            "is_video": asset.get("type") == "video-thumb" or (ad and ad.get("creative_type") == "video"),
            "video_id": str(ad.get("video_id", "")) if ad and ad.get("video_id") else None,
        })

    return scored


def normalize_and_rank(scored):
    """Min-max normalize each dimension, apply weights, sort by composite."""
    # Find min/max for each raw dimension
    dims = ["ad_perf", "conv_rate", "quality", "page_usage", "engagement"]
    mins = {}
    maxs = {}

    for dim in dims:
        vals = [s["raw"][dim] for s in scored]
        mins[dim] = min(vals) if vals else 0
        maxs[dim] = max(vals) if vals else 0

    # Normalize and compute composite
    for s in scored:
        breakdown = {}
        composite = 0
        for dim in dims:
            range_ = maxs[dim] - mins[dim]
            if range_ > 0:
                norm = (s["raw"][dim] - mins[dim]) / range_
            else:
                norm = 0
            breakdown[dim] = round(norm, 4)
            composite += WEIGHTS[dim] * norm

        s["breakdown"] = breakdown
        s["composite_score"] = composite  # will round after multiplier

        # Post-normalization multiplier for proven high-ROAS ads
        # These are validated winners that should rank above untested assets
        roas_val = s.get("metrics", {}).get("roas") or 0
        if roas_val >= 2.0:
            s["composite_score"] *= 2.5   # 2.5x for 2x+ ROAS (elite)
            s["roas_multiplier"] = 2.5
        elif roas_val >= 1.5:
            s["composite_score"] *= 1.8   # 1.8x for 1.5x+ ROAS (strong)
            s["roas_multiplier"] = 1.8
        elif roas_val >= 1.0:
            s["composite_score"] *= 1.3   # 1.3x for 1x+ ROAS (positive)
            s["roas_multiplier"] = 1.3
        else:
            s["roas_multiplier"] = 1.0

        s["composite_score"] = round(s["composite_score"], 4)

    # Sort by composite descending
    scored.sort(key=lambda x: x["composite_score"], reverse=True)

    # Assign ranks and take top N
    for i, s in enumerate(scored[:TOP_N]):
        s["rank"] = i + 1

    return scored[:TOP_N]


def format_output(ranked):
    """Format for leaderboard.json output."""
    assets = []
    for s in ranked:
        # Generate thumb filename (must match the thumb generation logic)
        ext = os.path.splitext(s["path"])[1] or ".jpg"
        basename = os.path.basename(s["path"])
        short_hash = hashlib.md5(s["path"].encode()).hexdigest()[:6]
        thumb_name = f"{short_hash}_{basename}"
        if ext.lower() in [".png", ".webp"]:
            thumb_name = thumb_name.rsplit(".", 1)[0] + ".jpg"

        assets.append({
            "rank": s["rank"],
            "path": s["path"],
            "thumb": f"thumbs/{thumb_name}",
            "product": s["product"],
            "type": s["type"],
            "source": s["source"],
            "composite_score": s["composite_score"],
            "breakdown": s["breakdown"],
            "metrics": s["metrics"],
            "tags": s["tags"],
            "pages": s["pages"],
            "best_use": s["best_use"],
            "review_text": s.get("review_text", ""),
            "reviewer_name": s.get("reviewer_name", ""),
            "entity_name": s.get("entity_name", ""),
            "issues": s.get("issues", []),
            "mood": s.get("mood", ""),
            "has_text_overlay": s.get("has_text_overlay", False),
            "is_video": s.get("is_video", False),
            "video_id": s.get("video_id"),
        })

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_assets_scored": len(assets),
        "total_assets_in_registry": 0,  # filled in main
        "scoring_weights": WEIGHTS,
        "score_ranges": {},  # filled in main
        "assets": assets,
    }


def main():
    print("=" * 60)
    print("Nancy Asset Leaderboard — Refresh")
    print("=" * 60)

    # 1. Load data sources
    print("\n[1/6] Loading data sources...")
    image_tags = load_json(os.path.join(ASSETS, "IMAGE_TAGS.json"))
    winning_ads = load_json(os.path.join(ASSETS, "winning-ads", "winning-ads-metadata.json"))
    loox_meta = load_json(os.path.join(ASSETS, "loox-reviews", "loox-metadata.json"))

    print(f"  IMAGE_TAGS: {len(image_tags)} assets")
    print(f"  Winning ads: {len(winning_ads)} records")
    print(f"  Loox reviews: {len(loox_meta)} records")

    # 2. Build lookups
    print("\n[2/6] Building lookups...")
    ad_lookup = build_ad_lookup(winning_ads)
    print(f"  Ad lookup keys: {len(ad_lookup)}")

    # 3. Scan HTML pages
    print("\n[3/6] Scanning HTML pages for asset usage...")
    page_usage = scan_html_pages()
    used_assets = {k for k, v in page_usage.items() if len(v) > 0}
    print(f"  {len(page_usage)} unique asset references across {len(used_assets)} used assets")

    # 4. Compute raw scores
    print("\n[4/6] Computing raw scores...")
    scored = compute_raw_scores(image_tags, ad_lookup, page_usage)
    print(f"  Scored {len(scored)} assets")

    # 5. Normalize & rank
    print("\n[5/6] Normalizing and ranking...")
    ranked = normalize_and_rank(scored)
    print(f"  Top {len(ranked)} assets selected")

    # 6. Output
    print("\n[6/6] Writing leaderboard.json...")
    output = format_output(ranked)
    output["total_assets_in_registry"] = len(image_tags)

    # Compute score stats
    scores = [a["composite_score"] for a in output["assets"]]
    if scores:
        output["score_ranges"] = {
            "min": round(min(scores), 4),
            "max": round(max(scores), 4),
            "avg": round(sum(scores) / len(scores), 4),
            "median": round(sorted(scores)[len(scores) // 2], 4),
        }

    out_path = os.path.join(LEADERBOARD_DIR, "leaderboard.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n  Written to: {out_path}")
    print(f"  {len(output['assets'])} assets ranked")
    print(f"  Score range: {output['score_ranges'].get('min', 0)} → {output['score_ranges'].get('max', 0)}")
    print(f"  Average score: {output['score_ranges'].get('avg', 0)}")

    # Quick breakdown
    by_source = {}
    by_product = {}
    ad_count = 0
    for a in output["assets"]:
        by_source[a["source"]] = by_source.get(a["source"], 0) + 1
        by_product[a["product"]] = by_product.get(a["product"], 0) + 1
        if a["metrics"].get("roas"):
            ad_count += 1

    print(f"\n  By source: {json.dumps(by_source)}")
    print(f"  By product: {json.dumps(by_product)}")
    print(f"  Assets with ad data: {ad_count}")
    print("\nDone!")


if __name__ == "__main__":
    main()
