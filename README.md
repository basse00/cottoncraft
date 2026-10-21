# CottonCraft

Our modpack: Minecraft 26.3 on Fabric. This repo holds the **list** of mods,
resource packs, shaders and configs; the files themselves come from
[Modrinth](https://modrinth.com). When something is merged to `main`, it is
published to <https://basse00.github.io/cottoncraft/pack.toml>, and
everyone's game and the server pick it up by themselves.

## Playing

1. Install [Prism Launcher](https://prismlauncher.org) and log in with your
   Microsoft account (Settings > Accounts).
2. Download <https://basse00.github.io/cottoncraft/CottonCraft.zip>, then in
   Prism: **Add Instance > Import**, pick the zip.
3. Launch it. Before the game starts, a small window downloads the mods.
   The first time it asks about optional ones (shaders); pick what you like.

That's all. Every time you press Launch it fetches whatever changed since
last time. Changes reach the site a few minutes after they're merged.

If the game won't start with a version mismatch, the Minecraft or Fabric
version has changed: right-click the instance > Edit > Version, and set it
to what `pack.toml` says (or import the zip again).

## Changing the pack

### The easy way: a form on GitHub

No tools needed. On this repo: **Actions** > **Change the pack** (left) >
**Run workflow** (right). Pick add, remove or update everything, type the
Modrinth name (the last part of its link: `modrinth.com/resourcepack/fresh-animations`
is `fresh-animations`), and press **Run workflow**. A minute later a pull
request shows up under **Pull requests**; open it, check it, and press
**Merge**. Everyone gets it on their next launch; the server at its 05:00
restart.

Resource packs and shaders download for everyone, but each player turns
them on in game (Options > Resource Packs, or Video Settings > Shader
Packs). If it needs other mods, they're added too.

### With packwiz on your PC

You need [git](https://git-scm.com) and
[packwiz](https://packwiz.infra.link/installation/). Never commit `.jar`
files: packwiz writes a small `.pw.toml` file per mod instead.

```bash
git clone https://github.com/basse00/cottoncraft.git
cd cottoncraft
git switch -c add-create          # a branch for your change

packwiz modrinth add create       # a mod, by its name in the Modrinth URL
packwiz modrinth add faithful-32x # a resource pack or a shader works the same
packwiz remove create             # take one out
packwiz update --all              # newer versions of everything

git checkout -- index.toml pack.toml   # leave these out (see below)
git add -A && git commit -m "Add Create" && git push -u origin add-create
```

Then open a pull request on GitHub. Once it's merged, it's live.

`index.toml` and the hash in `pack.toml` are rebuilt when the pack is
published, so leave their changes out of your commit (the `git checkout`
line above). If every pull request carried them, any two open at once
would conflict. Only commit `pack.toml` when you mean to change it (a new
Minecraft or Fabric version).

Things to know:

- **Which side**: each `.pw.toml` has `side = "both"`, `"client"` or
  `"server"`. Mods that change the world, items or blocks must be `both`,
  or players can't join. Things only for the screen (Sodium, Iris,
  minimaps, shaders) are `client`. When packwiz warns "marked for both",
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
  for everyone. Ask Daniel to try a branch first if unsure.
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
| Complementary Reimagined, Complementary Unbound | client, optional (on by default) | shaders; turn on in Options > Video > Shader Packs |
