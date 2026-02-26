#!/usr/bin/env python3
"""
Build all 4 ICP landing pages from the menopause base template.
Each page clones lem-menopause.html and swaps the 7 variable sections.
All text uses straight ASCII quotes/apostrophes to match the HTML source.
"""

import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_base():
    with open(os.path.join(BASE_DIR, 'lem-menopause.html'), 'r', encoding='utf-8') as f:
        return f.read()

def safe_replace(html, old, new, label="", count=1):
    if old not in html:
        print(f"  WARNING: Could not find for {label}")
        # Show what we're looking for (first 80 chars)
        print(f"    Looking for: {repr(old[:80])}")
        return html
    occurrences = html.count(old)
    if count == 0:  # replace all
        html = html.replace(old, new)
    else:
        html = html.replace(old, new, count)
    return html

def build_icp(config):
    """Build one ICP page from config dictionary."""
    html = load_base()
    name = config['filename']
    print(f"\n{'='*60}")
    print(f"Building {name}")
    print(f"{'='*60}")

    # 0. Proof badge (MUST run before badge replacement to avoid collision when badge="Beginner Friendly")
    html = safe_replace(html,
        'Beginner Friendly</span>',
        config.get('proof_badge', 'Beginner Friendly') + '</span>',
        'proof_badge_span')
    html = safe_replace(html,
        'alt="Beginner Friendly"',
        'alt="' + config.get('proof_badge', 'Beginner Friendly') + '"',
        'proof_badge_alt')

    # 1. Page title
    html = safe_replace(html,
        'Powerful Orgasms After Menopause',
        config['page_title'],
        'page_title')

    # 2. Badge
    html = safe_replace(html,
        'Menopause Wellness',
        config['badge'],
        'badge')

    # 3. H1 line 1 (before the em dash)
    html = safe_replace(html,
        'Powerful Orgasms You Thought Menopause Ended',
        config['h1_line1'],
        'h1_line1')

    # H1 highlight (inside the rotated span)
    html = safe_replace(html,
        "They're Back.",
        config['h1_highlight'],
        'h1_highlight')

    # 4. Subhead paragraph (uses straight quotes)
    html = safe_replace(html,
        "Hormonal changes don't have to mean the end of pleasure. The LEM's gentle air-pulse technology is designed to gently increase blood flow and sensitivity \u2014 exactly what your body needs right now.",
        config['subhead'],
        'subhead')

    # 5a. Countdown heading (must be replaced BEFORE cta_primary to avoid double-replace)
    html = safe_replace(html,
        'Reclaim Your Pleasure Today',
        config.get('countdown_heading', config['cta_primary'] + ' Today'),
        'countdown_heading')

    # 5b. CTA buttons (replace all remaining instances)
    html = safe_replace(html,
        'Reclaim Your Pleasure',
        config['cta_primary'],
        'cta_primary', count=0)
    html = safe_replace(html,
        'Feel Like Yourself Again',
        config['cta_secondary'],
        'cta_secondary', count=0)

    # 6. Checklist first item
    html = safe_replace(html,
        'Loved by Menopausal Women',
        config['checklist_1'],
        'checklist_1')

    # 7. Problem card 1: Sensitivity Fade
    html = safe_replace(html,
        'The "Sensitivity Fade"',
        config['problem1_title'],
        'problem1_title')
    html = safe_replace(html,
        "After menopause, declining estrogen reduces blood flow to clitoral tissue. What once took minutes now takes forever \u2014 or doesn't happen at all. You're not broken. It's biology.",
        config['problem1_desc'],
        'problem1_desc')

    # 8. Problem card 2: "It's Normal" Myth
    html = safe_replace(html,
        '''The "It's Normal" Myth''',
        config['problem2_title'],
        'problem2_title')
    html = safe_replace(html,
        '''You've been told declining pleasure is just part of aging. That it's "normal." But losing your ability to climax isn't inevitable \u2014 you've just never been given the right technology for your body now.''',
        config['problem2_desc'],
        'problem2_desc')

    # 9. Problem card 3: Wrong Tools
    html = safe_replace(html,
        'The "Wrong Tools" Problem',
        config['problem3_title'],
        'problem3_title')
    html = safe_replace(html,
        "Traditional vibrators weren't designed for post-menopausal tissue. They overstimulate the surface causing numbness or irritation. No wonder they've stopped working.",
        config['problem3_desc'],
        'problem3_desc')

    # 10. Featured testimonial header
    html = safe_replace(html,
        '"MENOPAUSAL WOMEN: BUY IT!"',
        config['featured_title'],
        'featured_title')

    # Featured testimonial body (straight quotes, em dashes)
    html = safe_replace(html,
        '''"I bought the Lem as a gift for myself, for my 65th birthday. I have been struggling to get aroused or have any orgasm at all because of menopausal hormone shifts. I tried everything, from supplements to a magic wand. I was doubtful about the Lemon but OMG \u2014 with complete arousal, right into my pelvis, I had the first intense full body climax I've had in several years. On my second round that night, I squirted; something I thought was a long gone pleasure. I cannot recommend it enough!''',
        config['featured_body'],
        'featured_body')

    # Featured name
    html = safe_replace(html,
        'Karen R., Age 65',
        config['featured_name'],
        'featured_name')

    # Avatar
    if 'featured_avatar' in config:
        html = safe_replace(html,
            'images/karen-avatar.jpg',
            config['featured_avatar'],
            'featured_avatar', count=0)

    # 11. "Your Body Still Works" section
    html = safe_replace(html,
        "Your Body Still Works.",
        config['proof_title'],
        'proof_title')
    html = safe_replace(html,
        "Here's Proof.",
        config['proof_subtitle'],
        'proof_subtitle')

    # Proof paragraph
    html = safe_replace(html,
        "Menopause didn't take your pleasure away. It changed the lock \u2014 and you've been using the wrong key. The LEM's air-pulse technology reaches the 90% of your clitoris that's internal, restoring blood flow to tissue that hormones have left dormant.",
        config['proof_paragraph'],
        'proof_paragraph')

    # 12. Value reframe
    html = safe_replace(html,
        'Cheaper Than a Massage.',
        config['value_header1'],
        'value_header1')
    html = safe_replace(html,
        'Better Than Therapy.',
        config['value_header2'],
        'value_header2')
    html = safe_replace(html,
        'Monthly Supplements',
        config['value_bad_title'],
        'value_bad_title')
    html = safe_replace(html,
        '>$120<',
        f'>{config["value_bad_price"]}<',
        'value_bad_price')
    html = safe_replace(html,
        'Repeat: Every month, forever',
        config['value_bad_subtitle'],
        'value_bad_subtitle')

    # 13. UGC Gallery
    html = safe_replace(html,
        'Real Women. Real Ages.',
        config['gallery_header'],
        'gallery_header')
    html = safe_replace(html,
        "From 45 to 78 \u2014 proving it's never too late to feel like yourself again.",
        config['gallery_subtitle'],
        'gallery_subtitle')

    # 14. Bottom testimonials
    # Judith W. (card 1)
    html = safe_replace(html,
        '"75 years old and... OH MY!"',
        config['review1_title'],
        'review1_title')
    html = safe_replace(html,
        '''"75 yo widowed lady\u2026been alone for many years. Decided to try this and\u2026OH MY! Enough said and that's on the lower settings. Older ladies\u2026give it a try."''',
        config['review1_body'],
        'review1_body')
    html = safe_replace(html,
        'Judith W., Age 75',
        config['review1_name'],
        'review1_name')

    # Linda C. (card 2)
    # Need to find exact text
    html = safe_replace(html,
        "Linda C., Late 50s",
        config['review2_name'],
        'review2_name')

    # Milly H. (card 3) - body replaced in section 15 below, name here
    html = safe_replace(html,
        'Milly H., Age 78',
        config['review3_name'],
        'review3_name')

    # Margaret S. (card 4)
    html = safe_replace(html,
        '"I Actually Cried With Relief"',
        config['review4_title'],
        'review4_title')
    html = safe_replace(html,
        '''"As a 66-year old, post-menopausal woman with no libido, this little lemon has restored my enjoyment of orgasams with lithe to no effort."''',
        config['review4_body'],
        'review4_body')
    html = safe_replace(html,
        'Margaret S., Age 66',
        config['review4_name'],
        'review4_name')

    # Linda card title (h4)
    html = safe_replace(html,
        '"Strongest climax in years"',
        config.get('review2_title', '"Strongest climax in years"'),
        'review2_title')

    # Milly card title (h4)
    html = safe_replace(html,
        '"I\'m almost 78 and it\'s been amazing"',
        config.get('review3_title', '"I\'m almost 78 and it\'s been amazing"'),
        'review3_title')

    # Linda's body - find and replace
    # Need to find it first from the HTML
    linda_idx = html.find('Linda C.')
    if linda_idx < 0:
        linda_idx = html.find(config.get('review2_name', 'NOTFOUND'))
    if linda_idx >= 0:
        # The quote body is in the previous <p> tag
        search_block = html[max(0, linda_idx-800):linda_idx]
        p_matches = list(re.finditer(r'<p[^>]*>(.*?)</p>', search_block, re.DOTALL))
        for pm in reversed(p_matches):
            text = re.sub(r'<[^>]+>', '', pm.group(1)).strip()
            if len(text) > 30:
                # Replace this paragraph's content
                full_p = pm.group(0)
                old_text = pm.group(1)
                # We only want to replace the text content, keep the <p> tag
                new_p = full_p.replace(old_text, config['review2_body'])
                html = html.replace(full_p, new_p, 1)
                print(f"  Replaced Linda's review body")
                break

    # 15. Fix Milly's review body (exact text from HTML - uses curly apostrophe \u2019)
    html = safe_replace(html,
        '"I love it .my husband died quite suddenly over four years ago .I didn\u2019t realise I was missing anything sexually until a friend told me about the Lemon ,it\u2019s been amazing and I am a fit almost 78 year old .And enjoying sharing my bed with a lemon .',
        config['review3_body'],
        'review3_body')

    # 16b. Remaining menopause-specific text that needs per-ICP replacement
    # Quote overlay badge on gallery
    html = safe_replace(html,
        '"Changed everything after menopause!"',
        config.get('overlay_quote', '"Changed everything!"'),
        'overlay_quote')

    # Section header "Why Menopause Doesn't Mean"
    html = safe_replace(html,
        "Why Menopause Doesn't Mean",
        config.get('science_header', "Why 80% of Women Don't"),
        'science_header')

    # Section subtext
    html = safe_replace(html,
        "Menopause reduces blood flow to clitoral tissue",
        config.get('science_subtext', "Most stimulation only reaches 10% of the clitoris"),
        'science_subtext')

    # Karen's verified buyer tag
    html = safe_replace(html,
        'Post-Menopausal, Verified Buyer',
        config.get('featured_tag', 'Verified Buyer'),
        'featured_tag')

    # Dr. quote and title: KEEP ORIGINAL from hellonancy.com (do not modify per-ICP)

    # "Pleasure After Menopause" section header
    html = safe_replace(html,
        'Pleasure After Menopause',
        config.get('pleasure_header', 'Your Best Pleasure Yet'),
        'pleasure_header')

    # Gallery overlay "Works after menopause!"
    html = safe_replace(html,
        'Works after menopause!',
        config.get('gallery_overlay', 'Game changer!'),
        'gallery_overlay')

    # 17. FAQ answers
    if 'faq1' in config:
        html = safe_replace(html,
            "Absolutely. The LEM is made from 100% medical-grade, non-porous silicone. It's hypoallergenic, phthalate-free, and completely body-safe. It's also IPX7 waterproof.",
            config['faq1'],
            'faq1')

    if 'faq2' in config:
        html = safe_replace(html,
            "Unlike traditional vibrators, the LEM uses rhythmic pulses of air to create a gentle suction effect around the clitoris. This stimulates the entire clitoris \u2014 including the 90% hidden beneath the surface \u2014 leading to a deeper, more intense experience.",
            config['faq2'],
            'faq2')

    if 'faq4' in config:
        html = safe_replace(html,
            "The LEM is perfect for beginners! It features 12 intensity levels, so you can start slow and find the perfect setting for your body. Many women in their 50s, 60s, and 70s tell us it's the first product that actually worked for them.",
            config['faq4'],
            'faq4')

    # Write output
    outpath = os.path.join(BASE_DIR, name)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(html)

    # Count remaining menopause references
    meno_count = html.lower().count('menopaus')
    print(f"\n  Wrote {outpath} ({len(html)} bytes)")
    print(f"  Remaining 'menopaus*' references: {meno_count}")
    return html


