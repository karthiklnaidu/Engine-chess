class ChessBoard:
    def __init__(self):
        self.board = [
            ['r', 'n', 'b', 'k', 'q', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', ' ', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', 'p', ' ', ' ', ' '],
            [' ', ' ', ' ', 'P', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', ' ', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
            
    
class Pawn:
    def __init__(self, color, square):
        self.color = color
        self.position = square

    def function(self, _from, _to):
        current_file, current_rank = switch(self.position)
        start_file, start_rank = switch(_from)
        end_file, end_rank = switch(_to)

        #Moving the piece forward
        if(self.position == _from):
            if(start_rank == 6 and start_file == end_file):
                if(end_rank >=4 and end_rank < start_rank):
                    return True
            elif(start_rank == --end_rank and end_file == start_file):
                return True
            else:
                return False
        else:
            return False

        #Capturing the piece
    
class GamePlay(ChessBoard):
    def __init__(self):
        ChessBoard.__init__(self)
        self.currentPlayer = 'white'

        self.white_pawn = [Pawn("white", 'a2'), Pawn('white', 'b2'), Pawn("white", 'c2'), Pawn('white', 'd2'),
                Pawn("white", 'e2'), Pawn('white', 'f2'), Pawn("white", 'g2'), Pawn('white', 'h2')]
        
        self.black_pawn = [Pawn("black", 'a6'), Pawn('black', 'b6'), Pawn("black", 'c6'), Pawn('black', 'd6'),
                Pawn("black", 'e6'), Pawn('black', 'f6'), Pawn("black", 'g6'), Pawn('black', 'h6')]

    def to_move_piece(self, _from, _to):
        for i in 8:
            if(self.white_pawn[i].position == _from):
                
        if self.is_valid_move(_from, _to):
            start_file, start_rank = switch(_from)
            end_file, end_rank = switch(_to)

            self.board[end_rank][end_file] = self.board[start_rank][start_file]
            self.board[start_rank][start_file] = ' '
            self.white_pawn[4].position = _to
            self.currentPlayer = 'black'
        else:
            print("Invalid!")

    def is_valid_move(self, _from, _to):
        return self.white_pawn[4].function(_from, _to)
    
    def printBoard(self):
        for rank in self.board:
            print(' '.join(rank))
        print(self.white_pawn[4].position)

def switch(square):
        file_index = ord(square[0]) - ord('a')
        rank_index = 8 - int(square[1])
        return file_index, rank_index

chessBoard = GamePlay()
print(chessBoard.printBoard())
chessBoard.to_move_piece('e2', 'e3')
print(chessBoard.printBoard())

