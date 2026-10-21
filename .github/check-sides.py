#!/usr/bin/env python3
"""Check that every mod's required dependencies are installed on the same
side (players, server, or both) as the mod itself, using Modrinth's data.

  check-sides.py          report problems, exit 1 if there are any
  check-sides.py --fix    widen a dependency's side instead (to "both")

Example: Tree Harvester (server) needs Collective, so Collective was added
for the server only; GUI Compass (players) needs it too, and the game
refused to start on players' PCs until Collective was "both".
"""
import json
import urllib.parse
import pathlib
import re
import sys
import urllib.request

fix = "--fix" in sys.argv
mods = {}
for path in sorted(pathlib.Path("mods").glob("*.pw.toml")):
    text = path.read_text()
    pid = re.search(r'^mod-id = "(.*)"', text, re.M)
    vid = re.search(r'^version = "(.*)"', text, re.M)
    side = re.search(r'^side = "(.*)"', text, re.M)
    if pid and vid:
        mods[pid[1]] = {"path": path, "version": vid[1],
                        "side": side[1] if side else "both"}

ids = json.dumps([m["version"] for m in mods.values()])
url = "https://api.modrinth.com/v2/versions?ids=" + urllib.parse.quote(ids)
req = urllib.request.Request(url, headers={"User-Agent": "basse00/cottoncraft check-sides"})
versions = {v["id"]: v for v in json.load(urllib.request.urlopen(req, timeout=60))}

needs = {"client": {"client", "both"}, "server": {"server", "both"}, "both": {"both"}}
problems = 0
changed = True
while changed:  # a widened dependency may have dependencies of its own
    changed = False
    for mod in mods.values():
        for dep in versions.get(mod["version"], {}).get("dependencies", []):
            if dep["dependency_type"] != "required" or dep["project_id"] not in mods:
                continue
            d = mods[dep["project_id"]]
            if d["side"] in needs[mod["side"]]:
                continue
            msg = f'{mod["path"]} ({mod["side"]}) needs {d["path"]}, which is "{d["side"]}"'
            if fix:
                d["path"].write_text(re.sub(r'^side = ".*"', 'side = "both"',
                                            d["path"].read_text(), count=1, flags=re.M))
                d["side"] = "both"
                changed = True
                print(f"fixed: {msg}; now \"both\"")
            else:
                problems += 1
                print(f"::error file={d['path']}::{msg}; make it \"both\"")
sys.exit(1 if problems else 0)
