"""Command-line entry point, requiring no third-party packages."""

import argparse
import json

from quantum import BASES, STATES, experiment, parse_gates


def main():
    parser = argparse.ArgumentParser(description="Explore one qubit. Gates run left to right.")
    parser.add_argument("--gates", default="H Z", help='Quoted sequence, e.g. "H Z"; empty means no gates.')
    parser.add_argument("--initial", choices=STATES, default="0")
    parser.add_argument("--basis", choices=BASES, default="X")
    parser.add_argument("--shots", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=1806)
    args = parser.parse_args()
    try:
        result = experiment(parse_gates(args.gates), args.initial, args.basis, args.shots, args.seed)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
