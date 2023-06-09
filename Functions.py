import pygame
import Data
from sys import exit
from time import strftime,gmtime



def drawText(text, color, x, y, screen):

    scrText = Data.fontMedium.render(text, True, color)

    screen.blit(scrText, (x,y))



def drawButton(x, y, color, text, screen, function, state = 'Normal'):

    buttonColor = color if state == 'Normal' else (255, 255, 255)

    buttonSurface = pygame.surface.Surface(150, 50)







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



def calculatePiecesOnBoard():

    pieces = [x for x in Data.boardArray if x != 0]

    Data.totalPieces = len(pieces)



def enPassantHandler(pawnIndex, mode: str):
        
    fileTable = {

        0 : 'a',
        1 : 'b',
        2 : 'c',
        3 : 'd',
        4 : 'e',
        5 : 'f',
        6 : 'g',
        7 : 'h'

    }

    rank = ((pawnIndex - 8) // 8) + 1 if Data.isWhiteTurn else ((pawnIndex + 8) // 8) + 1

    file = pawnIndex % 8

    splitFen = Data.codeFen.split(' ')



    def addEnPassant():

        splitFen[3] = fileTable[file] + str(rank)

        if Data.isWhiteTurn:

            Data.enPassantSquare = (pawnIndex - 8)

        else:

            Data.enPassantSquare = (pawnIndex + 8)

    

    def removeEnPassant():

        splitFen[3] = '-'

        Data.enPassantSquare = -1



    if mode == 'add':

        addEnPassant()

    elif mode == 'remove':

        removeEnPassant()

    else:

        raise Exception('Mode not Found')
    
    Data.codeFen = ' '.join(splitFen)



def castlingHandler(mode: str, squareIndex = -1):

    def castlingCalculation():

        startIndex = 0 if Data.isWhiteTurn else 2

        endIndex = 2 if Data.isWhiteTurn else 4

        squaresToSearch = [[0, 1, 2, 3, 4], [4, 5, 6, 7], [56, 57, 58, 59, 60], [60, 61, 62, 63]]

        squares = []

        squareRequirements = [[13, 0, 0, 0, 9], [9, 0, 0, 13], [21, 0, 0, 0, 17], [17, 0, 0, 21]]

        for searchSquares in range(startIndex, endIndex):

            for square in squaresToSearch[searchSquares]:

                if square in Data.movedPieces and ((Data.boardArray[square] == 9 or Data.boardArray[square] == 17) or (Data.boardArray[square] == 13 or Data.boardArray[square] == 21)):

                    break 

                squares.append(Data.boardArray[square])

            if squares == squareRequirements[searchSquares]:

                if searchSquares == 0 or searchSquares == 2:

                    if 4 in Data.moves or 60 in Data.moves:

                        if Data.isWhiteTurn and searchSquares == 0:

                            Data.moves[4].append(2)

                        elif not Data.isWhiteTurn and searchSquares == 2:

                            Data.moves[60].append(58)

                    else:

                        if  Data.isWhiteTurn and searchSquares == 0:

                            Data.moves[4] = [2]

                        elif not Data.isWhiteTurn and searchSquares == 2:

                            Data.moves[60] = [58]

                elif searchSquares == 1 or searchSquares == 3:

                    if 4 in Data.moves or 60 in Data.moves:

                        if Data.isWhiteTurn and searchSquares == 1:

                            Data.moves[4].append(6)

                        elif not Data.isWhiteTurn and searchSquares == 3:

                            Data.moves[60].append(62)

                    else:

                        if Data.isWhiteTurn and searchSquares == 1:

                            Data.moves[4] = [6]

                        elif not Data.isWhiteTurn and searchSquares == 3:

                            Data.moves[60] = [62]

            squares = []

    def castleFenHandler():

        splitFen = Data.codeFen.split(' ')
                
        if squareIndex == 0 and 'K' in splitFen[2]:

            castlingLetters = [*splitFen[2]]

            castlingLetters.remove('K')

            splitFen[2] = ''.join(castlingLetters)

        elif squareIndex == 7 and 'Q' in splitFen[2]:

            castlingLetters = [*splitFen[2]]

            castlingLetters.remove('Q')

            splitFen[2] = ''.join(castlingLetters)

        elif squareIndex == 56 and 'k' in splitFen[2]:

            castlingLetters = [*splitFen[2]]

            castlingLetters.remove('k')

            splitFen[2] = ''.join(castlingLetters)

        elif squareIndex == 63 and 'q' in splitFen[2]:

            castlingLetters = [*splitFen[2]]

            castlingLetters.remove('q')

            splitFen[2] = ''.join(castlingLetters)

        elif squareIndex == 4 and ('K' in splitFen[2] or 'Q' in splitFen[2]):

            castlingLetters = [*splitFen[2]]

            if 'K' in castlingLetters:

                castlingLetters.remove('K')

            if 'Q' in castlingLetters:

                castlingLetters.remove('Q')

            splitFen[2] = ''.join(castlingLetters)

        elif squareIndex == 60 and ('k' in splitFen[2] or 'q' in splitFen[2]):

            castlingLetters = [*splitFen[2]]

            if 'k' in castlingLetters:

                castlingLetters.remove('k')

            if 'q' in castlingLetters:

                castlingLetters.remove('q')

            splitFen[2] = ''.join(castlingLetters)

        if len(splitFen[2]) == 0:

            splitFen[2] = '-'

        Data.codeFen = ' '.join(splitFen)

    if mode == 'add':

        castlingCalculation()

    elif mode == 'remove':

        castleFenHandler()

    else:

        raise Exception('Mode not Found')



def pawnPromotionHandler(square, screen):

    selectionTable = {

        0 : (11,19),
        1 : (12,20),
        2 : (13,21),
        3 : (14,22)

    }

    squareCord = square * 100 if square < 50 else (square - 56) * 100

    screenX = squareCord + 150

    screenY = 100 if square in range(56, 64) else 900

    screenSurf = pygame.Surface((81, 81))

    backgroundSurf = pygame.Surface((75,75))

    while True:

        mouseInputX, mouseInputY = -1, -1

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:

                mouseInputX, mouseInputY = pygame.mouse.get_pos()

        drawBoard(50, 100, screen)

        for selectionSquare in range(0, 4):

            pieceOrder = ((11, 12, 13, 14), (19, 20, 21, 22))

            textureAddress = getTextureAddress(pieceOrder[Data.isWhiteTurn][selectionSquare])

            imageSurf = pygame.image.load(textureAddress)

            imageSurf = pygame.transform.scale(imageSurf, (80,80))

            screenSurf.fill(Data.BLACK)

            backgroundSurf.fill(Data.WHITE)

            screenSurf.blit(backgroundSurf, (3,3))

            screenSurf.blit(imageSurf, (0,0))

            screen.blit(screenSurf, (screenX, screenY + (selectionSquare * 80) if not Data.isWhiteTurn else screenY - 80 - (selectionSquare * 80)))


        if mouseInputX in range(screenX, screenX + 80) and mouseInputY in range(screenY, screenY + 320 if not Data.isWhiteTurn else screenY - 320, 1 if not Data.isWhiteTurn else -1):

            mouseSelection = (mouseInputY // 80) - 1 if not Data.isWhiteTurn else ((mouseInputY // 80) - 10) * -1

            Data.boardArray[square] = selectionTable[mouseSelection][0] if not Data.isWhiteTurn else selectionTable[mouseSelection][1]

            break


        drawUI(screen)

        pygame.display.flip()

        screen.fill(Data.BACKGROUNDCOLOR)



def drawUI(screen):

    drawText(f'Time Elapsed:', Data.WHITE, 1000, 100, screen)

    drawText(f'{strftime("%H:%M:%S", gmtime(pygame.time.get_ticks() // 1000))}', Data.WHITE, 1060, 150, screen)

    drawText(f'White Points: {Data.whitePoints}', Data.WHITE, 900, 300, screen)

    drawText(f'Black Points: {Data.blackPoints}', Data.WHITE, 904, 350, screen)

    drawStatusBox(263, 25, screen)



def drawStatusBox(x, y, Screen):


    msgColor = Data.WHITE

    msgText = ''

    if Data.isWhiteTurn or Data.kingBlackState == 2:

        msgColor = Data.WHITE

    if Data.kingBlackState == 2 or Data.kingWhiteState == 2:

        msgText = 'White Side Wins' if Data.kingBlackState == 2 else 'Black Side Wins'

    elif Data.gameState == 3:

        msgText = "           Draw"

    elif Data.isWhiteTurn:

        msgText = "White Side's Turn"

    elif not Data.isWhiteTurn:

        msgText = "Black Side's Turn"


    textBox = Data.fontLarge.render(msgText, True, msgColor)

    Screen.blit(textBox, (x, y))



def updateGameState():

    if Data.kingWhiteState == 2 or Data.kingBlackState == 2:

        Data.gameState = 1 if Data.kingBlackState == 2 else 2


    if Data.turnHalf == 100:

        Data.gameState = 3



def updateTurn():

    splitFen = Data.codeFen.split(' ')

    if Data.isWhiteTurn:
        
        Data.isWhiteTurn = False
        splitFen[1] = 'b'

    else:

        Data.isWhiteTurn = True
        splitFen[1] = 'w'

        Data.turnFull += 1

        splitFen[len(splitFen) - 1] = str(Data.turnFull)

    if (Data.originalSquareValue == 10 or Data.originalSquareValue == 18) or Data.totalPiecesLastTurn > Data.totalPieces:
        
        Data.turnHalf = 0

        splitFen[len(splitFen) - 2] = str(Data.turnHalf)

    else:

        Data.turnHalf += 1

        splitFen[len(splitFen) - 2] = str(Data.turnHalf)

    Data.codeFen = ' '.join(splitFen)

    Data.totalPieces = 0



def updatePoints():

    if Data.isWhiteTurn and Data.pieceTaken in Data.piecePointValues: 

        Data.whitePoints += Data.piecePointValues[Data.pieceTaken]

    elif Data.pieceTaken in Data.piecePointValues:

        Data.blackPoints += Data.piecePointValues[Data.pieceTaken]



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

                Data.totalPieces += 1
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

    #Memory Leak?

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



def checkMoveHandler():

    movesToBeRemoved = []

    squaresToBeRemoved = []

    for square in Data.moves:
        for move in Data.moves[square]:

            if isKing(Data.boardArray[square]):

                break

            elif ((Data.boardArray[square] < 16 and Data.kingWhiteState == 1) or (Data.boardArray[square] > 16 and Data.kingBlackState == 1)) and move not in Data.kingCheckingSquares:#move not in Data.kingCheckingSquares and ((Data.kingWhiteState == 1 and isOurTurn(Data.boardArray[square])) or (Data.kingBlackState == 1 and isOurTurn(Data.boardArray[square]))):

                movesToBeRemoved.append(move)

        for move in movesToBeRemoved:

            Data.moves[square].remove(move)

        if len(Data.moves[square]) == 0:

            squaresToBeRemoved.append(square)

        movesToBeRemoved = []
                
    for square in squaresToBeRemoved:

        Data.moves.pop(square)

    Data.kingCheckingSquares = []


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

            if square in Data.pinnedSquares and len(Data.moves) > 0:

                if piece == 9:

                    Data.kingWhiteState = 1

                else:

                    Data.kingBlackState = 1

                break
            
            elif len(Data.moves) == 0:

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

                    



def generatePawnMoves(startsquare, piece):

    pieceDirection = 1 if piece > 16 else 0

    numSquares = Data.MoveData.numSquaresToEdge[startsquare][0] if piece == 10 else Data.MoveData.numSquaresToEdge[startsquare][1]

    if (7 < startsquare < 16 and piece < 16) or (47 < startsquare < 56 and piece > 16):

        for i in range(2):

            if i == 0:

                for j in range(-1, 2, 2):

                    numSquaresX = -1

                    if i == -1:

                        numSquaresX = Data.MoveData.numSquaresToEdge[startsquare][2]

                    elif i == 1:

                        numSquaresX = Data.MoveData.numSquaresToEdge[startsquare][3]

                    if numSquaresX == 0:

                        continue

                    targetSquare = startsquare + Data.directionalOffsets[pieceDirection] + j
                    pieceOnTargetSquare = Data.boardArray[targetSquare]

                    if isKing(pieceOnTargetSquare) and not isFriendly(piece, pieceOnTargetSquare):

                        Data.pinnedSquares.append(targetSquare)

                        Data.kingCheckingSquares.append(startsquare)

                        break

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

            if pieceOnTargetSquare != 0 or not isOurTurn(piece):

                continue

            if startsquare not in Data.moves:

                Data.moves[startsquare] = [targetSquare]

            else:

                Data.moves[startsquare].append(targetSquare)

    else:

        for i in range(-1, 2):

            numSquaresX = -1

            if numSquares == 0:

                if not isOurTurn(piece):

                    Data.pawnPromotion, Data.pawnPromotionSquare = True, startsquare

                break

            if i == -1:

                numSquaresX = Data.MoveData.numSquaresToEdge[startsquare][2]

            elif i == 1:

                numSquaresX = Data.MoveData.numSquaresToEdge[startsquare][3]

            if numSquaresX == 0:

                continue

            targetSquare = startsquare + Data.directionalOffsets[pieceDirection] + i
            pieceOnTargetSquare = Data.boardArray[targetSquare]

            if isKing(pieceOnTargetSquare) and not isFriendly(piece, pieceOnTargetSquare):

                Data.pinnedSquares.append(targetSquare)

                Data.kingCheckingSquares.append(startsquare)

                break

            if i != 0 and not isOurTurn(piece):#(pieceOnTargetSquare == 0 or isFriendly(piece, pieceOnTargetSquare)) and not isOurTurn(piece):

                Data.pinnedSquares.append(targetSquare)

            if (i == 0 and pieceOnTargetSquare != 0) or not isOurTurn(piece):

                continue

            elif i != 0 and (pieceOnTargetSquare != 0 and not isFriendly(piece, pieceOnTargetSquare)) or i == 0 or targetSquare == Data.enPassantSquare and pieceOnTargetSquare == 0:

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

                if isKing(pieceOnTargetSquare) and not isFriendly(piece, pieceOnTargetSquare):

                    Data.pinnedSquares.append(targetSquare)

                    Data.kingCheckingSquares.append(startsquare)

                    break

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

    squaresTraveled = 0

    for direction in range(startDirIndex,endDirIndex):

        numSquares = Data.MoveData.numSquaresToEdge[startsquare][direction]

        squaresTraveled = 1

        for n in range(0, numSquares):

            targetSquare = startsquare + Data.directionalOffsets[direction] * (n + 1)
            pieceOnTargetSquare = Data.boardArray[targetSquare]

            if not isOurTurn(piece):

                if isKing(pieceOnTargetSquare) and not isFriendly(piece, pieceOnTargetSquare):

                    offsetTable = {

                        0 : -8,
                        1 : 8,
                        2 : 1,
                        3 : -1,
                        4 : -7,
                        5 : 7,
                        6 : -9,
                        7 : 9

                    }

                    for dangerSquares in range(1, squaresTraveled):

                        Data.kingCheckingSquares.append(targetSquare + (dangerSquares * offsetTable[direction]))

                    else:

                        if squaresTraveled == 1:

                            Data.kingCheckingSquares.append(targetSquare + squaresTraveled)

                    for remainingSquares in range(n, numSquares):

                        targetSquare = startsquare + Data.directionalOffsets[direction] * (remainingSquares + 1)

                        Data.pinnedSquares.append(targetSquare)

                    break

                if isFriendly(piece, pieceOnTargetSquare):

                    Data.pinnedSquares.append(targetSquare)

                if pieceOnTargetSquare == 0:

                    squaresTraveled += 1

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



def enterEndGameState():

    while True:

        for event in pygame.event.get():

            if event == pygame.QUIT:

                pygame.quit()

                exit()

            elif event == pygame.MOUSEBUTTONDOWN:

                mouseX, mouseY = pygame.mouse.get_pos()

            
        
            


def initializeGame():

    updatePositionFromFen(Data.codeFen)

    generateMoves()
    