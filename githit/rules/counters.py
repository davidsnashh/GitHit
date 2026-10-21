from githit.rules.common import MIN_ATTEMPTS
from githit.rules.common import fighter_events, opponent, landed_events, with_result, with_strike
from githit.rules.common import share, count_followed


def no_response_after_hit(events, fighter):
    own = fighter_events(events, fighter)
    other_landed = landed_events(fighter_events(events, opponent(fighter)))
    if len(other_landed) < MIN_ATTEMPTS:
        return None
    answered = count_followed(other_landed, own, 2.0)
    if share(len(other_landed) - answered, len(other_landed)) > 0.60:
        return "When he hits you, hit back. You freeze."
    return None


def no_counter_rate(events, fighter):
    own = fighter_events(events, fighter)
    other = fighter_events(events, opponent(fighter))
    if len(other) < MIN_ATTEMPTS:
        return None
    if share(count_followed(other, own, 1.0), len(other)) < 0.10:
        return "No counters. He throws for free."
    return None


def no_counter_to_misses(events, fighter):
    own = fighter_events(events, fighter)
    misses = with_result(fighter_events(events, opponent(fighter)), "missed")
    if len(misses) < MIN_ATTEMPTS:
        return None
    answered = count_followed(misses, own, 1.0)
    if share(len(misses) - answered, len(misses)) > 0.70:
        return "He is missing and you are not making him pay."
    return None


def lets_kicker_reset(events, fighter):
    own = fighter_events(events, fighter)
    kicks = with_strike(fighter_events(events, opponent(fighter)), ["kick"])
    if len(kicks) < MIN_ATTEMPTS:
        return None
    answered = count_followed(kicks, own, 1.2)
    if share(len(kicks) - answered, len(kicks)) > 0.70:
        return "He kicks and resets for free. Counter the kick."
    return None


COUNTERS_RULES = [no_response_after_hit, no_counter_rate, no_counter_to_misses, lets_kicker_reset]
