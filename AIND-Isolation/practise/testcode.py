# Feel free to modify this code for testing, however the "submit" button
# will NOT recognize any of these changes
from practise import gamestate as gs
from practise import minimax

best_moves = set([(0, 0), (2, 0), (0, 1)])
rootNode = gs.GameState()
minimax_move = minimax.minimax_decision(rootNode)

print("Best move choices: {}".format(list(best_moves)))
print("Your code chose: {}".format(minimax_move))

if minimax_move in best_moves:
    print("That's one of the best move choices. Looks like your minimax-decision function worked!")
else:
    print("Uh oh...looks like there may be a problem.")
