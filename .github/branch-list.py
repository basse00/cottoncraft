#!/usr/bin/env python3
"""Write the open pack branches into the Change the pack form's dropdown.

GitHub can't fill a dropdown by itself: its choices are fixed text in
change-pack.yml. branch-list.yml runs this after each form run, merge or
deleted branch, with the open pull requests (gh pr list --json) in argv[1].

The form reads only the first word of a choice (the branch name without
pack/), so the rest of the label is free to say what's in it.
"""
import json, re, sys
from pathlib import Path

FORM = Path(__file__).parent / "workflows/change-pack.yml"
FIXED = ["new branch", "new branch, named below"]

prs = json.load(open(sys.argv[1]))
labels = []
for pr in sorted(prs, key=lambda p: p["headRefName"]):
    head = pr["headRefName"]
    if not head.startswith("pack/"):
        continue
    name = head.removeprefix("pack/")
    # Automatic names are run numbers; the title says what's in them.
    labels.append(f"{name} ({pr['title'][:60]})" if name.isdigit() else name)

text = FORM.read_text()
start, end = "# BEGIN branch list", "# END branch list"
m = re.search(rf"^( *){re.escape(start)}.*?\n.*?^ *{re.escape(end)}[^\n]*\n", text, re.S | re.M)
if not m:
    sys.exit(f"{FORM}: markers not found")
pad = m.group(1)
block = [f"{pad}{start} (branch-list.yml writes this part)\n"]
block += [f"{pad}- {json.dumps(label)}\n" for label in FIXED + labels]
block += [f"{pad}{end}\n"]
new = text[:m.start()] + "".join(block) + text[m.end():]
if new != text:
    FORM.write_text(new)
print("branches:", ", ".join(labels) or "none open")
