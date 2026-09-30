import csv
import sys

FIGHTERS = {"red", "blue"}
EVENT_COLUMNS = ["round", "time_sec", "fighter", "strike", "target", "result"]
TARGETS = {"head", "body", "legs"}
RESULT = {"missed", "blocked", "landed_flush", "landed"}
STRIKES = {"jab", "cross", "hook", "uppercut", "overhand", "elbow", "knee", "kick", "teep"}
LANDED_RESULTS = {"landed_flush", "landed"}
ROUND_SECONDS = 300
ALLOWED = {"fighter": FIGHTERS, "strike": STRIKES, "target": TARGETS, "result": RESULT}

STATS_FIGHTER_KEYS = [
    "thrown", "landed", "landed_flush", "blocked", "missed",
    "accuracy", "thrown_per_min", "landed_per_min",
    "by_strike", "by_target", "by_round",
]
BUCKET_KEYS = ["thrown", "landed"]


def validate_event(row, line_no):
    where = f"line {line_no}: "

    missing = [col for col in EVENT_COLUMNS if not (row.get(col) or "").strip()]
    if missing:
        return [f"{where}missing value for '{col}'" for col in missing]

    problems = []
    if not row["round"].strip().isdigit() or int(row["round"]) < 1:
        problems.append(f"{where}round must be a positive integer, got '{row['round']}'")
    try:
        t = float(row["time_sec"])
        if not 0 <= t <= ROUND_SECONDS:
            problems.append(f"{where}time_sec must be between 0 and {ROUND_SECONDS}, got {t}")
    except ValueError:
        problems.append(f"{where}time_sec must be a number, got '{row['time_sec']}'")
    for col, allowed in ALLOWED.items():
        if row[col].strip().lower() not in allowed:
            problems.append(f"{where}{col} must be one of {sorted(allowed)}, got '{row[col]}'")
    return problems


def read_events(path):
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != EVENT_COLUMNS:
            raise ValueError(f"{path}: header must be exactly {EVENT_COLUMNS}, got {reader.fieldnames}")
        rows = list(reader)

    problems = []
    for line_no, row in enumerate(rows, start=2):
        problems += validate_event(row, line_no)
    if problems:
        raise ValueError(f"{path}: {len(problems)} problem(s)\n" + "\n".join(problems))

    events = []
    for row in rows:
        event = {col: row[col].strip().lower() for col in EVENT_COLUMNS}
        event["round"] = int(event["round"])
        event["time_sec"] = float(event["time_sec"])
        events.append(event)
    return events


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python schemas.py events.csv")
        sys.exit(1)

    failed = False
    for path in sys.argv[1:]:
        try:
            print(f"{path}: OK, {len(read_events(path))} events")
        except (ValueError, FileNotFoundError) as e:
            print(e)
            failed = True
    sys.exit(1 if failed else 0)