# Adds parsed game data to open book

# IMPORTS
from lookup import *
from shared_constants import *

def create_book(size: int):
    # creates and saves a new open book of given size
    book = OpenBook(size)
    with open(BOOK_PICKLE_FILENAME, 'wb') as f:
        pickle.dump(book, f)

def process_games():
    open_book = None
    record = Record()

    # attempt to load from pickle file, or create new competition
    with open(GAMES_PICKLE_FILENAME, "rb") as games_f, open(BOOK_PICKLE_FILENAME, "rb") as book_f:
        competition = pickle.load(games_f)
        open_book = pickle.load(book_f)

    for game in competition.get_game_list():
        open_book.add_game(game, OPPONENT, record)

    with open(BOOK_PICKLE_FILENAME, "wb") as book_f:
        pickle.dump(open_book, book_f)

    print("Successfully added games from:", GAMES_PICKLE_FILENAME)
    record.print_stats()

if __name__ == "__main__":
    # creates a new book; uncomment if needed
    # create_book(15)

    # opens the pre-existing open book and updates it with games from GAMES_PICKLE_FILENAME
    process_games()
