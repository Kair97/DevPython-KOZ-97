from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable
import itertools
from enum import Enum
from datetime import datetime, timezone, timedelta 
from abc import ABC, abstractmethod

id_gen_l = itertools.count(1)
id_gen_b = itertools.count(1)

class Status(Enum):
    AVAILABLE = "Available"
    BORROWED = "Borrowed"


class LibraryError(Exception):
    pass

class BookNotAvailable(LibraryError):
    pass 




@dataclass
class Book:
    book_id: int = field(default_factory=lambda: next(id_gen_b), init=False)
    name: str
    genre: str 
    author: str = "Unknown"
    status: Status = Status.AVAILABLE

    def borrow(self) -> None:
        if self.status is Status.BORROWED:
            raise BookNotAvailable("This book is alreay borrowed ")

        self.status = Status.BORROWED

    def return_item(self) -> None:  
        self.status = Status.AVAILABLE

    def get_info(self) -> None:
            print(f"Book name: {self.name} --- Genre: {self.genre} --- Author: {self.author} --- Status: {self.status}")
    

@dataclass
class Loan:
    book_id: int 
    reader_id: int 
    is_returned: bool = False 
    loan_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))



id_gen_r = itertools.count(1)

@dataclass
class Reader:
    reader_id: int = field(default_factory=lambda: next(id_gen_r), init=False)
    name: str | None = None    

    def __post_init__(self) -> None:
        if self.name is None: 
            self.name = f"Reader_{self.reader_id}"

@dataclass
class Library:
    library_id: int = field(default_factory=lambda: next(id_gen_l), init=False)
    books: list[Book] = field(default_factory=list)
    readers: list[Reader] = field(default_factory=list)
    loans: list[Loan] = field(default_factory=list)

    def add_book(self, book: Book) -> None:
        self.books.append(book)

    def add_reader(self, reader: Reader) -> None:
        self.readers.append(reader)


    def lend_book(self, book: Book, reader: Reader) -> Loan:

        if book not in self.books:
            raise LibraryError("This book deosn't exist in our library")

        if reader not in self.readers:
            raise LibraryError("This reader doesn't exist in our library")
        
        book.borrow()

        loan = Loan(book.book_id, reader.reader_id) 
        self.loans.append(loan)

        return loan

    def return_book(self, book:Book) -> None:

        if book not in self.books:
            raise LibraryError("This book deosn't exist in our library")

        for loan in self.loans:
            if loan.book_id == book.book_id and not loan.is_returned:
                book.return_item()
                loan.is_returned = True 
                return 

        raise LibraryError("This book is not borrowed")


    def find_book(self, book_id: int) -> Book:
        for book in self.books:
            if book.book_id == book_id:
                return book

        raise LibraryError(f"The book with id: {book_id} not found")

    def find_reader(self, reader_id: int) -> Reader:
        for reader in self.readers:
            if reader.reader_id == reader_id:
                return reader 

        raise LibraryError(f"The reader with id: {reader_id} not found")

    def get_available_books(self) -> list[Book]:
        available_books = []

        for book in self.books:
            if book.status == Status.AVAILABLE:
                available_books.append(book)
                
        return available_books
        

    def get_info(self) -> None:
        
        for book in self.books:     
            print(f"Book name: {book.name} --- Genre: {book.genre} --- Author: {book.author} --- Status: {book.status}")