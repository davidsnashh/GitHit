from githit.rules.pace import PACE_RULES
from githit.rules.offense import OFFENSE_RULES
from githit.rules.variety import VARIETY_RULES
from githit.rules.defense import DEFENSE_RULES
from githit.rules.counters import COUNTERS_RULES

ALL_RULES = PACE_RULES + OFFENSE_RULES + VARIETY_RULES + DEFENSE_RULES + COUNTERS_RULES


def run_rules(events, fighter):
    sentences = []
    for rule in ALL_RULES:
        sentence = rule(events, fighter)
        if sentence is not None:
            sentences.append(sentence)
    return sentences
