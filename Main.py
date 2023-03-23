import pygame
import sys
import Functions
import Data

pygame.init()

testClock = pygame.time.Clock()


pygame.display.set_caption('Chess by Vladislav Petkov')


screen = pygame.display.set_mode((1400,1000))

mouseDraging = False
mouseSurf = pygame.Surface((100,100))
currentPieceAddress = ''
pieceMoved = False

Functions.updatePositionFromFen(Data.codeFen)
Functions.generateMoves()

while True:
    
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

                #-- Needs Rework--

                if 0 < Data.boardArray[Data.originalSquareIndex] < 16 and Data.isWhiteTurn:

                    mouseDraging = True

                    Data.originalSquareValue = Data.boardArray[Data.originalSquareIndex]

                    currentPieceAddress = Functions.getTextureAddress(Data.boardArray[Data.originalSquareIndex])                

                    Data.boardArray[Data.originalSquareIndex] = 0

                elif Data.boardArray[Data.originalSquareIndex] > 16 and not Data.isWhiteTurn:

                    mouseDraging = True

                    Data.originalSquareValue = Data.boardArray[Data.originalSquareIndex]

                    currentPieceAddress = Functions.getTextureAddress(Data.boardArray[Data.originalSquareIndex])                

                    Data.boardArray[Data.originalSquareIndex] = 0

                print(f'rank - {rank} file - {file} index - {Data.originalSquareIndex}')

        elif event.type == pygame.MOUSEBUTTONUP:

            if (50 < mouseX < 850) and (100 < mouseY < 900) and mouseDraging == True:

                rank = (((mouseY - 100) // 100) - 7) * -1

                file = (mouseX - 50) // 100

                squareIndex = rank * 8 + file

                #---Needs rework---

                if squareIndex != Data.originalSquareIndex and (Data.boardArray[squareIndex] > 16 or Data.boardArray[squareIndex] == 0) and squareIndex in Data.moves[Data.originalSquareIndex] and Data.isWhiteTurn:

                    Data.boardArray[squareIndex] = Data.originalSquareValue

                    currentPieceAddress = ''

                    mouseDraging = False

                    pieceMoved = True

                elif squareIndex != Data.originalSquareIndex and (Data.boardArray[squareIndex] < 16 or Data.boardArray[squareIndex] == 0) and squareIndex in Data.moves[Data.originalSquareIndex] and not Data.isWhiteTurn:

                    Data.boardArray[squareIndex] = Data.originalSquareValue

                    currentPieceAddress = ''

                    mouseDraging = False

                    pieceMoved = True

                else:

                    Data.boardArray[Data.originalSquareIndex] = Data.originalSquareValue

                    currentPieceAddress = ''

                    mouseDraging = False

                    pieceMoved = False

                    Data.originalSquareIndex = -1

    if event.type == pygame.MOUSEMOTION or currentPieceAddress != '':
        
        if mouseDraging:

            mouseX,mouseY = pygame.mouse.get_pos()
                
            pieceTexture = pygame.image.load(currentPieceAddress)

            screen.blit(pieceTexture,(mouseX - 50, mouseY - 50))


    if pieceMoved:

        Functions.updateFenFromPosition(Data.boardArray)

        Functions.updateTurn()

        Functions.updatePositionFromFen(Data.codeFen)

        Data.moves = {}

        Functions.generateMoves()

        Data.originalSquareIndex = -1

        pieceMoved = False

    pygame.display.flip()

    screen.fill((25,25,25))

# Test Version 1.3