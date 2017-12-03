from game import Game;

g = Game()
g.randomlyAdd()
loop = True
while loop:
    print(g);
    move = 0
    while True:
        moveInput = input("Move (l, r, u, d)? ")
        if moveInput.lower() == "l":
            move = 2
            break
        elif moveInput.lower() == "u":
            move = 1
            break;
        elif moveInput.lower() == "r":
            move = 0
            break;
        elif moveInput.lower() == "d":
            move = 3
            break;
    result = g.step(move)
    if result == -1:
        print("Invalid move!")
    elif result == 0:
        loop = False
print("Game over!")
