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
                    "color" : squareColor,
                    "value" : int(str(rank) + str(file)),
                    "piece" : None
                }
        self.board['a8']['piece'] = 'R'
        self.board['b8']['piece'] = 'N'
        self.board['c8']['piece'] = 'B'
        self.board['d8']['piece'] = 'K'
        self.board['e8']['piece'] = 'Q'
        self.board['f8']['piece'] = 'B'
        self.board['g8']['piece'] = 'N'
        self.board['h8']['piece'] = 'R'

        self.board['a7']['piece'] = 'P'
        self.board['b7']['piece'] = 'P'
        self.board['c7']['piece'] = 'P'
        self.board['d7']['piece'] = 'P'
        self.board['e7']['piece'] = 'P'
        self.board['f7']['piece'] = 'P'
        self.board['g7']['piece'] = 'P'
        self.board['h7']['piece'] = 'P'

        self.board['a1']['piece'] = 'R'
        self.board['b1']['piece'] = 'N'
        self.board['c1']['piece'] = 'B'
        self.board['d1']['piece'] = 'K'
        self.board['e1']['piece'] = 'Q'
        self.board['f1']['piece'] = 'B'
        self.board['g1']['piece'] = 'N'
        self.board['h1']['piece'] = 'R'

        self.board['a2']['piece'] = 'P'
        self.board['b2']['piece'] = 'P'
        self.board['c2']['piece'] = 'P'
        self.board['d2']['piece'] = 'P'
        self.board['e2']['piece'] = 'P'
        self.board['f2']['piece'] = 'P'
        self.board['g2']['piece'] = 'P'
        self.board['h2']['piece'] = 'P'

    def __getitem__(self, key):
        return self.board[key] 
    
    
