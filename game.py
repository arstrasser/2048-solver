import numpy as np;
np.random.seed(12345)

class Game:
    def __init__(self):
        self.board = [];
        for i in range(0,4):
            self.board.append([]);
            for j in range(0,4):
                self.board[i].append(0);
        self.randomlyAdd()
    def step(self, move):
        if(not self.moveTiles(move)):
            if self.isFull():
                return 0
            return -1
        self.randomlyAdd()
        return 1;
    def getLogState(self):
        final = []
        for row in self.board:
            for val in row:
                if val == 0:
                    final.append(0)
                else:
                    final.append(np.log2(val))
        return final
    def moveTiles(self, direction):
        madeMove = False
        if(direction == 0):
            for i in range(0, 4):
                limit = 4
                for j in range(2, -1, -1):
                    if(self.board[i][j] != 0):
                        while j+1 < limit:
                            if(self.board[i][j+1] == 0):
                                self.board[i][j+1] = self.board[i][j];
                                self.board[i][j] = 0
                                madeMove = True;
                            elif(self.board[i][j+1] == self.board[i][j]):
                                self.board[i][j+1] += self.board[i][j]
                                self.board[i][j] = 0
                                limit = j+1
                                madeMove = True;
                                break;
                            else:
                                limit = j+1
                                break;
                            j+=1
        elif direction == 1:
            for i in range(0, 4):
                limit = -1
                for j in range(1, 4):
                    if(self.board[j][i] != 0):
                        while j-1 > limit:
                            if(self.board[j-1][i] == 0):
                                self.board[j-1][i] = self.board[j][i];
                                self.board[j][i] = 0
                                madeMove = True
                            elif(self.board[j-1][i] == self.board[j][i]):
                                self.board[j-1][i] += self.board[j][i]
                                self.board[j][i] = 0
                                limit = j-1
                                madeMove = True
                                break;
                            else:
                                limit = j-1
                                break;
                            j-=1
        elif direction == 2:
            for i in range(0, 4):
                limit = -1
                for j in range(1, 4):
                    if(self.board[i][j] != 0):
                        while j-1 > limit:
                            if(self.board[i][j-1] == 0):
                                self.board[i][j-1] = self.board[i][j];
                                self.board[i][j] = 0
                                madeMove = True
                            elif(self.board[i][j-1] == self.board[i][j]):
                                self.board[i][j-1] += self.board[i][j]
                                self.board[i][j] = 0
                                limit = j-1
                                madeMove = True
                                break;
                            else:
                                limit = j-1
                                break;
                            j-=1
        else:
            for i in range(0, 4):
                limit = 4
                for j in range(2, -1, -1):
                    if(self.board[j][i] != 0):
                        while j+1 < limit:
                            if(self.board[j+1][i] == 0):
                                self.board[j+1][i] = self.board[j][i];
                                self.board[j][i] = 0
                                madeMove = True
                            elif(self.board[j+1][i] == self.board[j][i]):
                                self.board[j+1][i] += self.board[j][i]
                                self.board[j][i] = 0
                                limit = j+1
                                madeMove = True
                                break;
                            else:
                                limit = j+1
                                break;
                            j+=1
        return madeMove
    def randomlyAdd(self):
        possibilities = []
        for i in range(0,4):
            for j in range(0,4):
                if(self.board[i][j] == 0):
                    possibilities.append([i, j]);
        if(len(possibilities) == 0):
            return False;
        position = possibilities[np.random.randint(len(possibilities))]
        if(np.random.random() <= 0.9):
            self.board[position[0]][position[1]] = 2
        else:
            self.board[position[0]][position[1]] = 4
        return True;
    def isFull(self):
        for i in range(0,4):
            for j in range(0,4):
                if(self.board[i][j] == 0):
                    return False;
        return True
    def __str__(self):
        string = ""
        for i in range(0, 4):
            string += str(self.board[i]) +"\n"
        return string

if __name__ == "__main__":
    g = Game()
    g.randomlyAdd()
    while not g.step(randrange(4)) == 0:
        nextMove = randrange(4)
