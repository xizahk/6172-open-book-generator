# directory of pickle files
PICKLE_DIR = "./pickle/"

# pickle file of scrimmage data
SCRIMMAGE_PICKLE_FILENAME = PICKLE_DIR + "competition.pkl"

# pickle file of open book
BOOK_PICKLE_FILENAME = PICKLE_DIR + "openbook.pkl"

# name of opponent bot (e.g. "reference_plusx4")
OPPONENT = "<Opponent name>"

# url of autotest games to pull from (e.g. "http://scrimmage.csail.mit.edu/autotest?autoid=xxxx")
AUTOTEST_URL = "<Autotest url>"

# pickle file of games to process
GAMES_PICKLE_FILENAME = PICKLE_DIR + f"autotest_{AUTOTEST_URL[-4:]}.pkl"

# default time control of scrimmages
TIMECONTROL = "Scrim Match (Regular)"
