import pygame
import Data



def getTextureAddress(value):

    pieceColor = Data.Piece.White if value < 16 else Data.Piece.Black
    pieceType = value - 8 if pieceColor == 8 else value - 16

    return Data.PieceTable.textureTable[pieceColor] + Data.PieceTable.textureTable[pieceType]



def isSlidingPiece(piece):

    if 11 < piece < 15 or 19 < piece < 23:

        return True
        
    return False
    


def isKnight(piece):

    if piece == 11 or piece == 19:

        return True
    
    return False

def isKing(piece):

    if piece == 9 or piece == 17:

        return True
    
    return False

def isPawn(piece):

    if piece == 10 or piece == 18:

        return True
    
    return False

def isFriendly(piece, targetPiece):

    if 0 < piece < 16 and 0 < targetPiece < 16:

        return True
    
    elif 16 < piece < 32 and 16 < targetPiece < 32:

        return True

    return False


def isOurTurn(piece):

    if (piece < 16 and Data.isWhiteTurn) or (piece > 16 and not Data.isWhiteTurn):

        return True

    return False



def calculateRemainingPieces():

    global remainingPieces
    remainingPieces = 0

    for num in Data.boardArray:

        if num > 0:

            remainingPieces += 1

def drawStatusBox(x, y, Screen, Font):

    msgColor = (0)

    msgText = ''

    if Data.isWhiteTurn or Data.kingBlackState == 2:

        msgColor = Data.WHITE

    elif not Data.isWhiteTurn or Data.kingWhiteState == 2:

        msgColor = Data.BLACK

    if Data.kingBlackState == 2 or Data.kingWhiteState == 2:

        msgText = 'White Side Wins' if Data.kingBlackState == 2 else 'Black Side Wins'

    elif Data.isWhiteTurn:

        msgText = "White Side's Turn"

    elif not Data.isWhiteTurn:

        msgText = "Black Side's Turn"

    textBox = Font.render(msgText, True, msgColor)

    Screen.blit(textBox, (x, y))



def updateTurn():

    if Data.isWhiteTurn:
        
        Data.isWhiteTurn = False
        splitFen = Data.codeFen.split(' ')
        splitFen[1] = 'b'
        Data.codeFen = ' '.join(splitFen)

    else:

        Data.isWhiteTurn = True
        splitFen = Data.codeFen.split(' ')
        splitFen[1] = 'w'
        Data.codeFen = ' '.join(splitFen)



def updatePositionFromFen(fen):

    fenBoard = fen.split(' ')[0]
    rank, file = 7, 0

    for symbol in fenBoard:
        if symbol == '/':
            file = 0
            rank -= 1
        else:
            if symbol.isdigit():
                file += int(symbol)
            else:
                pieceColor = Data.Piece.White if symbol.isupper() else Data.Piece.Black
                pieceType = Data.PieceTable.typeSymbolTable[symbol.lower()]
                Data.boardArray[rank * 8 + file] = pieceType + pieceColor
                file += 1



def updateFenFromPosition(array):

    freeSpaceCounter = 0

    fenString = ''

    for rank in range(7, -1, -1):
        for file in range(8):

            symbol = array[rank * 8 + file]
            
            if symbol == 0:
                freeSpaceCounter += 1

                if freeSpaceCounter == 8 or file == 7:
                    fenString += f'{freeSpaceCounter}'
                    freeSpaceCounter = 0
                
            else:
                if freeSpaceCounter > 0:

                    fenString += f'{freeSpaceCounter}'
                    freeSpaceCounter = 0

                isWhite = True if symbol < 16 else False
                pieceType = Data.PieceTable.valueSymbolTable[symbol - 8] if isWhite == True else Data.PieceTable.valueSymbolTable[symbol - 16]
                
                fenString += f'{pieceType.upper()}' if isWhite == True else f'{pieceType}'

        fenString += '/' if rank > 0 else ''
            

    Data.codeFen = Data.codeFen.replace(f"{Data.codeFen.split(' ')[0]}", fenString)



