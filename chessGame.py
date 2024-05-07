import initBoard as chessBoard

class Player:
    def __init__(self):
        # Initialize player points
        self.points = {'white': 0, 'black': 0}

class King:
    def __init__(self, color, square):
        # Initialize king attributes
        self.color = color
        self.position = square
        self.can_castle = True
        self.long_castling = True
        self.short_castling = True

    def move(self, player, from_square, to_square, to_position):
        # Check if the move is valid for a king
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

    def move(self, player, from_square, to_square, to_position):
        # Check if the move is valid for a queen
        difference = abs(from_square['value'] - to_square['value'])
        if from_square['piece'] == 'queen' and self.color == player:
            if (difference % 10 == 0 or difference <= 7) or (difference % 9 == 0 or difference % 11 == 0):
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

    def move(self, player, from_square, to_square, to_position):
        # Check if the move is valid for a rook
        difference = abs(from_square['value'] - to_square['value'])
        if from_square['piece'] == 'rook' and self.color == player:
            if difference % 10 == 0 or difference <= 7 and to_square['piece-color'] != player:
                if(to_square['piece'] is not None):
                    game.allocate_points(player, to_square, to_position)
                    self.position = to_position
                    return True
                else:
                    self.position = to_position
                    return True
        return False

class Bishop:
    def __init__(self, color, square):
        # Initialize bishop attributes
        self.color = color
        self.position = square
        self.value = 3
        self.on_board = True

    def move(self, player, from_square, to_square, to_position):
        # Check if the move is valid for a bishop
        difference = abs(from_square['value'] - to_square['value'])
        if from_square['piece'] == 'bishop' and self.color == player:
            if (difference % 9 == 0 or difference % 11 == 0) and (to_square['piece-color'] != player):
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

    def move(self, player, from_square, to_square, to_position):
        # Check if the move is valid for a knight
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

    def move(self, player, from_square, to_square, to_position):
        # Get the difference between square values
        difference = abs(from_square['value'] - to_square['value'])
        
        # Check if the move is valid for a pawn
        if from_square['piece'] == 'pawn' and self.color == player:
            if difference in (20, 11, 10, 9):
                # Moving forward
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

