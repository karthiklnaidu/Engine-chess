class ChessBoard:
    def __init__(self) -> None:
        self.board = {}

    # INITization considerations of a board
    # 1. a typical board consists 8x8 grid squares          =>      dictionary
    # 2. in total of 64 squares, at each diagonally attached squares make dichotomy colors
    # 3. each has given below properties          =>    Nested dictionary
    #       -> color
    #       -> name
    #       -> value
    #       -> piece acquired
    #       -> isEmpty
    #

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
        return self.board[key] 
    
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

        for rank in range(8, 1, -1):
            for file in range(97, 105):
                square_name = chr(file) + str(rank)
                self.board[square_name]['file'] = chr(file)
                self.board[square_name]['rank'] = str(rank)

        # self.board['a8']['piece'] = 'R'
        # self.board['b8']['piece'] = 'N'
        # self.board['c8']['piece'] = 'B'
        # self.board['e8']['piece'] = 'K'
        # self.board['d8']['piece'] = 'Q'
        # self.board['f8']['piece'] = 'B'
        # self.board['g8']['piece'] = 'N'
        # self.board['h8']['piece'] = 'R'

#         # self.board['a7']['piece'] = 'P'
        # self.board['b7']['piece'] = 'P'
        # self.board['c7']['piece'] = 'P'
        # self.board['d7']['piece'] = 'P'
        # self.board['e7']['piece'] = 'P'
        # self.board['f7']['piece'] = 'P'
        # self.board['g7']['piece'] = 'P'
        # self.board['h7']['piece'] = 'P'

#         # self.board['a1']['piece'] = 'R'
        # self.board['b1']['piece'] = 'N'
        # self.board['c1']['piece'] = 'B'
        # self.board['e1']['piece'] = 'K'
        # self.board['d1']['piece'] = 'Q'
        # self.board['f1']['piece'] = 'B'
        # self.board['g1']['piece'] = 'N'
        # self.board['h1']['piece'] = 'R'

#         # self.board['a2']['piece'] = 'P'
        # self.board['b2']['piece'] = 'P'
        # self.board['c2']['piece'] = 'P'
        # self.board['d2']['piece'] = 'P'
        # self.board['e2']['piece'] = 'P'
        # self.board['f2']['piece'] = 'P'
        # self.board['g2']['piece'] = 'P'
        # self.board['h2']['piece'] = 'P'

#         # self.board['a2']['piece-color'] = "white"
        # self.board['b2']['piece-color'] = "white"
        # self.board['c2']['piece-color'] = "white"
        # self.board['d2']['piece-color'] = "white"
        # self.board['e2']['piece-color'] = "white"
        # self.board['f2']['piece-color'] = "white"
        # self.board['g2']['piece-color'] = "white"
        # self.board['h2']['piece-color'] = "white"

#         # self.board['a7']['piece-color'] = "black"
        # self.board['b7']['piece-color'] = "black"
        # self.board['c7']['piece-color'] = "black"
        # self.board['d7']['piece-color'] = "black"
        # self.board['e7']['piece-color'] = "black"
        # self.board['f7']['piece-color'] = "black"
        # self.board['g7']['piece-color'] = "black"
        # self.board['h7']['piece-color'] = "black"
    # 
# 