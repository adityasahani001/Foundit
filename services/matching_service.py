from difflib import SequenceMatcher


# ===== SAFE TEXT SIMILARITY =====
def similarity(a, b):
    if not a or not b:
        return 0
    return SequenceMatcher(None, str(a).lower(), str(b).lower()).ratio()


# ===== MAIN MATCH FUNCTION =====
def match_items(items):

    lost_items = [item for item in items if item.get("type") == "lost"]
    found_items = [item for item in items if item.get("type") == "found"]

    matches = []
    seen_pairs = set()

    for lost in lost_items:
        for found in found_items:

            # 🔥 avoid duplicate pairs
            pair_id = (lost.get("id"), found.get("id"))
            if pair_id in seen_pairs:
                continue

            score = 0

            # 🔥 Title similarity (main factor)
            title_score = similarity(lost.get("title"), found.get("title"))
            score += title_score * 0.5

            # 🔥 Category match
            if lost.get("category") and found.get("category"):
                if lost.get("category") == found.get("category"):
                    score += 0.2

            # 🔥 Location similarity
            location_score = similarity(lost.get("location"), found.get("location"))
            score += location_score * 0.2

            # 🔥 Description similarity (NEW)
            desc_score = similarity(lost.get("description"), found.get("description"))
            score += desc_score * 0.1

            # 🔥 Threshold (slightly improved)
            if score >= 0.55:
                matches.append({
                    "lost_item": lost,
                    "found_item": found,
                    "score": round(score, 2)
                })
                seen_pairs.add(pair_id)

    # 🔥 Sort best matches first
    matches.sort(key=lambda x: x["score"], reverse=True)

    return matches