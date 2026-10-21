from githit.rules.common import MINUTES_PER_ROUND, MIN_ATTEMPTS, MIN_ROUNDS
from githit.rules.common import fighter_events, round_events, rounds_present, opponent, landed_events
from githit.rules.common import with_strike, with_target, share, count_by, biggest_count
from githit.rules.common import count_followed, count_in_last_minute, round_line


def opponent_landed(events, fighter):
    return landed_events(fighter_events(events, opponent(fighter)))


def high_absorption(events, fighter):
    rounds = rounds_present(events)
    if len(rounds) == 0:
        return None
    landed = opponent_landed(events, fighter)
    if len(landed) / (len(rounds) * MINUTES_PER_ROUND) > 4:
        return "You are eating too much. Tighten up."
    return None


def head_absorption(events, fighter):
    landed = opponent_landed(events, fighter)
    if len(landed) < MIN_ATTEMPTS:
        return None
    if share(len(with_target(landed, "head")), len(landed)) > 0.65:
        return "Everything he lands is on your head. Hands up, chin down."
    return None


def body_worn_down(events, fighter):
    landed = opponent_landed(events, fighter)
    for round_number in rounds_present(events):
        if len(with_target(round_events(landed, round_number), "body")) >= 8:
            return round_line(round_number, "He is investing in your body. Elbows in.")
    return None


def opponent_kicks(events, fighter, target):
    return with_target(with_strike(fighter_events(events, opponent(fighter)), ["kick"]), target)


def kick_landed_rate(kicks, minimum_thrown):
    if len(kicks) < minimum_thrown:
        return None
    return share(len(landed_events(kicks)), len(kicks))


def eats_leg_kicks(events, fighter):
    rate = kick_landed_rate(opponent_kicks(events, fighter, "legs"), 4)
    if rate is not None and rate > 0.70:
        return "Check the leg kicks. He is landing every one."
    return None


def eats_body_kicks(events, fighter):
    rate = kick_landed_rate(opponent_kicks(events, fighter, "body"), 3)
    if rate is not None and rate > 0.60:
        return "Body kicks are getting through. Catch or block."
    return None


def head_kick_landed(events, fighter):
    if len(landed_events(opponent_kicks(events, fighter, "head"))) >= 1:
        return "He landed a head kick. Your rear hand was not there."
    return None


def same_strike_repeated(events, fighter):
    landed = opponent_landed(events, fighter)
    for round_number in rounds_present(events):
        if biggest_count(count_by(round_events(landed, round_number), "strike")) >= 4:
            return round_line(round_number, "Same shot four times. Find it and shut it down.")
    return None


def opponent_accuracy_high(events, fighter):
    other = fighter_events(events, opponent(fighter))
    if len(other) < MIN_ATTEMPTS:
        return None
    if share(len(landed_events(other)), len(other)) > 0.50:
        return "He is landing half of what he throws. Make him miss."
    return None


def absorption_rises(events, fighter):
    rounds = rounds_present(events)
    if len(rounds) < MIN_ROUNDS:
        return None
    landed = opponent_landed(events, fighter)
    for i in range(1, len(rounds)):
        before = len(round_events(landed, rounds[i - 1]))
        after = len(round_events(landed, rounds[i]))
        if after <= before:
            return None
    return "You get easier to hit as the fight goes on."


def late_round_absorption(events, fighter):
    landed = opponent_landed(events, fighter)
    if len(landed) < MIN_ATTEMPTS:
        return None
    if share(count_in_last_minute(landed), len(landed)) > 0.40:
        return "You are eating shots in the last minute. That is where rounds are scored."
    return None


def hit_after_throwing(events, fighter):
    own = fighter_events(events, fighter)
    if len(own) < MIN_ATTEMPTS:
        return None
    hit = count_followed(own, opponent_landed(events, fighter), 1.5)
    if share(hit, len(own)) > 0.40:
        return "You are getting hit after you throw. Get out after the combo."
    return None


def trades_when_landing(events, fighter):
    own_landed = landed_events(fighter_events(events, fighter))
    if len(own_landed) < MIN_ATTEMPTS:
        return None
    traded = count_followed(own_landed, opponent_landed(events, fighter), 1.5)
    if share(traded, len(own_landed)) > 0.50:
        return "Every time you land you take one back. Land and leave."
    return None


DEFENSE_RULES = [high_absorption, head_absorption, body_worn_down, eats_leg_kicks, eats_body_kicks, head_kick_landed,
                 same_strike_repeated, opponent_accuracy_high, absorption_rises, late_round_absorption,
                 hit_after_throwing, trades_when_landing]
