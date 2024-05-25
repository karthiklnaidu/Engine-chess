class King:
    def __init__(self, color, square):
        # Initialize king attributes
        self.color = color
        self.position = square
        self.make_castle = True
        self.long_castling = True
        self.short_castling = True
        self.long_rook = 'a1' if color == 'white' else 'a8'
        self.short_rook = 'h8' if color == 'black' else 'h1'

    def move(self, player, game, from_square, to_square):
        # Check if the move is valid for a king
        to_position = get_position(to_square)
        difference = abs(from_square['value'] - to_square['value'])
        file_distance = abs(ord(from_square['file']) - ord(to_square['file']))
        rank_distance = abs(int(from_square['rank']) - int(to_square['rank']))

        # Normal king move (one square in any direction)
        if difference in (1, 10, 11, 9) and (file_distance <= 1 and rank_distance <= 1):
            if to_square['piece'] is not None and to_square['piece-color'] is not player:
                game.allocate_points(player, to_square, to_position)
                self.position = to_position
                return True
            else:
                self.position = to_position
                return True
        # Castling
        elif difference == 20 and not self.has_moved and to_square['piece'] is None:
            return True
        else:
            return False

class Queen:
    def __init__(self, color, square):
        # Initialize queen attributes
        self.color = color
        self.position = square
        self.value = 9
        self.on_board = True

    def move(self, player, game, from_square, to_square):
        # Check if the move is valid for a queen
        to_position = get_position(to_square)
        from_position = from_square['file'] + str(from_square['rank'])
        difference = abs(from_square['value'] - to_square['value'])
        diff = from_square['value'] - to_square['value']
        if from_square['piece'] == 'queen' and self.color == player:
            if (difference % 10 == 0 or difference <= 7) or (difference % 9 == 0 or difference % 11 == 0):
                if not game.anyPieceAtMiddle(from_position, to_position):
                    if(to_square['piece'] is not None):
                        game.allocate_points(player, to_square, to_position)
                        self.position = to_position
                        return True
                    else:
                        self.position = to_position
                        return True
        return False

class Rook:
    def __init__(self, color, square):
        # Initialize rook attributes
        self.color = color
        self.position = square
        self.value = 5
        self.on_board = True

    def move(self, player, game, from_square, to_square):
        # Check if the move is valid for a rook
        to_position = get_position(to_square)
        from_position = from_square['file'] + str(from_square['rank'])
        difference = abs(from_square['value'] - to_square['value'])
        diff = from_square['value'] - to_square['value']
        if from_square['piece'] == 'rook' and self.color == player:
            if difference % 10 == 0 or difference <= 7 and to_square['piece-color'] != player:
                if not game.anyPieceAtMiddle(from_position, to_position):
                    if(to_square['piece'] is not None):
                        game.allocate_points(player, to_square, to_position)
                        self.position = to_position
                        return True
                    else:
                        self.position = to_position
                        return True
        return False

class Bishop:
    def __init__(self,color, square):
        # Initialize bishop attributes
        self.color = color
        self.position = square
        self.value = 3
        self.on_board = True

    def move(self, player, game, from_square, to_square):
        # Check if the move is valid for a bishop
        to_position = get_position(to_square)
        from_position = from_square['file'] + str(from_square['rank'])
        difference = abs(from_square['value'] - to_square['value'])
        diff = from_square['value'] - to_square['value']
        if from_square['piece'] == 'bishop' and self.color == player:
            if (difference % 9 == 0 or difference % 11 == 0) and (to_square['piece-color'] != player):
                if not game.anyPieceAtMiddle(from_position, to_position):
                    if(to_square['piece'] is not None):
                        game.allocate_points(player, to_square, to_position)
                        self.position = to_position
                        return True
                    else:
                        self.position = to_position
                        return True
        return False

class Knight:
    def __init__(self, color, square):
        # Initialize knight attributes
        self.color = color
        self.position = square
        self.value = 3
        self.on_board = True

    def move(self, player, game, from_square, to_square):
        # Check if the move is valid for a knight
        to_position = get_position(to_square)
        difference = abs(from_square['value'] - to_square['value'])
        if (from_square['piece'] == 'knight') and (self.color == player):
            if difference in (21, 19, 12, 8) and to_square['piece-color'] != player:
                if(to_square['piece'] is not None):
                    game.allocate_points(player, to_square, to_position)
                    self.position = to_position
                    return True
                else:
                    self.position = to_position
                    return True
        return False

class Pawn:
    def __init__(self, color, square):
        # Initialize pawn attributes
        self.color = color
        self.position = square
        self.value = 1
        self.on_board = True
        self.can_jump = True # At initial position a pawn can jump to two squares
        self.en_passant_vurnerable = False

    def move(self, player, game, from_square, to_square):
        # Get the difference between square values
        to_position = get_position(to_square)
        difference = abs(from_square['value'] - to_square['value'])
        
        # Check if the move is valid for a pawn
        if from_square['piece'] == 'pawn' and self.color == player:
            if difference in (20, 11, 10, 9):
                # Moving forward
                self.position = to_position
                if difference == 20 and self.can_jump and to_square['piece'] is None:
                    self.en_passant_vurnerable = True
                    return True
                elif to_square['piece'] is None and difference == 10:
                    self.can_jump = False
                    return True
                # Capturing
                elif difference in (11, 9):
                    if to_square['piece'] is not None and to_square['piece-color'] != player:
                        game.allocate_points(player, to_square, to_position)
                        self.can_jump = False
                        return True
        return False
    
def get_position(square):
    file = square['file']
    rank = square['rank']
    return file + str(rank)

