default_pieces = {
    # White Others
    "a1": {"color": True, "type": "r"},
    "b1": {"color": True, "type": "n"},
    "c1": {"color": True, "type": "b"},
    "d1": {"color": True, "type": "q"},
    "e1": {"color": True, "type": "k"},
    "f1": {"color": True, "type": "b"},
    "g1": {"color": True, "type": "n"},
    "h1": {"color": True, "type": "r"},
    # White Pawns
    "a2": {"color": True, "type": "p"},
    "b2": {"color": True, "type": "p"},
    "c2": {"color": True, "type": "p"},
    "d2": {"color": True, "type": "p"},
    "e2": {"color": True, "type": "p"},
    "f2": {"color": True, "type": "p"},
    "g2": {"color": True, "type": "p"},
    "h2": {"color": True, "type": "p"},
    # Black Others
    "a8": {"color": False, "type": "r"},
    "b8": {"color": False, "type": "n"},
    "c8": {"color": False, "type": "b"},
    "d8": {"color": False, "type": "q"},
    "e8": {"color": False, "type": "k"},
    "f8": {"color": False, "type": "b"},
    "g8": {"color": False, "type": "n"},
    "h8": {"color": False, "type": "r"},
    # Black Pawns
    "a7": {"color": False, "type": "p"},
    "b7": {"color": False, "type": "p"},
    "c7": {"color": False, "type": "p"},
    "d7": {"color": False, "type": "p"},
    "e7": {"color": False, "type": "p"},
    "f7": {"color": False, "type": "p"},
    "g7": {"color": False, "type": "p"},
    "h7": {"color": False, "type": "p"},
}

piece_types = {
    "r": {
        "name": "Rook",
        "points": 5,
        "move": [
            {"type": "direction", "x": 1, "y": 0, "capture": True, "move": True},
            {"type": "direction", "x": -1, "y": 0, "capture": True, "move": True},
            {"type": "direction", "x": 0, "y": 1, "capture": True, "move": True},
            {"type": "direction", "x": 0, "y": -1, "capture": True, "move": True},
        ]
    },
    "b": {
        "name": "Bishop",
        "points": 3,
        "move": [
            {"type": "direction", "x": 1, "y": 1, "capture": True, "move": True},
            {"type": "direction", "x": -1, "y": 1, "capture": True, "move": True},
            {"type": "direction", "x": 1, "y": -1, "capture": True, "move": True},
            {"type": "direction", "x": -1, "y": -1, "capture": True, "move": True},
        ]
    },
    "n": {
        "name": "Knight",
        "points": 3,
        "move": [
            {"type": "position", "x": 1, "y": 2, "capture": True, "move": True},
            {"type": "position", "x": -1, "y": 2, "capture": True, "move": True},

            {"type": "position", "x": 1, "y": -2, "capture": True, "move": True},
            {"type": "position", "x": -1, "y": -2, "capture": True, "move": True},

            {"type": "position", "x": -2, "y": -1, "capture": True, "move": True},
            {"type": "position", "x": -2, "y": 1, "capture": True, "move": True},

            {"type": "position", "x": 2, "y": -1, "capture": True, "move": True},
            {"type": "position", "x": 2, "y": 1, "capture": True, "move": True}
        ]
    },
    "q": {
        "name": "Queen",
        "points": 9,
        "move": [
            {"type": "direction", "x": 1, "y": 0, "capture": True, "move": True},
            {"type": "direction", "x": -1, "y": 0, "capture": True, "move": True},
            {"type": "direction", "x": 0, "y": 1, "capture": True, "move": True},
            {"type": "direction", "x": 0, "y": -1, "capture": True, "move": True},
            {"type": "direction", "x": 1, "y": 1, "capture": True, "move": True},
            {"type": "direction", "x": -1, "y": 1, "capture": True, "move": True},
            {"type": "direction", "x": 1, "y": -1, "capture": True, "move": True},
            {"type": "direction", "x": -1, "y": -1, "capture": True, "move": True},
        ]
    },
    "k": {
        "name": "King",
        "points": 0,
        "move": [
            {"type": "position", "x": 1, "y": 0, "capture": True, "move": True},
            {"type": "position", "x": -1, "y": 0, "capture": True, "move": True},
            {"type": "position", "x": 0, "y": 1, "capture": True, "move": True},
            {"type": "position", "x": 0, "y": -1, "capture": True, "move": True},
            {"type": "position", "x": 1, "y": 1, "capture": True, "move": True},
            {"type": "position", "x": -1, "y": 1, "capture": True, "move": True},
            {"type": "position", "x": 1, "y": -1, "capture": True, "move": True},
            {"type": "position", "x": -1, "y": -1, "capture": True, "move": True},
        ]
    },
    "p": {
        "name": "Pawn",
        "points": 1,
        "move": [
            {"type": "position", "x": 0, "y": 1, "capture": False, "move": True},
            {"type": "position", "x": 1, "y": 1, "capture": True, "move": False},
            {"type": "position", "x": -1, "y": 1, "capture": True, "move": False}
        ]
    }
}

