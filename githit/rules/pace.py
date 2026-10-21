from githit.schemas import ROUND_SECONDS
from githit.rules.common import MINUTES_PER_ROUND, MIN_ATTEMPTS, MIN_ROUNDS
from githit.rules.common import fighter_events, round_events, rounds_present, opponent
from githit.rules.common import landed_events, share, seconds_between, round_line
from githit.rules.common import count_in_first_minute, count_in_last_minute

MIN_GAPS = 5


def low_output(events, fighter):
    own = fighter_events(events, fighter)
    for round_number in rounds_present(events):
        attempts = len(round_events(own, round_number))
        if attempts / MINUTES_PER_ROUND < 3:
            return round_line(round_number, "Volume. You are not throwing enough to win rounds.")
    return None


def output_fade(events, fighter):
    own = fighter_events(events, fighter)
    rounds = rounds_present(events)
    if len(rounds) < MIN_ROUNDS:
        return None
    for i in range(1, len(rounds)):
        before = len(landed_events(round_events(own, rounds[i - 1])))
        after = len(landed_events(round_events(own, rounds[i])))
        if before > 0 and (before - after) / before > 0.33:
            return round_line(rounds[i], "Your output fell off a cliff from last round. Get it back.")
    return None


def round3_collapse(events, fighter):
    own = fighter_events(events, fighter)
    rounds = rounds_present(events)
    if 1 not in rounds or 3 not in rounds:
        return None
    first = len(round_events(own, 1))
    third = len(round_events(own, 3))
    if first > 0 and third / first < 0.6:
        return "Third round was half the first. Pace yourself or fix your gas tank."
    return None


def slow_start(events, fighter):
    own = fighter_events(events, fighter)
    for round_number in rounds_present(events):
        attempts = round_events(own, round_number)
        if len(attempts) < MIN_ATTEMPTS:
            continue
        if share(count_in_first_minute(attempts), len(attempts)) < 0.12:
            return round_line(round_number, "Start faster. You spent the first minute watching.")
    return None


def late_flurry_only(events, fighter):
    own = fighter_events(events, fighter)
    for round_number in rounds_present(events):
        attempts = round_events(own, round_number)
        if len(attempts) < MIN_ATTEMPTS:
            continue
        if share(count_in_last_minute(attempts), len(attempts)) > 0.40:
            return round_line(round_number, "Stealing the last minute does not win the round. Spread it out.")
    return None


def outworked(events, fighter):
    own = fighter_events(events, fighter)
    other = fighter_events(events, opponent(fighter))
    for round_number in rounds_present(events):
        own_count = len(round_events(own, round_number))
        other_count = len(round_events(other, round_number))
        if other_count < MIN_ATTEMPTS:
            continue
        if own_count / other_count < 0.6:
            return round_line(round_number, "You are getting outworked. Match his volume at minimum.")
    return None


def longest_quiet_gap(attempts):
    last_time = 0.0
    longest = 0.0
    for event in attempts:
        longest = max(longest, event["time_sec"] - last_time)
        last_time = event["time_sec"]
    return max(longest, ROUND_SECONDS - last_time)


def dead_stretch(events, fighter):
    own = fighter_events(events, fighter)
    for round_number in rounds_present(events):
        if longest_quiet_gap(round_events(own, round_number)) > 30:
            return round_line(round_number, "Thirty seconds without a strike. Stay busy.")
    return None


def gaps_between(attempts):
    gaps = []
    for i in range(1, len(attempts)):
        gap = seconds_between(attempts[i - 1], attempts[i])
        if gap is not None:
            gaps.append(gap)
    return gaps


def mean(values):
    total = 0.0
    for value in values:
        total += value
    return total / len(values)


def standard_deviation(values):
    average = mean(values)
    total = 0.0
    for value in values:
        total += (value - average) ** 2
    return (total / len(values)) ** 0.5


def metronome_rhythm(events, fighter):
    gaps = gaps_between(fighter_events(events, fighter))
    if len(gaps) < MIN_GAPS:
        return None
    average = mean(gaps)
    if average > 0 and standard_deviation(gaps) / average < 0.3:
        return "Same rhythm every time. Break it up so he cannot time you."
    return None


PACE_RULES = [low_output, output_fade, round3_collapse, slow_start, late_flurry_only, outworked, dead_stretch, metronome_rhythm]
