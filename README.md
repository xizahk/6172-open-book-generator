# Purpose
This collection of files generates open book data by parsing autotest game data using BeautifulSoup and compiling moves from winning games into the book. Big thanks to Johnny Bui for providing the code for `competition.py`!

# Setup
1) Provide URL of autotests to `AUTOTEST_URL`
2) Enter name of opponent bot (most likely a reference bot) for `OPPONENT`

# To use
1) If this is your first time running this generator or if you'd like to reset your open book, uncomment the call to `create_book()` in the main function of `process_games.py`
2) Run `parse_autotest_games.py` to parse games from given url
3) Run `process_games.py` to add parsed games to open book
4) Run `print_book.py` to print the open book in c-format for lookup.h
