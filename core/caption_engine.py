"""
core/caption_engine.py — Rule-based Instagram Caption Engine.

Pipeline:
  1. Clean    — strip hashtags, normalize whitespace
  2. Classify — keyword scoring → category
  3. Build    — [PRE-HOOK CTA] + [HOOK] + [BODY] + [HASHTAGS]

Caption structure:
  Line 1 (PRE-HOOK): Direct engagement ask — "🔥 Comment if this is you"
                     Visible before "...more" — drives engagement immediately.
  Line 2 blank
  Line 3+ (HOOK): Short, punchy opener (same category)
  blank
  (BODY): Original caption, cleaned
  blank
  (HASHTAGS): Category-specific

One CTA per caption (the pre-hook). No separate CTA at bottom.
All components drawn from the SAME category — never mixed.

Categories: scenic | adventure | cultural | motivation | general
"""

import re
import random
from typing import Optional

# ── Category keyword banks (lowercase) ────────────────────────────────────────
_KEYWORDS: dict[str, list[str]] = {
    "scenic": [
        "view", "landscape", "mountain", "valley", "forest", "sea", "lake",
        "sunrise", "sunset", "waterfall", "nature", "scenic", "vista",
        "cliff", "canyon", "river", "manzara", "dag", "orman", "deniz",
    ],
    "adventure": [
        "hiking", "trekking", "camping", "climbing", "kayak", "rafting",
        "extreme", "outdoor", "backpack", "trail", "expedition", "explore",
        "yuruyus", "kamp", "macera", "dag", "zirve",
    ],
    "cultural": [
        "food", "local", "village", "culture", "history", "market", "street",
        "traditional", "cuisine", "tea", "coffee", "authentic", "hidden",
        "cay", "kofte", "pide", "baklava", "koyu",
    ],
    "motivation": [
        "wanderlust", "freedom", "journey", "life", "live", "inspire",
        "dream", "explore", "discover", "adventure", "goals", "travel",
        "believe", "never stop", "go", "yol", "ozgur",
    ],
}

# ── Per-category content pools ─────────────────────────────────────────────────

# PRE-HOOK: The very first line — direct engagement ask.
# Shown before "...more" — drives comments immediately.
_PRE_HOOKS: dict[str, list[str]] = {
    "scenic": [
        "Drop a 🏔️ if you'd drop everything and go here right now!",
        "Tag someone you'd watch this sunset with 👇❤️",
        "Comment 🌊 if this view took your breath away!",
        "Save this 📌 — you'll need it for your next travel list!",
    ],
    "adventure": [
        "Drop a 🏕️ if you'd do this on your next trip!",
        "Tag your adventure buddy 👇 — they NEED to see this!",
        "Comment 🔥 if this gave you travel goals!",
        "Who's adding this to their bucket list? Comment below 👇",
    ],
    "cultural": [
        "Drop a ❤️ if you love discovering local gems like this!",
        "Save this 📌 — hidden spots you can't miss!",
        "Tag someone who appreciates authentic culture 👇🌿",
        "Comment 🍜 if this made you hungry for an adventure!",
    ],
    "motivation": [
        "Drop a ✈️ if travel is your answer to everything!",
        "Tag someone who needs to pack their bags right now 👇",
        "Comment 🌍 if the world is your home!",
        "Save this 📌 — your next adventure starts here!",
    ],
    "general": [
        "Drop a 🏔️ if you'd go here right now!",
        "Tag someone you'd explore this with 👇",
        "Comment 🌿 if this made you want to travel!",
        "Save this for your travel bucket list 📌🔥",
    ],
}

_HOOKS: dict[str, list[str]] = {
    "scenic": [
        "Nature just created the most stunning canvas 🌄✨",
        "This view is what dreams are made of 🏔️💚",
        "No filter needed — the world does this on its own 🌊",
        "You can hear the silence from here 🌿💨",
        "The kind of view that makes you forget time exists ✨🌅",
    ],
    "adventure": [
        "This is what living feels like 🏕️🔥",
        "Some trails lead to places words can't describe 💚",
        "The mountains are calling — and you should answer 🏔️",
        "Every summit unlocks a new version of you 🚀",
        "The best views come after the hardest climbs 🏆",
    ],
    "cultural": [
        "This is the real Turkey — raw, beautiful, and authentic 🌿",
        "Local gems you'll never find in a guidebook 🗺️✨",
        "The flavours, the colours, the stories — all of it ❤️",
        "Culture is the best souvenir you'll ever take home 🌍",
        "This is what makes a trip unforgettable 🥎✨",
    ],
    "motivation": [
        "Your next adventure is waiting — go find it ✈️",
        "Life is too short to stay in one place 🌍🔥",
        "Travel isn't an expense — it's an investment in yourself 💰✨",
        "Stop waiting for the right time. This IS the right time 🚀",
        "The world rewards those who are brave enough to explore it 🏔️",
    ],
    "general": [
        "Turkey is hiding places most people will never see 🇹🇷🔥",
        "This is why travel changes everything ✨",
        "Not all classrooms have walls 🌿🏔️",
        "Best thing you'll see today 📸🔥",
        "Some moments are too beautiful to keep to yourself 🌊",
    ],
}

