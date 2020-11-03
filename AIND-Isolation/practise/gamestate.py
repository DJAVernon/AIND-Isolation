from copy import deepcopy
xlim, ylim = 3, 2  # board dimension constants

class GameState:
    """
    Attributes
    ----------
    _board: list(list)
        Represent the board with a 2d array _board[x][y]
        where open spaces are 0 and closed spaces are 1
        and a coordinate system where [0][0] is the top-
        left corner, and x increases to the right while
        y increases going down (this is an arbitrary
        convention choice -- there are many other options
        that are just as good)

    _parity: bool
        Keep track of active player initiative (which
        player has control to move) where 0 indicates that
        player one has initiative and 1 indicates player two

    _player_locations: list(tuple)
        Keep track of the current location of each player
        on the board where position is encoded by the
        board indices of their last move, e.g., [(0, 0), (1, 0)]
        means player one is at (0, 0) and player two is at (1, 0)
    """

    def __init__(self):
        self._board = [[0] * ylim for _ in range(xlim)]
        self._board[-1][-1] = 1  # block lower-right corner
        self._parity = 0
        self._player_locations = [None, None]

    def get_blank_spaces(self):
        blankList = []
        for x in range(xlim):
            for y in range(ylim):
                if self._board[x][y] == 0:
                    blankList.append((x,y))
        return blankList

    # List of all legal moves for active player
    def get_legal_moves(self):
        """ Return a list of all legal moves available to the
        active player.  Each player should get a list of all
        empty spaces on the board on their first move, and
        otherwise they should get a list of all open spaces
        in a straight line along any row, column or diagonal
        from their current position. (Players CANNOT move
        through obstacles or blocked squares.) Moves should
        be a pair of integers in (column, row) order specifying
        the zero-indexed coordinates on the board.
        """
        legal_moves = []
        activePlayer = self._parity
        currentLocation = self._player_locations[activePlayer]
        # If no current location
        if not currentLocation:
            return self.get_blank_spaces()
        board = self._board

        # Rays are lines that moves infinitly in one direction - THese are the directions
        rays = [(1, 0), (1, -1), (0, -1), (-1, -1),
                (-1, 0), (-1, 1), (0, 1), (1, 1)]


        # for each ray line
        for dx,dy in rays:
            # Get the x and y values for the current location
            x,y = currentLocation
            # For this ray - While x is in the range of the board and so is y
            while 0 <= x + dx < xlim and 0 <= y + dy < ylim:
                x = x + dx
                y = y + dy
                # Don't understand this section - TODO: Find out what it does
                if self._board[x][y]:
                    break
                legal_moves.append((x,y))
        return legal_moves

    # Change board, Change ACtive player, Change player location
    def forecast_move(self, move):
        """ Return a new board object with the specified move
        applied to the current game state.

        Parameters
        ----------
        move: tuple
            The target position for the active player's next move
            (e.g., (0, 0) if the active player will move to the
            top-left corner of the board)
        """
        # Copies the entire board
        if move not in self.get_legal_moves():
            raise RuntimeError("Attempted forecast of illegal move")
        newBoard = deepcopy(self)
        activePlayer = newBoard._parity
        # Change the player location to the new move
        newBoard._player_locations[activePlayer] = move
        # Exclusive or (bitwise) Cool way of doing 0 or 1
        # CHange the active player
        newBoard._parity ^= 1
        # Change the board
        x,y = move
        newBoard._board[x][y] = 1
        return newBoard


if __name__ == "__main__":
    # This code is only executed if "gameagent.py" is the run
    # as a script (i.e., it is not run if "gameagent.py" is
    # imported as a module)
    emptyState = GameState()  # create an instance of the object
    print(emptyState._board)
