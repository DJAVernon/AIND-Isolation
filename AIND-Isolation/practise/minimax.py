from practise import minimax_helpers as mh

# Finds the best possible move given a boardstate
def minimax_decision(gameState):
    """ Return the move along a branch of the game tree that
    has the best possible value.  A move is a pair of coordinates
    in (column, row) order corresponding to a legal move for
    the searching player.

    You can ignore the special case of calling this function
    from a terminal state.
    """
    best_score = float('-inf')
    best_move = None
    # Get the legal moves available at the current gamestate
    legal_moves = gameState.get_legal_moves()
    for move in legal_moves:
        # Find the minimum value for each move
        value = mh.min_value(gameState.forecast_move(move))
        if best_score < value:
            best_move = move
            best_score = value
    return best_move

