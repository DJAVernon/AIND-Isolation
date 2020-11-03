import random
import math

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # The one from lectures
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    movesSoFar = game.move_count

    # More moves played the more relevant the number of legal moves is

    own_moves = len(game.get_legal_moves(player))*movesSoFar
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))*movesSoFar
    return float(own_moves - opp_moves)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # More spaces less valuable number of legal moves is
    spacesLeft = len(game.get_blank_spaces())
    # More moves taken more valuable opp moves is
    movesTaken = game.move_count
    # Take the board size to get some relevance
    boardSize = game.width*game.height
    # Create a value function that is relative to boardsize so values don't get too large - High number of moves taken will lead to a number closer to 0
    calibration = (movesTaken + (boardSize - spacesLeft))/boardSize
    # To make it have a larger impact on the values - change this based on performance
    normalisationFactor = 10
    calibration = calibration * normalisationFactor


    # Aim is to emphasise the opponents moves so own player is more likely to be aggresive
    own_moves = len(game.get_legal_moves(player)) * calibration
    opp_moves = len(game.get_legal_moves(game.get_opponent(player))) * calibration

    # The more spaces left the less likely the number of legal moves means

    return float(own_moves-opp_moves)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    playerMoves = len(game.get_legal_moves(player))
    oppPlayer = game.get_opponent(player)
    oppMoves = len(game.get_legal_moves(oppPlayer))

    # Find the distance between the two player locations and reward player for being further away
    playerLocation = game.get_player_location(player)
    oppLocation = game .get_player_location(oppPlayer)

    # Height and width of triangle use pythag theorem to get distance
    xSquared = (playerLocation[0] - oppLocation[0])*(playerLocation[0] - oppLocation[0])
    ySquared = (playerLocation[1] - oppLocation[1]) * (playerLocation[1] - oppLocation[1])

    distance = float(math.sqrt(xSquared + ySquared))

    return float((playerMoves + distance)-oppMoves)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=12.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()


        best_score = float('-inf')
        best_move = None
        # Get the legal moves available at the current gamestate
        #if len(game.get_legal_moves()) == 1:

        legal_moves = game.get_legal_moves()

        best_score = float("-inf")
        best_move = None
        for m in game.get_legal_moves():

            # call has been updated with a depth limit
            v = self.min_value(game.forecast_move(m), depth - 1)
            if v > best_score:
                best_score = v
                best_move = m
        return best_move

    def min_value(self,game,depth):
        """ Return the value for a win (+1) if the game is over,
         otherwise return the minimum value over all legal child
         nodes.
         """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game,self)
        v = float("inf")
        for m in game.get_legal_moves():
            # TODO: pass a decremented depth parameter to each
            #       recursive call
            v = min(v, self.max_value(game.forecast_move(m), depth - 1))
        return v

    def max_value(self,game, depth):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        # If leaf node return score
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth == 0:
            return self.score(game,self)

        #       when the depth parameter reaches 0 -- for now
        #       just return a value of 0 at the depth limit
        if depth == 0:
            return 0
        v = float("-inf")
        for m in game.get_legal_moves():
            #       recursive call
            v = max(v, self.min_value(game.forecast_move(m), depth - 1))
        return v




class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left


        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        if len(game.get_legal_moves()) >= 1:
            best_move = game.get_legal_moves()[0]
        else:
            return best_move

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            tree = range(1,len(game.get_blank_spaces()))
            for depth in tree:
                possible_best = self.alphabeta(game, depth)
                # If possible_best is an empty tuple then return previous iteration
                if possible_best == ():
                    return best_move
                else:
                    best_move = possible_best

        except SearchTimeout:
            return best_move

        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Get the legal moves available at the current gamestate
        legal_moves = game.get_legal_moves()

        best_score = float("-inf")
        # Return an empty tuple instead of none
        best_move = ()

        for m in legal_moves:
            v = self.min_value(game.forecast_move(m), depth - 1,alpha,beta)
            if v > best_score:
                best_score = v
                best_move = m

            # KEYLOGIC:  If score beats the upper limit then break and return the best possible move
            if best_score >= beta:
                break
            # Sets the lowerbound
            alpha = max(alpha,best_score)
        return best_move


    def min_value(self,game,depth,alpha,beta):
        """ Return the value for a win (+1) if the game is over,
         otherwise return the minimum value over all legal child
         nodes.
         """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game,self)

        v = float("inf")

        for m in game.get_legal_moves():
            v = min(v, self.max_value(game.forecast_move(m), depth - 1,alpha,beta))
            # Then new min value
            if v <= alpha:
                return v
            beta = min(v,beta)

        return v

    def max_value(self,game, depth,alpha,beta):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        # If leaf node return score
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth == 0:
            return self.score(game,self)

        #       when the depth parameter reaches 0 -- for now
        #       just return a value of 0 at the depth limit
        if depth == 0:
            return 0
        v = float("-inf")
        for m in game.get_legal_moves():
            #       recursive call
            v = max(v, self.min_value(game.forecast_move(m), depth - 1,alpha,beta))
            # Then upper value
            if v >= beta:
                return v
            alpha = max(v,alpha)
        return v
