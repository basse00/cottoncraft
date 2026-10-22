#!/usr/bin/env python3
"""Write the pack branches into the Change the pack form's dropdown.

GitHub can't fill a dropdown by itself: its choices are fixed text in
change-pack.yml. branch-list.yml runs this after each form run, merge or
deleted branch, with the pack/ branches (one per line) in argv[1] and the
open pull requests (gh pr list --json) in argv[2].

Every named branch is listed, merged or not: each person keeps one branch
and goes on using it (the form brings it up to date with main first).
Branches with a number for a name (made by "new branch") are listed only
while their pull request is open, or the list would fill up with them.

The form reads only the first word of a choice (the branch name without
pack/), so the rest of the label is free to say what's in it.
"""
import json, re, sys
from pathlib import Path

FORM = Path(__file__).parent / "workflows/change-pack.yml"
FIXED = ["new branch", "new branch, named below"]

branches = sorted(b.strip().removeprefix("refs/heads/").removeprefix("pack/")
                  for b in open(sys.argv[1]) if b.strip())
open_prs = {pr["headRefName"].removeprefix("pack/"): pr["title"]
            for pr in json.load(open(sys.argv[2])) if pr["headRefName"].startswith("pack/")}
labels = []
for name in branches:
    if not name.isdigit():
        labels.append(name)
    elif name in open_prs:
        # Automatic names are run numbers; the title says what's in them.
        labels.append(f"{name} ({open_prs[name][:60]})")

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
