# CottonCraft

Our modpack: Minecraft 26.3 on Fabric. This repo holds the **list** of mods
and configs; the files themselves come from
[Modrinth](https://modrinth.com). When something is merged to `main`, it is
published to <https://basse00.github.io/cottoncraft/pack.toml>, and
everyone's game and the server pick it up by themselves.

## Playing

1. Install [Prism Launcher](https://prismlauncher.org) and log in with your
   Microsoft account (Settings > Accounts).
2. In Prism: **Add Instance > Import**, paste
   `https://basse00.github.io/cottoncraft/CottonCraft.zip` into the box and
   press OK. No need to download it first.
3. Launch it. Before the game starts, a small window downloads the mods.
   If it asks about optional mods, pick what you like.
4. Resource packs and shaders are up to you (see below).
5. The server is already in **Multiplayer** as "CottonCraft" (you still
   need to be on the whitelist: `/mc add` on Discord).

The instance gets the CottonCraft icon on import. Imported before it
existed? Right-click the instance > **Change Icon** > **Add Icon**, and
pick [cottoncraft.png](https://raw.githubusercontent.com/basse00/cottoncraft/main/prism/cottoncraft.png)
(save it first).

That's all. Every time you press Launch it fetches whatever changed since
last time. Changes reach the site a few minutes after they're merged.

The server list comes from `servers.dat` here, but only for players who
don't have a server list yet (it is marked `preserve` in `index.toml`, so
nobody's own list is ever overwritten). If the server's address changes,
change it in `servers.dat` and tell everyone to edit their entry.

### Your own resource packs and shaders

They aren't in the pack: everyone picks their own. In Prism, right-click
the instance > **Edit** > **Resource packs** (or **Shader packs**) >
**Download**, or drop a zip from Modrinth into those folders. The pack
never touches them. Shaders work because Iris is in the pack, and
resource packs with animated or custom mobs (Fresh Animations and the
like) because Entity Model Features and Entity Texture Features are.

### Extras: small fixes you can add

Resource packs made for this pack, for anyone who wants them. Download
the zip and drop it in the instance's resource packs (as above), then
turn it on in Options > Resource Packs.

- [dark-iron-chandelier-1.0.0.zip](https://basse00.github.io/cottoncraft/extras/dark-iron-chandelier-1.0.0.zip):
  the iron chandelier (Macaw's Lights) with a frame half as bright.
  Shaders such as Complementary make blocks that give light glow, so its
  frame looked almost white; without shaders it looks very dark.
- [polydex-bar-1.3.1.zip](https://basse00.github.io/cottoncraft/extras/polydex-bar-1.3.1.zip):
  for the bar at the top on our server (it shows while you mine or look at
  a creature).
  - `/polydex color <theme>` picks its look: `obsidian` (deep purple),
    `dark`, `cotton`, `emerald` or `copper`, each a little thinner than
    the normal bar; `classic` is the normal white and red one.
  - `/polydex hover names on` also shows the name of every block you look
    at; with this pack that is just the name, without an empty bar under
    it. `/polydex hover names off` to go back.

  Without this pack a theme shows as a plain coloured bar. The pictures
  are made by `.github/make-bar.py`.

The files are in `extras/`; each folder becomes a zip on the site, named
after the folder and its `VERSION` file. Changed one? Raise its `VERSION`
and the link above to match (the site isn't published until they do).

If the game won't start with a version mismatch, the Minecraft or Fabric
version has changed: right-click the instance > Edit > Version, and set it
to what `pack.toml` says (or import the zip again).

## Changing the pack

### The easy way: a form on GitHub

No tools needed. On this repo: **Actions** > **Change the pack** (left) >
**Run workflow** (right). Pick add, remove or update everything, type the
Modrinth name (the last part of its link: `modrinth.com/mod/appleskin`
is `appleskin`), and press **Run workflow**. A minute later a pull
request shows up under **Pull requests**; open it, check it, and press
**Merge**. Everyone gets it on their next launch; the server at its 05:00
restart.

**Branch** decides where the change goes: **new branch** (the default)
makes one with a number for a name; **new branch, named below** uses the
name you type under it (e.g. `sneakyspank`); or pick a branch from the
list to go on with it. Easiest: one branch each, named after you, and
always pick that one. It's brought up to date with the newest pack first,
merged or not; while its pull request is open your changes are added to
it, and after a merge the next change opens a new one. The list updates
itself a minute after each run; reload the page to see it.

If it needs other mods, they're added too. Resource packs and shaders are
refused: each player adds their own (see Playing).

### With packwiz on your PC

You need [git](https://git-scm.com) and
[packwiz](https://packwiz.infra.link/installation/). Never commit `.jar`
files: packwiz writes a small `.pw.toml` file per mod instead.

Once, get the repo:

```
git clone https://github.com/basse00/cottoncraft.git
```

Then every change goes the same four steps: get the newest pack, make a
branch, change things, send it.

**1. Start (every time)**
```
cd cottoncraft
git switch main
git pull
git switch -c <short-name>        # e.g. add-appleskin
packwiz refresh                   # first: brings index.toml up to date
```

**2. Change the pack**
```
packwiz modrinth add <name>       # add a mod; <name> = last part of its Modrinth link
packwiz remove <name>             # remove; <name> = file name in mods/ without .pw.toml
packwiz update <name>             # newer version of one mod
packwiz update --all              # newer versions of everything
```
- No `mr` with `remove` or `update`; only `add` has it.
- Mods only. Resource packs and shaders are each player's own choice.
- If packwiz says "marked for both", that's usually fine.

**3. Send it**
```
git checkout -- index.toml pack.toml   # always: publishing builds these two
git status                             # check only your changes are listed
git add -A
git commit -m "Add AppleSkin"
git push -u origin <short-name>
```

**4. On GitHub**
- **Compare & pull request**, then **Create**.
- Wait for the green check, then **Merge**.
- Players get it on their next launch. The server gets it at 05:00, or
  straight away with `/mc restart` in Discord.

**If something goes wrong**

| Problem | Fix |
|---|---|
| "Can't find this file" | Run `packwiz refresh` first |
| Merge conflict | Start a new branch from the newest main and redo the change |
| Red check on the pull request | Click it: it says which mod is missing what |
| Forgot to make a branch | Fine: push the branch you're on and make a pull request from it |
| Want to undo something on a branch | Do the opposite (`add` / `remove`), then commit and push again |

`index.toml` and the hash in `pack.toml` are rebuilt when the pack is
published, so leave their changes out of your commit (the `git checkout`
line above). If every pull request carried them, any two open at once
would conflict. Only commit `pack.toml` when you mean to change it (a new
Minecraft or Fabric version).

Things to know:

- **Which side**: each `.pw.toml` has `side = "both"`, `"client"` or
  `"server"`. Mods that change the world, items or blocks must be `both`,
  or players can't join. Things only for the screen (Sodium, Iris,
  minimaps) are `client`. When packwiz warns "marked for both",
  that's usually fine to leave.
- **Optional**: add this to a `.pw.toml` to let each player choose:
  ```toml
  [option]
  optional = true
  default = false
  description = "What it does"
  ```
- **Configs**: put a config file in `config/` (same path as in
  `.minecraft/config/`) and run `packwiz refresh`; it's sent to everyone and
  the server, and overwrites their own copy when it changes here.
- **Test before merging** big changes: a mod that breaks the server stops it
  for everyone. Ask Basse to try a branch first if unsure.
- **Minecraft or Fabric version**: change it in `pack.toml` with
  `packwiz migrate minecraft <version>`, and check every mod has a build for
  it. Players then update their instance once (see above).

## What's in it

| Mod | Side | What it does |
|---|---|---|
| Fabric API | both | needed by most mods |
| Waystones (+ Balm, Shogi) | both | teleport stones |
| VeinMiner (+ Fabric Language Kotlin) | both | mine a whole ore vein at once |
| VeinMiner Hotkey | client | the key to turn VeinMiner on |
| Tree Harvester (+ Collective) | server | chop one log, the whole tree falls |
| BlueMap | server | the web map |
| Lithium, FerriteCore | both | faster, less memory |
| Sodium, Mod Menu (+ Text Placeholder API) | client | faster rendering, mod list in the menu |
| Iris | client | shader support |
