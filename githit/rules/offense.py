from githit.rules.common import PUNCHES, POWER_PUNCHES, MIN_ATTEMPTS, MIN_COMBOS
from githit.rules.common import fighter_events, round_events, rounds_present, landed_events
from githit.rules.common import with_result, with_strike, share, seconds_between, round_line
from githit.rules.common import count_followed, count_preceded, multi_strike_combos
from githit.rules.common import values_of, count_values, biggest_count


def single_shots(events, fighter):
    own = fighter_events(events, fighter)
    if len(own) < MIN_ATTEMPTS:
        return None
    followed = count_followed(own, own, 1.5)
    if share(len(own) - followed, len(own)) > 0.70:
        return "Singles. Put strikes together."
    return None


def three_strike_bursts(own):
    count = 0
    for i in range(2, len(own)):
        gap = seconds_between(own[i - 2], own[i])
        if gap is not None and gap <= 2.5:
            count += 1
    return count


def no_three_strike_combos(events, fighter):
    own = fighter_events(events, fighter)
    if len(own) < MIN_ATTEMPTS:
        return None
    if three_strike_bursts(own) == 0:
        return "No combinations. Two is not a combination."
    return None


def low_accuracy(events, fighter):
    own = fighter_events(events, fighter)
    if len(own) < MIN_ATTEMPTS:
        return None
    if share(len(landed_events(own)), len(own)) < 0.35:
        return "Accuracy is down. Set them up instead of throwing to throw."
    return None


def high_miss_rate(events, fighter):
    own = fighter_events(events, fighter)
    if len(own) < MIN_ATTEMPTS:
        return None
    if share(len(with_result(own, "missed")), len(own)) > 0.40:
        return "You are punching air. Close the distance first."
    return None


def high_blocked_rate(events, fighter):
    own = fighter_events(events, fighter)
    if len(own) < MIN_ATTEMPTS:
        return None
    if share(len(with_result(own, "blocked")), len(own)) > 0.40:
        return "He sees everything coming. Hide it behind the jab."
    return None


def three_strike_sequences(combos):
    sequences = []
    for combo in combos:
        names = values_of(combo, "strike")
        for i in range(2, len(names)):
            sequences.append(names[i - 2] + " " + names[i - 1] + " " + names[i])
    return sequences


def combo_repeat(events, fighter):
    own = fighter_events(events, fighter)
    for round_number in rounds_present(events):
        combos = multi_strike_combos(round_events(own, round_number))
        if len(combos) < MIN_COMBOS:
            continue
        if biggest_count(count_values(three_strike_sequences(combos))) >= 3:
            return round_line(round_number, "Same combo three times. He is waiting on it now.")
    return None


def first_strikes(combos):
    names = []
    for combo in combos:
        names.append(combo[0]["strike"])
    return names


def last_strikes(combos):
    names = []
    for combo in combos:
        names.append(combo[-1]["strike"])
    return names


def predictable_opener(events, fighter):
    combos = multi_strike_combos(fighter_events(events, fighter))
    if len(combos) < MIN_COMBOS:
        return None
    if share(biggest_count(count_values(first_strikes(combos))), len(combos)) > 0.60:
        return "You open every combo the same way. Change the first strike."
    return None


def predictable_finisher(events, fighter):
    combos = multi_strike_combos(fighter_events(events, fighter))
    if len(combos) < MIN_COMBOS:
        return None
    if share(biggest_count(count_values(last_strikes(combos))), len(combos)) > 0.60:
        return "He knows what the last shot is. Finish somewhere else."
    return None


def same_target(combo):
    for event in combo:
        if event["target"] != combo[0]["target"]:
            return False
    return True


def level_never_changes(events, fighter):
    combos = multi_strike_combos(fighter_events(events, fighter))
    if len(combos) < MIN_COMBOS:
        return None
    same = 0
    for combo in combos:
        if same_target(combo):
            same += 1
    if share(same, len(combos)) > 0.80:
        return "Change levels inside the combo. Head, body, head."
    return None


def no_jab_setup_for_power(events, fighter):
    own = fighter_events(events, fighter)
    power = with_strike(own, POWER_PUNCHES)
    if len(power) < MIN_ATTEMPTS:
        return None
    set_up = count_preceded(power, with_strike(own, ["jab"]), 1.0)
    if share(len(power) - set_up, len(power)) > 0.70:
        return "Jab first. Your power shots have no setup."
    return None


def naked_kicks(events, fighter):
    own = fighter_events(events, fighter)
    kicks = with_strike(own, ["kick"])
    if len(kicks) < MIN_ATTEMPTS:
        return None
    set_up = count_preceded(kicks, with_strike(own, PUNCHES), 1.2)
    if share(len(kicks) - set_up, len(kicks)) > 0.70:
        return "Kick behind punches. Naked kicks get caught."
    return None


def no_follow_after_landing(events, fighter):
    own = fighter_events(events, fighter)
    landed = landed_events(own)
    if len(landed) < MIN_ATTEMPTS:
        return None
    followed = count_followed(landed, own, 1.5)
    if share(len(landed) - followed, len(landed)) > 0.60:
        return "When it lands, stay on him. You keep stopping after the first one."
    return None


OFFENSE_RULES = [single_shots, no_three_strike_combos, low_accuracy, high_miss_rate, high_blocked_rate, combo_repeat,
                 predictable_opener, predictable_finisher, level_never_changes, no_jab_setup_for_power, naked_kicks,
                 no_follow_after_landing]
