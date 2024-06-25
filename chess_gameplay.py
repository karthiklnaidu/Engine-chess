import Board as cb
import Pieces as piece
import sys

class Player:
    def __init__(self):
        # Initialize player points
        self.points = {'white': 0, 'black': 0}

class GamePlay:
    def __init__(self):
        self.current_player = 'white'
        # pawn instances
        self.white_pawn = [piece.Pawn("white", 'a2'), piece.Pawn('white', 'b2'), piece.Pawn("white", 'c2'), piece.Pawn('white', 'd2'),
                            piece.Pawn("white", 'e2'), piece.Pawn('white', 'f2'), piece.Pawn("white", 'g2'), piece.Pawn('white', 'h2')]
        self.black_pawn = [piece.Pawn("black", 'a7'), piece.Pawn('black', 'b7'), piece.Pawn("black", 'c7'), piece.Pawn('black', 'd7'),
                            piece.Pawn("black", 'e7'), piece.Pawn('black', 'f7'), piece.Pawn("black", 'g7'), piece.Pawn('black', 'h7')]
        # piece.Knight instances
        self.white_knight = [piece.Knight("white", 'b1'), piece.Knight('white', 'g1')]
        self.black_knight = [piece.Knight('black', 'b8'), piece.Knight('black', 'g8')]
        # piece.Bishop instances
        self.white_bishop = [piece.Bishop("white", 'c1'), piece.Bishop('white', 'f1')]
        self.black_bishop = [piece.Bishop('black', 'c8'), piece.Bishop('black', 'f8')]
        # piece.Rook instances
        self.white_rook = [piece.Rook('white', 'a1'), piece.Rook('white', 'h1')]
        self.black_rook = [piece.Rook('black', 'a8'), piece.Rook('black', 'h8')]
        # piece.Queen instance
        self.white_queen = [piece.Queen('white', 'd1')]
        self.black_queen = [piece.Queen('black', 'd8')]
        # piece.King instances
        self.white_king = piece.King('white', 'e1')
        self.black_king = piece.King('black', 'e8')

        # Initialize the chessboard
        self.board = cb.ChessBoard()
        self.board.initializePieces()
        
    def allocate_points(self, player, to_square, to_position):
        # Allocate points when a piece is captured
        opponent = 'black' if player == 'white' else 'white'
        if to_square['piece'] == 'pawn':
            for pawn in getattr(self, f'{opponent}_pawn'):
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
            for queen in getattr(self, f'{opponent}_queen'):
                if queen.position == to_position:
                    queen.on_board = False
                    player_points.points[player] += 9
                    player_points.points[opponent] -= 9
        else:
            exit("something went wrong while allocating points..")

    def anyPieceAtMiddle(self, attacker_square, target_square):
            attacker_file, attacker_rank = ord(attacker_square[0]), int(attacker_square[1])
            target_file, target_rank = ord(target_square[0]), int(target_square[1])

            file_diff = target_file - attacker_file
            rank_diff = target_rank - attacker_rank

            # Check if the move is straight
            if file_diff == 0 or rank_diff == 0:
                step_file = 0 if file_diff == 0 else int(file_diff / abs(file_diff))
                step_rank = 0 if rank_diff == 0 else int(rank_diff / abs(rank_diff))

            # Check if the move is diagonal
            elif abs(file_diff) == abs(rank_diff):
                step_file = int(file_diff / abs(file_diff))
                step_rank = int(rank_diff / abs(rank_diff))

            else:
                return False  # Invalid move direction

            current_file, current_rank = attacker_file + step_file, attacker_rank + step_rank
            while (current_file != target_file or current_rank != target_rank):
                square = chr(current_file) + str(current_rank)
                if square in self.board.board and self.board.board[square]['piece'] is not None:
                    return True
                current_file += step_file
                current_rank += step_rank

            return False

    def is_legal_escape(self, square, player_color):
        for _ in self.board.board:
            if _ == square:
                if self.board[square]['piece-color'] is not player_color and not self.is_check(player_color, square):
                   return True
        return False
    
    def get_attacker(self, player_color, king_position):
        for square_name in self.board.board:
            square = self.board[square_name]
            # Check if the square contains an opponent's piece
            if square['piece-color'] != player_color and square['piece'] is not None:
                # Check if the opponent's piece can attack the king's position
                if self.can_attack(square, king_position):
                    attacker = square['file'] + str(square['rank'])
                    return attacker
        return None
    
    def is_able_to_obstruct(self, player_color, king_position, attacker_position):
        target = self.board.board[king_position]
        attacker = self.board.board[attacker_position]
        difference = target['value'] - attacker['value']
        
        target_file, target_rank = ord(target['file']), int(target['rank'])
        attacker_file, attacker_rank = ord(attacker['file']), int(attacker['rank'])

        file_direction = 1 if attacker_file - target_file > 0 else -1
        rank_direction = 1 if attacker_rank - target_rank > 0 else -1

        if abs(difference) % 9 == 0 or abs(difference) % 11 == 0:
            while True:
                target_file += file_direction
                target_rank += rank_direction
                square_to_obstruct = chr(target_file) + str(target_rank)

                for square_name in self.board.board:
                    piece_to_obstruct = self.board[square_name]
                    if piece_to_obstruct['piece-color'] == player_color and piece_to_obstruct['piece'] != 'king':
                        if self.can_attack(piece_to_obstruct, square_to_obstruct):
                            return True
                if(square_to_obstruct == attacker_position):
                    return False
        elif abs(difference) % 10 == 0 or abs(difference) <= 7:
            if attacker_file - target_file == 0:
                target_file, target_rank = ord(target['file']), int(target['rank'])
                attacker_file, attacker_rank = ord(attacker['file']), int(attacker['rank'])
                while True:
                    target_rank += rank_direction
                    square_to_obstruct = chr(target_file) + str(target_rank)

                    for square_name in self.board.board:
                        piece_to_obstruct = self.board[square_name]
                        if piece_to_obstruct['piece-color'] == player_color and piece_to_obstruct['piece'] is not 'king':
                            if self.can_attack(piece_to_obstruct, square_to_obstruct):
                                return True
                    if(square_to_obstruct == attacker_position):
                        return False
            else:
                while True:
                    target_file, target_rank = ord(target['file']), int(target['rank'])
                    attacker_file, attacker_rank = ord(attacker['file']), int(attacker['rank'])
                    target_file += file_direction
                    square_to_obstruct = chr(target_file) + str(target_rank)

                    for square_name in self.board.board:
                        piece_to_obstruct = self.board[square_name]
                        if piece_to_obstruct['piece-color'] == player_color and piece_to_obstruct['piece'] is not None:
                            if self.can_attack(piece_to_obstruct, square_to_obstruct):
                                return True
                    if(square_to_obstruct == attacker_position):
                        return False



    def is_checkmate(self, player_color, king_position):
        file, rank = king_position[0], int(king_position[1])
        attacker_position = self.get_attacker(player_color, king_position)

        x = ord(file) + 1
        square1 = str(chr(x)) + str(rank)
        square2 = str(chr(x)) + str(rank+1)
        square3 = chr(x) + str(rank-1)
        x = ord(file)
        square4 = chr(x) + str(rank+1)
        square5 = chr(x) + str(rank-1)
        x = ord(file) - 1
        square6 = chr(x) + str(rank)
        square7 = chr(x) + str(rank+1)
        square8 = chr(x) + str(rank-1)

        if self.is_legal_escape(square1, player_color):
            return False
        elif self.is_legal_escape(square2, player_color):
            return False
        elif self.is_legal_escape(square3, player_color):
            return False
        elif self.is_legal_escape(square4, player_color):
            return False
        elif self.is_legal_escape(square5, player_color):
            return False
        elif self.is_legal_escape(square6, player_color):
            return False
        elif self.is_legal_escape(square7, player_color):
            return False
        elif self.is_legal_escape(square8, player_color):
            return False
        elif self.is_able_to_obstruct(player_color, king_position, attacker_position):
            return False
        else:
            return True        

    def is_check(self, player_color, king_position):
        # Iterate through all squares on the board
        for square_name in self.board.board:
            square = self.board[square_name]
            # Check if the square contains an opponent's piece
            if square['piece-color'] != player_color and square['piece'] is not None:
                # Check if the opponent's piece can attack the king's position
                if self.can_attack(square, king_position):
                    return True
        return False

    def can_attack(self, attacker_square, target_position):
        # Check if the attacker on 'attacker_square' can attack the target position
        attacker_piece = attacker_square['piece']
        # attacker_color = attacker_square['piece-color']
        attacker_position = attacker_square['file'] + str(attacker_square['rank'])

        # Check if the attacker can move to the target position
        if attacker_piece == 'pawn':
            return self.pawn_can_attack(attacker_position, target_position)
        elif attacker_piece == 'knight':
            return self.knight_can_attack(attacker_position, target_position)
        elif attacker_piece == 'bishop':
            return self.bishop_can_attack(attacker_position, target_position)
        elif attacker_piece == 'rook':
            return self.rook_can_attack(attacker_position, target_position)
        elif attacker_piece == 'queen':
            return self.queen_can_attack(attacker_position, target_position)
        elif attacker_piece == 'king':
            return self.king_can_attack(attacker_position, target_position)
        exit("something went wrong in can_attack()...")
        
    def pawn_can_attack(self, pawn_position, target_square):
        """
        Check if a pawn at the given position can attack the target square.

        Parameters:
        - pawn_position (str): Position of the pawn (e.g., 'a2')
        - target_square (str): Target square to check (e.g., 'b3')

        Returns:
        - bool: True if the pawn can attack the target square, False otherwise.
        """
        # Get the file and rank of the pawn position and target square
        pawn_file, pawn_rank = pawn_position[0], int(pawn_position[1])
        target_file, target_rank = target_square[0], int(target_square[1])

        # Determine the direction of the pawn based on its color
        if self.board[pawn_position]['piece-color'] == 'white':
            direction = 1  # White pawn move upwards
        else:
            direction = -1  # Black pawn move downwards

        # Calculate the file and rank differences
        file_difference = ord(target_file) - ord(pawn_file)
        rank_difference = target_rank - pawn_rank

        # Check if the target square is diagonally adjacent and in the correct direction
        if abs(file_difference) == 1 and rank_difference == direction:
            target_square_piece = self.board[target_square]['piece']
            # Check if there is a piece of the opponent's color on the target square
            if target_square_piece is not None and self.board[target_square]['piece-color'] != self.board[pawn_position]['piece-color']:
                return True
        return False

    def bishop_can_attack(self, bishop_position, target_square):
        """
        Check if a bishop at the given position can attack the target square.

        Parameters:
        - bishop_position (str): Position of the bishop (e.g., 'c1')
        - target_square (str): Target square to check (e.g., 'f4')

        Returns:
        - bool: True if the bishop can attack the target square, False otherwise.
        """
        # Get the file and rank of the bishop position and target square
        bishop_file, bishop_rank = bishop_position[0], int(bishop_position[1])
        target_file, target_rank = target_square[0], int(target_square[1])

        # Calculate the file and rank differences
        file_difference = ord(target_file) - ord(bishop_file)
        rank_difference = target_rank - bishop_rank

        # Check if the target square is diagonally reachable from the bishop's position
        if abs(file_difference) == abs(rank_difference):
            if not self.anyPieceAtMiddle(bishop_position, target_square):
                return True
        return False

    def knight_can_attack(self, knight_position, target_square):
        """
        Check if a knight at the given position can attack the target square.

        Parameters:
        - knight_position (str): Position of the knight (e.g., 'b1')
        - target_square (str): Target square to check (e.g., 'c3')

        Returns:
        - bool: True if the knight can attack the target square, False otherwise.
        """
        # Get the file and rank of the knight position and target square
        knight_file, knight_rank = knight_position[0], int(knight_position[1])
        target_file, target_rank = target_square[0], int(target_square[1])

        # Calculate the file and rank differences
        file_difference = abs(ord(target_file) - ord(knight_file))
        rank_difference = abs(target_rank - knight_rank)

        # Check if the knight's move is L-shaped (1 rank and 2 files, or 2 ranks and 1 file)
        if (file_difference == 1 and rank_difference == 2) or (file_difference == 2 and rank_difference == 1):
            return True
        else:
            return False

    def rook_can_attack(self, rook_position, target_square):
        """
        Check if a rook at the given position can attack the target square.

        Parameters:
        - rook_position (str): Position of the rook (e.g., 'a1')
        - target_square (str): Target square to check (e.g., 'a8')

        Returns:
        - bool: True if the rook can attack the target square, False otherwise.
        """
        # Get the file and rank of the rook position and target square
        rook_file, rook_rank = rook_position[0], int(rook_position[1])
        target_file, target_rank = target_square[0], int(target_square[1])

        # Check if the rook can attack the target square
        if rook_file == target_file or rook_rank == target_rank:
            if not self.anyPieceAtMiddle(rook_position, target_square):
                return True
        else:
            return False

    def queen_can_attack(self, queen_position, target_square):
        """
        Check if a queen at the given position can attack the target square.

        Parameters:
        - queen_position (str): Position of the queen (e.g., 'd1')
        - target_square (str): Target square to check (e.g., 'a8')

        Returns:
        - bool: True if the queen can attack the target square, False otherwise.
        """
        # Check if the queen can attack along the same file, rank, or diagonal as a rook or bishop
        if self.rook_can_attack(queen_position, target_square) or self.bishop_can_attack(queen_position, target_square):
            return True
        else:
            return False

    def king_can_attack(self, king_position, target_square):
        """
        Check if a king at the given position can attack the target square.

        Parameters:
        - king_position (str): Position of the king (e.g., 'e1')
        - target_square (str): Target square to check (e.g., 'e8')

        Returns:
        - bool: True if the king can attack the target square, False otherwise.
        """
        # Get the file and rank of the king
        king_file, king_rank = king_position[0], int(king_position[1])
        
        # Get the file and rank of the target square
        target_file, target_rank = target_square[0], int(target_square[1])

        # Check if the target square is within one square distance from the king in any direction
        if abs(ord(king_file) - ord(target_file)) <= 1 and abs(king_rank - target_rank) <= 1:
            return True
        else:
            return False


    def make_move(self, piece_to_move, piece_to_move_from, piece_to_move_to):
        if piece_to_move_to['piece'] is not None:
            capturing_square = piece_to_move_to['file'] + str(piece_to_move_to['rank'])
            capturing_piece = piece_to_move_to['piece']
            piece_color = piece_to_move_to['piece-color']
            for _piece_ in getattr(self, f'{piece_color}_{capturing_piece}'):
                if _piece_.position == capturing_square:
                    _piece_.position = None
                    _piece_.on_board = False

        piece_to_move_from['piece'] = None
        piece_to_move_from['piece-color'] = None

        piece_to_move_to['piece'] = piece_to_move
        piece_to_move_to['piece-color'] = self.current_player

    def make_castle(self, king_position, rook_position):
        def make_move(king_to, rook_to):
            self.board[king_position]['piece'] = None
            self.board[rook_position]['piece'] = None
            self.board[king_position]['piece-color'] = None
            self.board[rook_position]['piece-color'] = None
            self.board[king_to]['piece'] = 'king'
            self.board[rook_to]['piece'] = 'rook'
            self.board[king_to]['piece-color'] = self.current_player
            self.board[rook_to]['piece-color'] = self.current_player

            for rook in getattr(self, f'{self.current_player}_rook'):
                if rook.position == rook_position:
                    rook.position = rook_to
            king = getattr(self, f'{self.current_player}_king')
            king.position = king_to

        if(self.current_player == 'black'):
            if not self.anyPieceAtMiddle(king_position, rook_position):
                if rook_position == "h8":
                    if(self.is_check(self.current_player, 'g8') or self.is_check(self.current_player, 'f8')):
                        exit("cannot castle!")
                    make_move(king_to = 'g8', rook_to='f8')
                else:
                    if(self.is_check(self.current_player, 'c8') or self.is_check(self.current_player, 'd8')):
                        exit("cannot castle!")
                    make_move(king_to='c8', rook_to='d8')
            else:
                exit("cannot castle!")
        else:
            if not self.anyPieceAtMiddle(king_position, rook_position):
                if rook_position == "h1":
                    if(self.is_check(self.current_player, 'g1') or self.is_check(self.current_player, 'f1')):
                        exit("cannot castle!")
                    make_move(king_to = 'g1', rook_to='f1')
                else:
                    if(self.is_check(self.current_player, 'c1') or self.is_check(self.current_player, 'd1')):
                        exit("cannot castle!")
                    make_move(king_to='c1', rook_to='d1')
            else:
                exit("cannot castle!")
        
    def pawn_promotion(self, promoting_square):
        select_piece_to_promote = input("promote : queen, rook, bishop or knight?").lower()
        class_name = select_piece_to_promote.capitalize()

        PieceClass = getattr(piece, class_name)
        promoted_piece = PieceClass(self.current_player, promoting_square)
        PieceObject = getattr(self, f'{self.current_player}_{select_piece_to_promote}')
        PieceObject.append(promoted_piece)

        self.board.board[promoting_square]['piece'] = select_piece_to_promote
        for pawn in getattr(self, f'{self.current_player}_pawn'):
            if pawn.position == promoting_square:
                pawn.on_board = False
                pawn.position = None

    def move_piece(self, from_square = None, to_square = None, special_move = None):
        if special_move is not None:
            king_position = getattr(self, f'{self.current_player}_king')
            if king_position.make_castle == False:
                exit("cannot castle!")
            if(special_move == "o-o" and king_position.short_castling  == True):
                self.make_castle(king_position.position, king_position.short_rook)
            elif special_move == "o-o-o" and king_position.long_castling == True:
                self.make_castle(king_position.position, king_position.long_rook)
            else:
                exit("Invalid move")
            self.current_player = 'black' if self.current_player == 'white' else 'white'
            self.print_board()
            return

        # if self.is_valid_move(from_square, to_square):
        piece_to_move = self.board[from_square]['piece']
        self.make_move(piece_to_move, self.board[from_square], self.board[to_square])

        king_position = getattr(self, f'{self.current_player}_king')
        if(self.is_check(self.current_player, king_position.position)):
            self.make_move(piece_to_move, self.board[to_square], self.board[from_square])
            exit("Invalid move, king will be in check!")
            
        if(piece_to_move == 'pawn' and int(to_square[1]) in (1, 8)):
            self.pawn_promotion(to_square) 
    # Switch the player turn
        self.current_player = 'black' if self.current_player == 'white' else 'white'

        self.print_board()
        king_position = getattr(self, f'{self.current_player}_king')
        if(self.is_check(self.current_player, king_position.position)):
            if(self.is_checkmate(self.current_player, king_position.position)):
                exit(f"{self.current_player} got CHECKMATED!!")
            print(f"{self.current_player} king is in check")            
        # else:
        #     exit("Invalid move!")

    def is_valid_move(self, from_square, to_square):
        if self.board[from_square]['piece'] == 'pawn':
            for pawn in getattr(self, f'{self.current_player}_pawn'):
                if pawn.position == from_square:
                    return pawn.move(self.current_player, self, self.board[from_square], self.board[to_square])
        elif self.board[from_square]['piece'] == 'knight':
            for knight in getattr(self, f'{self.current_player}_knight'):
                if knight.position == from_square:
                    return knight.move(self.current_player, self, self.board[from_square], self.board[to_square])
        elif self.board[from_square]['piece'] == 'bishop':
            for bishop in getattr(self, f'{self.current_player}_bishop'):
                if bishop.position == from_square:
                    return bishop.move(self.current_player, self, self.board[from_square], self.board[to_square])
        elif self.board[from_square]['piece'] == 'rook':
            for rook in getattr(self, f'{self.current_player}_rook'):
                if rook.position == from_square:
                    return rook.move(self.current_player, self, self.board[from_square], self.board[to_square])
        elif self.board[from_square]['piece'] == 'queen':
            for queen in getattr(self, f'{self.current_player}_queen'):
                if queen.position == from_square:
                    return queen.move(self.current_player, self, self.board[from_square], self.board[to_square])
        elif self.board[from_square]['piece'] == 'king':
            king = getattr(self, f'{self.current_player}_king')
            if king.position == from_square:
                return king.move(self.current_player, self, self.board[from_square], self.board[to_square]) 
        return False 
    
    def print_board(self):
        # Print the current state of the chessboard
        for rank in range(8, 0, -1):
            for file in range(97, 105):  # ASCII values for 'a' to 'h'
                square_name = chr(file) + str(rank)
                flag = self.board[square_name]['piece']
                color = self.board[square_name]['piece-color']

                if(flag == 'pawn'):
                    piece = '♙' if color == 'white' else '♟︎'
                elif flag == 'knight':
                    piece = '♘' if color == 'white' else '♞'
                elif flag == 'bishop':
                    piece = '♗' if color == 'white' else '♝'
                elif flag == 'rook':
                    piece = '♖' if color == 'white' else '♜'
                elif flag == 'queen':
                    piece = '♕' if color == 'white' else '♛'
                elif flag == 'king':
                    piece = '♔' if color == 'white' else '♚'
                else:
                    piece = flag
                print(piece if piece else '-', end=" ")
            print()
        print("\n----------------------------\n")