_HASHTAGS: dict[str, str] = {
    "scenic": (
        "#NatureReels #ScenicViews #TravelTurkey #LandscapePhotography #NatureLovers "
        "#Karadeniz #TravelReels #Shorts #ViralReels #Wanderlust "
        "#MountainLife #NatureVibes #OutdoorLife #TravelInspiration #TurkeyTravel"
    ),
    "adventure": (
        "#AdventureReels #HikingTurkey #OutdoorAdventure #TravelReels #Trekking "
        "#Shorts #ViralReels #AdventureTime #ExploreMore #WildNature "
        "#HikingLife #Backpacking #MountainAdventure #NatureExplorer #Karadeniz"
    ),
    "cultural": (
        "#TurkishCulture #HiddenGems #TravelTurkey #LocalLife #AuthenticTravel "
        "#Shorts #ViralReels #TravelReels #CulturalExperience #FoodTravel "
        "#TurkeyFood #LocalCuisine #TravelVibes #ExploreMore #TurkeyHiddenPlaces"
    ),
    "motivation": (
        "#TravelMotivation #Wanderlust #ExploreTheWorld #TravelGoals #AdventureAwaits "
        "#Shorts #ViralReels #TravelReels #BucketList #JourneyOfLife "
        "#TravelInspiration #NeverStopExploring #GoExplore #TravelLife #WorldTravel"
    ),
    "general": (
        "#TravelReels #TravelTurkey #Nature #Shorts #ViralReels "
        "#Karadeniz #AdventureReels #Wanderlust #ExploreMore #TurkeyTravel "
        "#NatureLovers #TravelInspiration #HiddenGems #OutdoorLife #TravelVibes"
    ),
}


# ── Public API ────────────────────────────────────────────────────────────────

def clean_caption(text: str) -> str:
    """
    Remove hashtags and normalize whitespace.
    Keeps emojis intact — they add authentic personality.
    Returns cleaned body text only.
    """
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [l.rstrip() for l in text.splitlines()]
    return "\n".join(lines).strip()


def classify_caption(text: str) -> str:
    """
    Score the cleaned caption against each category's keyword bank.
    Returns the highest-scoring category name, or 'general' if no match.
    """
    lower = text.lower()
    scores: dict[str, int] = {cat: 0 for cat in _KEYWORDS}

    for category, keywords in _KEYWORDS.items():
        for kw in keywords:
            if kw in lower:
                scores[category] += 1

    best_cat = max(scores, key=lambda c: scores[c])
    return best_cat if scores[best_cat] > 0 else "general"


def build_caption(
    original: str,
    add_credit: bool = False,
    credit_handle: str = "karadenizli.maceraci",
    category_override: Optional[str] = None,
) -> str:
    """
    Full pipeline:
      1. Clean the original caption (strip hashtags, normalize whitespace)
      2. Classify into a category via keyword scoring
      3. Assemble:
           [PRE-HOOK CTA]   ← direct engagement ask, shown before "...more"
           [HOOK]           ← short punchy opener
           [BODY]           ← cleaned original
           [HASHTAGS]       ← category-specific
      4. All components come from the SAME category — never mixed.
      5. One CTA only (the pre-hook). No repeat at the bottom.
    """
    body = clean_caption(original)

    if category_override and category_override in _KEYWORDS:
        category = category_override
    else:
        category = classify_caption(body)

    # Instagram hard limit is 2,200 characters.
    # We'll target 2,100 to leave a safe buffer for emojis and special chars.
    MAX_LEN = 2100
    
    # Estimate fixed lengths
    fixed_parts = f"{pre_hook}\n\n{hook}\n\n\n\n{hashtags}"
    if add_credit:
        fixed_parts += f"\n\nVia @{credit_handle} 🎬"
        
    remaining_space = MAX_LEN - len(fixed_parts)
    
    if len(body) > remaining_space:
        body = body[:remaining_space - 3] + "..."

    parts = [
        pre_hook,
        "",
        hook,
        "",
        body,
        "",
        hashtags,
    ]

    if add_credit:
        parts += ["", f"Via @{credit_handle} 🎬"]

    return "\n".join(parts)
