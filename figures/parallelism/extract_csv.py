# -*- coding: utf-8 -*-

from pathlib import Path
import pandas as pd

INPUT_DIR_8 = Path("../../gurobi_8_threads")
INPUT_DIR_1 = Path("../../gurobi_1_thread")
OUTPUT_DIR = Path("data")

OUTPUT_DIR.mkdir(exist_ok=True)


def parse_file(path, max_obj):
    times = []
    objs = []
    seen = set()

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()

            if not line.startswith("H"):
                continue

            parts = line.split()

            try:
                # time
                time_str = parts[-1]
                if not time_str.endswith("s"):
                    continue
                time = int(time_str[:-1])

                # objective value
                obj_raw = float(parts[-5])
                obj = int(round(obj_raw))

                if obj > max_obj:
                    obj = max_obj

                if time not in seen:
                    seen.add(time)
                    times.append(time)
                    objs.append(obj)

            except Exception:
                continue

    df = pd.DataFrame({"time": times, "obj": objs})
    df = df.sort_values("time")
    return df


def process_directory(input_dir: Path, suffix: str):
    for file in input_dir.glob("*_1_GUROBI*.out"):

        name = file.stem

        # explicitne ignoruj nechcené varianty
        if "BARRIER" in name:
            continue

        # ocakávaný názov:
        # 20260219_88x1257_1_GUROBI.out
        # 20260219_88x1257_1_GUROBI_1_THREAD.out
        parts = name.split("_")

        day = parts[0]
        size_part = parts[1]
        obj_version = parts[2]

        # ? len Objective 1
        if obj_version != "1":
            continue

        try:
            seq_len = int(size_part.split("x")[1])
            max_obj = seq_len - 1
        except:
            print(f"ERROR parsing sequence length in {file.name}")
            continue

        df = parse_file(file, max_obj)

        if df.empty:
            print(f"WARNING: no data parsed for {file.name}")
            continue

        out_name = f"{day}_obj1_{suffix}.csv"
        out_path = OUTPUT_DIR / out_name

        df.to_csv(out_path, index=False)

        print(f"{file.name} -> {out_name} ({len(df)} points)")


def main():
    print("Processing 8-thread runs...")
    process_directory(INPUT_DIR_8, "8thread")

    print("\nProcessing 1-thread runs...")
    process_directory(INPUT_DIR_1, "1thread")


if __name__ == "__main__":
    main()