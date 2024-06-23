class ChessBoard:
    def __init__(self) -> None:
        self.board = {}

        for rank in range(8):
            for file in range(8):
                squareName = chr(97 + file) + str(8 - rank)
                squareColor = "black" if((rank + file) % 2 == 0) else "white"
                self.board[squareName] = {
                    'file' : None,
                    'rank' : None,
                    "color" : squareColor,
                    "value" : int(str(rank) + str(file)),
                    "piece" : None,
                    "piece-color" : None
                }

    def __getitem__(self, key):
        try:
            return self.board[key]
        except KeyError:
            return False
    
    def initializePieces(self):
        major_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for file in range(8):
            square_name = chr(97 + file) + str(1)
            self.board[square_name]['piece'] = major_pieces[file]
            self.board[square_name]['piece-color'] = 'white'

        for file in range(8):
            square_name = chr(97 + file) + str(8)
            self.board[square_name]['piece'] = major_pieces[file]
            self.board[square_name]['piece-color'] = 'black'

        for file in range(97, 105):
            square_name1 = chr(file) + str(2)
            square_name2 = chr(file) + str(7)

            self.board[square_name1]['piece'] = 'pawn'
            self.board[square_name1]['piece-color'] = 'white'

            self.board[square_name2]['piece'] = 'pawn'
            self.board[square_name2]['piece-color'] = 'black'

        for rank in range(8, 0, -1):
            for file in range(97, 105):
                square_name = chr(file) + str(rank)
                self.board[square_name]['file'] = chr(file)
                self.board[square_name]['rank'] = rank

    def get_piece(self, row, col):
        """
        Returns the piece at the specified row and column.
        If no piece is present, returns None.
        """
        square_name = chr(97 + col) + str(8 - row)
        square = self.board.get(square_name)
        if square:
            piece = square['piece']
            piece_color = square['piece-color']
            if piece and piece_color:
                return f"{piece_color[0]}{'n' if piece == 'knight' else piece[0].lower()}"
        return None

if __name__ == "__main__":
    cb = ChessBoard()
    cb.initializePieces()

    for i in range(97, 105):
        for j in range(8, 0, -1):
            square = chr(i) + str(j)
            print(cb.board[square]['file'], cb.board[square]['rank'])
        print()

        