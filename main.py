from board import Board
import random
import evaluater

color_input = input("Enter AI's Color (w/b): ")

if color_input == "b":
    user_color = True # True is white, False is black
    ai_color = not user_color
elif color_input == "w":
    user_color = False
    ai_color = not user_color
else:
    print("Invalid Color")
    exit()

# board_dict = {
#     "a8": {"type": "k", "color": True},
#     "h1": {"type": "k", "color": False},
#     "c3": {"type": "r", "color": True},
#     "f3": {"type": "r", "color": True},
#     "h5": {"type": "q", "color": False},
# }

# board = Board(pieces=board_dict) # Custom Board
board = Board() # Default Board

# print(board.evaluate_hanging_pieces(ai_color))
# print(board.is_checkmate(user_color))
# print(board.list_moves("e1", True))

# exit()
# print(board)
print(board)
while True:
    if board.turn == user_color:
        print("Your Turn")
        move = input("Enter Move: ")
        if move == "exit" or move == "quit" or move == "q" or move == "e" or move == "forfeit" or move == "ff":
            print("User Forfeited - AI Wins")
            break
        elif move == "draw":
            print("User Drawed - Draw")
            break
        
        splitted = move.split("-")
        result = board.move(move, user_color, True)
        print(result)
        if board.is_checkmate(ai_color):
            print("Checkmate - User Wins")
            break
    else:
        print("AI's Turn")

        pieces = board.get_pieces(board.turn)
        # pieces = ["e1"]
        
        moves_total = 0
        evaluation = None
        possible_moves = []
        all_moves = []
        
        for piece in pieces:
            piece_type = board.pieces[piece]["type"]
            moves = board.list_moves(piece, ai_color)
            moves_total += len(moves)
            for move in moves:
                all_moves.append(f"{piece}-{move}")
                simulated_board = board.move_simulate(f"{piece}-{move}", ai_color)

                if simulated_board.is_check(ai_color): continue # Invalid Move

                # ev = simulated_board.evaluate_board(ai_color)
                ev = evaluater.evaluate_board(simulated_board, ai_color)

                if evaluation == None:
                    evaluation = ev
                    possible_moves.append(f"{piece}-{move}")
                elif ev > evaluation:
                    evaluation = ev
                    possible_moves = []
                    possible_moves.append(f"{piece}-{move}")
                elif ev == evaluation:
                    possible_moves.append(f"{piece}-{move}")

        print("Pieces Count:", len(pieces))
        print("Moves Total:", moves_total)
        
        print("Pieces:")
        print(pieces)
        print(f"Possible Moves:")
        print(all_moves)
        print(f"Evaluated Moves (Eval {evaluation}):")
        print(possible_moves)

        if len(possible_moves) == 0:
            print("AI has no moves - Forfeit")
            exit()
        
        chosen_move = random.choice(possible_moves)
        print("Chosen Move:")
        print(chosen_move)

        message, status = board.move(chosen_move, ai_color, True)
        print(message)
        if status == False:
            print("AI Error - Forfeit")
            break
        
        # print(board, end="")
        # print(board)
        print("hi")
        if board.is_checkmate(user_color):
            print("Checkmate - AI Wins")
            break
        print(board)
        print(chosen_move)
        print("New History")
        print(board.history)

print("\nWell Played, Bye!")