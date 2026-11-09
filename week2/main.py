from models import Book, Reader, Loan, Library, Status, LibraryError
import sys 

# Harry_Potter = Book("Harry Potter", "fantasy", "Joanne Rowling")



def main() -> None:
    library = Library()


    while (True):

        print("Welcome to my Library management system")
        print("1 --> To add a book to library")
        print("2 --> To add a reader to library")
        print("3 --> To get all available books to borrow")
        print("4 --> To borrow a book")
        print("5 --> Return borrowed book")
        print("0 --> To exit (all progress will reset)")

        inp = input("Enter: ")
        try:
            choice = int(inp)
        except ValueError:
            print("Please enter a menu number")
            continue

        match choice:
            case 1:
                print()
                print("Please enter the book details")
                name = input("Enter the name of book: ")
                genre = input("Enter the genre: ")
                author = input("Enter the name of author: ")

                book = Book(name, genre, author)
                library.add_book(book)

            case 2:
                print()
                name = input("Enter the name of reader: ")
                library.add_reader(Reader(name))
            case 3:
                print()
                books = library.get_available_books()
                if not books:
                    print("There is no available books currently")
                else:
                    print("Here is the list of available books")
                    for book in books:
                        book.get_info()
                print()
                print()
            case 5:
                print()
                try:
                    book_id = int(input("Enter the book ID to return: "))
                    book = library.find_book(book_id)
                    library.return_book(book)
                except ValueError:
                    print("Book ID must be a number")
                except LibraryError as error:
                    print(error)    
                else:
                    print("Book was returned successfully")

            case 4:
                print()
                try:
                    reader_id = int(input("Enter your reader ID: "))
                    book_id = int(input("Enter the book ID: "))

                    reader = library.find_reader(reader_id)
                    book = library.find_book(book_id)
                    library.lend_book(book, reader)
                except ValueError:
                    print("Reader ID and book ID must be numbers")
                except LibraryError as error:
                    print(error)
                else:
                    print(f"{reader.name} borrowed {book.name}")

                continue 
            case 0:
                print()
                print("GoodBye")
                return 
            case _:
                print("This option is not defined")
            



if __name__ == "__main__":
    sys.exit(main())
