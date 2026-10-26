import sys
from pathlib import Path
import argparse
import csv 
from datetime import date


Expense = tuple[date, str, float]

class InputError(Exception):
     pass

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="tool", description="...")
    parser.add_argument("path", type=Path, help="input file")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("-i", "--interactive", action="store_true", help="...")
    args = parser.parse_args() 
    return args


def read_rows(path: Path) -> list[dict[str, str]]:

    if path.suffix != ".csv":
        raise InputError("Incorrect type of file please enter csv file")

    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

def run_menu(expenses: list[Expense]) -> None:
    #  while True:
    #     print("1) By category\n2) By month\n3) Top N\n0) Exit")
    #     choice = input("> ").strip()
    #     if choice == "1":

    #     elif choice == "2":

    #     elif choice == "0":
    #         break
    #     else:
    #         print("Unknown option")


def print_report(expenses: list[Expense]) -> None:

    return None 
    


def main() -> None:

    args = parse_args()
    expenses = read_rows(args.path)

    if args.interactive:
        run_menu(expenses)
    else:
        print_report(expenses)
    return 0
    
    

    return None

if __name__ == "__main__":
    main()