def drawBoard(xCord, yCord, Screen):

    board = pygame.Surface((800,800))

    squareIndex = 0

    for rank in range(7, -1, -1):

        for file in range(8):

            square = pygame.Surface((100,100))

            squareColor = pygame.Rect(0,0,100,100)

            if (Data.originalSquareIndex in Data.moves) and (squareIndex in Data.moves[Data.originalSquareIndex]) and isOurTurn(Data.originalSquareValue) and (file + rank) % 2 == 0:

                pygame.draw.rect(square, Data.BOARDPIECETARGETCOLLIGHT, squareColor)

            elif (Data.originalSquareIndex in Data.moves) and (squareIndex in Data.moves[Data.originalSquareIndex]) and isOurTurn(Data.originalSquareValue) and (file + rank) % 2 != 0:

                pygame.draw.rect(square, Data.BOARDPIECETARGETCOLDARK, squareColor)

            elif (file + rank) % 2 == 0:

                pygame.draw.rect(square, Data.BOARDCOLBLACK, squareColor)

            else:

                pygame.draw.rect(square, Data.BOARDCOLWHITE , squareColor)

            if Data.boardArray[squareIndex] > 0:
            
                pieceTexture = pygame.image.load(getTextureAddress(Data.boardArray[squareIndex]))
 
                square.blit(pieceTexture,(0,0))

            squareIndex += 1
            board.blit(square,(file * 100, rank * 100))
            

    Screen.blit(board, (xCord, yCord))



def generateMoves():

    for startSquare in range(64):

        piece = Data.boardArray[startSquare]

        if piece != 0:

            if isSlidingPiece(piece):

                generateSlidingMoves(startSquare,piece)

            elif isKnight(piece):

                generateKnightMoves(startSquare,piece)

            elif isPawn(piece):

                generatePawnMoves(startSquare,piece)



def checkForChecks():

    for square, piece in enumerate(Data.boardArray):
         
        if isKing(piece) and isOurTurn(piece):

            if square in Data.pinnedSquares and square in Data.moves:

                if piece == 9:

                    Data.kingWhiteState = 1

                else:

                    Data.kingBlackState = 1

                break
            
            elif square in Data.pinnedSquares and square not in Data.moves:

                if piece == 9:

                    Data.kingWhiteState = 2

                else:

                    Data.kingBlackState = 2

                break

            else:

                if piece == 9:

                    Data.kingWhiteState = 0

                else:

                    Data.kingBlackState = 0



def generatePawnMoves(startsquare,piece):

    pieceDirection = 1 if piece > 16 else 0

    numSquares = Data.MoveData.numSquaresToEdge[startsquare][0]

    if (7 < startsquare < 16 and piece < 16) or (47 < startsquare < 56 and piece > 16):

        for i in range(2):

            if i == 0:

                for j in range(-1, 2, 2):

                    targetSquare = startsquare + Data.directionalOffsets[pieceDirection] + j
                    pieceOnTargetSquare = Data.boardArray[targetSquare]

                    if isFriendly(piece,pieceOnTargetSquare):

                        if not isOurTurn(piece):

                            Data.pinnedSquares.append(targetSquare)

                        continue

                    if (pieceOnTargetSquare == 0 and j != 0) and not isOurTurn(piece):

                        Data.pinnedSquares.append(targetSquare)

                    elif pieceOnTargetSquare != 0:

                        if startsquare not in Data.moves:

                            Data.moves[startsquare] = [targetSquare]

                        else:

                            Data.moves[startsquare].append(targetSquare)

            targetSquare = startsquare + Data.directionalOffsets[pieceDirection] * (i + 1)
            pieceOnTargetSquare = Data.boardArray[targetSquare]

            if pieceOnTargetSquare > 0:

                break

            if startsquare not in Data.moves:

                Data.moves[startsquare] = [targetSquare]

            else:

                Data.moves[startsquare].append(targetSquare)

    else:

        for i in range(-1, 2):

            numSquaresX = -1

            if i == -1:

                numSquaresX = Data.MoveData.numSquaresToEdge[startsquare][2]

            elif i == 1:

                numSquaresX = Data.MoveData.numSquaresToEdge[startsquare][3]

            if numSquaresX == 0:

                continue

            targetSquare = startsquare + Data.directionalOffsets[pieceDirection] + i
            pieceOnTargetSquare = Data.boardArray[targetSquare]

            if (i == 0 and pieceOnTargetSquare != 0) or numSquares == 0:

                continue

            if i != 0 and (pieceOnTargetSquare == 0 or isFriendly(piece, pieceOnTargetSquare)) and not isOurTurn(piece):

                Data.pinnedSquares.append(targetSquare)

            elif i != 0 and (pieceOnTargetSquare != 0 and not isFriendly(piece, pieceOnTargetSquare)) or i == 0 and pieceOnTargetSquare == 0:

                if startsquare not in Data.moves:

                    Data.moves[startsquare] = [targetSquare]

                else:

                    Data.moves[startsquare].append(targetSquare)



