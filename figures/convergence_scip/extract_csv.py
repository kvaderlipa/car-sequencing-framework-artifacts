# -*- coding: utf-8 -*-


import re
import pandas as pd

from pathlib import Path
import pandas as pd

INPUT_DIR = Path("../../scip")      # uprav
OUTPUT_DIR = Path("data")

OUTPUT_DIR.mkdir(exist_ok=True)



TIME_RE = re.compile(r"(\d+)\s*([sm])")

def parse_file(path, max_obj):
    records = []

    best_obj = None
    best_time = None

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "|" not in line:
                continue

            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 16:
                continue

            # ---------- TIME (ROBUSTNE) ----------
            m = TIME_RE.search(parts[0])
            if not m:
                continue

            time_val = int(m.group(1))
            unit = m.group(2)

            time = time_val if unit == "s" else time_val * 60

            # ---------- PRIMALBOUND ----------
            primal = parts[15]
            if primal == "--":
                continue

            try:
                obj = int(round(float(primal)))
            except ValueError:
                continue

            if obj > max_obj:
                obj = max_obj

            # ---------- INCUMBENT CHANGE ----------
            if best_obj is None:
                best_obj = obj
                best_time = time
                records.append((time, obj))
                continue

            if obj < best_obj:
                if time == best_time:
                    # rovnaký cas ? ber lepší
                    records[-1] = (time, obj)
                else:
                    records.append((time, obj))
                    best_time = time

                best_obj = obj

    return pd.DataFrame(records, columns=["time", "obj"])

def main():
    for file in INPUT_DIR.glob("*.out"):

        # napr: 20260219_88x1257_1_SCIP.out
        parts = file.stem.split("_")

        day = parts[0]
        size_part = parts[1]
        obj_version = parts[-2]

        if obj_version == "0":
            continue

        try:
            seq_len = int(size_part.split("x")[1])
            max_obj = seq_len - 1
        except:
            print(f"ERROR parsing sequence length in {file.name}")
            continue

        df = parse_file(file, max_obj)

        if df.empty:
            print(f"WARNING: no incumbent changes in {file.name}")
            continue

        out_name = f"{day}_obj{obj_version}_SCIP.csv"
        out_path = OUTPUT_DIR / out_name

        df.to_csv(out_path, index=False)

        print(f"{file.name} -> {out_name} ({len(df)} changes)")


if __name__ == "__main__":
    main()