#!/usr/bin/env python3
"""Generate IMAGE_TAGS.json from loox metadata, winning ads metadata, and local image inventory."""
import json
import os
import glob

BASE = "/Users/rahul/Downloads/nancy-landing-pages"
ASSETS = os.path.join(BASE, "assets")

def get_file_size_kb(path):
    try:
        return round(os.path.getsize(path) / 1024, 1)
    except:
        return 0

def tag_loox_images():
    """Auto-tag loox review images from metadata."""
    tags = []
    meta_path = os.path.join(ASSETS, "loox-reviews", "loox-metadata.json")
    if not os.path.exists(meta_path):
        print("  loox-metadata.json not found yet, skipping loox auto-tag")
        return tags

    with open(meta_path) as f:
        reviews = json.load(f)

    for r in reviews:
        for img_path in r.get("image_paths", []):
            full_path = os.path.join(ASSETS, img_path)
            tags.append({
                "path": f"assets/{img_path}",
                "source": "loox",
                "product": r.get("product", "unknown"),
                "type": "review-photo",
                "organic_score": 5,
                "mood": "authentic",
                "shows_product": True,
                "shows_person": False,
                "has_text_overlay": False,
                "size_kb": get_file_size_kb(full_path),
                "best_use": ["review-avatar", "ugc-grid", "social-proof"],
                "rating": r.get("rating", 0),
                "verified_purchase": r.get("verified_purchase", False),
                "review_text": r.get("review", "")[:100],
                "reviewer_name": r.get("nickname", ""),
                "ad_roas": None,
                "ad_spend_hkd": None,
                "ad_conversions": None,
                "issues": [],
                "tags": ["customer-photo", f"{r.get('rating', 0)}-star"]
            })
    return tags

def tag_winning_ads():
    """Auto-tag winning ad creatives from metadata."""
    tags = []
    meta_path = os.path.join(ASSETS, "winning-ads", "winning-ads-metadata.json")
    if not os.path.exists(meta_path):
        print("  winning-ads-metadata.json not found, skipping")
        return tags

    with open(meta_path) as f:
        ads = json.load(f)

    for ad in ads:
        fname = ad.get("filename", "")
        full_path = os.path.join(ASSETS, "winning-ads", fname)
        ctype = ad.get("creative_type", "image")
        roas = ad.get("roas", 0)

        tags.append({
            "path": f"assets/winning-ads/{fname}",
            "source": "ad-creative",
            "product": "lem",
            "type": "video-thumb" if ctype == "video" else "ad-static",
            "organic_score": 1,
            "mood": "aspirational",
            "shows_product": True,
            "shows_person": False,
            "has_text_overlay": True,
            "size_kb": get_file_size_kb(full_path),
            "best_use": ["ad-reference", "winning-creative-study"],
            "rating": None,
            "verified_purchase": None,
            "ad_roas": roas,
            "ad_spend_hkd": ad.get("spend_hkd", 0),
            "ad_conversions": ad.get("conversions", 0),
            "entity_name": ad.get("entity_name", ""),
            "issues": [],
            "tags": [ctype, f"roas-{roas:.1f}x", ad.get("status", "").lower()]
        })
    return tags