# ============================================================
# ICP CONFIGS
# ============================================================

icp2 = {
    'filename': 'lem-gift-for-her.html',
    'page_title': "The Perfect Gift for Her - LEM by Hello Nancy",
    'badge': 'Gift Guide',
    'h1_line1': "The Gift She'll Never Forget (And You'll Both Enjoy)",
    'h1_highlight': "Get It For Her.",
    'subhead': "Looking for something that actually makes her eyes light up? The LEM's award-winning air-pulse technology delivers sensations she's never felt before \u2014 and you'll love the reaction.",
    'cta_primary': 'Surprise Her Tonight',
    'cta_secondary': 'Get The Perfect Gift',
    'checklist_1': 'Loved by 500,000+ Women',
    'problem1_title': 'The Guessing Game',
    'problem1_desc': "You want to get her something she'll actually love \u2014 not another candle or gift card. But shopping for intimate products feels like navigating a minefield. What if she doesn't like it? What if it's weird?",
    'problem2_title': 'The Generic Gift Trap',
    'problem2_desc': "Jewelry, flowers, dinner \u2014 she's seen it all. You want to show her you're thoughtful, adventurous, and paying attention to what actually matters. The LEM makes that easy.",
    'problem3_title': 'The Performance Pressure',
    'problem3_desc': "Let's be honest \u2014 sometimes you want to help her feel amazing, but you're not sure how to bring it up. The LEM is a gift that speaks for itself.",
    'featured_title': '"THE BEST GIFT I\'VE EVER GIVEN HER"',
    'featured_body': '"I bought this for my wife for Christmas. A few years ago, I bought her a tiny clitoral vibrator \u2014 since then she always says it\'s the best present I\'ve ever given her. The lemon is next level. She loves everything about it: \\"It\'s so cute! It\'s so comfortable in my hand! It works SO WELL!\\" It\'s definitely her new favourite gift from me."',
    'featured_name': 'Daniel G., Verified Buyer',
    'featured_avatar': 'https://i.pravatar.cc/150?img=12',
    'proof_title': "She'll Thank You.",
    'proof_subtitle': 'Repeatedly.',
    'proof_paragraph': "Whether it's a birthday, anniversary, or just a Tuesday \u2014 this is the gift that keeps giving. The LEM's air-pulse technology reaches the 90% of the clitoris that's internal, delivering sensations no other gift can match. Easy to wrap. Impossible to forget.",
    'value_header1': "Cheaper Than Jewelry.",
    'value_header2': "Better Than Flowers.",
    'value_bad_title': 'A Nice Necklace',
    'value_bad_price': '$150+',
    'value_bad_subtitle': "She'll wear it twice, maybe",
    'gallery_header': 'Real Gifts. Real Reactions.',
    'gallery_subtitle': "From surprised wives to grateful girlfriends \u2014 see why men are calling this the best gift they've ever given.",
    'review1_title': '"Maybe you don\'t get too many reviews from men..."',
    'review1_body': '"Maybe you don\'t get too many reviews from men. But here is mine. I purchased this for my wife. It sat in a drawer for a couple days. Then I get a message at work: oh god oh god! The sensation is like nothing she has ever experienced. She urged me to send out a positive review."',
    'review1_name': 'Adam T., Verified Buyer',
    'review2_body': '"Bought it for my partner for her birthday. Really didn\'t expect that much, especially as my partner tends to be very fussy with toys. Am I glad I took the risk? Holy moly she didn\'t just love it \u2014 the sheets needed changing and I was a very popular man. 10 out of 10 will purchase again."',
    'review2_name': 'Daniel M., Verified Buyer',
    'review3_body': '"Game changer \u2014 surprised my wife with this for Christmas. She had purchased something similar, but we put that thing back in the box. We went from average sex once in a while, to amazing sex multiple times a week. 10/10 would recommend."',
    'review3_name': 'Andrew C., Verified Buyer',
    'review4_title': '"She Loved It So Much..."',
    'review4_body': '"Bought as a gift for my wife. She loved it so much she purchased 5 more for her best friends at Christmas. If that doesn\'t tell you everything you need to know, I don\'t know what will."',
    'review4_name': 'Malcolm S., Verified Buyer',
    'review2_title': '"The sheets needed changing"',
    'review3_title': '"Game changer for our marriage"',
    'countdown_heading': 'Surprise Her Tonight',
    'proof_badge': 'Gift Guide Pick',
    'faq4': "The LEM is perfect for beginners and experienced users alike! It features 12 intensity levels, so she can start slow and find the perfect setting. Many men tell us their partners were skeptical at first but now can't stop talking about it.",
    'overlay_quote': '"Best gift I\'ve ever given her!"',
    'science_header': "Why Most Gifts Don't",
    'science_subtext': "Most intimate gifts miss the mark entirely",
    'featured_tag': 'Verified Buyer',
    'dr_quote': 'less responsive to traditional vibration over time.',
    'dr_title': 'Clinical Sexologist &amp; Women\'s Health Expert',
    'pleasure_header': 'The Gift That Keeps Giving',
    'gallery_overlay': 'She loved it!',
}

