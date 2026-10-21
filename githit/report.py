from githit.rules import run_rules
from githit.schemas import read_events
from githit.stats import FIGHTERS, build_stats


def header_line(fighter, stats):
    percent = stats["accuracy"] * 100
    return f"{fighter}: {stats['landed']}/{stats['thrown']} landed, {percent:.1f}% accuracy, {stats['landed_per_min']:.1f} landed/min, {stats['landed_flush']} flush"


def fighter_lines(events, fighter, stats):
    lines = [header_line(fighter, stats)]
    for sentence in run_rules(events, fighter):
        lines.append(f"  - {sentence}")
    return lines


def build_report(events, stats):
    lines = []
    for fighter in FIGHTERS:
        lines += fighter_lines(events, fighter, stats["fighters"][fighter])
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    events = read_events("data/labels/fixture_round1/events.csv")
    print(build_report(events, build_stats(events)))
