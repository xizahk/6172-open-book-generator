# Contains data structures used for open book

# IMPORTS
from competition import *
from typing import List, Union, Dict
from enum import IntEnum

# CLASSES
class TeamColor(IntEnum):
    TANGERINE = 0
    LAVENDER = 1

class Record():
    def __init__(self):
        self.t_wins = 0
        self.l_wins = 0
        self.draws = 0
        self.opp_wins = 0

    def print_stats(self):
        num_decided_games = self.t_wins + self.l_wins + self.opp_wins
        print("Game stats:")
        print("Tangerine wins:", self.t_wins)
        print("Lavender wins:", self.l_wins)
        print("Opponent wins:", self.opp_wins)
        print("Draws:", self.draws)
        print("Win rate:", (self.t_wins + self.l_wins) / num_decided_games)
        print("Lose rate", (self.opp_wins) / num_decided_games)

    def add_game(self, game: Game):
        if game.is_draw():
            self.draws += 1
        elif game.team1 == OPPONENT and game.score1 == 0:
            self.l_wins += 1
        elif game.team2 == OPPONENT and game.score2 == 0:
            self.t_wins += 1
        else:
            # opponent won
            self.opp_wins += 1

class TableValue:
    def __init__(self):
        # move str to number of occurrences
        self.values: Dict[str, int] = {}

    def add_value(self, value):
        self.values.setdefault(value, 1)
        self.values[value] += 1

    def get_most_freq(self):
        return sorted(self.values, key=lambda x: self.values[x]).pop()

class LookupTable:
    def __init__(self):
        # history move str to TableValue
        self.table: Dict[str, TableValue] = {}

    def get_num_keys(self):
        return len(self.table)

    def add_entry(self, key, value):
        self.table.setdefault(key, TableValue())
        self.table[key].add_value(value)

    def get_most_freq_pairs(self):
        pairs = []
        for key in self.table:
            value = self.table[key].get_most_freq()
            pairs.append((key, value))
        return pairs

    def print_table(self):
        # prints table with format: `{{move_history1, best_move1, move_history2, best_move2, ...}`
        pairs = self.get_most_freq_pairs()

        print('{', end='')
        for count, (history, mv) in enumerate(pairs):
            print(f'"{history}", "{mv}"', end="")
            if count < len(pairs) - 1:
                print(", ", end='')
        print('};')

class OpenBook:
    def __init__(self, size):
        self.tables = [LookupTable() for _ in range(size)]

    def size(self):
        return len(self.tables)

    def increase_depth(self, size):
        while len(self.tables) < size:
            self.tables.append(LookupTable())

    def add_move(self, key, value, depth):
        self.tables[depth].add_entry(key, value)

    def get_table(self, depth):
        self.tables[depth].get_most_freq_pairs()

    def add_move_with_side(self, game: Game, side: TeamColor):
        mv_history = ""
        max_depth = self.size()
        for ply, move in enumerate(game.get_recording().get_combined_moves()):
            if ply >= max_depth:
                return
            mv_str = move.move
            if ply % 2 == int(side):
                # add this move to open book since this is a TeamColor move
                self.add_move(mv_history, mv_str, ply)
            mv_history += mv_str

    def add_tangerine_moves(self, game: Game):
        self.add_move_with_side(game, TeamColor.TANGERINE)

    def add_lavender_moves(self, game: Game):
        self.add_move_with_side(game, TeamColor.LAVENDER)

    def add_game(self, game: Game, opponent: str, record: Record):
        # add game's moves to the book if the reference bot lost
        if game.is_draw():
            pass
        elif game.team1 == opponent and game.score1 == 0:
            self.add_lavender_moves(game)
        elif game.team2 == opponent and game.score2 == 0:
            self.add_tangerine_moves(game)
        record.add_game(game)

    def print_book(self):
        # prints the book in c-format for lookup.h
        size = self.size()

        # prints macro for book depth
        print(f"#define OPEN_BOOK_DEPTH {size}")

        # prints an array of each depth's size
        print(f"int lookup_sizes[OPEN_BOOK_DEPTH] = ", end="")
        print('{', end="")
        for i in range(size):
            print(self.tables[i].get_num_keys()*2, end="")
            if i < size - 1:
                print(", ", end="")
        print('};')
        print()

        # prints individual tables from each depth
        for i in range(size):
            print(f"char * lookup_table_depth_{i}[] = ", end="")
            self.tables[i].print_table()
        print()

        # prints lookup_tables that contains tables from all depths
        print("char** lookup_tables[OPEN_BOOK_DEPTH] = {")
        for i in range(size):
            print(f"  lookup_table_depth_{i}", end="")
            if i < size - 1:
                print(",")
            else:
                print()
        print("};")
