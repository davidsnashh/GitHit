import json

from schemas import read_events, LANDED_RESULTS

FIGHTERS = ["red", "blue"]
RESULTS = ["blocked", "missed", "landed_flush"]
ROUND_MINUTES = 5


def highest_round(events):
    rounds = 0
    for event in events:
        rounds = max(rounds, event["round"])
    return rounds


def safe_divide(top, bottom):
    if bottom == 0:
        return 0.0
    return top / bottom


def add_to_group(group, key, result):
    if key not in group:
        group[key] = {"thrown": 0, "landed": 0}
    group[key]["thrown"] += 1
    if result in LANDED_RESULTS:
        group[key]["landed"] += 1


def fighter_stats(events, fighter, minutes):
    stats = {"thrown": 0, "landed": 0, "landed_flush": 0, "blocked": 0,
             "missed": 0, "accuracy": 0.0, "thrown_per_min": 0.0,
             "landed_per_min": 0.0, "by_strike": {}, "by_target": {},
             "by_round": {}}
    for event in events:
        if event["fighter"] != fighter:
            continue
        result = event["result"]
        stats["thrown"] += 1
        if result in RESULTS:
            stats[result] += 1
        if result in LANDED_RESULTS:
            stats["landed"] += 1
        add_to_group(stats["by_strike"], event["strike"], result)
        add_to_group(stats["by_target"], event["target"], result)
        add_to_group(stats["by_round"], event["round"], result)
    stats["accuracy"] = safe_divide(stats["landed"], stats["thrown"])
    stats["thrown_per_min"] = safe_divide(stats["thrown"], minutes)
    stats["landed_per_min"] = safe_divide(stats["landed"], minutes)
    return stats


def build_stats(events):
    rounds = highest_round(events)
    minutes = rounds * ROUND_MINUTES
    fighters = {}
    for fighter in FIGHTERS:
        fighters[fighter] = fighter_stats(events, fighter, minutes)
    return {"rounds": rounds, "fighters": fighters}


if __name__ == "__main__":
    data = build_stats(read_events("events.csv"))
    with open("stats.json", "w") as f:
        json.dump(data, f, indent=2)
    for fighter in FIGHTERS:
        stats = data["fighters"][fighter]
        percent = stats["accuracy"] * 100
        score = f"{stats['landed']}/{stats['thrown']}"
        print(f"{fighter}: {score} landed, {percent:.1f}% accuracy")
