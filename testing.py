import chess

test = chess.board()

test.place(notation='Rb4', team=0)
test.place(notation='c4', team=0)
test.place(notation='nb5', team=0)
test.place('bc5', 0)

print(test)

while True:
    note = str(input("Make move: "))
    encoded_move = test.full_decode(note)
    test.execute(encoded_move)
    test.turn = 0

    print(test)
