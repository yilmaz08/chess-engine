from board import Board

# PARAMETERS:
THE_MAX = 999_999_999_999_999

# Multipliers
PIECE_EVAL_MULTIPLIER = 1

PROTECTED_TILE_EVAL_MULTIPLIER = 0.05
ENEMY_PROTECTED_TILE_EVAL_MULTIPLIER = -0.02

HANGING_PIECES_EVAL_MULTIPLIER = -0.75
ENEMY_HANGING_PIECES_EVAL_MULTIPLIER = 0.25

TRADE_MULTIPLIER = 0.75

# Static Points
WIN_POINTS = THE_MAX
LOSE_POINTS = -THE_MAX
DRAW_POINTS = 0.05
BENEFICIAL_DRAW_POINTS = DRAW_POINTS # TODO
# DRAW_POINTS if input("Is Draw Beneficiable? (y/n):").lower() == "y" else -DRAW_POINTS

CHECK_POINTS = 0.4


PIECE_POINTS = { "p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 0 }

def evaluate_board(board: Board, color):
    if board.is_in_checkmate(not color):
        return WIN_POINTS

    if len(board.get_all_possible_moves(not color, only_captures=False, add_where_from=True, exclude_checks=True)) == 0:
        return BENEFICIAL_DRAW_POINTS # Stalemate

    evaluation = 0

    # Points
    evaluation += calculate_points(board, color) * PIECE_EVAL_MULTIPLIER
    # Protected Tiles
    evaluation += calculate_protected_tiles(board, color, exclude_checks=False) * PROTECTED_TILE_EVAL_MULTIPLIER # Can't exclude checks here because it would need a simulation although it is not its turn
    evaluation += calculate_protected_tiles(board, not color, exclude_checks=True) * ENEMY_PROTECTED_TILE_EVAL_MULTIPLIER
    # Hanging Pieces
    evaluation += calculate_hanging_pieces(board, color) * HANGING_PIECES_EVAL_MULTIPLIER
    evaluation += calculate_hanging_pieces(board, not color) * ENEMY_HANGING_PIECES_EVAL_MULTIPLIER
    # Trades
    evaluation += calculate_trades(board, color) * TRADE_MULTIPLIER

    # Static Controls
    if board.is_in_check(color):
        evaluation += CHECK_POINTS
    
    return evaluation

    


def calculate_points(board: Board, color: bool):
    pieces = board.get_pieces(color)
    enemy_pieces = board.get_pieces(not color)
    points = 0

    for piece in pieces:
        _piece = board.get_piece(piece)
        points += PIECE_POINTS[_piece["type"]]
    
    for piece in enemy_pieces:
        _piece = board.get_piece(piece)
        points -= PIECE_POINTS[_piece["type"]]

    return points

def calculate_protected_tiles(board: Board, color: bool, exclude_checks=False):
    every_protected_tile_repeating = board.get_all_possible_moves(color, only_captures=True, add_where_from=False, exclude_checks=exclude_checks)
    actual_tiles = [] # not repeating
    for tile in every_protected_tile_repeating:
        if board.get_piece(tile) == None:
            formatted_tile = tile[0:2]
            if formatted_tile not in actual_tiles:
                actual_tiles.append(formatted_tile)
    return len(actual_tiles)

def calculate_hanging_pieces(board: Board, color: bool):
    all_pieces = board.get_pieces(color)

    points = 0
    for piece in all_pieces:
        if board.is_in_danger(piece, color):
            points += PIECE_POINTS[board.get_piece(piece)["type"]]
    
    return points

def calculate_trades(board: Board, color: bool):
    pass