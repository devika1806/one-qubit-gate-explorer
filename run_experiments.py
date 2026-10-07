"""Save actual, reproducible runs of all eight investigations."""

import argparse
import csv
import json
from pathlib import Path

from lessons import LESSONS
from quantum import experiment, parse_gates


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="local-results")
    args = parser.parse_args()
    directory = Path(args.output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    rows, records = [], []
    for index, lesson in enumerate(LESSONS):
        for label in ("a", "b"):
            seed = 1806 + 2 * index + (label == "b")
            result = experiment(parse_gates(lesson[label]), lesson["initial"], lesson["basis"], 1000, seed)
            records.append({"lesson": lesson["title"], "circuit": label.upper(), **result})
            rows.append({"lesson": lesson["title"], "circuit": label.upper(),
                         "initial": result["initial"], "gates": " ".join(result["gates"]),
                         "basis": result["basis"], "shots": result["shots"], "seed": seed,
                         "exact_p0": result["probabilities"]["0"], "count_0": result["counts"]["0"],
                         "count_1": result["counts"]["1"], "observed_p0": result["observed_p0"],
                         "wilson_low": result["p0_wilson_95"][0], "wilson_high": result["p0_wilson_95"][1]})
    with (directory / "experiments.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (directory / "experiments.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(records)} circuit runs to {directory}")


if __name__ == "__main__":
    main()
