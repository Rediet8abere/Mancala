

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

"""
First_move: 10, 8
                Second_move:
            10, 9
            10, 11
            10, 12
            10, 13
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
# naming issue
h = {
    1: { owner : player, next : { player : 2, ai : 2}, role : "hole", "oop": 13, "distobank":  {player: 6, ai: 12}},
    2: { owner : player, next : { player : 3, ai : 3}, role : "hole", "oop": 12, "distobank":  {player: 5, ai: 11}},
    3: { owner : player, next : { player : 4, ai : 4}, role : "hole", "oop": 11, "distobank":  {player: 4, ai: 10}},
    4: { owner : player, next : { player : 5, ai : 5}, role : "hole", "oop": 10, "distobank":  {player: 3, ai: 9}},
    5: { owner : player, next : { player : 6, ai : 6}, role : "hole", "oop": 9, "distobank":  {player: 2, ai: 8}},
    6: { owner : player, next : { player : 7, ai : 7}, role : "hole", "oop": 8, "distobank":  {player: 1, ai: 6}},
    7: { owner : player, next : { player : 8, ai : 8}, role : "bank", "oop": None, "distobank": None},
    8: { owner : ai, next : { player : 9, ai : 9}, role : "hole", "oop": 6, "distobank":  {player: 12, ai: 6}},
    9: { owner : ai, next : { player : 10, ai : 10}, role : "hole", "oop": 5, "distobank":  {player: 11, ai: 5}},
    10: { owner : ai, next : { player : 11, ai : 11}, role : "hole", "oop": 4, "distobank":  {player: 10, ai: 4}},
    11: { owner : ai, next : { player : 12, ai : 12}, role : "hole", "oop": 3, "distobank":  {player: 9, ai: 3}},
    12: { owner : ai, next : { player : 13, ai : 13}, role : "hole", "oop": 2, "distobank":  {player: 8, ai: 2}},
    13: { owner : ai, next : { player : 1, ai : 14}, role : "hole", "oop": 1, "distobank":  {player: 7, ai: 1}},
    14: { owner : ai, next : { player : 1, ai : 1}, role : "bank", "oop": None, "distobank": None }
}

hand = 0
all_holes = range(1, 15)
class kalahGame():
    def __init__(self, players):
        self.players = players
        self.turn = player #shows players turn
        self.opp_turn = ai
        self.board = [0]*15 # index 0 holds all the marbles at first
        # print("self.board in init: ", len(self.board))
        self.marbles_per_hole = 4
        self.board[hand] = 12*self.marbles_per_hole
        print("starting over")
        self.show()
        self.reset_board()

    def is_own_bank(self, last_hole):
        #num of marble in this hole
        # print("in is_own_bank: ", last_hole)
        # print("self.board[last_hole]: ", self.board[last_hole])
        count = self.board[last_hole] % 13 #if number of marble is > 12 they go around and land in bank itself
        # print("count: ", count)
        # print("h: ", h[last_hole]["distobank"][self.turn])
        return count == h[last_hole]["distobank"][self.turn]

    def possible_moves(self):
        move_list = [[hole] for hole in self.possible_moves_choice()] # list of list
        # print("move_list: ", move_list)
        completed_list = []
        self.recurse_moves(move_list, completed_list)
        # print("completed_list: ", completed_list)
        return completed_list

    def make_move(self, move):
        for hole in move:
            return sef.make_move_choice(hole)



    "Is steal possible "

    def recurse_moves(self, move_list, completed_list):
        """Utility: is_own_bank """
        for move in move_list:
            last_hole = move[-1]
            # print("last_hole: ", last_hole)
            if self.is_own_bank(last_hole):
                # print("should not get here")
                board_copy = self.board.copy() # to restore the board
                self.make_move_choice(last_hole) # take marbles from last hole and go around to drop one
                aval_holes = self.possible_moves_choice() # next set of holes with marble/marbles
                if aval_holes:
                    next_vist = []
                    for hole in aval_holes:
                        next_vist.append(move+[hole]) # adding next available vists to exsiting ones
                    # print("next visit: ", next_vist)
                    self.recurse_moves(next_vist, completed_list)
                    # print("done!")
                else: # no available marbles in hole
                    completed_list.append(move)
                self.board = board_copy #not sure the need of restoring, if aval_holes is not triggered board will not be modified
            else: #last_hole is not bank
                completed_list.append(move)
                # print("completed_list: ", completed_list)


    def possible_moves_choice(self):
        possible = []
        for hole in holes[self.turn]:
            if self.board[hole]:
                possible.append(hole)

        # print("possible: ", possible)
        return possible

    def minimax(self, move, depth, maximazing_player):
        """
        depth: how long is it taking me to get to a certain move
        maximazing_player: to keep track of whose turn it is in the game
        and decides moves based on that.

        # http://people.cs.uchicago.edu/~jagolbec/cspp513/mancala.html

        # https://towardsdatascience.com/how-a-chess-playing-computer-thinks-about-its-next-move-8f028bd0e7b1
        Utility: holes with marbles and where those marbles are located,
                how close are we to winning, position of opponent

        Q/C: we are calculating our ai's move based on player's best moves
            : do we calcuate ai's move based on players action or do we assume
            user makes the best move they can make and calcuate the move store it
            and let ai play based on that?
        """
        """
        Assumptions: we go as far as we can and look at the counts of marbles in players and
                     ai's count
        """
        """
        for loop plays game subsequently which might not be the case when player plays the game
        """
        # evaluate who has more marbles
        # evaluate who has more moves that leads to bank and steal
        if depth == 0: #I need to account for game over
            self.play_move(move)
            print("opp_turn: ", self.opp_turn, "move: ", move)
            self.show()
            return self.board[banks[self.opp_turn]] #return current opponent's score

        if maximazing_player:
            max_score = float('-inf')
            # play move
            print("move in maximazing_player: ", move)
            self.play_move(move)
            print("###############board state after playing move#################")
            self.show()
            # now turn is opponent's
            # max_score = banks[self.opp_turn] #ai now have opp_turn after playing move
            # 0, 1
            opp_moves = self.possible_moves()
            print("opp_moves in maximazing_player: ", opp_moves, "depth: ", depth)
            board_copy = self.board[:]
            for op_move in opp_moves:
                eval = self.minimax(op_move, depth-1, False) #c
                self.board = board_copy[:]
                self.turn = player
                self.opp_turn = ai
                print("eval: ", eval)
                max_score = max(eval, max_score)
            return max_score

        else: # minimizing_player
            min_score = float('inf') #we wnat worst score for player
            # play move
            print("move in minimizing_player: ", move)
            print("************before playing ^ move************************")
            self.show()
            self.play_move(move)
            print("###############board state after playing move#################")
            self.show()
            # now turn is opponent's
            # min_score = banks[self.opp_turn] #opponent now have opp_turn
            #depth: 5
            # 2, 3
            # I need to recover board
            print("should be ai's turn: ", self.turn)
            ai_moves = self.possible_moves()
            print("ai_moves in minimizing_player: ", ai_moves, "depth: ", depth)
            board_copy = self.board[:]
            for ai_move in ai_moves:
                eval = self.minimax(ai_move, depth-1, True) #c
                self.board = board_copy[:]
                self.turn = ai
                self.opp_turn = player
                print("eval: ", eval)
                min_score = min(min_score, eval)
            return min_score





    def get_move(self):
        best_score = 0 #a move that would result in storing as many marbles as possible in ai bank
        best_move = []
        # print("ai getting move")
        poss_moves = self.possible_moves() #compelete list of moves
        print("poss_moves: ", poss_moves)
        print("**********current state***********")
        self.show()
        board_copy = self.board
        for move in poss_moves:
            #look for ai move that would result in best score(many marble in bank)
            ai_score = self.minimax(move, 2, True) #return score and move
            # compare score and replace move based on score
            print("-----------------after minmax excepecting my board to be alterd------------------")
            self.show()
            self.board = board_copy
            print("-----------------I restored my board----------------------")
            print(self.show())
            print("ai_score", ai_score, "best_score: ", best_score)
            print("best_move: ", best_move, "move: ", move)
            break
            if ai_score > best_score:
                best_move = move
                best_score = ai_score

        print("**********current state after choosing the best move***********")
        self.show()
        return
        return best_move



    def make_move_choice(self, hole):
        # pick all the marbles in hole
        self._scoop(hole)
        cur_hole = hole
        # print("cur_hole: ", cur_hole)
        # drop marbles to adjacent holes
        for i in range(self.board[hand]):
            # get the next hole
            next_hole = h[cur_hole][next][self.turn]
            self._drop(next_hole, 1) #start dropping marble
            cur_hole = next_hole

        # Capture if possible               Check we are not on bank
        if self.board[cur_hole] == 1 and cur_hole != (banks[player] or banks[ai]): # are we left with one marble
            if h[cur_hole][owner] == self.turn: # check turn
                if h[cur_hole][role] == hole: # check if we are on hole
                    if self.board[h[cur_hole][oop]]: #look for current hole's opponent
                        self._scoop(cur_hole) #take marble from current hole
                        self._scoop(h[cur_hole][oop]) #take marbles from opponent
                        self._drop_all(banks[self.turn])



    def play_move(self, moves):
        # print("about to play move: ", moves)
        for move in moves:
            self.make_move_choice(move)
        # print("Played!!")
        if self.turn == player:
            self.turn = ai
            self.opp_turn = player
        else: #self.turn == 0
            self.turn = player
            self.opp_turn = ai
        # print("self.turn: ", self.turn, "self.opp_turn: ", self.opp_turn)
        # if cur_hole == banks[players[self.turn]]:
        #
        #     print("who's turn: ", cur_hole)
        # print("self.turn: ", self.turn)

    def is_over(self):
        for player in players:
            # print("player in is over: ", player, "holes player: ", holes[player])
            has_marbles = False
            for hole in holes[player]:
                if self.board[hole]:
                    has_marbles = True
            if has_marbles is False:
                return True
        return False

    def show(self):
        print("player: {} score: {}".format(self.turn, self.score()))
        print("hand: {}".format(self.board[hand]))
        print("board:\n")
        print("             13         12         11          10           09          08                    ")
        print("       " + " ".join(
            ["    [{:02d}]   ".format(self.board[hole]) for hole in reversed(holes[ai])]
        ))
        print(" {:02d}  [{:02d}]                                                                     [{:02d}]  {:02d}".format(
            banks[ai], self.board[banks[ai]], self.board[banks[player]], banks[player]
        ))
        print("       " + " ".join(
            ["    [{:02d}]   ".format(self.board[hole]) for hole in holes[player]]
        ))
        print("             01         02         03          04           05          06                      ")

    def score(self, playing=None):
        if playing == None:
            playing = self.turn
        if playing == ai:
            self.turn = ai
            self.opp_turn = player
        else:
            self.turn = player
            self.opp_turn = ai
        return self.board[banks[self.turn]] - self.board[banks[self.opp_turn]]

    def reset_board(self):
        """ Creates a boad with 4 marbles in each
            hole and 0 marble in each bank
        """
        # print("board: ", self.board)
        for hole in all_holes: # for hole in the holes including bank holes
            # print("hole: ", hole)
            if self.board[hole]: # check if there is/are marble/marbles in specific hole
                self._scoop(hole) # get the marble/marbles at the specific hole

        for player in self.players:
            for hole in holes[player]:
                self._drop(hole, count = self.marbles_per_hole)

    def _scoop(self, hole): #not triggered when board is reset
        # print("hole: ", hole)
        self.board[hand] += self.board[hole]
        self.board[hole] = 0

    def _drop(self, hole, count): #drop 4 marbles for each hole in the board
        self.board[hand] -= count
        self.board[hole] += count

    def _drop_all(self, at_bank):
        self.board[at_bank] += self.board[hand]
        self.board[hand] = 0

    # def prompt(self):
        # play = int(input("what do you wanna play? "))
        # self.make_move(play)
        # game.show()

    def get_winner(self):
        player_score = self.score(playing=player)
        ai_score = self.score(playing=ai)
        if player_score > ai_score:
            return 1
        elif player_score < ai_score:
            return 2
        else: #player_score == ai_score
            return 0


if __name__ == '__main__':
    game = kalahGame(players)
    # game.possible_moves_choice()

    while not game.is_over():
        game.show()
        if game.turn == player:
            # moves = game.possible_moves_choice()
            moves = game.possible_moves()
            # print("moves: ", moves)
            # for i, move in enumerate(moves):
            #     print(i, move)
            # break
            for i, move in enumerate(moves): #no need to enumerate, show user their option and let them choose
                print(i, move)
            i = int(input("which move do you wanna play? "))
            move = moves[i]
            print("move: ", move)
            # print("moves available: ", moves)
            # print("move to be played: ", move)

        else:
            move = game.get_move()
            print("AI move: ", move)
            game.show()

        game.play_move(move)

    print("GAME OVER!")
    game.show()
    print("Result", ["Tie", "Player is Winner", "AI is Winner"][game.get_winner()])



    """
