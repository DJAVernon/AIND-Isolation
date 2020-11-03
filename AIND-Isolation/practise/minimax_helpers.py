def terminal_test(gameState):
    """ Return True if the game is over for the active player
    and False otherwise.
    """
    # If the list of legal moves is empty return True else return false
    return not bool(gameState.get_legal_moves())

def min_value(gameState):
    """ Return the value for a win (+1) if the game is over,
    otherwise return the minimum value over all legal child
    nodes.
    """
    if terminal_test(gameState):
        return 1
        # Defined as a infinite float
    v = float("inf")
    # For each legal move in the current state
    for move in gameState.get_legal_moves():
        # Iterate through each result and fine the value of each move - Presuming min and max
        _max = max_value(gameState.forecast_move(move))
        # If the min value is smaller than
        v = min(v, _max)
    return v

def max_value(gameState):
    """ Return the value for a loss (-1) if the game is over,
    otherwise return the maximum value over all legal child
    nodes.
    """
    if terminal_test(gameState):
        return -1
    # Defined as a infinite float
    v = float("-inf")
    # For each legal move in the current state
    for move in gameState.get_legal_moves():
        # Iterate through each result and fine the value of each move - Presuming min and max
        _min = min_value(gameState.forecast_move(move))
        # If the new v value is larger than the old one then replace it
        v = max(v,_min)
    return v

