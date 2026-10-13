# Data layout

Every fight gets a `fight_id`, a short folder name such as `fixture_round1`. The same id is used in all three tiers below.

## data/raw/<fight_id>/

Source video and anything else that came straight from the camera. Large and never committed: `data/raw/` is in `.gitignore`.

## data/labels/<fight_id>/events.csv

Human ground truth. One row per strike with the columns `round, time_sec, fighter, strike, target, result`, validated by `githit validate <fight_id>`. This is the only tier that is committed.

## data/derived/<fight_id>/

Machine output built from the labels, such as `stats.json` and `report.md`. Rebuilt by `githit stats` and `githit report`, so it is never committed: `data/derived/` is in `.gitignore`.
