def make_script(category, item):
    if category == "gta6":
        lines = [
            "GTA SIX DETAIL YOU SHOULD KNOW.",
            item["claim"],
            item["context"],
            "Why does this matter? A setting is more than a map. It influences the atmosphere, the people we meet, the stories told in side activities, and the kinds of places players can explore.",
            "Here is the interesting part: " + item["angle"] + ".",
            "Rockstar has not confirmed every detail fans discuss online, so keep theories separate from official information.",
            "That is what is officially known for now. Follow for more clear GTA six breakdowns."
        ]
        title = item["topic"] + " in GTA 6"
        description = f'{item["context"]}\nSource: {item["source"]}\n\nThis video separates official information from speculation.'
        tags = ["GTA6", "GrandTheftAuto", "Gaming"]
    else:
        lines = [
            "Imagine this.",
            item["seed"],
            "At first, it seemed like an ordinary day. The character tried to ignore the strange detail, but it kept appearing in places where it could not possibly be.",
            "They followed the clue, even though every sensible instinct told them to turn back.",
            item["twist"],
            "For a moment, everything went silent. Then one final detail made the whole story mean something different.",
            item["moral"],
            "What would you have done? Tell us in the comments, and follow for another original short story."
        ]
        title = "A " + item["theme"].title() + " Story With a Twist"
        description = "An original short story created for this channel. Characters and events are fictional."
        tags = ["ShortStory", "AnimatedStory", "Storytime"]
    script = " ".join(lines)
    return {"title": title[:95], "description": description, "tags": tags, "script": script, "scenes": lines, "category_id": "20" if category == "gta6" else "22"}

def estimate_duration(script, words_per_minute=145):
    words = len(script.split())
    return max(30, min(58, round(words / words_per_minute * 60)))
