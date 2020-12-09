# Big thanks to Johnny Bui for providing the base version of this file

# IMPORTS
import pickle
import requests
from enum import Enum
from typing import List, Union, Dict
from shared_constants import *

# TANGERINE = PLAYER 1
# LAVENDER = PLAYER 2

# CLASSES
class TimeControl(Enum):
    REGULAR = 1
    BLITZ = 2

class GameStatus(Enum):
    QUEUED = 0
    RUNNING = 1
    DONE = 2

class Move:
    def __init__(self, move: str, score: str, depth: str):
        self.move = move
        self.score = score
        self.depth = depth
    
    def __repr__(self):
        return f"Move({self.move}, {self.score}, {self.depth})"

class BestMove:
    def __init__(self):
        # maps move string to frequency
        self.frequency = {}
    
    def add_move(self, move: Move):
        """ Add moves that result in a win """
        self.frequency[move.move] = self.frequency.get(move.move, 0) + 1

    def get_most_freq_move(self):
        """ Find most common move that led to a win """
        best_move = max(self.frequency, key=self.frequency.get)
        return best_move

class Recording:
    def __init__(self, tangerine_moves: List[Move], lavender_moves: List[Move]):
        self.tangerine_moves = tangerine_moves
        self.lavender_moves = lavender_moves

        # combine recordings
        self.combined = []
        total_moves = len(tangerine_moves) + len(lavender_moves)
        for idx in range(total_moves // 2):
            self.combined.append(tangerine_moves[idx])
            self.combined.append(lavender_moves[idx])
        self.combined.extend(tangerine_moves[total_moves // 2:])
        self.combined.extend(lavender_moves[total_moves // 2:])

        assert(len(self.combined) == total_moves)
    
    def get_combined_moves(self) -> List[Move]:
        return self.combined

class Game:
    def __init__(self, gameid: int, team1: str, team2: str, score1: int, score2: int, timecontrol: Union[str, TimeControl], status: GameStatus):
        # parse time control
        if isinstance(timecontrol, TimeControl):
            self.timecontrol = timecontrol
        else:
            if timecontrol == "Scrim Match (Blitz)":
                self.timecontrol = TimeControl.BLITZ
            elif timecontrol == "Scrim Match (Regular)":
                self.timecontrol = TimeControl.REGULAR
            else:
                raise ValueError("Invalid timecontrol value.")

        self.gameid = int(gameid)
        self.team1 = team1
        self.team2 = team2
        self.score1 = score1
        self.score2 = score2
        self.status = status

        self.recording = None

    def __repr__(self):
        return f"Game({self.gameid}, {self.team1}, {self.team2}, {self.score1}, {self.score2}, {self.timecontrol}, {self.status})"

    def fetch_recording(self):
        # fetch tangerine moves
        TANGERINE_MOVE_URL = f"http://scrimmage.csail.mit.edu/log?gameid={self.gameid}&player=1&short=1&replay_game_iter=-1"
        tangerine_r = requests.get(TANGERINE_MOVE_URL)

        # fetch lavender moves
        LAVENDER_MOVE_URL = f"http://scrimmage.csail.mit.edu/log?gameid={self.gameid}&player=2&short=1&replay_game_iter=-1"
        lavender_r = requests.get(LAVENDER_MOVE_URL)

        # parse recording
        tangerine_moves = parse_recording(tangerine_r.text)
        lavender_moves = parse_recording(lavender_r.text)

        self.recording = Recording(tangerine_moves, lavender_moves)
        
    def get_recording(self) -> Recording:
        """
        Returns the game's Recording object
        """
        return self.recording

    def is_draw(self) -> bool:
        return self.score1 == self.score2

class Competition:
    def __init__(self):
        self.games: Dict[int, Game] = {} # maps gameid to game
    
    def get_game(self, gameid: int):
        return self.games.get(gameid, None)

    def game_exists(self, gameid: int) -> bool:
        return gameid in self.games
    
    def set_game(self, game: Game):
        self.games[game.gameid] = game

    def get_game_list(self):
        return self.games.values()

    def get_num_games(self):
        return len(self.games)

def parse_recording(recording: str) -> List[Move]:
    """
    Given a recording, parse it and return a list of Move objects
    """
    moves = []
    for move_str in recording.split("\n"):
        if len(move_str) == 0:
            continue
        if move_str.count(" ") > 1: # someone's doing something weird
            # bestmove c1L 463121|2|6
            pre_data = move_str.replace(" ", "|").split("|")
            metadata = [pre_data[1], pre_data[3], pre_data[4]]
        else: # this is normal
            # bestmove b6c7|-7|18
            metadata = move_str.split(" ")[1].split("|")
        move = Move(metadata[0], metadata[1], metadata[2])
        moves.append(move)
    
    return moves

if __name__ == "__main__":
    # attempt to load from pickle file, or create new competition
    with open(SCRIMMAGE_PICKLE_FILENAME, "rb") as f:
        competition = pickle.load(f)

    for game in competition.get_game_list():
        print(f"{game.team1} vs. {game.team2}")
        # score
        print(game.get_recording().get_combined_moves())
        break