def generateKingMoves():

    startSquare = 63 if Data.isWhiteTurn else 0

    endSquare = 0 if Data.isWhiteTurn else 64

    increment = -1 if Data.isWhiteTurn else 1

    for square in range(startSquare, endSquare, increment):

        if isKing(Data.boardArray[square]):

            for direction in range(8):

                numSquares = Data.MoveData.numSquaresToEdge[square][direction]

                if numSquares > 0:

                    targetSquare = square + Data.directionalOffsets[direction]
                    pieceOnTargetSquare = Data.boardArray[targetSquare]

                    if not isOurTurn(Data.boardArray[square]):

                        if isFriendly(Data.boardArray[square], pieceOnTargetSquare) or pieceOnTargetSquare == 0:

                            Data.pinnedSquares.append(targetSquare)
                        
                        continue

                    else:

                        if isFriendly(Data.boardArray[square], pieceOnTargetSquare):

                            continue

                        if square not in Data.moves:

                            Data.moves[square] = [targetSquare]

                        else:

                            Data.moves[square].append(targetSquare)

            if square in Data.moves:

                toBeRemoved = []

                for move in Data.moves[square]:

                    if move in Data.pinnedSquares:

                        toBeRemoved.append(move)

                for i in toBeRemoved:

                    Data.moves[square].remove(i)

                if len(Data.moves[square]) == 0:

                    Data.moves.pop(square)



def generateKnightMoves(startsquare, piece):

    offset = 0

    for direction in range(4):

        numSquares = Data.MoveData.numSquaresToEdge[startsquare][direction]

        if numSquares >= 2:

            for i in range(-1, 2, 2):

                numSquaresX = -1

                if direction < 2:

                    numSquaresX = Data.MoveData.numSquaresToEdge[startsquare][2] if i == -1 else Data.MoveData.numSquaresToEdge[startsquare][3]

                if numSquaresX == 0:

                    continue

                offset = 8 * i if direction > 1 else 1 * i
                    
                targetSquare = startsquare + (Data.directionalOffsets[direction] * 2) + offset

                if not 0 < targetSquare < 64:

                    continue

                pieceOnTargetSquare = Data.boardArray[targetSquare]

                if not isOurTurn(piece):

                    Data.pinnedSquares.append(targetSquare)

                    continue

                else:

                    if isFriendly(piece, pieceOnTargetSquare):

                        continue

                    if startsquare not in Data.moves:

                        Data.moves[startsquare] = [targetSquare]

                    else:

                        Data.moves[startsquare].append(targetSquare)





def generateSlidingMoves(startsquare, piece):

    startDirIndex = 4 if piece == 12 or piece == 20 else 0
    endDirIndex = 4 if piece == 13 or piece == 21 else 8

    for direction in range(startDirIndex,endDirIndex):

        numSquares = Data.MoveData.numSquaresToEdge[startsquare][direction]

        for n in range(0, numSquares):

            targetSquare = startsquare + Data.directionalOffsets[direction] * (n + 1)
            pieceOnTargetSquare = Data.boardArray[targetSquare]

            if not isOurTurn(piece):

                if isKing(pieceOnTargetSquare) and not isFriendly(piece, pieceOnTargetSquare):

                    for remainingSquares in range(n, numSquares):

                        targetSquare = startsquare + Data.directionalOffsets[direction] * (remainingSquares + 1)

                        Data.pinnedSquares.append(targetSquare)

                    break

                if isFriendly(piece, pieceOnTargetSquare):

                    Data.pinnedSquares.append(targetSquare)

                if pieceOnTargetSquare == 0:

                    Data.pinnedSquares.append(targetSquare)

                    continue

                break
            
            else:

                if isFriendly(piece, pieceOnTargetSquare):

                    break

                if startsquare not in Data.moves:

                    Data.moves[startsquare] = [targetSquare]

                else:

                    Data.moves[startsquare].append(targetSquare)

                if not isFriendly(piece, pieceOnTargetSquare) and pieceOnTargetSquare != 0:

                    break
