
boardArray = [0 for i in range(64)]

codeFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

directionalOffsets = [8, -8, -1, 1, 7, -7, 9, -9]

isWhiteTurn = True

#----Mouse Objects----

originalSquareValue = -1
originalSquareIndex = -1



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