def game1():
    print("\nBoard after moving white pawn from e2 to e4:")
    game.move_piece('e2', 'e4')

    print("\nBoard after moving black pawn from e7 to e5:")
    game.move_piece('e7', 'e5')

    print("\nBoard after moving bishop from f1 to c4:")
    game.move_piece('f1', 'c4')

    print("\nBoard after moving pawn from d7 to d6:")
    game.move_piece('d7', 'd6')

    print("\nBoard after moving queen from d1 to f3")
    game.move_piece('d1', 'f3')

    print("\nBoard after moving knight queen from b8 to c6")
    game.move_piece('b8', 'c6')

    print("\nBoard after moving queen f3 to f7")
    game.move_piece('f3', 'f7')

def game2():
    print("\nBoard after moving white pawn from e2 to e4:")
    game.move_piece('e2', 'e4')

    print("\nBoard after moving black pawn from e7 to e5:")
    game.move_piece('e7', 'e5')

    print("\nBoard after moving bishop from f1 to c4:")
    game.move_piece('f1', 'c4')

    print("\nBoard after moving pawn from d7 to d6:")
    game.move_piece('d7', 'd6')

    print("\nBoard after moving queen from d1 to f3")
    game.move_piece('d1', 'f3')

    print("\nBoard after moving knight queen from g8 to f6")
    game.move_piece('g8', 'f6')

    print("\nBoard after moving knight g1 to h3")
    game.move_piece('g1', 'h3')

    print("\nBoard after moving knight b8 to c6")
    game.move_piece('b8', 'c6')

    print("\nShort castling o-o")
    game.move_piece(special_move='o-o')
    game.print_board()

    print("\nBoard after moving knight f6 to h5")
    game.move_piece('f6', 'g4')

    print("\nBoard after moving queen f3 to f7")
    game.move_piece('f3', 'f7')

