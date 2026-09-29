# -*- coding: utf-8 -*-

from pathlib import Path
import pandas as pd

INPUT_DIR = Path("../../gurobi_8_threads")
OUTPUT_DIR = Path("data")

OUTPUT_DIR.mkdir(exist_ok=True)


def parse_file(path, max_obj):
    times = []
    objs = []
    seen = set()

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()

            # berieme len zmeny incumbentu
            if not line.startswith("H"):
                continue

            parts = line.split()

            try:
                # cas
                time_str = parts[-1]
                if not time_str.endswith("s"):
                    continue
                time = int(time_str[:-1])

                # objective
                obj_raw = float(parts[-5])
                obj = int(round(obj_raw))

                # cap na max pocet zmien
                if obj > max_obj:
                    obj = max_obj

                # unikátny cas (baseline)
                if time not in seen:
                    seen.add(time)
                    times.append(time)
                    objs.append(obj)

            except Exception:
                continue

    df = pd.DataFrame({"time": times, "obj": objs})
    df = df.sort_values("time")
    return df


def main():
    for file in INPUT_DIR.glob("*_1_GUROBI.out"):

        name = file.stem

        # ? explicitne ignoruj nechcené varianty
        if "1_THREAD" in name or "BARRIER" in name:
            continue

        # ocakávaný názov:
        # 20260219_88x1257_1_GUROBI.out
        parts = name.split("_")

        day = parts[0]
        size_part = parts[1]

        try:
            seq_len = int(size_part.split("x")[1])
            max_obj = seq_len - 1
        except:
            print(f"ERROR parsing sequence length in {file.name}")
            continue

        df = parse_file(file, max_obj)

        if df.empty:
            print(f"WARNING: no baseline data parsed for {file.name}")
            continue

        out_name = f"{day}_obj1_long.csv"
        out_path = OUTPUT_DIR / out_name

        df.to_csv(out_path, index=False)

        print(f"{file.name} -> {out_name} ({len(df)} points)")


if __name__ == "__main__":
    main()