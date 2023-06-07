

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUNDCOLOR = (25, 25, 25)
BOARDCOLWHITE = (160, 100, 57)
BOARDCOLBLACK = (255, 230, 179)
BOARDPIECETARGETCOLDARK = (200, 50, 50)
BOARDPIECETARGETCOLLIGHT = (255, 75, 75)



boardArray = [0 for i in range(64)]

codeFen = 'rkb4R/p7/p2N4/6p1/6Pp/P3K2P/1P6/R1B5 w - - 0 3'#'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

directionalOffsets = [8, -8, -1, 1, 7, -7, 9, -9]

isWhiteTurn = True

kingWhiteState = 0

kingBlackState = 0

#-------------------------#

gameState = 0

# 0 - Game in progress
# 1 - White Wins
# 2 - Black Wins
# 3 - Draw

#-------------------------#

pawnPromotion = False
pawnPromotionSquare = -1

# Pawn Promotion Variables

#-------------------------#


turnFull = 1

turnHalf = 0

totalPieces = 0

totalPiecesLastTurn = 32

originalSquareValue = -1

originalSquareIndex = -1

moveSquareIndex = -1

enPassantSquare = 46

movedPieces = []

pieceTaken = 0

kingCheckingSquares = []

#-------------------------#

piecePointValues = {

    10 : 1,
    11 : 3,
    12 : 3,
    13 : 5,
    14 : 9,
    18 : 1,
    19 : 3,
    20 : 3,
    21 : 5,
    22 : 9

}


whitePoints = 0

blackPoints = 0

#Game Data

#-------------------------#





class Piece:

    Non = 0
    King = 1
    Pawn = 2
    Knight = 3
    Bishop = 4
    Rook = 5
    Queen = 6

    White = 8
    Black = 16

class PieceTable:

    textureTable = {

        0 : 'NO TEXTURE FOR NONE',
        1 : 'King.png',
        2 : 'Pawn.png',
        3 : 'Knight.png',
        4 : 'Bishop.png',
        5 : 'Rook.png',
        6 : 'Queen.png',

        8 : 'textures/white/',
        16 : 'textures/black/'
    }

    typeSymbolTable = {

        'k' : Piece.King,
        'p' : Piece.Pawn,
        'n' : Piece.Knight,
        'b' : Piece.Bishop,
        'r' : Piece.Rook,
        'q' : Piece.Queen
    }

    valueSymbolTable = {

        Piece.King : 'k',
        Piece.Pawn : 'p',
        Piece.Knight : 'n',
        Piece.Bishop : 'b',
        Piece.Rook : 'r',
        Piece.Queen : 'q'
    }

class MoveData():

    numSquaresToEdge = [[] for i in range(64)]
    
    for file in range(8):
        for rank in range(8):

            numNorth = 7 - rank
            numSouth = rank
            numWest = file
            numEast = 7 - file

            squareIndex = rank * 8 + file

            numSquaresToEdge[squareIndex] = [

                numNorth,
                numSouth,
                numWest,
                numEast,
                min(numNorth,numWest),
                min(numSouth,numEast),
                min(numNorth,numEast),
                min(numSouth,numWest)

            ]


moves = {}

pinnedSquares = []