def tag_local_images():
    """Manually tag known local images."""
    tags = []

    # Product images (PDP shots)
    pdp_files = glob.glob(os.path.join(BASE, "images", "pdp*.jpg"))
    for f in pdp_files:
        fname = os.path.basename(f)
        tags.append({
            "path": f"images/{fname}",
            "source": "product-shoot",
            "product": "lem",
            "type": "product-hero",
            "organic_score": 3,
            "mood": "clinical",
            "shows_product": True,
            "shows_person": False,
            "has_text_overlay": False,
            "size_kb": get_file_size_kb(f),
            "best_use": ["product-showcase", "hero-image", "gallery"],
            "rating": None,
            "verified_purchase": None,
            "ad_roas": None,
            "ad_spend_hkd": None,
            "ad_conversions": None,
            "issues": [],
            "tags": ["pdp", "product-photo"]
        })

    # Loox review images (the 10 original ones in images/)
    loox_files = glob.glob(os.path.join(BASE, "images", "loox-review*.jpg"))
    for f in loox_files:
        fname = os.path.basename(f)
        tags.append({
            "path": f"images/{fname}",
            "source": "loox",
            "product": "lem",
            "type": "review-photo",
            "organic_score": 5,
            "mood": "authentic",
            "shows_product": True,
            "shows_person": False,
            "has_text_overlay": False,
            "size_kb": get_file_size_kb(f),
            "best_use": ["review-avatar", "ugc-grid", "social-proof"],
            "rating": 5,
            "verified_purchase": True,
            "ad_roas": None,
            "ad_spend_hkd": None,
            "ad_conversions": None,
            "issues": ["loox-review10.jpg may be AI-generated"] if "review10" in fname else [],
            "tags": ["customer-photo", "organic", "5-star"]
        })

    # UGC poster cards (branded)
    ugc_branded = {
        "lem/images/ugc/alyssa-g.png": {"name": "Alyssa Grenfell", "issue": "branded poster card with visible name text"},
        "lem/images/ugc/jordan-t.png": {"name": "Jordan Theresa", "issue": "branded poster card with visible name text"},
        "lem/images/ugc/daliza.png": {"name": "Daliza", "issue": "branded poster card with visible name text"},
        "lem/images/ugc/deliza.png": {"name": "Deliza", "issue": "branded poster card with visible name text"},
    }
    for path, info in ugc_branded.items():
        full = os.path.join(BASE, path)
        tags.append({
            "path": path,
            "source": "ugc-branded",
            "product": "lem",
            "type": "ugc-poster",
            "organic_score": 2,
            "mood": "aspirational",
            "shows_product": False,
            "shows_person": True,
            "has_text_overlay": True,
            "size_kb": get_file_size_kb(full),
            "best_use": ["NOT for avatars - name mismatch risk", "full-width ugc feature"],
            "rating": None,
            "verified_purchase": None,
            "ad_roas": None,
            "ad_spend_hkd": None,
            "ad_conversions": None,
            "issues": [info["issue"], f"shows '{info['name']}' - will mismatch if used as different person's avatar"],
            "tags": ["branded", "poster-card", "name-visible", "large-file"]
        })

    # TikTok UGC posters
    for i in range(1, 4):
        path = f"lem/images/product/ugc-poster-{i}.jpg"
        full = os.path.join(BASE, path)
        tags.append({
            "path": path,
            "source": "ugc-tiktok",
            "product": "lem",
            "type": "ugc-tiktok-screenshot",
            "organic_score": 4,
            "mood": "fun",
            "shows_product": True,
            "shows_person": True,
            "has_text_overlay": True,
            "size_kb": get_file_size_kb(full),
            "best_use": ["ugc-grid", "social-proof-scroll"],
            "rating": None,
            "verified_purchase": None,
            "ad_roas": None,
            "ad_spend_hkd": None,
            "ad_conversions": None,
            "issues": [],
            "tags": ["tiktok", "screenshot", "ugc"]
        })

    # Lem product images in lem/images/product/
    lem_product_map = {
        "lem-hero.jpg": {"type": "product-hero", "mood": "clinical", "tags": ["hero", "product-photo"]},
        "lem-product.jpg": {"type": "product-hero", "mood": "clinical", "tags": ["product-photo"]},
        "lem-in-hand.png": {"type": "lifestyle", "mood": "authentic", "tags": ["in-hand", "scale-reference"]},
        "lem-lifestyle.jpg": {"type": "lifestyle", "mood": "cozy", "tags": ["lifestyle", "nightstand"]},
        "lem-lifestyle.gif": {"type": "lifestyle", "mood": "cozy", "tags": ["animated", "lifestyle"]},
        "lem-rotate.gif": {"type": "product-hero", "mood": "clinical", "tags": ["animated", "360-view"]},
        "lem-cocktail.png": {"type": "lifestyle", "mood": "fun", "tags": ["cocktail", "lifestyle"]},
        "lem-lemon-slices.png": {"type": "lifestyle", "mood": "fun", "tags": ["lemon", "flatlay"]},
        "lem-with-lemons.png": {"type": "lifestyle", "mood": "fun", "tags": ["lemon", "flatlay"]},
        "lem-airpulse-diagram.png": {"type": "diagram", "mood": "clinical", "tags": ["technology", "diagram"]},
        "lem-airpulse-v2.png": {"type": "diagram", "mood": "clinical", "tags": ["technology", "airpulse"]},
        "lem-vs-traditional.png": {"type": "comparison", "mood": "clinical", "tags": ["comparison", "vs"]},
        "lem-unboxing.png": {"type": "unboxing", "mood": "authentic", "tags": ["unboxing", "packaging"]},
        "lem-hero-alt.webp": {"type": "product-hero", "mood": "aspirational", "tags": ["hero", "alt"]},
        "lem-lifestyle-bathroom.png": {"type": "lifestyle", "mood": "cozy", "tags": ["bathroom", "ai-generated"]},
        "lem-lifestyle-nightstand.png": {"type": "lifestyle", "mood": "cozy", "tags": ["nightstand", "ai-generated"]},
        "lem-lifestyle-travel.png": {"type": "lifestyle", "mood": "aspirational", "tags": ["travel", "ai-generated"]},
    }
    for fname, meta in lem_product_map.items():
        full = os.path.join(BASE, "lem/images/product", fname)
        if not os.path.exists(full):
            continue
        is_ai = "ai-generated" in meta.get("tags", [])
        tags.append({
            "path": f"lem/images/product/{fname}",
            "source": "ai-generated" if is_ai else "product-shoot",
            "product": "lem",
            "type": meta["type"],
            "organic_score": 2 if is_ai else 4,
            "mood": meta["mood"],
            "shows_product": True,
            "shows_person": False,
            "has_text_overlay": False,
            "size_kb": get_file_size_kb(full),
            "best_use": ["product-showcase", "gallery"] if meta["type"] == "product-hero" else ["section-illustration"],
            "rating": None,
            "verified_purchase": None,
            "ad_roas": None,
            "ad_spend_hkd": None,
            "ad_conversions": None,
            "issues": ["AI-generated - check for artifacts"] if is_ai else [],
            "tags": meta["tags"]
        })

    # Media logos
    media_logos = glob.glob(os.path.join(BASE, "lem/images/media/*"))
    for f in media_logos:
        fname = os.path.basename(f)
        tags.append({
            "path": f"lem/images/media/{fname}",
            "source": "media-logo",
            "product": "nancy-brand",
            "type": "media-logo",
            "organic_score": 5,
            "mood": "clinical",
            "shows_product": False,
            "shows_person": False,
            "has_text_overlay": True,
            "size_kb": get_file_size_kb(f),
            "best_use": ["press-bar", "trust-signal"],
            "rating": None,
            "verified_purchase": None,
            "ad_roas": None,
            "ad_spend_hkd": None,
            "ad_conversions": None,
            "issues": [],
            "tags": ["logo", "press", "trust"]
        })

    # Winning comparison image
    vs_rose = os.path.join(BASE, "lem/images/winning/lem-vs-rose.png")
    if os.path.exists(vs_rose):
        tags.append({
            "path": "lem/images/winning/lem-vs-rose.png",
            "source": "ad-creative",
            "product": "lem",
            "type": "comparison",
            "organic_score": 2,
            "mood": "clinical",
            "shows_product": True,
            "shows_person": False,
            "has_text_overlay": True,
            "size_kb": get_file_size_kb(vs_rose),
            "best_use": ["comparison-section", "vs-competitor"],
            "rating": None,
            "verified_purchase": None,
            "ad_roas": None,
            "ad_spend_hkd": None,
            "ad_conversions": None,
            "issues": [],
            "tags": ["comparison", "rose", "competitor"]
        })

    # Brand logos
    logo_files = glob.glob(os.path.join(BASE, "lem/images/logos/*"))
    for f in logo_files:
        fname = os.path.basename(f)
        tags.append({
            "path": f"lem/images/logos/{fname}",
            "source": "brand-asset",
            "product": "nancy-brand",
            "type": "brand-logo",
            "organic_score": 5,
            "mood": "clinical",
            "shows_product": False,
            "shows_person": False,
            "has_text_overlay": True,
            "size_kb": get_file_size_kb(f),
            "best_use": ["nav-logo", "footer-logo"],
            "rating": None,
            "verified_purchase": None,
            "ad_roas": None,
            "ad_spend_hkd": None,
            "ad_conversions": None,
            "issues": [],
            "tags": ["logo", "nancy", "brand"]
        })

    return tags

def main():
    all_tags = []

    print("Tagging loox review images...")
    all_tags.extend(tag_loox_images())

    print("Tagging winning ad creatives...")
    all_tags.extend(tag_winning_ads())

    print("Tagging local images...")
    all_tags.extend(tag_local_images())

    # Deduplicate by path
    seen = set()
    unique_tags = []
    for t in all_tags:
        if t["path"] not in seen:
            seen.add(t["path"])
            unique_tags.append(t)

    out_path = os.path.join(ASSETS, "IMAGE_TAGS.json")
    with open(out_path, 'w') as f:
        json.dump(unique_tags, f, indent=2)

    # Stats
    by_source = {}
    by_product = {}
    by_type = {}
    for t in unique_tags:
        by_source[t["source"]] = by_source.get(t["source"], 0) + 1
        by_product[t["product"]] = by_product.get(t["product"], 0) + 1
        by_type[t["type"]] = by_type.get(t["type"], 0) + 1

    print(f"\nTotal tagged: {len(unique_tags)}")
    print(f"By source: {json.dumps(by_source, indent=2)}")
    print(f"By product: {json.dumps(by_product, indent=2)}")
    print(f"By type: {json.dumps(by_type, indent=2)}")

if __name__ == "__main__":
    main()
