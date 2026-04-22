from difflib import SequenceMatcher


# ===== TEXT SIMILARITY =====
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


# ===== MAIN MATCH FUNCTION =====
def match_items(items):
    """
    Input: list of all items
    Output: list of matched pairs
    """

    lost_items = [item for item in items if item.get("type") == "lost"]
    found_items = [item for item in items if item.get("type") == "found"]

    matches = []

    for lost in lost_items:
        for found in found_items:

            score = 0

            # 🔥 Title similarity (important)
            title_score = similarity(lost.get("title", ""), found.get("title", ""))
            score += title_score * 0.5

            # 🔥 Category match
            if lost.get("category") == found.get("category"):
                score += 0.2

            # 🔥 Location similarity
            location_score = similarity(lost.get("location", ""), found.get("location", ""))
            score += location_score * 0.3

            # threshold
            if score > 0.5:
                matches.append({
                    "lost_item": lost,
                    "found_item": found,
                    "score": round(score, 2)
                })

    # sort best matches first
    matches.sort(key=lambda x: x["score"], reverse=True)

    return matches