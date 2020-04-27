

player = 0
ai = 1

players = [player, ai]

"""
Board Layout
    13 12 11 10 09 08      AI
14                     07
    01 02 03 04 05 06      Player

Hand: 00
"""

holes = {
    player : [1, 2, 3, 4, 5, 6],
    ai : [8, 9, 10, 11, 12, 13]
}

banks = {
    player: 7,
    ai: 14
}
owner = 0
next = 1
role = 2

house = 88
bank = 99

hole = {
    1: { owner : player, next : { player : 2, ai : 2}, role : house },
    2: { owner : player, next : { player : 3, ai : 3}, role : house },
    3: { owner : player, next : { player : 4, ai : 4}, role : house },
    4: { owner : player, next : { player : 5, ai : 5}, role : house },
    5: { owner : player, next : { player : 6, ai : 6}, role : house },
    6: { owner : player, next : { player : 7, ai : 7}, role : house },
    7: { owner : player, next : { player : 8, ai : 8}, role : bank },
    8: { owner : ai, next : { player : 9, ai : 9}, role : house },
    9: { owner : ai, next : { player : 10, ai : 10}, role : house },
    10: { owner : ai, next : { player : 11, ai : 11}, role : house },
    11: { owner : ai, next : { player : 12, ai : 12}, role : house },
    12: { owner : ai, next : { player : 13, ai : 13}, role : house },
    13: { owner : ai, next : { player : 1, ai : 14}, role : house },
    14: { owner : ai, next : { player : 1, ai : 1}, role : bank }
}
hand = 0
all_marbles = range(0, 14)
class kalahGame():
    def __init__(self):
        self.players = players
        self.turn = 1 #shows players turn
        self.board = [0]*15
        self.marbles_per_hole = 4
        self.board[hand] = 12*self.marbles_per_hole
        self.reset_board()

    def possible_moves(self):
        pass

    def make_move(self):
        pass

    def is_over(self):
        pass

    def show(self):
        print("player: {}".format(self.turn))
        print("hand: {}".format(self.board[hand]))
        print("board:\n")
        print("             13         12         11          10           09          08                    ")
        print("       " + " ".join(
            ["    [{:02d}]   ".format(self.board[hole]) for hole in reversed(holes[ai])]
        ))
        print(" {:02d}  [{:02d}]                                                                     [{:02d}]  {:02d}".format(banks[ai], hand, hand, banks[player]))
        print("       " + " ".join(
            ["    [{:02d}]   ".format(self.board[hole]) for hole in reversed(holes[player])]
        ))
        print("             01         02         03          04           05          06                      ")

    def score(self):
        pass

    def reset_board(self):
        for marble in all_marbles:
            if self.board[marble]:
                self._scoop(marble)

        for player in self.players:
            for hole in holes[player]:
                self._drop(hole, count = self.marbles_per_hole)

    def _scoop(self, marble):
        self.board[hand] += self.board[marble]
        self.board[marble] = 0

    def _drop(self, hole, count):
        self.board[hand] -= count
        self.board[hole] += count

if __name__ == '__main__':
    game = kalahGame()
    game.show()