[ [8]
, [9]




, [10, 8]
, [10, 9]
, [10, 11, 8]
, [10, 11, 9]
, [10, 11, 12]
, [10, 11, 13]
, [10, 12, 8]
, [10, 12, 9]
, [10, 12, 11, 8]
, [10, 12, 11, 9]
, [10, 12, 11, 12]
, [10, 12, 11, 13]
, [10, 12, 13]
, [10, 13]





, [11], [12], [13, 8], [13, 9], [13, 10, 8], [13, 10, 9], [13, 10, 11, 8], [13
, 10, 11, 9], [13, 10, 11, 12], [13, 10, 11, 13], [13, 10, 12, 8], [13, 10, 12, 9], [13, 10, 12, 11, 8], [13, 10, 12, 11, 9], [13, 10, 12, 11, 12]
, [13, 10, 12, 11, 13], [13, 10, 12, 13], [13, 10, 13, 8], [13, 10, 13, 9], [13, 10, 13, 11, 8], [13, 10, 13, 11, 9], [13, 10, 13, 11, 12], [13, 1
0, 13, 11, 13, 8], [13, 10, 13, 11, 13, 9], [13, 10, 13, 11, 13, 12], [13, 10, 13, 12, 8], [13, 10, 13, 12, 9], [13, 10, 13, 12, 11, 8], [13, 10,
13, 12, 11, 9], [13, 10, 13, 12, 11, 12], [13, 10, 13, 12, 11, 13], [13, 10, 13, 12, 13, 8], [13, 10, 13, 12, 13, 9], [13, 10, 13, 12, 13, 11, 8],
 [13, 10, 13, 12, 13, 11, 9], [13, 10, 13, 12, 13, 11, 12], [13, 10, 13, 12, 13, 11, 13, 8], [13, 10, 13, 12, 13, 11, 13, 9], [13, 10, 13, 12, 13,
 11, 13, 12], [13, 11], [13, 12]]
    """

"""
0 [2]
1 [4, 1]
2 [4, 2]
3 [4, 3]
4 [4, 4]
5 [4, 5, 1]
6 [4, 5, 2]
7 [4, 5, 3]
8 [4, 5, 4]
9 [4, 5, 6]
10 [4, 6]
11 [6, 2]
12 [6, 4, 1]
13 [6, 4, 2]
14 [6, 4, 3]
15 [6, 4, 4]
16 [6, 4, 5, 1]
17 [6, 4, 5, 2]
18 [6, 4, 5, 3]
19 [6, 4, 5, 4]
20 [6, 4, 5, 6]
21 [6, 4, 6]
"""