class GamePlay:
    def __init__(self):
        self.current_player = 'white'
        # Pawns instances
        self.white_pawns = [Pawn("white", 'a2'), Pawn('white', 'b2'), Pawn("white", 'c2'), Pawn('white', 'd2'),
                            Pawn("white", 'e2'), Pawn('white', 'f2'), Pawn("white", 'g2'), Pawn('white', 'h2')]
        self.black_pawns = [Pawn("black", 'a7'), Pawn('black', 'b7'), Pawn("black", 'c7'), Pawn('black', 'd7'),
                            Pawn("black", 'e7'), Pawn('black', 'f7'), Pawn("black", 'g7'), Pawn('black', 'h7')]
        # Knight instances
        self.white_knight = [Knight("white", 'b1'), Knight('white', 'g1')]
        self.black_knight = [Knight('black', 'b8'), Knight('black', 'g8')]
        # Bishop instances
        self.white_bishop = [Bishop("white", 'c1'), Bishop('white', 'f1')]
        self.black_bishop = [Bishop('black', 'c8'), Bishop('black', 'f8')]
        # Rook instances
        self.white_rook = [Rook('white', 'a1'), Rook('white', 'h1')]
        self.black_rook = [Rook('black', 'a8'), Rook('black', 'h8')]
        # Queen instance
        self.white_queen = Queen('white', 'd1')
        self.black_queen = Queen('black', 'd8')
        # King instances
        self.white_king = King('white', 'e1')
        self.black_king = King('black', 'e8')

        # Initialize the chessboard
        self.board = chessBoard.ChessBoard()
        self.board.initializePieces()

    def allocate_points(self, player, to_square, to_position):
        # Allocate points when a piece is captured
        opponent = 'black' if player == 'white' else 'white'
        if to_square['piece'] == 'pawn':
            for pawn in getattr(self, f'{opponent}_pawns'):
                if pawn.position == to_position:
                    pawn.on_board = False
                    player_points.points[player] += 1
                    player_points.points[opponent] -= 1
        elif to_square['piece'] == 'knight':
            for knight in getattr(self, f'{opponent}_knight'):
                if knight.position == to_position:
                    knight.on_board = False
                    player_points.points[player] += 3
                    player_points.points[opponent] -= 3
        elif to_square['piece'] == 'bishop':
            for bishop in getattr(self, f'{opponent}_bishop'):
                if bishop.position == to_position:
                    bishop.on_board = False
                    player_points.points[player] += 3
                    player_points.points[opponent] -= 3
        elif to_square['piece'] == 'rook':
            for rook in getattr(self, f'{opponent}_rook'):
                if rook.position == to_position:
                    rook.on_board = False
                    player_points.points[player] += 5
                    player_points.points[opponent] -= 5
        elif to_square['piece'] == 'queen':
            queen = getattr(self, f'{opponent}_queen')
            if queen.position == to_position:
                queen.on_board = False
                player_points.points[player] += 9
                player_points.points[opponent] -= 9
        else:
            exit(1)


    def move_piece(self, from_square, to_square):
        # Move a piece from one square to another
        if self.is_valid_move(from_square, to_square):
            # Get the piece to move
            piece_to_move = self.board[from_square]['piece']
            if piece_to_move is not None:
                # Update the destination square with the piece
                self.board[to_square]['piece'] = piece_to_move
                self.board[to_square]['piece-color'] = self.current_player
                # Empty the source square
                self.board[from_square]['piece'] = None
                self.board[from_square]['piece-color'] = None
                # Update the pawn's position and status
                for pawns in (self.white_pawns, self.black_pawns):
                    for pawn in pawns:
                        if pawn.position == from_square:
                            pawn.position = to_square
                            pawn.has_moved = True
                            break
                # Switch the player turn
                self.current_player = 'black' if self.current_player == 'white' else 'white'
            else:
                print("No piece at the starting position.")
        else:
            print("Invalid move!")

    def is_valid_move(self, from_square, to_square):
        # Check if the move is valid
        if self.board[from_square]['piece'] == 'pawn':
            for pawn in getattr(self, f'{self.current_player}_pawns'):
                if pawn.position == from_square:
                    return pawn.move(self.current_player, self.board[from_square], self.board[to_square], to_square)
        elif self.board[from_square]['piece'] == 'knight':
            for knight in getattr(self, f'{self.current_player}_knight'):
                if knight.position == from_square:
                    return knight.move(self.current_player, self.board[from_square], self.board[to_square], to_square)
        elif self.board[from_square]['piece'] == 'bishop':
            for bishop in getattr(self, f'{self.current_player}_bishop'):
                if bishop.position == from_square:
                    return bishop.move(self.current_player, self.board[from_square], self.board[to_square], to_square)
        elif self.board[from_square]['piece'] == 'rook':
            for rook in getattr(self, f'{self.current_player}_rook'):
                if rook.position == from_square:
                    return rook.move(self.current_player, self.board[from_square], self.board[to_square], to_square)
        elif self.board[from_square]['piece'] == 'queen':
            queen = getattr(self, f'{self.current_player}_queen')
            if queen.position == from_square:
                return queen.move(self.current_player, self.board[from_square], self.board[to_square], to_square)
        elif self.board[from_square]['piece'] == 'king':
            king = getattr(self, f'{self.current_player}_king')
            if king.position == from_square:
                return king.move(self.current_player, self.board[from_square], self.board[to_square], to_square) 
        return False       

    def print_board(self):
        # Print the current state of the chessboard
        for rank in range(8, 0, -1):
            for file in range(97, 105):  # ASCII values for 'a' to 'h'
                square_name = chr(file) + str(rank)
                flag = self.board[square_name]['piece']
                if(flag == 'pawn'):
                    piece = 'P'
                elif flag == 'knight':
                    piece = 'N'
                elif flag == 'bishop':
                    piece = 'B'
                elif flag == 'rook':
                    piece = 'R'
                elif flag == 'queen':
                    piece = 'Q'
                elif flag == 'king':
                    piece = 'K'
                else:
                    piece = flag
                print(piece if piece else ' ', end=" ")
            print()

# Initialize player points
player_points = Player()
# Start the game
game = GamePlay()

# Print the initial board state
print("Initial Board:")
game.print_board()

game.move_piece('e2', 'e4')
print("\nBoard after moving white pawn from e2 to e4:")
game.print_board()

game.move_piece('e7', 'e5')
print("\nBoard after moving black pawn from e7 to e5:")
game.print_board()

game.move_piece('f1', 'c4')
print("\nBoard after moving bishop from f1 to c4:")
game.print_board()

game.move_piece('d7', 'd6')
print("\nBoard after moving pawn from d7 to d6:")
game.print_board()

game.move_piece('d1', 'f3')
print("\nBoard after moving queen from d1 to f3")
game.print_board()

game.move_piece('b8', 'c6')
print("\nBoard after moving knight queen from b8 to c6")
game.print_board()

game.move_piece('f3', 'f7')
print("\nBoard after moving queen f3 to f7")
game.print_board()

# Print player points
print("\nPlayer Points:")
print("White:", player_points.points['white'])
print("Black:", player_points.points['black'])

