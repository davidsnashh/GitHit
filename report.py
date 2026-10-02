import json

FIGHTERS = ["red", "blue"]

def percent_of(part, whole):
    if whole == 0:
        return 0.0
    return part / whole * 100

def target_count(stats, target, key):
    if target in stats["by_target"]:
        return stats["by_target"][target][key]
    return 0

def low_accuracy(stats):
    percent = stats["accuracy"] * 100
    if percent < 35:
        return f"Only {percent:.0f}% landing. Pick your shots."
    return None

def one_strike_carrying(stats):
    for strike, bucket in stats["by_strike"].items():
        if bucket["landed"] > stats["landed"] / 2:
            return f"{strike} is {bucket['landed']} of your {stats['landed']} landed. Mix it up."
    return None

def few_body_shots(stats):
    percent = percent_of(target_count(stats, "body", "thrown"), stats["thrown"])
    if percent < 10:
        return f"Only {percent:.0f}% to the body. Go downstairs."
    return None

def few_leg_kicks(stats):
    percent = percent_of(target_count(stats, "legs", "thrown"), stats["thrown"])
    if percent < 5:
        return f"Only {percent:.0f}% to the legs. Chop that lead leg."
    return None

def low_output(stats):
    if stats["thrown_per_min"] < 3:
        return f"{stats['thrown_per_min']:.1f} strikes a minute is too slow. Let your hands go."
    return None

def fading_rounds(stats):
    rounds = sorted(stats["by_round"], key=int)
    for i in range(1, len(rounds)):
        before = stats["by_round"][rounds[i - 1]]["landed"]
        after = stats["by_round"][rounds[i]]["landed"]
        if after < before * 2 / 3:
            return f"Landed {before} in round {rounds[i - 1]} but only {after} in round {rounds[i]}. Keep working."
    return None

def getting_blocked(stats):
    percent = percent_of(stats["blocked"], stats["thrown"])
    if percent > 40:
        return f"{percent:.0f}% of your shots are blocked. Feint first and go around the guard."
    return None

def headhunting(stats):
    percent = percent_of(target_count(stats, "head", "landed"), stats["landed"])
    if percent > 65:
        return f"{percent:.0f}% of what you landed was upstairs. Headhunting makes you predictable."
    return None

RULES = [low_accuracy, one_strike_carrying, few_body_shots, few_leg_kicks, low_output, fading_rounds, getting_blocked, headhunting]

def fighter_lines(fighter, stats):
    percent = stats["accuracy"] * 100
    lines = [f"{fighter}: {stats['landed']}/{stats['thrown']} landed, {percent:.1f}% accuracy, {stats['landed_per_min']:.1f} landed/min, {stats['landed_flush']} flush"]
    for rule in RULES:
        sentence = rule(stats)
        if sentence is not None:
            lines.append(f"  - {sentence}")
    return lines

def main():
    with open("stats.json") as f:
        data = json.load(f)
    lines = []
    for fighter in FIGHTERS:
        lines += fighter_lines(fighter, data["fighters"][fighter])
        lines.append("")
    text = "\n".join(lines)
    print(text)
    with open("report.md", "w") as f:
        f.write(text)

if __name__ == "__main__":
    main()
