# Parses game metadata using beautiful soup

# IMPORTS
from lookup import *
from bs4 import BeautifulSoup
from urllib.request import urlopen

# Game (object)
#     def __init__(self, gameid: int, team1: str, team2: str, score1: int, score2: int, timecontrol: Union[str, TimeControl], status: GameStatus):

def parse_autotest_games(url, timecontrol):
    # parses all game data from given url

    # extract html with all game metadata from url
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    game_list = soup.find("div", {"id": "game_list"})\
                    .find("div", {"style": "width:490px; text-align:left; position:relative; margin-left:auto; margin-right:0px; height:360px; overflow-y:scroll; overflow-x:hidden;"})
    competition = Competition()

    record = Record()

    # parse all games
    for count, game in enumerate(game_list.find_all("div", recursive=False)):
        info = game.find_all("div")
        # extract game id
        game_id = int(info[1].text.strip())

        # extract team names
        teams = info[2].text.strip().split()
        team1 = teams[0]
        team2 = teams[2]

        # extract status
        status = GameStatus[info[3].text.strip().upper()]

        # skip non-complete games
        if status != GameStatus.DONE:
            continue

        # extract scores
        scores = [s for s in info[4].text.strip()]
        if len(scores) > 3:
            # set both team's scores to 0 if draw
            score1 = 0
            score2 = 0
        else:
            # otherwise record score normally
            score1 = int(scores[0])
            score2 = int(scores[2])

        # fetch recording of  the game & add game to competition
        game = Game(game_id, team1, team2, score1, score2, timecontrol, status)

        # add game's result to the record
        record.add_game(game)

        game.fetch_recording()
        competition.set_game(game)

    record.print_stats()

    return competition

def main():
    competition = parse_autotest_games(AUTOTEST_URL, TIMECONTROL)
    print("Num games:", competition.get_num_games())
    print("Filename: ", GAMES_PICKLE_FILENAME)

    with open(GAMES_PICKLE_FILENAME, 'wb') as f:
        pickle.dump(competition, f)

    print("Successfully parsed games from:", AUTOTEST_URL)

if __name__ ==  "__main__":
    main()