class Board:
    # True is white, False is black
    whiteOO = True
    blackOO = True
    whiteOOO = True
    blackOOO = True

    turn = True
    pieces = {}
    history = []

    def __str__(self):
        return f"Chess Board. Turn: {('White' if self.turn else 'Black')}.\nBlack Castle: {self.blackOO} {self.blackOOO}\nWhite Castle: {self.whiteOO} {self.whiteOOO}\n\n{self.print_board()}"

    def __init__(self, turn: bool = True, pieces: dict = default_pieces, history: list = [], whiteOO: bool = True, blackOO: bool = True, whiteOOO: bool = True, blackOOO: bool = True):
        self.pieces = pieces
        self.turn = turn
        self.history = history

        whiteOO_validity = False
        if "e1" in pieces and "h1" in pieces:
            whiteOO_validity = pieces["e1"]["type"] == "k" and pieces["h1"]["type"] == "r"

        blackOO_validity = False
        if "e8" in pieces and "h8" in pieces:
            blackOO_validity = pieces["e8"]["type"] == "k" and pieces["h8"]["type"] == "r"

        whiteOOO_validity = False
        if "e1" in pieces and "a1" in pieces:
            whiteOOO_validity = self.pieces["e1"]["type"] == "k" and self.pieces["a1"]["type"] == "r"

        blackOOO_validity = False
        if "e8" in pieces and "a8" in pieces:
            blackOOO_validity = self.pieces["e8"]["type"] == "k" and self.pieces["a8"]["type"] == "r"

        self.whiteOO = whiteOO and whiteOO_validity
        self.blackOO = blackOO and blackOO_validity
        self.whiteOOO = whiteOOO and whiteOOO_validity
        self.blackOOO = blackOOO and blackOOO_validity

    def move(self, the_move, color: bool = None, willCheck: bool = True):
        splitted = the_move.split("-")
        outgoing = "-".join(splitted[1:])
        piece_type = self.pieces[splitted[0]]["type"]

        if willCheck:
            if color != self.turn: return "Invalid Move - Not your turn", False

            possible_moves = self.list_moves(splitted[0], self.turn)

            if outgoing not in possible_moves: return "Invalid Move - Not Possible", False
            
            simulated_board_check = self.move_simulate(f"{splitted[0]}-{outgoing}", color).is_check(color)
            if simulated_board_check: return "Invalid Move - Checked", False


            print("Move from", splitted[0], "to", outgoing)
        # else:
        #     print("Simulated move from", splitted[0], "to", outgoing)
        # Move the piece
        if len(splitted) > 2: # Pawn Stuff (EP & Promotion)
            if splitted[2] == "ep":
                # En passant
                _from = splitted[0]
                _to = splitted[1]
                print("From:", _from, "To:", _to)

                letter_of_to = _to[0]
                number_of_from = _from[1]

                en_passanted_pos = f"{letter_of_to}{number_of_from}"

                self.pieces.pop(splitted[0])
                self.pieces.pop(en_passanted_pos)
                self.pieces[splitted[1]] = {"color": color, "type": "p"}

                print("OMG! EN PASSANT!")
                # print("En passant bitch")
                # exit()
            else:
                # Promotion
                self.pieces.pop(splitted[0])
                self.pieces[splitted[1]] = {"color": color, "type": splitted[2]}
        elif outgoing == "OO":
            number = "1" if color else "8"
            king_letter = "e"
            rook_letter = "h"

            king_new_letter = "g"
            rook_new_letter = "f"
            
            # Remove rook and king
            self.pieces.pop(f"{king_letter}{number}")
            self.pieces.pop(f"{rook_letter}{number}")
            # Put the new rook and king
            self.pieces[f"{king_new_letter}{number}"] = {"color": color, "type": "k"}
            self.pieces[f"{rook_new_letter}{number}"] = {"color": color, "type": "r"}

            if color:
                self.whiteOO = False
                self.whiteOOO = False
            else:
                self.blackOO = False
                self.blackOOO = False
        elif outgoing == "OOO":
            number = "1" if color else "8"
            king_letter = "e"
            rook_letter = "a"
            king_new_letter = "c"
            rook_new_letter = "d"

            # Remove rook and king
            self.pieces.pop(f"{king_letter}{number}")
            self.pieces.pop(f"{rook_letter}{number}")
            # Put the new rook and king
            self.pieces[f"{king_new_letter}{number}"] = {"color": color, "type": "k"}
            self.pieces[f"{rook_new_letter}{number}"] = {"color": color, "type": "r"}
            # Disable Castling
            if color:
                self.whiteOO = False
                self.whiteOOO = False
            else:
                self.blackOO = False
                self.blackOOO = False
        else:
            # Disable Castling
            if piece_type == "k":
                if color:
                    self.whiteOO = False
                    self.whiteOOO = False
                else:
                    self.blackOO = False
                    self.blackOOO = False
            elif piece_type == "r":
                if color:
                    if splitted[0] == "a1":
                        self.whiteOOO = False
                    elif splitted[0] == "h1":
                        self.whiteOO = False
                else:
                    if splitted[0] == "a8":
                        self.blackOOO = False
                    elif splitted[0] == "h8":
                        self.blackOO = False

            # Normal Move
            self.pieces[splitted[1]] = {"color": color, "type": piece_type}
            self.pieces.pop(splitted[0])

            

        # Add to history
        self.history.append(f"{piece_type}-{the_move}")

        self.turn = not self.turn # Change turn
        return "Successful Move", True

    def move_simulate(self, the_move, color):
        # print("Simulated move from", pos_from, "to", pos_to)
        # print("Just Before")
        new_board = Board(self.turn, self.pieces.copy(), self.history.copy())
        new_board.move(the_move, color, False)
        # print("Just After")
        return new_board
    
    def print_board(self, bottom_color: bool = True):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
        result = ""
        if bottom_color: numbers.reverse()

        for a in numbers:
            for letter in letters:
                piece_pos = f"{letter}{a}"
                piece = self.pieces.get(piece_pos)
                if piece:
                    if piece["color"]:
                        result += piece["type"].upper()
                    else:
                        result += piece["type"]
                else:
                    result += "x"
            result += "\n"
        return result

    def get_piece(self, pos):
        return self.pieces.get(pos)
    
    def get_move_types(self, piece_type, piece_color, pos_in_xy, without_castle: bool = False):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        if piece_type == "p":
            move_types = piece_types[piece_type]["move"].copy()
            # new_move_types = []
            x = pos_in_xy[0]
            y = pos_in_xy[1]

            # 2 steps forward
            if y == 1 and piece_color and self.get_piece(f"{letters[x]}{y + 2}") == None or y == 6 and not piece_color and self.get_piece(f"{letters[x]}{y}") == None:
                move_types.append({"type": "position", "x": 0, "y": 2, "capture": False, "move": True})
            # Promotion
            elif y == 6 and piece_color or y == 1 and not piece_color:
                move_types = []
                possible_promotions = ["q", "r", "b", "n"]
                for promotion in possible_promotions:
                    move_types.append({"type": "position", "x": 0, "y": 1, "capture": False, "move": True, "promotion": promotion})
                    move_types.append({"type": "position", "x": 1, "y": 1, "capture": True, "move": False, "promotion": promotion})
                    move_types.append({"type": "position", "x": -1, "y": 1, "capture": True, "move": False, "promotion": promotion})
            # En passant
            elif (y == 3 and not piece_color) or (y == 4 and piece_color):
                if len(self.history) > 0:
                    last_move = self.history[-1]
                    the_x_change = -1

                    _possible_letters = []
                    if x > 0: _possible_letters.append(letters[x - 1])
                    if x < 7: _possible_letters.append(letters[x + 1])

                    for a in _possible_letters:
                        if last_move == f"p-{a}{y - 2}-{a}{y + 1}" or last_move == f"p-{a}{y + 3}-{a}{y + 1}":
                            move_types.append({"type": "position", "x": the_x_change, "y": 1, "capture": True, "move": False, "en_passant": f"{a}{y}"})
                            the_x_change = 1
            final_move_types = move_types.copy()
        
        elif piece_type == "k":
            # move_types = piece_types[piece_type]["move"]
            move_types = piece_types[piece_type]["move"].copy()
            the_OO = self.whiteOO if piece_color else self.blackOO
            the_OOO = self.whiteOOO if piece_color else self.blackOOO

            if the_OO and not without_castle:
                if piece_color:
                    if self.get_piece("f1") == None and self.get_piece("g1") == None:
                        if not self.is_check(color=self.turn):
                            move_types.append({"type": "castle", "side": "OO"})
                else:
                    if self.get_piece("f8") == None and self.get_piece("g8") == None:
                        if not self.is_check(color=self.turn):
                            move_types.append({"type": "castle", "side": "OO"})     
            if the_OOO and not without_castle:
                if piece_color:
                    if self.get_piece("b1") == None and self.get_piece("c1") == None and self.get_piece("d1") == None:
                        if not self.is_check(color=self.turn):
                            move_types.append({"type": "castle", "side": "OOO"})
                else:
                    if self.get_piece("b8") == None and self.get_piece("c8") == None and self.get_piece("d8") == None:
                        if not self.is_check(color=self.turn):
                            move_types.append({"type": "castle", "side": "OOO"})
            final_move_types = move_types.copy()
        else:
            move_types = piece_types[piece_type]["move"]
            final_move_types = move_types.copy()
        return final_move_types

    def list_moves(self, pos, turn: bool, without_castle: bool = False):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        piece = self.pieces.get(pos)
        if not piece: return []
        
        piece_type = piece["type"]
        piece_color = piece["color"]

        if turn is not None and piece_color != turn: return []

        pos_in_xy = (letters.index(pos[0]), int(pos[1]) - 1)

        if piece_type not in piece_types: return []

        moves = []
        
        move_types = self.get_move_types(piece_type, piece_color, pos_in_xy, without_castle)

        for move_type in move_types:
            if move_type["type"] == "castle":
                moves.append(f"{move_type['side']}")
            elif move_type["type"] == "direction":
                multiplier = 1 if piece_color else -1
                x = pos_in_xy[0] # x
                y = pos_in_xy[1] # y
                while True:
                    x += move_type["x"] * multiplier
                    y += move_type["y"] * multiplier
                    if x < 0 or x > 7 or y < 0 or y > 7: break
                    piece = self.get_piece(f"{letters[x]}{y + 1}")
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
                    piece = self.get_piece(f"{letters[x]}{y + 1}")
                    if move_type["capture"]:
                        if piece != None:
                            if piece["color"] != piece_color:
                                moves.append(f"{letters[x]}{y + 1}-{move_type['promotion']}")
                                # moves.append(f"{letters[x]}{y + 1}")
                    elif move_type["move"]:
                        if piece == None:
                            # moves.append(f"{letters[x]}{y + 1}")
                            moves.append(f"{letters[x]}{y + 1}-{move_type['promotion']}")
                    else:
                        print("wtf? x2")
                else:
                    piece = self.get_piece(f"{letters[x]}{y + 1}")
                    if move_type["move"] and move_type["capture"]:
                        if piece != None:
                            if piece["color"] != piece_color:
                                moves.append(f"{letters[x]}{y + 1}")
                        else:
                            moves.append(f"{letters[x]}{y + 1}")
                    elif move_type["move"]:
                        if piece == None:
                            moves.append(f"{letters[x]}{y + 1}")
                    elif move_type["capture"]:
                        if piece != None:
                            if piece["color"] != piece_color:
                                moves.append(f"{letters[x]}{y + 1}")
                    else:
                        print("wtf?")
        # print("moves:", moves)
        return moves

    def is_check(self, color: bool):
        # Get King Position
        king_pos = None
        for piece in self.pieces:
            if self.pieces[piece] == {"color": color, "type": "k"}:
                king_pos = piece
                break
        if not king_pos: return False # No King Found
        
        # Check if any piece can capture the king
        opponent_pieces = self.get_pieces(not color)
        for piece in opponent_pieces:
            if self.pieces[piece]["type"] == "k": continue
            moves = self.list_moves(piece, not color, True)
            for move in moves:
                splitted = move.split("-")
                if splitted[0] == king_pos: return True
        return False
    
    def is_checkmate(self, color: bool):
        if not self.is_check(color): return False # Not even checked

        pieces = self.get_pieces(color)
        # print(pieces)
        # print(self.list_moves("e8", color))
        # exit()
        for piece in pieces:
            moves = self.list_moves(piece, color, True)
            for move in moves:
                print("Possible Move to Escape:", f"{piece}-{move}")
                simulated_board = self.move_simulate(f"{piece}-{move}", color)
                if not simulated_board.is_check(color):
                    return False
        return True

    def get_pieces(self, filter):
        if filter == None:
            return self.pieces
        else:
            result = []
            for piece in self.pieces:
                if self.pieces[piece]["color"] == filter:
                    result.append(piece)
            return result
