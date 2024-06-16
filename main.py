from board import Board
import random
import evaluater

color_input = input("Enter AI's Color (W/b): ")
if color_input == "b": user_color, ai_color = True, False
else: user_color, ai_color = False, True

fen_code = input("Enter FEN Code (For default leave empty): ")
if fen_code != "": board = Board(fen_code)
else: board = Board()

while True:
    if board.turn == user_color:
        print(board)
        if board.is_in_checkmate(user_color):
            print("Checkmate - AI Wins")
            break
        
        while True:
            move = input("Enter Move: ")
            try:
                if move == "exit":
                    print("Forfeit - AI Wins")
                    board.turn = None
                    break
                elif move == "draw":
                    print("Draw")
                    board.turn = None
                    break
                else:
                    converted = board.convert_from_algebraic(move, user_color)
                    board.move(move=converted)
                    break
            except:
                print("Invalid Input")
    elif board.turn == ai_color:
        if board.is_in_checkmate(ai_color):
            print(board)
            print("Checkmate - User Wins")
            break
        print("AI's Turn")
        # All Moves
        possible_moves = board.get_all_possible_moves(ai_color, only_captures=False, add_where_from=True, exclude_checks=True)
        
        print("All Moves:", ",".join(possible_moves))
        print("All Moves Count:", len(possible_moves))

        # Best Moves
        best_evaluation = None
        best_moves = []

        for move in possible_moves:
            simulated_board = board.move_simulate(move=move)
            simulated_board_ev = evaluater.evaluate_board(simulated_board, ai_color)

            if best_evaluation == None:
                best_evaluation = simulated_board_ev
                best_moves.append(move)
            elif simulated_board_ev > best_evaluation:
                best_evaluation = simulated_board_ev
                best_moves = []
                best_moves.append(move)
            elif simulated_board_ev == best_evaluation:
                best_moves.append(move)

        print("Best Moves:", ", ".join(best_moves))
        print("Best Evaluation:", best_evaluation)
        print("Best Moves Count:", len(best_moves))

        # Chosen Move
        chosen_move = random.choice(best_moves)
        print("Chosen Move:", chosen_move)
        board.move(move=chosen_move)
    else:
        break

print("\nWell Played, Bye!")
