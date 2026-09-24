import csv
counta = {}
with open("events.csv") as x:
  for row in csv.DictReader(x):
    key = (row["fighter"], row["strike"], row["result"])
        counts[key] = counts.get(key, 0) + 1
