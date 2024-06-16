import copy

DEFAULT_BOARD = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

RANKS = {
    True: {"promotion": 7, "2-move": 1},
    False: {"promotion": 0, "2-move": 6}
}
PROMOTE_TO = ["q", "r", "b", "n"]

HORSEY_MOVES = [(2, 1),(2, -1),(-2, 1),(-2, -1),(1, 2),(-1, 2),(1, -2),(-1, -2)]
KING_MOVES = [(1, 1),(1, -1),(-1, 1),(-1, -1),(0, 1),(0, -1),(1, 0),(-1, 0)]

LETTERS = "abcdefgh"
NUMBERS = "12345678"
REVERSED_NUMBERS = "87654321"

class Board:
    pieces = {}
    turn = True # True: White, False: Black
    # Castling
    whiteOO, whiteOOO, blackOO, blackOOO = False, False, False, False
    # En Passant
    en_passant_pos = None
    # Halfmove Clock
    halfmove_clock = 0
    # Fullmove Number
    fullmove_number = 1

    def __init__(self, fen_code: str = DEFAULT_BOARD):
        self.pieces, self.turn, self.whiteOO, self.whiteOOO, self.blackOO, self.blackOOO, self.en_passant_pos, self.halfmove_clock, self.fullmove_number = self.import_fen(fen_code)

    def __str__(self):
        return f"Chess Board. Turn: {('White' if self.turn else 'Black')}.\nEn Passant Pos: {self.en_passant_pos}\nBlack Castle (OO OOO): {self.blackOO} {self.blackOOO}\nWhite Castle (OO OOO): {self.whiteOO} {self.whiteOOO}\n\n{self.draw_board()}"

    ### PIECES
    def get_pieces(self, color = None):
        if color == None: # No filtering
            return self.pieces
        else:
            result = []
            for piece in self.pieces:
                if self.pieces[piece]["color"] == color:
                    result.append(piece)
            return result
    def get_piece(self, pos):
        return self.pieces.get(pos)

    ### OUTPUT ###
    def draw_board(self, color = True):
        result = ""
        numbers = REVERSED_NUMBERS if color else NUMBERS
        for number in numbers:
            for letter in LETTERS:
                piece_pos = f"{letter}{number}"
                piece = self.get_piece(piece_pos)
                if piece:
                    if piece["color"]:
                        result += str(piece["type"]).upper()
                    else:
                        result += str(piece["type"]).lower()
                else:
                    result += " " # Empty Tile
            result += "\n"
        return result
    
    ### FEN ###
    def import_fen(self, fen_code: str):
        splitted = fen_code.replace(" ", "_").split("_")
        
        pieces = {}
        current_x, current_y = 0, 8 # FEN starts from 8th rank
        for row in splitted[0].split("/"):
            current_x = 0
            current_y -= 1
            for letter in row:
                if letter.isnumeric():
                    current_x += int(letter)
                else:
                    pieces[f"{LETTERS[current_x]}{current_y + 1}"] = {"color": (not letter.islower()), "type": letter.lower()}
                    current_x += 1
            
        if splitted[1] == "w": turn = True
        elif splitted[1] == "b": turn = False
        else: raise Exception("Invalid FEN Code")

        whiteOO, whiteOOO, blackOO, blackOOO = False, False, False, False
        if "K" in splitted[2]: whiteOO = True
        if "Q" in splitted[2]: whiteOOO = True
        if "k" in splitted[2]: blackOO = True
        if "q" in splitted[2]: blackOOO = True

        if splitted[3] == "-": en_passant_pos = None
        else: en_passant_pos = splitted[3]

        halfmove_clock = int(splitted[4])
        fullmove_number = int(splitted[5])

        return pieces, turn, whiteOO, whiteOOO, blackOO, blackOOO, en_passant_pos, halfmove_clock, fullmove_number
    def export_fen(self):
        print("Exporting FEN") # TODO

    ### MOVEMENT ###
    def move(self, move):
        splitted_move = move.split("-")
        pos = splitted_move[0]
        piece = self.get_piece(pos)
        # from 1 to end is the target
        target = "-".join(splitted_move[1:])

        if piece == None: raise Exception("Invalid Move - Piece Doesn't Exist")
        if piece["color"] != self.turn: raise Exception("Invalid Move - Wrong Turn")

        possible_moves = self.get_possible_moves(pos)
        if target not in possible_moves: raise Exception("Invalid Move - Not Possible")

        self.en_passant_pos = None
        
        splitted_target = target.split("-")
        if len(splitted_target) > 1:
            if splitted_target[1] == "enpassant": # en passant
                target_en_passant_pos = f"{splitted_target[0][0]}{pos[1]}" # letter from target, number from pos to find the en passant target

                self.pieces[splitted_target[0]] = piece.copy()
                self.pieces.pop(pos)
                self.pieces.pop(target_en_passant_pos)

            elif splitted_target[1] == "2forward": # 2 forward
                self.pieces[splitted_target[0]] = piece.copy()
                self.pieces.pop(pos)

                new_y = NUMBERS.index(splitted_target[0][1])
                old_y = NUMBERS.index(pos[1])

                y_avg = (new_y + old_y) / 2

                self.en_passant_pos = f"{pos[0]}{NUMBERS[int(y_avg)]}"
        else:
            split_for_promotion = splitted_target[0].split("=")
            if len(split_for_promotion) > 1: # Promotion
                self.pieces[split_for_promotion[0]] = {"color": piece["color"], "type": split_for_promotion[1]}
                self.pieces.pop(pos)
            elif splitted_target[0] == "OO" or splitted_target[0] == "OOO": # Castle
                if piece["color"]:
                    if splitted_target[0] == "OO":
                        self.pieces["g1"] = self.pieces["e1"].copy()
                        self.pieces.pop("e1")
                        self.pieces["f1"] = self.pieces["h1"].copy()
                        self.pieces.pop("h1")
                    else:
                        self.pieces["c1"] = self.pieces["e1"].copy()
                        self.pieces.pop("e1")
                        self.pieces["d1"] = self.pieces["a1"].copy()
                        self.pieces.pop("a1")
                else:
                    if splitted_target[0] == "OO":
                        self.pieces["g8"] = self.pieces["e8"].copy()
                        self.pieces.pop("e8")
                        self.pieces["f8"] = self.pieces["h8"].copy()
                        self.pieces.pop("h8")
                    else:
                        self.pieces["c8"] = self.pieces["e8"].copy()
                        self.pieces.pop("e8")
                        self.pieces["d8"] = self.pieces["a8"].copy()
                        self.pieces.pop("a8")
            else: # Normal Move
                self.pieces[splitted_target[0]] = piece.copy() # Copy the piece to the new position
                self.pieces.pop(pos) # Delete the old position
        self.halfmove_clock += 1
        if self.turn == False: self.fullmove_number += 1
        self.turn = not self.turn
    def move_simulate(self, move):
        new_board = copy.deepcopy(self)
        new_board.move(move)
        return new_board

    ### CALCULATE ###
    def get_possible_moves(self, pos, only_captures = False, exclude_checks = False):
        piece = self.get_piece(pos)
        if piece == None: raise Exception("No Piece")
        piece_color = piece["color"]
        color_as_positive_or_negative = 1 if piece_color else -1

        moves = []
        if piece["type"] == "p": # PAWN
            y_position = NUMBERS.index(pos[1])
            if only_captures == False: # If non capture moves are allowed
                # 1 FORWARD MOVE
                one_forward = self.move_from_pos(pos, 0, 1 * color_as_positive_or_negative)
                if one_forward != None:
                    if self.get_piece(one_forward) == None:
                        if y_position + 1 * color_as_positive_or_negative == RANKS[piece_color]["promotion"]:
                            for promote_to in PROMOTE_TO:
                                moves.append(f"{one_forward}={promote_to}")
                        else:
                            moves.append(one_forward)

                        # 2 FORWARD MOVE
                        if RANKS[piece_color]["2-move"] == y_position:
                            two_forward = self.move_from_pos(pos, 0, 2 * color_as_positive_or_negative)
                            if two_forward != None:
                                if self.get_piece(two_forward) == None:
                                    if y_position + 2 * color_as_positive_or_negative == RANKS[piece_color]["promotion"]:
                                        for promote_to in PROMOTE_TO:
                                            moves.append(f"{two_forward}={promote_to}-2forward")
                                    else:
                                        moves.append(f"{two_forward}-2forward")
            # CAPTURE
            # x negative
            capture_x_negative = self.move_from_pos(pos, -1, color_as_positive_or_negative)
            if capture_x_negative != None:
                target_piece = self.get_piece(capture_x_negative)
                if target_piece == None:
                    if self.en_passant_pos == capture_x_negative:
                        if y_position + 1 * color_as_positive_or_negative == RANKS[piece_color]["promotion"]:
                            for promote_to in PROMOTE_TO:
                                moves.append(f"{capture_x_negative}={promote_to}-enpassant")
                        else:
                            moves.append(f"{capture_x_negative}-enpassant")
                elif target_piece["color"] != piece_color:
                    if y_position + 1 * color_as_positive_or_negative == RANKS[piece_color]["promotion"]:
                        for promote_to in PROMOTE_TO:
                            moves.append(f"{capture_x_negative}={promote_to}")
                    else:
                        moves.append(capture_x_negative)
            # x positive
            capture_x_positive = self.move_from_pos(pos, 1, color_as_positive_or_negative)
            if capture_x_positive != None:
                target_piece = self.get_piece(capture_x_positive)
                if target_piece == None:
                    if self.en_passant_pos == capture_x_positive:
                        if y_position + 1 * color_as_positive_or_negative == RANKS[piece_color]["promotion"]:
                            for promote_to in PROMOTE_TO:
                                moves.append(f"{capture_x_positive}={promote_to}-enpassant")
                        else:
                            moves.append(f"{capture_x_positive}-enpassant")
                elif target_piece["color"] != piece_color:
                    if y_position + 1 * color_as_positive_or_negative == RANKS[piece_color]["promotion"]:
                        for promote_to in PROMOTE_TO:
                            moves.append(f"{capture_x_positive}={promote_to}")
                    else:
                        moves.append(capture_x_positive)
        elif piece["type"] == "k": # KING
            for _move in KING_MOVES:
                new_pos = self.move_from_pos(pos, _move[0], _move[1])
                if new_pos != None:
                    target_piece = self.get_piece(new_pos)
                    if target_piece == None: moves.append(new_pos)
                    elif target_piece["color"] != piece_color: moves.append(new_pos)
            # Castling


            if only_captures == False: # If non capture moves are allowed
                ## Check validity
                if piece_color:
                    if self.get_piece("e1") != {"color": piece_color, "type": "k"}:
                        self.whiteOO, self.whiteOOO = False, False
                    if self.get_piece("h1") != {"color": piece_color, "type": "r"}:
                        self.whiteOO = False
                    if self.get_piece("a1") != {"color": piece_color, "type": "r"}:
                        self.whiteOOO = False
                else:
                    if self.get_piece("e8") != {"color": piece_color, "type": "k"}:
                        self.blackOO, self.blackOOO = False, False
                    if self.get_piece("h8") != {"color": piece_color, "type": "r"}:
                        self.blackOO = False
                    if self.get_piece("a8") != {"color": piece_color, "type": "r"}:
                        self.blackOOO = False

                if piece_color:
                    if self.whiteOO and self.is_in_check(piece_color) == False: # allowed and not in check
                        if self.get_piece("f1") == None and self.get_piece("g1") == None:
                            if self.is_in_danger("f1", piece_color) == False and self.is_in_danger("g1", piece_color) == False:
                                moves.append(f"OO")
                    if self.whiteOOO and self.is_in_check(piece_color) == False: # allowed and not in check
                        if self.get_piece("d1") == None and self.get_piece("c1") == None and self.get_piece("b1") == None:
                            if self.is_in_danger("d1", piece_color) == False and self.is_in_danger("c1", piece_color) == False:
                                moves.append(f"OOO")
                else:
                    if self.blackOO and self.is_in_check(piece_color) == False: # allowed and not in check
                        if self.get_piece("f8") == None and self.get_piece("g8") == None:
                            if self.is_in_danger("f8", piece_color) == False and self.is_in_danger("g8", piece_color) == False:
                                moves.append(f"OO")
                    if self.blackOOO and self.is_in_check(piece_color) == False: # allowed and not in check
                        if self.get_piece("d8") == None and self.get_piece("c8") == None and self.get_piece("b8") == None:
                            if self.is_in_danger("d8", piece_color) == False and self.is_in_danger("c8", piece_color) == False:
                                moves.append(f"OOO")
        elif piece["type"] == "n": # KNIGHT
            for _move in HORSEY_MOVES:
                new_pos = self.move_from_pos(pos, _move[0], _move[1])
                if new_pos != None: # Not Out of Bounds
                    target_piece = self.get_piece(new_pos)
                    # If Empty or Enemy Piece
                    if target_piece == None: moves.append(new_pos)
                    elif target_piece["color"] != piece_color: moves.append(new_pos)
        else: # Directional Pieces - Rook, Bishop, Queen
            if piece["type"] != "r": # DIAGONAL
                moves.extend(self.calculate_directional_move(pos, 1, 1))
                moves.extend(self.calculate_directional_move(pos, 1, -1))
                moves.extend(self.calculate_directional_move(pos, -1, 1))
                moves.extend(self.calculate_directional_move(pos, -1, -1))
            if piece["type"] != "b": # STRAIGHT
                moves.extend(self.calculate_directional_move(pos, 0, 1))
                moves.extend(self.calculate_directional_move(pos, 0, -1))
                moves.extend(self.calculate_directional_move(pos, 1, 0))
                moves.extend(self.calculate_directional_move(pos, -1, 0))
        
        if exclude_checks:
            result = []
            for move in moves:
                simulated_board = self.move_simulate(f"{pos}-{move}")
                if simulated_board.is_in_check(piece_color) == False:
                    result.append(move)
            return result
        
        return moves
    def get_all_possible_moves(self, color, only_captures = False, add_where_from = False, exclude_checks = False):
        pieces = self.get_pieces(color)
        moves = []
        for piece in pieces:
            if add_where_from:
                piece_moves = self.get_possible_moves(piece, only_captures=only_captures, exclude_checks=exclude_checks)
                for move in piece_moves:
                    moves.append(f"{piece}-{move}")
            else:
                moves.extend(self.get_possible_moves(piece, only_captures=only_captures, exclude_checks=exclude_checks))
        return moves

    def calculate_directional_move(self, pos, x, y):
        piece = self.get_piece(pos)
        if piece == None: raise Exception("No Piece")

        moves = []
        change = 1
        while True:
            new_pos = self.move_from_pos(pos, change*x, change*y)
            if new_pos == None: break # Out of Bounds
            target_piece = self.get_piece(new_pos)
            if target_piece == None: # Empty Tile
                moves.append(new_pos)
            else:
                if target_piece["color"] != piece["color"]: # Capture
                    moves.append(new_pos)
                break # Break either way (capture or blocked)
            change += 1
        return moves
    
    def move_from_pos(self, pos, x, y):
        pos_x = LETTERS.index(pos[0])
        pos_y = NUMBERS.index(pos[1])

        new_x = pos_x + x
        new_y = pos_y + y

        if new_x < 0 or new_x > 7 or new_y < 0 or new_y > 7: return None # Out of Bounds

        return f"{LETTERS[new_x]}{NUMBERS[new_y]}"

    ### CONTROLS ###
    def is_in_danger(self, pos, color):
        moves = self.get_all_possible_moves(color=not color, only_captures=True)
        for move in moves:
            if str(move).startswith(pos):
                return True
        return False
    def is_in_check(self, color):
        pieces = self.get_pieces(color)
        for piece in pieces:
            the_piece = self.get_piece(piece)
            if the_piece["type"] == "k":
                # CHECK IF KING IS IN DANGER AND RETURN
                return self.is_in_danger(piece, color)
        return False
    def is_in_checkmate(self, color):
        if self.is_in_check(color) == False: return False
        # TRY ALL POSSIBLE MOVES TO GET OUT OF CHECK
        possible_moves = self.get_all_possible_moves(color, only_captures=False, add_where_from=True)
        for move in possible_moves:
            simulated_board = self.move_simulate(move)
            if simulated_board.is_in_check(color) == False:
                return False
        return True

    ### NOTATION ###
    def convert_from_algebraic(self, move_in_algebraic, color):
        # remove + and # 
        move_in_algebraic = move_in_algebraic.replace("+", "").replace("#", "")

        if move_in_algebraic == "O-O": # Castle
            if color: return "e1-OO"
            else: return "e8-OO"
        elif move_in_algebraic == "O-O-O":
            if color: return "e1-OOO"
            else: return "e8-OOO"

        capturing = False
        piece = move_in_algebraic[0]
        notation_starts_from = 1
        if piece.isupper(): piece = piece.lower()
        else: 
            piece = "p"
            notation_starts_from = 0
        
        # Last 2 is the target
        promotion_split = move_in_algebraic.split("=")
        if len(promotion_split) > 1:
            promote_to = str(promotion_split[1]).lower()
        else:
            promote_to = None
        without_promotion = promotion_split[0]
        target_pos = without_promotion[-2:]

        rest_of_the_notation = without_promotion[notation_starts_from:-2]

        if "x" in rest_of_the_notation:
            capturing = True
        ambigious_solver = rest_of_the_notation.replace("x", "")

        # all_possible_moves = self.get_all_possible_moves(color, only_captures=False, add_where_from=True, exclude_checks=False)
        all_pieces = self.get_pieces(color)
        filtered_pieces = []
        for _piece in all_pieces:
            if self.get_piece(_piece)["type"] == piece:
                if ambigious_solver != None:
                    # print(f"{_piece}-{ambigious_solver}: {ambigious_solver in _piece}")
                    if ambigious_solver in _piece:
                        filtered_pieces.append(_piece)
                else:
                    filtered_pieces.append(_piece)
        # print(filtered_pieces)
        
        for _piece in filtered_pieces:
            possible_moves = self.get_possible_moves(_piece, only_captures=capturing)
            for move in possible_moves:
                if move[0:2] == target_pos:
                    return f"{_piece}-{move}"

        return f"Piece: {piece} - Target: {target_pos}- Promotion: {promote_to} - Ambigious_Solver: {ambigious_solver} - Couldn't solve: {move_in_algebraic}"    
    def convert_to_algebraic(self, move):
        # TODO
        pass

    ### COMPLEX CALCULATIONS ### TODO
    def get_attackers(self, pos, attacker_color, exclude_checks = False):
        piece = self.get_piece(pos)

        if piece == None: # Empty Tile
            attacker_pieces = self.get_pieces(attacker_color)
            attackers = []
            for attacker_piece in attacker_pieces:
                attacker_moves = self.get_possible_moves(attacker_piece, only_captures=True, exclude_checks=exclude_checks)
                for move in attacker_moves:
                    if move[0:2] == pos:
                        attackers.append(attacker_piece)
            

        
        if piece["color"] != attacker_color: # its own piece
            return []
        



    def get_defenders(self, pos, color):
        pass