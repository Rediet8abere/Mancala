"""
This work is based on John Dupuy's YouTube tutorial
link: https://www.youtube.com/watch?v=Y6P-_sTYQcM

Board Layout
    13 12 11 10 09 08      AI
14                     07
    01 02 03 04 05 06      Player

Hand: 00

"""

player = 0
ai = 1

players = [player, ai]

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
    13: { owner : ai, next : { player : 14, ai : 14}, role : "hole", "oop": 1, "distobank":  {player: 7, ai: 1}},
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
        self.reset_board()

    def is_own_bank(self, last_hole):
        count = self.board[last_hole] % 13 #if number of marble is > 12 they go around and land in bank itself
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




    def recurse_moves(self, move_list, completed_list):
        """Utility: is_own_bank """
        for move in move_list:
            last_hole = move[-1]
            if self.is_own_bank(last_hole):
                board_copy = self.board.copy() # to restore the board
                self.make_move_choice(last_hole) # take marbles from last hole and go around to drop one
                aval_holes = self.possible_moves_choice() # next set of holes with marble/marbles
                if aval_holes:
                    next_vist = []
                    for hole in aval_holes:
                        next_vist.append(move+[hole]) # adding next available vists to exsiting ones
                    self.recurse_moves(next_vist, completed_list)
                else: # no available marbles in hole
                    completed_list.append(move)
                self.board = board_copy # restoring board
            else: #last_hole is not bank
                completed_list.append(move)


    def possible_moves_choice(self):
        possible = []
        for hole in holes[self.turn]:
            if self.board[hole]:
                possible.append(hole)
        return possible

    def minimax(self, move, depth, maximazing_player):
        """
        depth: how long is it taking me to get to a certain move
        maximazing_player: to keep track of whose turn it is in the game
        and decides moves based on that.
        """
        # evaluate who has more marbles
        # evaluate who has more moves that leads to bank and steal
        if depth == 0: #I need to account for game over
            return self.score()

        if maximazing_player:
            max_score = float('-inf')
            # play move
            self.play_move(move)
            self.turn = player
            self.opp_turn = ai
            opp_moves = self.possible_moves()
            board_copy = self.board[:]
            for op_move in opp_moves:
                eval_score = self.minimax(op_move, depth-1, False)
                self.board = board_copy[:] #restore board after evaluation
                self.turn = player #give turn to player after playing
                self.opp_turn = ai
                max_score = max(eval_score, max_score)
            return max_score

        else: # minimizing_player
            min_score = float('inf')
            self.play_move(move)
            self.turn = ai
            self.opp_turn = player
            ai_moves = self.possible_moves()
            board_copy = self.board[:]
            for ai_move in ai_moves:
                eval_score = self.minimax(ai_move, depth-1, True)
                self.board = board_copy[:] #restore board after evaluation
                self.turn = ai
                self.opp_turn = player
                min_score = min(min_score, eval_score) #we want to minimize score for player
            return min_score





    def get_move(self):
        """AI gets the best move by calling minimax function"""
        best_score = float('-inf') #a move that would result in storing as many marbles as possible in ai bank
        best_move = []
        poss_moves = self.possible_moves() #compelete list of moves
        board_copy = self.board[:]
        for move in poss_moves:
            #look for ai move that would result in best score(many marble in bank)
            ai_score = self.minimax(move, 2, True) #return score and move
            self.board = board_copy[:]
            if ai_score > best_score:
                best_move = move
                best_score = ai_score
        self.turn = ai
        return best_move



    def make_move_choice(self, hole):
        # pick all the marbles in hole
        self._scoop(hole)
        cur_hole = hole
        # drop marbles to adjacent holes
        for i in range(self.board[hand]):
            # get the next hole
            next_hole = h[cur_hole][next][self.turn]
            self._drop(next_hole, 1) #start dropping marble
            cur_hole = next_hole

        # Capture if possible               Check we are not on bank
        if self.board[cur_hole] == 1: # are we left with one marble
            if h[cur_hole][owner] == self.turn: # check turn
                if h[cur_hole][role] == hole: # check if we are on hole
                    if self.board[h[cur_hole]["oop"]]: #look for current hole's opponent
                        self._scoop(cur_hole) #take marble from current hole
                        self._scoop(h[cur_hole]["oop"]) #take marbles from opponent
                        self._drop_all(banks[self.turn])



    def play_move(self, moves):
        for move in moves:
            self.make_move_choice(move)

        if self.turn == player:
            self.turn = ai
            self.opp_turn = player
        elif self.turn == ai:
            self.turn = player
            self.opp_turn = ai

    def is_over(self):
        for player in players:
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
        #positive for if ai is lead
        return self.board[banks[self.turn]] - self.board[banks[self.opp_turn]]

    def reset_board(self):
        """ Creates a board with 4 marbles in each
            hole and 0 marble in each bank
        """
        for hole in all_holes: # for hole in the holes including bank holes
            if self.board[hole]: # check if there is/are marble/marbles in specific hole
                self._scoop(hole) # get the marble/marbles at the specific hole

        for player in self.players:
            for hole in holes[player]:
                self._drop(hole, count = self.marbles_per_hole)

    def _scoop(self, hole): #not triggered when board is reset
        self.board[hand] += self.board[hole]
        self.board[hole] = 0

    def _drop(self, hole, count): #drop 4 marbles for each hole in the board
        self.board[hand] -= count
        self.board[hole] += count

    def _drop_all(self, at_bank):
        self.board[at_bank] += self.board[hand]
        self.board[hand] = 0


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

    count = 0
    while not game.is_over():
        game.show()
        print("................................game turn........................................", game.turn)
        if game.turn == player:
            moves = game.possible_moves()
            for i, move in enumerate(moves): #no need to enumerate, show user their option and let them choose
                print(i, move)
            i = int(input("which move do you wanna play? "))
            move = moves[i]
            print("move: ", move)

        else:
            move = game.get_move()

        game.play_move(move)


    print("GAME OVER!")
    game.show()
    print("Result", ["Tie", "Player is Winner", "AI is Winner"][game.get_winner()])
