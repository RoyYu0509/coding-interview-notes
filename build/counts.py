import csv, os, sys
R = {r["title"].lower(): r for r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "problems_ranked.csv"), encoding="utf-8"))}
def cnt(title):
    return int(R[title.lower()]["n_companies"])
def rank(title):
    return int(R[title.lower()]["rank"])
if __name__ == "__main__":
    for t in sys.argv[1:]:
        r = R.get(t.lower())
        print(t, "|", r and (r["rank"], r["n_companies"]))
