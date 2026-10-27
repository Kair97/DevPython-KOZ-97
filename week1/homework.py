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
        print(reader.fieldnames)
        return list(reader)


def parse_row(row: dict[str, str], line: int) -> Expense:
    try:
        d = date.fromisoformat(row['date'])
        cat = row['category'].strip()
        amount = float(row['amount'])
    except(ValueError, KeyError, TypeError):
        raise InputError(f"строка {line}: неверные данные")    

    if amount <= 0:
        raise InputError(f"строка {line}: amount нижу нуля")

    return (d, cat, amount)

# def run_menu(expenses: list[Expense]) -> None:
#      while True:
#         print("1) By category\n2) By month\n3) Top N\n0) Exit")
#         choice = input("> ").strip()
#         if choice == "1":
            
#         elif choice == "2":

#         elif choice == "0":
#             break
#         else:
#             print("Unknown option")




# def print_report(expenses: list[Expense]) -> None:

#     return None 
    


def main() -> None:

    args = parse_args()
    file_path = args.path

    rows = read_rows(file_path)
    print(rows[0])

    print(parse_row(rows[1], 1))

    # if args.interactive:
    #     run_menu(expenses)
    # else:
    #     print_report(expenses)
    # return 0
    
    

    return None

if __name__ == "__main__":
    main()