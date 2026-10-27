import sys
from pathlib import Path
import argparse
import csv 
from datetime import date
from collections.abc import Callable
import math

Expense = tuple[date, str, float]

class InputError(Exception):
     pass

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="tool", description="...")
    parser.add_argument("path", type=Path, help="input file")
    parser.add_argument("--report", choices=["category", "month", "year"], default="category", help="Type of report")
    parser.add_argument("--min", type=float, default=None, help='Показать суммы не меньше чем n')
    parser.add_argument("--max", type=float, default=None, help='Показать суммы не больше чем n')
    parser.add_argument("--year", type=int, default=None, help='Показать только этот год')
    args = parser.parse_args() 
    return args


def read_rows(path: Path) -> list[dict[str, str]]:

    if path.suffix.lower() != ".csv":
        raise InputError("нужен файл .csv")

    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def parse_row(row: dict[str, str], line: int) -> Expense:
    try:
        d = date.fromisoformat(row['date'])
        cat = row['category'].strip()
        amount = float(row['amount'])
    except(ValueError, KeyError, TypeError):
        raise InputError(f"строка {line}: неверные данные")    

    if not math.isfinite(amount) or amount <= 0:
        raise InputError(f"строка {line}: сумма должна быть больше 0")

    return (d, cat, amount)

def load_expenses(rows: list[dict[str, str]]) -> list[Expense]:

    if not rows:
        raise InputError("Файл пустой")

    return [parse_row(row, i) for i, row in enumerate(rows, start = 2)]



def category_of(e: Expense) -> str:
    return e[1]

def month_of(e: Expense) -> str:
    return e[0].strftime("%Y-%m")

def year_of(e: Expense) -> str:
    return e[0].strftime("%Y")

def group_sum(expenses: list[Expense], key: Callable[[Expense], str]) -> dict[str, float]:
    totals: dict[str, float] = {}

    for e in expenses:
        k = key(e)
        totals[k] = totals.get(k, 0.0) + e[2]

    return totals


def make_range_filter(low: float | None, high: float | None,) -> Callable[[float], bool]:
    def check(total: float) -> bool:
        if low is not None and total < low:
            return False
        if high is not None and total > high:
            return False
        
        return True 
    return check


def format_totals(title: str, totals: dict[str, float]) -> str | None:

    if not totals:
        return None

    lines = [f"{k}: {v:.2f}" for k, v in sorted(totals.items())]
    return title + "\n" + "\n".join(lines)
    
def apply_filter(totals: dict[str, str], keep: Callable[[float], bool]) -> dict[str, float]:

    filtered = {k: v for k, v in totals.items() if keep(v)}

    return filtered 

def print_report(expenses: list[Expense], keep: Callable[[float], bool]) -> None:
    if not expenses:
        print("Нет данных")
        return

    categories = {category_of(e) for e in expenses}
    print(f"Уникальных категорий: {len(categories)}")
    print()

    by_cat = format_totals("По категориям:", apply_filter(group_sum(expenses, category_of), keep))
    by_month = format_totals("По месяцам:", apply_filter(group_sum(expenses, month_of), keep))
    by_year = format_totals("По годам:", apply_filter(group_sum(expenses, year_of), keep))

    if by_cat is not None:
        print(by_cat)
        print()
    if by_month is not None:
        print(by_month)
        print()
    if by_year is not None:
        print(by_year)
    if not by_month and not by_year and not by_cat:
        print("Нет данных")
    


def main() -> int:
    args = parse_args()
    keep = make_range_filter(args.min, args.max)
    try:
        expenses = load_expenses(read_rows(args.path))
    except InputError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print("Ошибка: файл не в кодировке UTF-8", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"Ошибка: не удалось прочитать файл ({e.strerror})", file=sys.stderr)
        return 1

    if args.year is not None:
        expenses = [e for e in expenses if e[0].year == args.year]

    print_report(expenses, keep)
    return 0

if __name__ == "__main__":
    sys.exit(main())