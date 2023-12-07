import chess

test = chess.board()

test.reset()
print(test)

while True:
    note = str(input("Make move: "))
    encoded_move = test.full_decode(note)
    test.execute(encoded_move)

    print(test)