def game3():
    print("\nBoard after moving f2 to f3")
    game.move_piece('f2', 'f3')

    print("\nBoard after moving e7 to e5")
    game.move_piece('e7', 'e5')

    print("\nBoard after moving g2 to g4")
    game.move_piece('g2', 'g4')

    print("\nBoard after moving d8 to h4")
    game.move_piece('d8', 'h4')

def game4():
    game.move_piece('e2', 'e4')
    game.move_piece('e7', 'e5')
    game.move_piece('d1', 'h5')
    game.move_piece('b8', 'c6')
    game.move_piece('f1', 'c4')
    game.move_piece('g7', 'g6')
    game.move_piece('h5', 'f3')
    game.move_piece('g8', 'f6')
    game.move_piece('d2', 'd3')
    game.move_piece('f8', 'g7')
    game.move_piece('c1', 'g5')
    game.move_piece(special_move='o-o')
    game.move_piece('b1', 'd2')
    game.move_piece('f8', 'e8')
    game.move_piece('c4', 'f7')
    game.move_piece('g8', 'f7')
    game.move_piece('h2', 'h3')
    game.move_piece('f7', 'g8')
    game.move_piece('g5', 'f6')
    game.move_piece('g7', 'f6')
    game.move_piece('a1', 'c1')
    game.move_piece('f6', 'g5')
    game.move_piece('d3', 'd4')
    game.move_piece('g5', 'd2')
    game.move_piece('e1', 'd2')
    game.move_piece('d7', 'd5')
    game.move_piece('d2', 'e2')
    game.move_piece('c6', 'd4')
    game.move_piece('e2', 'd3')
    game.move_piece('d4', 'f3')
    game.move_piece('g1', 'f3')
    game.move_piece('d5', 'e4')
    game.move_piece('d3', 'e4')
    game.move_piece('c8', 'f5')
    game.move_piece('e4', 'e3')
    game.move_piece('e5', 'e4')
    game.move_piece('f3', 'h2')
    game.move_piece('d8', 'd3')
    game.move_piece('c2', 'd3')
    game.move_piece('e4', 'd3')
    game.move_piece('e3', 'f3')
    game.move_piece('d3', 'd2')
    game.move_piece('c1', 'c2')
    game.move_piece('d2', 'd1')
    game.move_piece('f3', 'g3')
    game.move_piece('d1', 'd3')
    game.move_piece('g3', 'h4')
    game.move_piece('e8', 'e4')
    game.move_piece('h4', 'g5')
    game.move_piece('d3', 'd8')
    game.move_piece('g5', 'h6')
    game.move_piece('d8', 'h4')

def gameinput():
    while(True):
        move = input("Move? ")
        if move == "exit":
            exit('Game Aborted!')
        if move == 'o-o' or move == 'o-o-o':
            game.move_piece(special_move=move)
        else:
            src, dtn = move.split(' ')
            game.move_piece(src, dtn)

def validate_move(from_pos, to_pos):
    # Your move validation logic here
    # Return "valid" or "invalid"
    # Example:
    if from_pos == "e2" and to_pos == "e4":
        return "valid"
    else:
        return "invalid"


# Initialize player points
player_points = Player()
# Start the game
game = GamePlay()


if __name__ == "__main__":
    # Print the initial board state
    print("Initial Board:")
    game.print_board()

    game2()
    # Print player points
    print("\nPlayer Points:")
    print("White:", player_points.points['white'])
    print("Black:", player_points.points['black'])