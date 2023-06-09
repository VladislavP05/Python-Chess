import pygame
import sys
import Functions
import Data
from time import time



pygame.init()

testClock = pygame.time.Clock()

programFont = pygame.font.Font(None, 65)

pygame.display.set_caption('Chess by Vladislav Petkov')

screen = pygame.display.set_mode((1400,1000))

mouseDraging = False

mouseSurf = pygame.Surface((100,100))

currentPieceAddress = ''

pieceMoved = False

Functions.initializeGame()



while True:

    Data.startTimer = time()
    
    testClock.tick(120)

    Functions.drawBoard(50,100, screen)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()

            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouseX,mouseY = pygame.mouse.get_pos()

            if (50 < mouseX < 850) and (100 < mouseY < 900) and mouseDraging == False:

                rank = (((mouseY - 100) // 100) - 7) * -1

                file = (mouseX - 50) // 100

                Data.originalSquareIndex = rank * 8 + file

                Data.originalSquareValue = Data.boardArray[Data.originalSquareIndex]

                if Data.boardArray[Data.originalSquareIndex] > 0 and Functions.isOurTurn(Data.boardArray[Data.originalSquareIndex]):

                    mouseDraging = True

                    currentPieceAddress = Functions.getTextureAddress(Data.boardArray[Data.originalSquareIndex])                

                    Data.boardArray[Data.originalSquareIndex] = 0

        elif event.type == pygame.MOUSEBUTTONUP:

            if (50 < mouseX < 850) and (100 < mouseY < 900) and mouseDraging == True:

                rank = (((mouseY - 100) // 100) - 7) * -1

                file = (mouseX - 50) // 100

                squareIndex = rank * 8 + file

                if Data.originalSquareIndex not in Data.moves or squareIndex not in Data.moves[Data.originalSquareIndex]:

                    Data.boardArray[Data.originalSquareIndex] = Data.originalSquareValue

                    currentPieceAddress = ''

                    mouseDraging = False

                    pieceMoved = False

                    Data.originalSquareIndex = -1

                elif squareIndex != Data.originalSquareIndex and squareIndex in Data.moves[Data.originalSquareIndex]:

                    Data.moveSquareIndex = squareIndex

                    Data.pieceTaken = Data.boardArray[Data.moveSquareIndex]

                    Data.boardArray[squareIndex] = Data.originalSquareValue

                    currentPieceAddress = ''

                    mouseDraging = False

                    pieceMoved = True

    if event.type == pygame.MOUSEMOTION or currentPieceAddress != '':
        
        if mouseDraging:

            mouseX,mouseY = pygame.mouse.get_pos()
                
            pieceTexture = pygame.image.load(currentPieceAddress)

            screen.blit(pieceTexture,(mouseX - 50, mouseY - 50))

    if pieceMoved:

        if (Data.originalSquareValue == 10 or Data.originalSquareValue == 18) and (Data.originalSquareIndex in range(8, 16) or Data.originalSquareIndex in range(48, 56)) and (Data.moveSquareIndex in range(24, 32) or Data.moveSquareIndex in range(32, 40)):

            Functions.enPassantHandler(Data.moveSquareIndex, 'add')

        elif (Data.originalSquareValue == 10 or Data.originalSquareValue == 18) and Data.moveSquareIndex == Data.enPassantSquare:

            if Data.isWhiteTurn:

                Data.pieceTaken = Data.boardArray[Data.enPassantSquare - 8]

                Data.boardArray[Data.enPassantSquare - 8] = 0

            else:

                Data.pieceTaken = Data.boardArray[Data.enPassantSquare + 8]

                Data.boardArray[Data.enPassantSquare + 8] = 0

            Functions.enPassantHandler(Data.moveSquareIndex, 'remove')

        elif (Data.originalSquareValue == 10 or Data.originalSquareValue == 18) and (Data.originalSquareIndex in range(24, 32) or Data.originalSquareIndex in range(32, 40)) and (Data.moveSquareIndex in range(32, 40) or Data.moveSquareIndex in range(24, 32)) or Functions.isOurTurn(Data.originalSquareValue):

            Functions.enPassantHandler(Data.moveSquareIndex, 'remove')

        if (Data.originalSquareIndex == 4 or Data.originalSquareIndex == 60) or (Data.originalSquareIndex == 0 or Data.originalSquareIndex == 7) or (Data.originalSquareIndex == 56 or Data.originalSquareIndex == 63):

            Functions.castlingHandler('remove', Data.originalSquareIndex)

        if Data.originalSquareIndex == 4 and Data.moveSquareIndex == 2 and Data.originalSquareIndex not in Data.movedPieces:

            Data.boardArray[3] = 13

            Data.boardArray[0] = 0

        elif Data.originalSquareIndex == 4 and Data.moveSquareIndex == 6 and Data.originalSquareIndex not in Data.movedPieces:

            Data.boardArray[5] = 13

            Data.boardArray[7] = 0

        elif Data.originalSquareIndex == 60 and Data.moveSquareIndex == 58 and Data.originalSquareIndex not in Data.movedPieces:

            Data.boardArray[59] = 21

            Data.boardArray[56] = 0

        elif Data.originalSquareIndex == 60 and Data.moveSquareIndex == 62 and Data.originalSquareIndex not in Data.movedPieces:

            Data.boardArray[61] = 21

            Data.boardArray[63] = 0

        Functions.updateFenFromPosition(Data.boardArray)

        Functions.calculatePiecesOnBoard()

        if Data.totalPieces < Data.totalPiecesLastTurn:

            Functions.updatePoints()

        Data.totalPiecesLastTurn = Data.totalPieces

        Functions.updateTurn()

        Functions.updatePositionFromFen(Data.codeFen)

        Data.moves = {}

        Data.pinnedSquares = []

        if (Data.kingWhiteState == 0 and Data.isWhiteTurn) or (Data.kingBlackState == 0 and not Data.isWhiteTurn):

            Functions.castlingHandler('add')

        Functions.generateMoves()

        if Data.pawnPromotion:

            Functions.pawnPromotionHandler(Data.pawnPromotionSquare, screen)

            Data.pawnPromotion, Data.pawnPromotionSquare = False, -1

        Functions.generateKingMoves()

        Functions.checkForChecks()

        if Data.kingWhiteState == 1 or Data.kingBlackState == 1:

            Functions.checkMoveHandler()

        Functions.checkForChecks()

        Functions.updateGameState()

        Data.moveFenCodes.append(Data.codeFen)

        if Data.gameState != 0:

            Functions.enterEndGameState(screen)

        if Data.originalSquareIndex not in Data.movedPieces:

            Data.movedPieces.append(Data.originalSquareIndex)

        Data.lastPieceMoved = Data.originalSquareValue

        print(f"Fen: {Data.codeFen}")

        Data.pieceTaken = 0

        Data.originalSquareIndex = -1

        pieceMoved = False

    Data.endTimer = time()

    Data.timePlayed += Data.endTimer - Data.startTimer

    Functions.drawUI(screen)

    pygame.display.flip()

    screen.fill(Data.BACKGROUNDCOLOR)

# Test Version 1.0
