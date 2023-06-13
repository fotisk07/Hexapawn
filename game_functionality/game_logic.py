class Board:
    EMPTY = 0
    WHITE = 1
    BLACK = 2

    def __init__(self):
        self.turn = self.WHITE
        self.board = [self.EMPTY for _ in range(9)]
        self.outputIndex = {}
        self.legal_moves = None

        self.WHITE_PAWN_CAPTURES = [[],
                                    [],
                                    [],
                                    [1],
                                    [0, 2],
                                    [1],
                                    [4],
                                    [3, 5],
                                    [4]]

        self.BLACK_PAWN_CAPTURES = [[4],
                                    [3, 5],
                                    [4],
                                    [7],
                                    [6, 8],
                                    [7],
                                    [],
                                    [],
                                    []]

    def setStartingPosition(self):
        self.board = [self.BLACK, self.BLACK, self.BLACK,
                      self.EMPTY, self.EMPTY, self.EMPTY,
                      self.WHITE, self.WHITE, self.WHITE]

        self.turn = self.WHITE
        self.legal_moves = self.generateMove()

    def getNetworOutputIndex(self, move):
        return self.outputIndex[str(move)]

    def applyMove(self, move):
        fromsquare = move[0]
        tosquare = move[1]

        self.board[tosquare] = self.board[fromsquare]
        self.board[fromsquare] = self.EMPTY

        self.turn = self.WHITE if self.turn == self.BLACK else self.BLACK
        self.legal_moves = None

    def generateMove(self):
        if self.legal_moves is None:
            moves = []
            for i in range(9):
                if self.board[i] == self.turn:
                    if self.turn == self.WHITE:
                        toSquare = i - 3
                        # check if we can move one square up
                        if toSquare >= 0:
                            if self.board[toSquare] == self.EMPTY:
                                moves.append([i, toSquare])
                        potCaptureSquares = self.WHITE_PAWN_CAPTURES[i]

                        moves.extend(
                            [i, toSquare]
                            for toSquare in potCaptureSquares
                            if self.board[toSquare] == self.BLACK
                        )
                    if self.turn == self.BLACK:
                        toSquare = i + 3
                        # check if we can move one square down
                        if toSquare <= 8:
                            if self.board[toSquare] == self.EMPTY:
                                moves.append([i, toSquare])
                        potCaptureSquares = self.BLACK_PAWN_CAPTURES[i]

                        moves.extend(
                            [i, toSquare]
                            for toSquare in potCaptureSquares
                            if self.board[toSquare] == self.WHITE
                        )
            self.legal_moves = moves
        return self.legal_moves

    def isTerminal(self):
        winner = None
        if (self.board[6] == self.BLACK) or (self.board[7] == self.BLACK) or (self.board[8] == self.BLACK):
            winner = self.BLACK
        elif (self.board[0] == self.WHITE) or (self.board[1] == self.WHITE) or (self.board[2] == self.WHITE):
            winner = self.WHITE

        elif (len(self.generateMove()) == 0):
            winner = self.BLACK if self.turn == self.WHITE else self.WHITE

        return winner is not None, winner

    def toNetworkInput(self):
        posVec = []
        for i in range(9):
            if self.board[i] == self.WHITE:
                posVec.append(1)
            else:
                posVec.append(0)

        for i in range(9):
            if self.board[i] == self.BLACK:
                posVec.append(1)
            else:
                posVec.append(0)

        for _ in range(3):
            if self.turn == self.WHITE:
                posVec.append(1)
            else:
                posVec.append(0)
        return posVec