icp3 = {
    'filename': 'lem-first-toy.html',
    'page_title': "Your First Toy - LEM by Hello Nancy",
    'badge': 'Beginner Friendly',
    'h1_line1': "Your First Toy Shouldn't Be Scary. It Should Be",
    'h1_highlight': 'This.',
    'subhead': "Never tried a toy before? You're not alone. The LEM's gentle air-pulse technology and 12 intensity levels let you start slow and discover what your body loves \u2014 at your own pace.",
    'cta_primary': 'Try Your First',
    'cta_secondary': "Discover What You've Been Missing",
    'checklist_1': 'Loved by First-Time Users',
    'problem1_title': 'The Intimidation Factor',
    'problem1_desc': "Most toys look clinical, aggressive, or just plain confusing. No wonder you've been putting it off. The LEM looks like a cute lemon \u2014 not something from a medical catalog. It's the least intimidating toy you'll ever meet.",
    'problem2_title': 'The Shame Spiral',
    'problem2_desc': "Society told you to feel weird about wanting pleasure. So you've been ignoring it or pretending it doesn't matter. It matters. And there's zero shame in discovering what your body loves.",
    'problem3_title': 'Analysis Paralysis',
    'problem3_desc': "500 products, 200 brands, TikTok reviews that contradict each other. You've been researching for months and still haven't bought anything. Let 500,000+ happy users make the choice easy.",
    'featured_title': '"MY VERY FIRST TOY \u2014 AND WOW"',
    'featured_body': '"This little lemon is my very first toy and I\'m not gonna lie, I was nervous. I have never flown solo or learned what my body is fully capable of. Until today. Level 1 was a nice intro. Level 2 I felt it in my hips, legs, and brain. Level 3 made me lose my mind! Feeling pleasure should feel empowering \u2014 and that\'s what I feel."',
    'featured_name': 'Olivia D., First-Time Buyer',
    'featured_avatar': 'https://i.pravatar.cc/150?img=5',
    'proof_title': 'Your Body Is Ready.',
    'proof_subtitle': 'Are You?',
    'proof_paragraph': "You don't need experience. You don't need to know what you like. The LEM's air-pulse technology reaches the 90% of your clitoris that's internal, delivering sensations completely different from anything you've felt before. Start at level 1. Go at your pace. Your body will tell you the rest.",
    'value_header1': "Cheaper Than a Bad Date.",
    'value_header2': "Better Than Wondering What If.",
    'value_bad_title': 'A Disappointing Night Out',
    'value_bad_price': '$150+',
    'value_bad_subtitle': "Uber, dinner, drinks, regret",
    'gallery_header': 'Real First-Timers. Real Reactions.',
    'gallery_subtitle': "First-timers who wish they'd started sooner \u2014 from nervous to \"why didn't I do this years ago?\"",
    'review1_title': '"I was quite sceptical..."',
    'review1_body': '"I was quite sceptical about how this wee lem toy would work as I haven\'t owned anything like it before. Tried it out and OMG the orgasm was building straight away. I climaxed so fast it was a rush. I\'ve never had an orgasm from a toy like it ever."',
    'review1_name': 'Lynda, First-Time Buyer',
    'review2_body': '"The first time I used it I was nervous and excited. I have never played with a toy in front of my husband but this one was a must. He enjoyed it just as much as I did. It didn\'t take long to get to an incredible orgasm. Just do it. You won\'t regret it. I promise."',
    'review2_name': 'Devan L., Verified Buyer',
    'review3_body': '"I was a little hesitant to purchase because I\'ve never had something like this. I\'m glad I took the plunge though! It lives on my nightstand and it\'s worth its weight in gold!"',
    'review3_name': 'Lexi C., Verified Buyer',
    'review4_title': '"Highly Recommend for First-Timers"',
    'review4_body': '"Lem is my first sex toy. Setting 3 felt good and I didn\'t last beyond setting 4. It was amazing! I\'ve tried some other toys from different brands \u2014 none compare. Highly recommend to anyone trying a sex toy for the first time. 10/10."',
    'review4_name': 'Tara, First-Time Buyer',
    'review2_title': '"I didn\'t just love it \u2014 I told my husband"',
    'review3_title': '"Lives on my nightstand now"',
    'countdown_heading': 'Try Your First Today',
    'proof_badge': 'First-Timer Approved',
    'faq4': "Absolutely \u2014 the LEM was MADE for beginners! It features 12 intensity levels starting whisper-soft, so you can explore at your own pace. There's no learning curve. Just hold it gently and let it do the work. Thousands of first-time users say it's the easiest toy they've ever tried.",
    'overlay_quote': '"My very first \u2014 and WOW!"',
    'science_header': "Why Your First Toy Shouldn't",
    'science_subtext': "Traditional toys overwhelm beginners with too much surface vibration",
    'featured_tag': 'First-Time Buyer',
    'dr_quote': 'less responsive to traditional vibration, especially for first-time users.',
    'dr_title': 'Clinical Sexologist &amp; Women\'s Health Expert',
    'pleasure_header': 'Your First Time Done Right',
    'gallery_overlay': 'Wish I started sooner!',
}

