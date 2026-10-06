import glob
import json
import os
import sys

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = max(glob.glob("evaluation/results/*.json"), key=os.path.getmtime)

with open(path, encoding="utf-8") as result_file:
    data = json.load(result_file)
print("file:", path)
found = False
for c in data.get("cases", []):
    if c.get("must_abstain") and not c.get("abstained"):
        found = True
        print(f"- MISSED REFUSAL {c['id']}\n  Q: {c['question']}\n  A: {c['answer'][:300]!r}")
    if not c.get("must_abstain") and c.get("abstained"):
        found = True
        print(f"- WRONG REFUSAL {c['id']}\n  Q: {c['question']}")
if not found:
    print("no abstention failures")
