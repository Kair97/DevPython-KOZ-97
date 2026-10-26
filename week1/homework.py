import sys
from pathlib import Path
import argparse
import csv 

parser = argparse.ArgumentParser(prog="tool", description="...")
parser.add_argument("path", type=Path, help="input file")
parser.add_argument("--top", type=int, default=10)
args = parser.parse_args()


def topk( n: int) -> list:
    
    


def main() -> None:

    file = args.path

    if file.suffix.lower() != ".csv":
        sys.exit(1) 

    with open(file, encoding="utf-8", newline="") as f:
        fieldnames=['date', 'category', 'amount', 'description', 'payment_method', 'city', 'is_reccuring']
        reader = csv.DictReader(f, fieldnames=fieldnames)
        print(reader)
    

    return None

if __name__ == "__main__":
    main()