icp4 = {
    'filename': 'lem-upgrade-from-rose.html',
    'page_title': "Upgrade From the Rose - LEM by Hello Nancy",
    'badge': 'The Upgrade',
    'h1_line1': "Tried the Rose? Here's What You've Been",
    'h1_highlight': 'Missing.',
    'subhead': "If your TikTok toy broke, disappointed, or left you wondering what the hype was about \u2014 you had the wrong one. The LEM's precision air-pulse technology is what the Rose tried to be.",
    'cta_primary': 'Upgrade Now',
    'cta_secondary': 'Make The Switch',
    'checklist_1': 'Loved by 500,000+ Women',
    'problem1_title': 'The $20 Disappointment',
    'problem1_desc': "You saw it on TikTok. You bought the cheap version on Amazon. It buzzed, it tickled, it did\u2026 not much. That wasn't air-suction \u2014 that was a vibrating piece of plastic shaped like a flower.",
    'problem2_title': 'The "It Broke Again" Cycle',
    'problem2_desc': "Cheap toys die in weeks. The charging port stops working. The motor gets weaker. You've bought 2, 3, maybe 4 replacements. You've already spent more than the LEM costs \u2014 and none of them delivered.",
    'problem3_title': 'The Knockoff Roulette',
    'problem3_desc': "Amazon listings with stolen reviews. Alibaba specials in sketchy packaging. You're gambling with body-safe materials every time. The LEM is 100% medical-grade silicone, phthalate-free, and built to last.",
    'featured_title': '"THE ROSE? MEH. THEN I FOUND NANCY."',
    'featured_body': '"I\'ve tried the Rose (meh), the Womanizer (didn\'t work for me), and a few off-brand nightmares. I was understandably skeptical. But then I unboxed Nancy\u2026 and everything changed. Nancy gives me stronger, longer lasting orgasms, with waves of pleasure that continue even after I finish! I have plans to purchase two as backups. I LOVE YOU, NANCY."',
    'featured_name': 'Jacqueline C., Verified Buyer',
    'featured_avatar': 'https://i.pravatar.cc/150?img=9',
    'proof_title': "You're Not Hard to Please.",
    'proof_subtitle': 'You Had the Wrong Toy.',
    'proof_paragraph': "The Rose and its knockoffs use basic vibration motors \u2014 they just buzz faster. The LEM uses true air-pulse technology that creates rhythmic waves of pressure, reaching the 90% of your clitoris that's internal. That's why the Rose tickled the surface while the LEM makes you lose your mind.",
    'value_header1': "Stop Buying $20 Toys.",
    'value_header2': "That Break in a Month.",
    'value_bad_title': 'Another Cheap Amazon Toy',
    'value_bad_price': '$20',
    'value_bad_subtitle': "Repeat: Every 2 months when it breaks",
    'gallery_header': 'Real Upgrades. Real Reactions.',
    'gallery_subtitle': "From Rose refugees to Amazon survivors \u2014 women who finally found what actually works.",
    'review1_title': '"Worth every penny over the bootleg version"',
    'review1_body': '"As a broke person who tried to get a bootleg Amazon version, I truly mean it when I say it is worth it. I had previously bought a cheap $20 massager and thought it was fine. I haven\'t used it since getting the lemon. I am also not a review writer usually! This speaks volumes."',
    'review1_name': 'hal b., Verified Buyer',
    'review2_body': '"If you\'ve tried the Womanizer and think you\'ve found the best there is \u2014 think again. Even if you\'re barely in the mood, this little citrus freak of nature will wake the dead. What I experienced was nothing short of a religious awakening. Looks like a lemon. Acts like a revolution."',
    'review2_name': 'Moa M., Verified Buyer',
    'review3_body': '"I was sceptical, I\'d never spent that much on a vibrator. I\'d already bought a cheap rose imitation that was ok, but the Lem blew it out of the water!! Love it!! Never fails to get me off. Best money I\'ve spent."',
    'review3_name': 'Nicole B., Verified Buyer',
    'review4_title': '"The Rose Has Been Retired"',
    'review4_body': '"I used to have the infamous rose that everyone raved about but that has now been retired! I love how discrete the Lem is with such a quiet motor. The size is just right \u2014 ergonomic enough to hold yourself but also small enough to use with your partner. Safe to say this will be my new go to!"',
    'review4_name': 'Adelaide, Verified Buyer',
    'review2_title': '"A religious awakening"',
    'review3_title': '"Best money I\'ve spent"',
    'countdown_heading': 'Upgrade Now \u2014 Save $70 Today',
    'proof_badge': 'The Upgrade',
    'faq2': "Unlike cheap rose toys that just vibrate faster, the LEM uses true air-pulse technology \u2014 rhythmic waves of pressure that create a gentle suction effect around the clitoris. This stimulates the entire clitoris, including the 90% hidden beneath the surface. It's the technology the Rose tried to copy but couldn't.",
    'faq4': "The LEM is perfect whether you're upgrading or starting fresh! It features 12 intensity levels and multiple patterns. If the Rose was too intense or not intense enough, the LEM lets you find your sweet spot. Many women tell us it's the first air-suction toy that actually delivered.",
    'overlay_quote': '"The Rose is retired!"',
    'science_header': "Why Cheap Toys Don't",
    'science_subtext': "Budget toys use basic vibration motors that buzz the surface",
    'featured_tag': 'Rose Toy Refugee, Verified Buyer',
    'dr_quote': 'less responsive to basic vibration from cheap devices.',
    'dr_title': 'Clinical Sexologist &amp; Women\'s Health Expert',
    'pleasure_header': 'The Upgrade You Deserve',
    'gallery_overlay': 'The Rose can\'t compare!',
}

