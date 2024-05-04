import initBoard as chessBoard

class Pawn:
    def __init__(self, color, square):
        self.color = color
        self.position = square
        self.value = 1
        self.onboard = True

    def function(self, player, _from, _to):
        fromSquare = board.board[_from];
        print(fromSquare['piece'])
        toSquare = board.board[_to];
        differance = fromSquare['value'] - toSquare['value']
        #Moving the piece forward
        if(fromSquare['piece'] != None):
            if(fromSquare['piece'] == 'P' and self.color is player):
                if(differance in (11, 10, 9)):
                    if(differance in (11, 9)):
                        if(toSquare['piece'] != None and self.color != player):
                            return True
                        else:
                            return False
                    else:
                        if(toSquare['piece'] == None):
                            return True
                        else:
                            return False
                else:
                    return False
            else:
                return False
        else:
            return False
                    

    
class GamePlay(chessBoard.ChessBoard):
    def __init__(self):
        chessBoard.ChessBoard.__init__(self)

        self.currentPlayer = 'white'

        self.white_pawn = [Pawn("white", 'a2'), Pawn('white', 'b2'), Pawn("white", 'c2'), Pawn('white', 'd2'),
                Pawn("white", 'e2'), Pawn('white', 'f2'), Pawn("white", 'g2'), Pawn('white', 'h2')]
        
        self.black_pawn = [Pawn("black", 'a6'), Pawn('black', 'b6'), Pawn("black", 'c6'), Pawn('black', 'd6'),
                Pawn("black", 'e6'), Pawn('black', 'f6'), Pawn("black", 'g6'), Pawn('black', 'h6')]

    def to_move_piece(self, _from, _to):
        if self.is_valid_move(_from, _to):
            # Get the piece to move
            piece_to_move = self.board[_from]['piece']
            if piece_to_move is not None:
                # Update the destination square with the piece
                self.board[_to]['piece'] = piece_to_move
                # Empty the source square
                self.board[_from]['piece'] = None
                # Update the pawn's position if it's a pawn
                for pawn in self.white_pawn:
                    if pawn.position == _from:
                        pawn.position = _to
                        break
                for pawn in self.black_pawn:
                    if pawn.position == _from:
                        pawn.position = _to
                        break
                # Switch the player turn
                self.currentPlayer = 'black' if self.currentPlayer == 'white' else 'white'
            else:
                print("No piece at the starting position.")
        else:
            print("Invalid move!")

    def is_valid_move(self, _from, _to):
        if(board[_from]['piece'] is 'P'):
            if self.currentPlayer is "white":
                for pawn in self.white_pawn:
                    if pawn.position is _from:
                        return pawn.function(self.currentPlayer, _from, _to)
            else:
                for pawn in self.black_pawn:
                    if pawn.position is _from:
                        return pawn.function(self.currentPlayer, _from, _to)
    
    def printBoard(self):
        temp = self.board
        for rank in range(8, 0, -1):
            for file in range(97, 105):  # ASCII values for 'a' to 'h'
                squareName = chr(file) + str(rank)
                piece = temp[squareName]['piece']
                print(piece if piece else ' ', end=" ")
            print()

board = chessBoard.ChessBoard()
cb = GamePlay()
print(cb.printBoard())
cb.to_move_piece('e2', 'e3')
print(cb.printBoard())

