import textwrap

def make_script(category, item):
    if category == "gta6":
        lines = [
            "GTA SIX DETAIL YOU SHOULD KNOW.",
            item["claim"],
            item["context"],
            "Here is the interesting part: " + item["angle"] + ".",
            "That is what is officially known. Anything beyond that is speculation until Rockstar confirms it.",
            "Follow for more clear GTA six breakdowns."
        ]
        title = item["topic"] + " in GTA 6"
        description = f'{item["context"]}\nSource: {item["source"]}\n\nThis video separates official information from speculation.'
        tags = ["GTA6", "GrandTheftAuto", "Gaming"]
    else:
        lines = [
            "Imagine this.",
            item["seed"],
            "At first, it seemed impossible. But one small detail changed everything.",
            item["twist"],
            "And that is when the truth finally became clear.",
            item["moral"],
            "Would you have made the same choice? Follow for another original story."
        ]
        title = "A " + item["theme"].title() + " Story With a Twist"
        description = "An original short story created for this channel. Characters and events are fictional."
        tags = ["ShortStory", "AnimatedStory", "Storytime"]
    script = " ".join(lines)
    return {"title": title[:95], "description": description, "tags": tags, "script": script, "scenes": lines}

def estimate_duration(script, words_per_minute=145):
    words = len(script.split())
    return max(30, min(58, round(words / words_per_minute * 60)))
