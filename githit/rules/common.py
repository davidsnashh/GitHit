from githit.schemas import LANDED_RESULTS, ROUND_SECONDS

PUNCHES = ["jab", "cross", "hook", "uppercut", "overhand"]
POWER_PUNCHES = ["cross", "hook", "overhand"]
INSIDE_WEAPONS = ["elbow", "knee", "uppercut"]
COMBO_GAP = 1.5
MINUTES_PER_ROUND = ROUND_SECONDS / 60
LAST_MINUTE_START = ROUND_SECONDS - 60
MIN_ATTEMPTS = 5
MIN_COMBOS = 3
MIN_ROUNDS = 2


def opponent(fighter):
    if fighter == "red":
        return "blue"
    return "red"


def fighter_events(events, fighter):
    picked = []
    for event in events:
        if event["fighter"] == fighter:
            picked.append(event)
    return picked


def round_events(events, round_number):
    picked = []
    for event in events:
        if event["round"] == round_number:
            picked.append(event)
    return picked


def rounds_present(events):
    rounds = []
    for event in events:
        if event["round"] not in rounds:
            rounds.append(event["round"])
    return sorted(rounds)


def is_landed(event):
    return event["result"] in LANDED_RESULTS


def landed_events(events):
    picked = []
    for event in events:
        if is_landed(event):
            picked.append(event)
    return picked


def with_result(events, result):
    picked = []
    for event in events:
        if event["result"] == result:
            picked.append(event)
    return picked


def with_strike(events, strikes):
    picked = []
    for event in events:
        if event["strike"] in strikes:
            picked.append(event)
    return picked


def with_target(events, target):
    picked = []
    for event in events:
        if event["target"] == target:
            picked.append(event)
    return picked


def values_of(events, key):
    values = []
    for event in events:
        values.append(event[key])
    return values


def count_values(values):
    counts = {}
    for value in values:
        if value not in counts:
            counts[value] = 0
        counts[value] += 1
    return counts


def count_by(events, key):
    return count_values(values_of(events, key))


def biggest_count(counts):
    biggest = 0
    for value in counts:
        if counts[value] > biggest:
            biggest = counts[value]
    return biggest


def share(part, whole):
    if whole == 0:
        return 0.0
    return part / whole


def seconds_between(first, second):
    if first["round"] != second["round"]:
        return None
    return second["time_sec"] - first["time_sec"]


def followed_within(others, event, window):
    for other in others:
        if other is event:
            continue
        gap = seconds_between(event, other)
        if gap is not None and 0 < gap <= window:
            return True
    return False


def preceded_within(others, event, window):
    for other in others:
        if other is event:
            continue
        gap = seconds_between(other, event)
        if gap is not None and 0 < gap <= window:
            return True
    return False


def count_followed(events, others, window):
    count = 0
    for event in events:
        if followed_within(others, event, window):
            count += 1
    return count


def count_preceded(events, others, window):
    count = 0
    for event in events:
        if preceded_within(others, event, window):
            count += 1
    return count


def split_combos(events):
    combos = []
    for event in events:
        if combos:
            gap = seconds_between(combos[-1][-1], event)
            if gap is not None and gap <= COMBO_GAP:
                combos[-1].append(event)
                continue
        combos.append([event])
    return combos


def multi_strike_combos(events):
    picked = []
    for combo in split_combos(events):
        if len(combo) >= 2:
            picked.append(combo)
    return picked


def count_in_first_minute(events):
    count = 0
    for event in events:
        if event["time_sec"] < 60:
            count += 1
    return count


def count_in_last_minute(events):
    count = 0
    for event in events:
        if event["time_sec"] >= LAST_MINUTE_START:
            count += 1
    return count


def round_line(round_number, line):
    return f"Round {round_number}: {line}"
