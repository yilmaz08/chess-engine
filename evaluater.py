### VALUES ###
THE_MAX = 999_999_999_999_999

PIECE_EVAL_MULTIPLIER = 1
CHECK_EVAL_MULTIPLIER = 0.5
PROTECTED_TILE_EVAL_MULTIPLIER = 0.05
ENEMY_PROTECTED_TILE_EVAL_MULTIPLIER = -0.05
HANGING_PIECE_EVAL_MULTIPLIER = -0.75
ENEMY_HANGING_PIECE_EVAL_MULTIPLIER = 0.25

### MODULES ###
from board import Board, piece_types

### FUNCTIONS ###
def evaluate_pieces(board: Board, color: bool):
    your_points = 0
    opponent_points = 0
    pieces = board.get_pieces(filter=None)

    for piece in pieces:
        if pieces[piece]["color"] != color:
            opponent_points += piece_types[pieces[piece]["type"]]["points"]
        else:
            your_points += piece_types[pieces[piece]["type"]]["points"]
    
    return your_points, opponent_points

def evaluate_hanging_pieces(board: Board, color):
    points = 0
    opponent_pieces = board.get_pieces(not color)
    # print("Opponent Pieces:", opponent_pieces)
    for piece in opponent_pieces:
        moves = board.list_moves(piece, not color)
        # print("moves:", moves)
        for move in moves:
            the_move = f"{piece}-{move}"
            splitted = the_move.split("-")
            # outgoing = "-".join(splitted[1:])
            attack_pos = splitted[1]
            if len(splitted) > 2:
                if splitted[2] == "ep":
                    _from = splitted[0]
                    _to = splitted[1]
                    letter_of_to = _to[0]
                    number_of_from = _from[1]
                    attack_pos = f"{letter_of_to}{number_of_from}"
            # Attacked Piece
            attacked_piece = board.get_piece(attack_pos)
            if attacked_piece == None: continue
            points += piece_types[attacked_piece["type"]]["points"]
            
    return points

def list_protected_tiles(board: Board, pos, turn: bool):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    piece = board.pieces.get(pos)
    if not piece: return []
    
    piece_type = piece["type"]
    piece_color = piece["color"]

    if turn is not None and piece_color != turn: return []

    pos_in_xy = (letters.index(pos[0]), int(pos[1]) - 1)

    if piece_type not in piece_types: return []

    moves = []
    
    move_types = board.get_move_types(piece_type, piece_color, pos_in_xy)

    for move_type in move_types:
        if move_type["type"] == "castle":
            pass # Castle can't be a threat
        elif move_type["type"] == "direction":
            multiplier = 1 if piece_color else -1
            x = pos_in_xy[0] # x
            y = pos_in_xy[1] # y
            while True:
                x += move_type["x"] * multiplier
                y += move_type["y"] * multiplier
                if x < 0 or x > 7 or y < 0 or y > 7: break
                piece = board.get_piece(f"{letters[x]}{y + 1}")
                if piece:
                    if piece["color"] != piece_color:
                        moves.append(f"{letters[x]}{y + 1}")
                    break
                else:
                    moves.append(f"{letters[x]}{y + 1}")
        elif move_type["type"] == "position":
            x = pos_in_xy[0] + move_type["x"] * (1 if piece_color else -1) # new x
            y = pos_in_xy[1] + move_type["y"] * (1 if piece_color else -1) # new y
            if x < 0 or x > 7 or y < 0 or y > 7: continue # outside of board

            if "en_passant" in move_type:
                moves.append(f"{letters[x]}{y + 1}-ep")
            elif "promotion" in move_type:
                piece = board.get_piece(f"{letters[x]}{y + 1}")
                if move_type["capture"]:
                    if piece != None:
                        if piece["color"] != piece_color:
                            moves.append(f"{letters[x]}{y + 1}-{move_type['promotion']}")
                            # moves.append(f"{letters[x]}{y + 1}")
                elif move_type["move"]:
                    pass # Can't be a threat
                else:
                    print("wtf? x2") 
            else:
                piece = board.get_piece(f"{letters[x]}{y + 1}")
                if move_type["move"] and move_type["capture"]:
                    if piece != None:
                        if piece["color"] != piece_color:
                            moves.append(f"{letters[x]}{y + 1}")
                    else:
                        moves.append(f"{letters[x]}{y + 1}")
                elif move_type["move"]:
                    pass # Can't be a threat
                elif move_type["capture"]:
                    if piece != None:
                        if piece["color"] != piece_color:
                            moves.append(f"{letters[x]}{y + 1}")
                else:
                    print("wtf?")
    # print("moves:", moves)
    return moves


def evaluate_board(board: Board, color):
    # is checkmate for the turn color
    if board.is_checkmate(color): # is color checkmated
        return -THE_MAX
    elif board.is_checkmate(not color): # is opponent checkmated
        return THE_MAX
    evaluation = 0

    all_protects = []
    for piece in board.pieces:
        if board.pieces[piece]["color"] == color:
            all_protects += list_protected_tiles(board, piece, color)
    
    all_enemy_protects = []
    for piece in board.pieces:
        if board.pieces[piece]["color"] != color:
            all_enemy_protects += list_protected_tiles(board, piece, not color)

    your_points, opponent_points = evaluate_pieces(board, color)
    evaluation += (your_points - opponent_points) * PIECE_EVAL_MULTIPLIER

    evaluation += (1 if board.is_check(not color) else 0) * CHECK_EVAL_MULTIPLIER

    evaluation += evaluate_hanging_pieces(board, color) * HANGING_PIECE_EVAL_MULTIPLIER
    evaluation += len(all_protects) * PROTECTED_TILE_EVAL_MULTIPLIER

    evaluation += evaluate_hanging_pieces(board, not color) * ENEMY_HANGING_PIECE_EVAL_MULTIPLIER
    evaluation += len(all_enemy_protects) * ENEMY_PROTECTED_TILE_EVAL_MULTIPLIER

    return evaluation