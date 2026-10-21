from githit.rules.common import PUNCHES, INSIDE_WEAPONS, MIN_ATTEMPTS
from githit.rules.common import fighter_events, landed_events, with_strike, with_target
from githit.rules.common import share, seconds_between, count_by, biggest_count


def head_hunting(events, fighter):
    own = fighter_events(events, fighter)
    if len(own) < MIN_ATTEMPTS:
        return None
    if share(len(with_target(own, "head")), len(own)) > 0.80:
        return "All head. Go to the body and the guard will open."
    return None


def no_body_work(events, fighter):
    own = fighter_events(events, fighter)
    if len(own) < MIN_ATTEMPTS:
        return None
    if share(len(with_target(own, "body")), len(own)) < 0.10:
        return "Zero body work. Start investing there in round one."
    return None


def no_leg_kicks(events, fighter):
    own = fighter_events(events, fighter)
    if len(own) < MIN_ATTEMPTS:
        return None
    leg_kicks = with_target(with_strike(own, ["kick"]), "legs")
    if share(len(leg_kicks), len(own)) < 0.05:
        return "No leg kicks. Take his base."
    return None


def one_weapon(events, fighter):
    landed = landed_events(fighter_events(events, fighter))
    if len(landed) < MIN_ATTEMPTS:
        return None
    if share(biggest_count(count_by(landed, "strike")), len(landed)) > 0.50:
        return "One weapon is carrying you. He will take it away."
    return None


def jab_absent(events, fighter):
    punches = with_strike(fighter_events(events, fighter), PUNCHES)
    if len(punches) < MIN_ATTEMPTS:
        return None
    if share(len(with_strike(punches, ["jab"])), len(punches)) < 0.15:
        return "Where is the jab? Everything comes off it."
    return None


def double_jabs(own):
    count = 0
    for i in range(1, len(own)):
        if own[i - 1]["strike"] != "jab" or own[i]["strike"] != "jab":
            continue
        gap = seconds_between(own[i - 1], own[i])
        if gap is not None and gap <= 1.0:
            count += 1
    return count


def never_doubles_jab(events, fighter):
    own = fighter_events(events, fighter)
    if len(own) < MIN_ATTEMPTS:
        return None
    if double_jabs(own) == 0:
        return "Double the jab. One jab is a range finder, two is an attack."
    return None


def jab_cross_only(events, fighter):
    punches = with_strike(fighter_events(events, fighter), PUNCHES)
    if len(punches) < MIN_ATTEMPTS:
        return None
    if share(len(with_strike(punches, ["jab", "cross"])), len(punches)) > 0.85:
        return "Straight punches only. Add hooks and uppercuts."
    return None


def no_inside_weapons(events, fighter):
    own = fighter_events(events, fighter)
    if len(own) < MIN_ATTEMPTS:
        return None
    if len(with_strike(own, INSIDE_WEAPONS)) == 0:
        return "No inside game. When it gets close you have nothing."
    return None


def rear_hand_dependency(events, fighter):
    landed_punches = with_strike(landed_events(fighter_events(events, fighter)), PUNCHES)
    if len(landed_punches) < MIN_ATTEMPTS:
        return None
    if share(len(with_strike(landed_punches, ["cross", "overhand"])), len(landed_punches)) > 0.60:
        return "Lead hand is dead. All your damage is the rear hand and he knows it."
    return None


def no_hooks(events, fighter):
    own = fighter_events(events, fighter)
    if len(own) < MIN_ATTEMPTS:
        return None
    if len(with_strike(own, ["hook"])) == 0:
        return "No hooks. You cannot go around a high guard."
    return None


def no_teep(events, fighter):
    own = fighter_events(events, fighter)
    if len(own) < MIN_ATTEMPTS:
        return None
    if len(with_strike(own, ["teep"])) == 0:
        return "No teep. You have no way to keep him off you."
    return None


def longest_same_strike_run(own):
    longest = 0
    run = 0
    last_strike = None
    for event in own:
        if event["strike"] == last_strike:
            run += 1
        else:
            run = 1
            last_strike = event["strike"]
        longest = max(longest, run)
    return longest


def same_strike_stretch(events, fighter):
    if longest_same_strike_run(fighter_events(events, fighter)) >= 5:
        return "Five of the same strike in a row. Mix it."
    return None


VARIETY_RULES = [head_hunting, no_body_work, no_leg_kicks, one_weapon, jab_absent, never_doubles_jab, jab_cross_only,
                 no_inside_weapons, rear_hand_dependency, no_hooks, no_teep, same_strike_stretch]
