# Prints data from open book in c-format

# IMPORTS
from shared_constants import *
from lookup import *

def main():
    with open(BOOK_PICKLE_FILENAME, "rb") as f:
        book = pickle.load(f)
        book.print_book()

if __name__ == "__main__":
    main()