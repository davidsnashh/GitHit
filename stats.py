"""Compute per-fighter striking stats from events.csv and save stats.json."""
import csv
import json

FIGHTERS = ["red", "blue"]
RESULTS = ["landed", "blocked", "missed"]
ROUND_MINUTES = 5


def read_events(path):
    """Return every row of the CSV file as a list of dicts."""
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def count_rounds(events):
    """Return the highest round number in the events, or 0 if none."""
    rounds = 0
    for event in events:
        rounds = max(rounds, int(event["round"]))
    return rounds


def safe_divide(top, bottom):
    """Return top / bottom, or 0.0 when bottom is 0 so we never crash."""
    if bottom == 0:
        return 0.0
    return top / bottom


def add_to_group(group, key, result):
    """Count one strike under key in a by_strike/by_target/by_round dict."""
    if key not in group:
        group[key] = {"thrown": 0, "landed": 0}
    group[key]["thrown"] += 1
    if result == "landed":
        group[key]["landed"] += 1


def fighter_stats(events, fighter, minutes):
    """Build the full stats dict for one fighter."""
    stats = {"thrown": 0, "landed": 0, "blocked": 0, "missed": 0,
             "accuracy": 0.0, "thrown_per_min": 0.0, "landed_per_min": 0.0,
             "by_strike": {}, "by_target": {}, "by_round": {}}
    for event in events:
        if event["fighter"] != fighter:
            continue
        result = event["result"]
        stats["thrown"] += 1
        if result in RESULTS:
            stats[result] += 1
        add_to_group(stats["by_strike"], event["strike"], result)
        add_to_group(stats["by_target"], event["target"], result)
        add_to_group(stats["by_round"], event["round"], result)
    stats["accuracy"] = safe_divide(stats["landed"], stats["thrown"])
    stats["thrown_per_min"] = safe_divide(stats["thrown"], minutes)
    stats["landed_per_min"] = safe_divide(stats["landed"], minutes)
    return stats


def main():
    """Read the events, compute each fighter's stats, then save and print."""
    events = read_events("events.csv")
    rounds = count_rounds(events)
    minutes = rounds * ROUND_MINUTES
    fighters = {}
    for fighter in FIGHTERS:
        fighters[fighter] = fighter_stats(events, fighter, minutes)
    with open("stats.json", "w") as f:
        json.dump({"rounds": rounds, "fighters": fighters}, f, indent=2)
    for fighter in FIGHTERS:
        stats = fighters[fighter]
        percent = stats["accuracy"] * 100
        score = f"{stats['landed']}/{stats['thrown']}"
        print(f"{fighter}: {score} landed, {percent:.1f}% accuracy")


if __name__ == "__main__":
    main()
