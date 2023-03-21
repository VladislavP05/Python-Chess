import Data
import Functions







# for x in range(8):
#         for y in range(8):
#             isLightSquare = (x + y) % 2 != 0
#             print(isLightSquare)



# test = [0 for i in range(64)]

# codeFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'


# def updatePositionFromFen(fen):

#     typeSymbolTable = {

#         'k' : Data.Piece.King,
#         'p' : Data.Piece.Pawn,
#         'n' : Data.Piece.Knight,
#         'b' : Data.Piece.Bishop,
#         'r' : Data.Piece.Rook,
#         'q' : Data.Piece.Queen

#     }

#     fenBoard = fen.split(' ')[0]
#     rank, file = 7, 0

#     for symbol in fenBoard:
#         if symbol == '/':
#             file = 0
#             rank -= 1
#         else:
#             if symbol.isdigit():
#                 file += int(symbol)
#             else:
#                 pieceColor = Data.Piece.White if symbol.isupper() else Data.Piece.Black
#                 pieceType = typeSymbolTable[symbol.lower()]
#                 test[rank * 8 + file] = pieceType + pieceColor
#                 file += 1

# def updateFenFromPosition(array):

#     freeSpaceCounter = 0

#     fenString = ''

#     for rank in range(7, -1, -1):
#         for file in range(8):

#             symbol = array[rank * 8 + file]
            
#             if symbol == 0:
#                 freeSpaceCounter += 1

#                 if freeSpaceCounter == 8 or file == 7:
#                     fenString += f'{freeSpaceCounter}'
#                     freeSpaceCounter = 0
                
#             else:
#                 if freeSpaceCounter > 0:

#                     fenString += f'{freeSpaceCounter}'
#                     freeSpaceCounter = 0

#                 isWhite = True if symbol < 16 else False
#                 pieceType = Data.PieceTable.valueSymbolTable[symbol - 8] if isWhite == True else Data.PieceTable.valueSymbolTable[symbol - 16]
                
#                 fenString += f'{pieceType.upper()}' if isWhite == True else f'{pieceType}'

#         fenString += '/' if rank > 0 else ''
            

#     global codeFen

#     codeFen = codeFen.replace(f"{codeFen.split(' ')[0]}", fenString)




# updatePositionFromFen(codeFen)

# test[11] = 0
# test[17] = 10

# updateFenFromPosition(test)

# print(codeFen)










# class MoveData():

#     numSquaresToEdge = [[] for i in range(64)]

#     for file in range(8):
#         for rank in range(8):

#             numNorth = 7 - rank
#             numSouth = rank
#             numWest = file
#             numEast = 7 - file

#             squareIndex = rank * 8 + file

#             numSquaresToEdge[squareIndex] = [

#                 numNorth,
#                 numSouth,
#                 numWest,
#                 numEast,
#                 min(numNorth,numWest),
#                 min(numSouth,numEast),
#                 min(numNorth,numEast),
#                 min(numSouth,numWest)

#             ]





# test = []

# test.append(Data.Move(12,15))





# print(True + True)

# def generateMoves():

#     for startSquare in range(64):

#         piece = Data.boardArray[startSquare]

#         if (0 < piece < 16 and Data.isWhiteTurn == True) or (16 < piece < 23 and Data.isWhiteTurn == False):

#             if Functions.isSlidingPiece(piece):

#                 generateSlidingMoves(startSquare,piece)




# def generateSlidingMoves(startsquare, piece):

#     startDirIndex = 4 if piece == 12 or piece == 20 else 0
#     endDirIndex = 4 if piece == 13 or piece == 21 else 8

#     for direction in range(startDirIndex,endDirIndex):

#         numSquares = Data.MoveData.numSquaresToEdge[startsquare][direction]

#         for n in range(0, numSquares):

#             targetSquare = startsquare + Data.directionalOffsets[direction] * (n + 1)
#             pieceOnTargetSquare = Data.boardArray[targetSquare]

#             if Functions.isFriendly(piece, pieceOnTargetSquare):

#                 break

#             if startsquare not in Data.moves:

#                 Data.moves[startsquare] = [targetSquare]

#             else:

#                 Data.moves[startsquare].append(targetSquare)

#             if not Functions.isFriendly(piece, pieceOnTargetSquare) and pieceOnTargetSquare != 0:

#                 break


# Functions.updatePositionFromFen(Data.codeFen)
# generateMoves()
# print(Data.moves)



# test = (0 < (14 and 20) < 16) or (16 < (14 and 20) < 32)

# print(test)






kilometers = int(input())

timeOfDay = input()

taxiRate = 0.79 if timeOfDay == 'day' else 0.90

if kilometers < 20:

    price = 0.70 + kilometers * taxiRate

elif kilometers < 100:

    price = 0.09 * kilometers

else:

    price = 0.06 * kilometers


print(price)


