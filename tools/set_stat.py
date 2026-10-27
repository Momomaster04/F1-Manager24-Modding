"""Set one part-design stat in an unpacked save database.

Edits the database in place, so run it on a copy.
Stat numbers are from Parts_Enum_Stats (10 = Power, see docs/db-map.md).

Usage: python set_stat.py <db.sqlite> <design_id> <stat> <unit_value> <value>
"""
import sqlite3
import sys


def set_stat(db: str, design_id: int, stat: int, unit_value: float, value: float) -> tuple:
    con = sqlite3.connect(db)
    with con:
        before = con.execute(
            "SELECT UnitValue, Value FROM Parts_Designs_StatValues WHERE DesignID = ? AND PartStat = ?",
            (design_id, stat)).fetchone()
        if before is None:
            raise ValueError(f"design {design_id} has no stat {stat}")
        con.execute(
            "UPDATE Parts_Designs_StatValues SET UnitValue = ?, Value = ? WHERE DesignID = ? AND PartStat = ?",
            (unit_value, value, design_id, stat))
    con.close()
    return before


def main() -> None:
    if len(sys.argv) != 6:
        sys.exit(__doc__)
    db, design_id, stat, unit_value, value = sys.argv[1:]
    before = set_stat(db, int(design_id), int(stat), float(unit_value), float(value))
    print(f"design {design_id} stat {stat}: UnitValue {before[0]} -> {unit_value}, Value {before[1]} -> {value}")


if __name__ == "__main__":
    main()