icp5 = {
    'filename': 'lem-couples.html',
    'page_title': "For Couples - LEM by Hello Nancy",
    'badge': "Couples' Choice",
    'h1_line1': "The 'Third Wheel' That Actually Saves",
    'h1_highlight': 'Relationships.',
    'subhead': "Stuck in a routine? Performance pressure killing the mood? The LEM takes the pressure off both of you \u2014 and turns ordinary nights into ones you'll both be thinking about all week.",
    'cta_primary': 'Explore Together',
    'cta_secondary': 'Bring The Spark Back',
    'checklist_1': 'Loved by Couples Everywhere',
    'problem1_title': 'The Bedroom Routine',
    'problem1_desc': "Same positions. Same sequence. Same result (or lack thereof). After months or years together, the spark doesn't die \u2014 it just needs a new match. The LEM is that match.",
    'problem2_title': 'The Performance Trap',
    'problem2_desc': "He's worried about lasting long enough. She's worried about taking too long. You're both so focused on the finish line that you forget to enjoy the race. The LEM changes the dynamic entirely.",
    'problem3_title': 'The Intimacy Plateau',
    'problem3_desc': "You love each other. The attraction is there. But somewhere between kids, work, and life, physical intimacy became another to-do item. The LEM turns it back into the highlight.",
    'featured_title': '"IT\'S NOT JUST GOOD FOR HER. IT\'S GREAT FOR US."',
    'featured_body': '"As a man, I bought the LEM for my partner. What I did not expect was to be gently demoted from \\"primary pleasure provider\\" to \\"supporting cast member.\\" And honestly? I\'m fine with it. This little beast turns bedroom time into a co-op multiplayer experience. It\'s honestly strengthened our teamwork more than any trust-fall exercise. Couples approved. Relationship buff unlocked."',
    'featured_name': 'Rob H., Verified Buyer',
    'featured_avatar': 'https://i.pravatar.cc/150?img=11',
    'proof_title': "It's Not About Doing More.",
    'proof_subtitle': "It's About Feeling More.",
    'proof_paragraph': "The LEM isn't a replacement \u2014 it's an amplifier. Its air-pulse technology reaches the 90% of the clitoris that's internal, delivering sensations impossible to replicate manually. Used together, it takes the pressure off both partners and puts the focus back where it belongs: connection, pleasure, and fun.",
    'value_header1': "Cheaper Than Couples Therapy.",
    'value_header2': "More Fun Too.",
    'value_bad_title': 'One Therapy Session',
    'value_bad_price': '$200',
    'value_bad_subtitle': "Repeat: Weekly, for months",
    'gallery_header': 'Real Couples. Real Spark.',
    'gallery_subtitle': "From bedroom ruts to \"why didn't we try this sooner\" \u2014 couples who found their spark again.",
    'review1_title': '"This toy has changed our sex life dramatically!"',
    'review1_body': '"After going through menopause, sex was the last thing on the wife\'s mind. NOW she thinks about it constantly! This toy has changed our sex life dramatically! Thanks for rekindling my wife\'s fire."',
    'review1_name': 'Zachary P., Verified Buyer',
    'review2_body': '"I bought this for my wife to help things in the bedroom. After two C-sections and perimenopause, things have been frustrating for her. The Lem has brought back some of those intense feelings. It has increased both the amount of sex we are having, but also the quality. Highly recommend for couples having ruts in the bedroom."',
    'review2_name': 'Shepley R., Verified Buyer',
    'review3_body': '"When I tell you that my soul left my body I am not exaggerating. The first time I tried it out was with my partner and even he was like, \\"I have only seen you O that hard before a couple of times.\\" If you\'re thinking about it, GET IT."',
    'review3_name': 'Alana H., Verified Buyer',
    'review4_title': '"I Felt Secure Enough to Go on an Adventure"',
    'review4_body': '"I may be pushing 40, but my experience with toys has been very limited. Now that I\'m with a partner who is a great communicator, I felt secure enough to go on an adventure. It\'s been a long time since something was that intensely focused. I did see stars."',
    'review4_name': 'Marc L., Pushing 40',
    'review2_title': '"Increased the amount AND the quality"',
    'review3_title': '"My soul left my body"',
    'countdown_heading': 'Explore Together Tonight',
    'proof_badge': "Couples' Favourite",
    'faq4': "The LEM is perfect for couples! It features 12 intensity levels so you can explore together and find what works for both of you. It's small enough to use during intimacy without getting in the way, and many couples tell us it completely transformed their bedroom experience.",
    'overlay_quote': '"Our new favourite thing!"',
    'science_header': "Why Couples Get Stuck In",
    'science_subtext': "Routine reduces excitement, and traditional toys don't bridge the gap",
    'featured_tag': 'Couples Buyer, Verified',
    'dr_quote': 'less responsive to routine stimulation in long-term relationships.',
    'dr_title': 'Clinical Sexologist &amp; Relationship Expert',
    'pleasure_header': 'Pleasure You Share',
    'gallery_overlay': 'Couples approved!',
}

# Build all 4 pages
for config in [icp2, icp3, icp4, icp5]:
    build_icp(config)

print("\n" + "="*60)
print("All 4 ICP pages built!")
print("="*60)
for config in [icp2, icp3, icp4, icp5]:
    print(f"  {config['filename']}")
