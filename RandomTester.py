import numpy as np
from game import Game
import matplotlib.pyplot as plt

numMoves = 0
game = Game()
x=0
results = [];

forceValidMoves = input("Force Valid Moves? ") == "Y"

np.random.seed(1)
while x < 500:
    #Random Player
    move = np.random.randint(4);

    #Play that move
    result = game.step(move)

    if (not forceValidMoves) and result == -1:
        results.append(numMoves+(3*np.log2(np.amax(game.board))))
        numMoves = 0;
        game = Game()
        x+=1
    else:
        if result == 0:
            results.append(numMoves+(3*np.log2(np.amax(game.board))))
            numMoves = 0;
            game = Game()
            x+=1
        elif result != -1:
            numMoves+=1

print("Maximum:", np.amax(results))
print("Average:", np.average(results))
plt.plot(sorted(results))
plt.show()
