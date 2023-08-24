import chess

test = chess.board()



test.place('nd6', 1)
test.place('rh4', 0)
test.place('g3',1)
test.place('a7',1)

print(test)

while True:
    operation = str(input('op:'))
    test.move(operation)
    print(test)