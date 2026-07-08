import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

        # Utility values of different features

        # continous pieces
        p_two_c = 1
        p_three = 10
        p_four = 100000
        # discontinuous piece
        p_two = 0.5
        
        # continous pieces
        o_two_c = -1.2            # higher in magnitude than p_two_c as a defensive strategy.
        o_three = -15             # higher penalty as one more move of opponent can result in losing.
        o_four = -100000          # highest penalty of losing the game.
        # discontinuous piece
        o_two = -0.75             # higher in magnitude than ptwo as a defensive strategy.

        p = self.player_number
        o = p ^ 1 ^ 2        

        # Define all possible valid window combinations
        self.d = {
             (p,p,p,p) : p_four,
             (p,p,p,0) : p_three,
             (0,p,p,p) : p_three,
             (p,0,p,p) : p_three,
             (p,p,0,p) : p_three,
             (0,0,p,p) : p_two_c,
             (p,p,0,0) : p_two_c,
             (0,p,p,0) : p_two_c,
             (p,0,p,0) : p_two,
             (0,p,0,p) : p_two,
             (p,0,0,p) : p_two,
             (o,o,o,o) : o_four,
             (o,o,o,0) : o_three,
             (0,o,o,o) : o_three,
             (o,0,o,o) : o_three,
             (o,o,0,o) : o_three,
             (0,0,o,o) : o_two_c,
             (o,o,0,0) : o_two_c,
             (0,o,o,0) : o_two_c,
             (o,0,o,0) : o_two,
             (0,o,0,o) : o_two,
             (o,0,0,o) : o_two}

    def actions(self, board):
        """
        Returns the set of unoccupied spaces as a list of tuples (row, col)
        """
        actions = []

        for j in range(len(board[0])):
            for i in range(len(board) - 1, -1, -1):
                # Add the first unoccupied space from bottom
                if board[i][j] == 0:
                    actions.append((i,j))
                    break
        return actions

    def cutoff_test(self, board, depth, maxdepth):
        """
        Returns True if depth reaches maxdepth else False, 
        along with utility value

        Args:
            board : current state of game
            depth : current depth
            maxdepth : maximum depth
        """

        v = self.evaluation_function(board)

        if depth > maxdepth: return True, v

        # If utility has an absolute value greater than 90000, return True
        # Using 90000 instead of 100000 because the board might have other configurations that can lower the score.
        if v >= 90000 or v <= -90000: return True, v

        if not self.actions(board):
            return True, v

        return False, v

    def max_value(self, board, alpha, beta, depth, maxdepth):
        """
        Returns utility value.
        
        Args: 
            board : state of game
            alpha : upper bound on utility
            beta  : lower bound on utility
            maxdepth : maximum depth
        """

        # If either player 1 or player 2 are in terminal state, return utility value
        test, val = self.cutoff_test(board, depth, maxdepth)
        if test :
            return val

        v = - float("inf")

        for a in self.actions(board):
            # Implement the change due to action a on board
            board[a[0]][a[1]] = self.player_number
            min_res = self.min_value(board, alpha, beta, depth + 1, maxdepth)
            # Reverse the change
            board[a[0]][a[1]] = 0

            v = max(v, min_res)

            # if v >= beta, we can prune that subtree as its no longer useful. Thus return
            if v >= beta: return v

            # Update alpha
            alpha = max(alpha, v)

        return v

    def min_value(self, board, alpha, beta, depth, maxdepth):
        """
        Returns utility value.
        
        Args: 
            board : state of game
            alpha : upper bound on utility
            beta  : lower bound on utility
            depth : depth of search
            maxdepth : maximum depth
        """

        # If either player 1 or player 2 are in terminal state, return utility value
        test, val = self.cutoff_test(board, depth, maxdepth)
        if test :
            return val

        v = float("inf")
       
        opp = self.player_number ^ 1 ^ 2

        for a in self.actions(board):
            # Implement the change due to action a on board
            board[a[0]][a[1]] = opp
            max_res = self.max_value(board, alpha, beta, depth + 1, maxdepth)
            # Reverse the change
            board[a[0]][a[1]] = 0

            v = min(v, max_res)

            # if v <= alpha, we can prune that subtree as its no longer useful. Thus return
            if v <= alpha: return v

            # Update beta
            beta = min(beta, v)

        return v

    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        
        # Initialize maxdepth
        maxdepth = 4

        # Get list of valid actions
        actions = self.actions(board)

        # Return None if no valid action
        if actions == [] :
            return None
      
        # Initialise res_action to first available move and utility to negative of infinity
        res_action = actions[0][1]
        v = - float("inf")

        alpha = - float("inf")
        beta = float("inf")

        # Implement the actions valid for the max player
        for a in actions:
            # Make changes due to action a on board
            board[a[0],a[1]] = self.player_number
            e_val = self.min_value(board, alpha, beta, 1, maxdepth)
            # Reverse the changes
            board[a[0]][a[1]] = 0
            # If a better utility value is obtained, update best utility and res_action
            if e_val > v :
                v = e_val
                res_action = a[1]
                alpha = e_val

        return res_action

    def expectimax(self, board, player, depth, maxdepth):
        """
        Returns the best utility value according to expectimax algorithm.

        Args:
            board : current state of game
            player : player who can play in this state
            depth : depth of search
            maxdepth : maximum depth
        """
        # If either player 1 or player 2 are in terminal state, return utility value
        test, val = self.cutoff_test(board, depth, maxdepth)
        if test :
            return val

        # Calculate number corresponding to opponent player
        opp = self.player_number ^ 1 ^ 2

        # If max player, find the best utility and return
        if player == self.player_number:
            v = -float("inf")
            res_action = None
            for a in self.actions(board):
                # Make changes due to action a on board
                board[a[0]][a[1]] = self.player_number
                e_val = self.expectimax(board, opp, depth + 1, maxdepth)
                # Reverse the change
                board[a[0]][a[1]] = 0
                # Update v
                v = max(e_val, v)

            return v

        # If condition node, return the expectation value of the utility value.
        # All actions have an equal probability.
        else:
            # Set of valid actions as list of tuples (row, col)
            actions = self.actions(board)
            n_a = len(actions)

            total = 0

            for a in actions : 
                # Make changes due to action a on board
                board[a[0]][a[1]] = opp
                e_val = self.expectimax(board, self.player_number, depth + 1, maxdepth)
                # Reverse the change
                board[a[0]][a[1]] = 0
                # Update the total with utility * probability of taking action 'a'
                total += e_val/n_a
            
            return total


    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        
        # Set of valid actions as list of tuples (row, col)
        actions = self.actions(board)

        # Return None if no action is possible
        if actions == [] :
            return None
    
        # Initialise maxdepth
        maxdepth = 3
        
        # Initialise res_action to first available move and utility to negative of infinity
        v = -float("inf")
        res_action = actions[0][1]
        opp = self.player_number ^ 1 ^ 2

        for a in actions:
            # Make changes due to action a on board
            board[a[0]][a[1]] = self.player_number
            e_val = self.expectimax(board, opp, 1, maxdepth)
            # Reverse the change
            board[a[0]][a[1]] = 0
            # Update result action if e_val is greater than v
            if v < e_val:
                v = e_val
                res_action = a[1]

        return res_action

    def evaluation_function(self, board):
        """
        Given the current state of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        
        # Windows can be vertical, horizontal, along left or right diagonals
        dirs = [(1,0),(0,1),(1,1),(1,-1)]

        rows = len(board)
        cols = len(board[0])

        score = 0

        p = self.player_number
        o = p ^ 1 ^ 2        

        # The number of pieces each player has near the middle column gives them extra score
        # Scores are assigned according to 'the number of valid windows which contain four contiguous pieces 
        # of the same player' which include a cell of that column, scaled down by 10.
        pos_wt = [3/10, 4/10, 5/10, 7/10, 5/10, 4/10, 3/10]
        for j in range(cols):
            col = board[:, j]
            score += np.count_nonzero(col == p) * pos_wt[j]
            score -= np.count_nonzero(col == o) * pos_wt[j]

        board_list = board.tolist()

        for j in range(cols):
            for i in range(rows - 1, -1, -1):
                # Check the window along each direction starting from current cell
                for dx, dy in dirs:
                    # Initialize player and opponent count in window
                    r = i + dx * 3
                    c = j + dy * 3
                    # If window goes out of bounds, ignore
                    if not (0 <= r < rows and 0 <= c < cols): continue
                    win = (board_list[i][j],
                           board_list[i + dx][j + dy],
                           board_list[i + dx * 2][j + dy * 2],
                           board_list[r][c])
                    if win in self.d :
                        score += self.d[win]
        return score

class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

