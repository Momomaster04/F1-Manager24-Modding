# F1 Manager 24 – Engine Development Mod

A Python tool that adds a living engine system to F1 Manager 24 career mode. Engines develop over time, regulation changes reshuffle the pecking order, and manufacturers come and go.

The game can't run new logic, so the tool works on the save file between sessions. You save in game, the tool edits the save's database, and you reload.

## Status

**Working and tested in game:**
- Unpacking a `.sav` into its SQLite databases
- Repacking them into a save the game loads. A round trip with no edits gives a byte-identical file.
- Editing engine stats. Raising Renault's power rating from 80 to 90 showed up as 90 in game.
- A map of the save's engine and supplier tables: [docs/db-map.md](docs/db-map.md)

**Planned:**
- A development model: hidden traits for each manufacturer (R&D strength, budget, risk-taking), random gains each development window, and diminishing returns so the field converges
- Regulation eras: new regs reshuffle the order, development years bring steady gains, freezes allow reliability fixes only, and a catch-up allowance helps manufacturers far behind
- Manufacturers entering, leaving and rebranding, and teams switching suppliers
- Works teams get a bonus over customer teams
- A trade-off between reliability and development speed
- The player's team starting its own engine programme mid-career
- An end-of-season engine report, plus a file watcher that runs the tool automatically on each save

## How a save is built

```
[Unreal GVAS header]
u32 compressed size
u32 database sizes ×3
[zlib data: three SQLite databases back to back]
```

Database 1 is the live career; 2 and 3 are older snapshots. Engine stats live in `Parts_Designs_StatValues`. Each manufacturer has a master design, and customer teams carry copies of it. The full breakdown is in [docs/db-map.md](docs/db-map.md).

## Usage

Requires Python 3.10+ (standard library only). **Always work on a copy of your save.** Saves live in `%LOCALAPPDATA%\F1Manager24\Saved\SaveGames\`.

```bash
# Split a save into save_db1.sqlite, save_db2.sqlite and save_db3.sqlite
python tools/unpack.py work/save.sav work

# Set a stat: design 10 (Renault engine), stat 10 (Power), rating 90, score 500
python tools/set_stat.py work/save_db1.sqlite 10 10 90 500

# Build a new save from the databases (never overwrites an existing file)
python tools/repack.py work/save.sav work/save_db1.sqlite work/save_db2.sqlite work/save_db3.sqlite work/save_edited.sav
```

Turn off Steam Cloud for the game while testing edited saves.

## Disclaimer

A fan project, not affiliated with Frontier Developments, Formula 1 or any team. Back up your saves before using it.
