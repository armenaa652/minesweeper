import pygame
import sys
import random
from pygame.locals import *

BLACK = (0, 0, 0)
DARKGREY = (60, 60, 60)
GREY = (100,100,100)
LIGHTGREY = (190, 190, 190)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 204, 0)
WHITE = (255, 255, 255)

pygame.init()

mainClock = pygame.time.Clock()

WINDOWWIDTH = 624
WINDOWHEIGHT = 624


windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Minesweeper')


def waitForPlayerToPressKey():
    while True:
        for gameEvent in pygame.event.get():
            if gameEvent.type == QUIT:
                pygame.quit()
                sys.exit()
            if gameEvent.type == MOUSEBUTTONUP:
                return

def chooseDifficulty():
    basicFont = pygame.font.SysFont(None, 90)
    BUTTONWIDTH = 400
    BUTTONHEIGHT = 70
    easy = pygame.Rect(WINDOWWIDTH/2-BUTTONWIDTH/2,280,BUTTONWIDTH,BUTTONHEIGHT)
    etext = basicFont.render('Easy', True, WHITE)
    etextpos = etext.get_rect()
    etextpos.centerx = easy.centerx
    etextpos.centery = easy.centery
    ecolor = GREY
    medium = pygame.Rect(WINDOWWIDTH / 2 - BUTTONWIDTH / 2, 360, BUTTONWIDTH, BUTTONHEIGHT)
    mtext = basicFont.render('Medium', True, WHITE)
    mtextpos = mtext.get_rect()
    mtextpos.centerx = medium.centerx
    mtextpos.centery = medium.centery
    mcolor = GREY
    hard = pygame.Rect(WINDOWWIDTH / 2 - BUTTONWIDTH / 2, 440, BUTTONWIDTH, BUTTONHEIGHT)
    htext = basicFont.render('Hard', True, WHITE)
    htextpos = htext.get_rect()
    htextpos.centerx = hard.centerx
    htextpos.centery = hard.centery
    hcolor = GREY
    windowSurface.fill((150, 150, 150))
    while True:

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                if easy.collidepoint(mousepos[0],mousepos[1]):
                    ecolor = DARKGREY
                if medium.collidepoint(mousepos[0],mousepos[1]):
                    mcolor = DARKGREY
                if hard.collidepoint(mousepos[0],mousepos[1]):
                    hcolor = DARKGREY
            if e.type == MOUSEBUTTONUP:
                ecolor = GREY
                mcolor = GREY
                hcolor = GREY
                mousepos = pygame.mouse.get_pos()
                if easy.collidepoint(mousepos[0],mousepos[1]):
                    return [8, 10, 90]
                if medium.collidepoint(mousepos[0],mousepos[1]):
                    return [16, 40, 48]
                if hard.collidepoint(mousepos[0],mousepos[1]):
                    return [24, 99, 38]
            pygame.draw.rect(windowSurface,ecolor, easy)
            pygame.draw.rect(windowSurface, BLACK, easy, 3)
            windowSurface.blit(etext, etextpos)
            pygame.draw.rect(windowSurface, mcolor, medium)
            pygame.draw.rect(windowSurface, BLACK, medium, 3)
            windowSurface.blit(mtext, mtextpos)
            pygame.draw.rect(windowSurface, hcolor, hard)
            pygame.draw.rect(windowSurface, BLACK, hard, 3)
            windowSurface.blit(htext, htextpos)
        pygame.display.update()

def drawCover(cover):
    grid = len(cover)
    for x in range(grid):
        for y in range(grid):
            if cover[x][y] == 0:
                box = pygame.Rect(x * (WINDOWWIDTH / grid), y * (WINDOWHEIGHT / grid), WINDOWHEIGHT / grid, WINDOWWIDTH / grid)
                pygame.draw.rect(windowSurface, LIGHTGREY, box)
                pygame.draw.rect(windowSurface, DARKGREY, box, 1)
            elif cover[x][y] == 2:
                box = pygame.Rect(x * (WINDOWWIDTH / grid), y * (WINDOWHEIGHT / grid), WINDOWHEIGHT / grid, WINDOWWIDTH / grid)
                pygame.draw.rect(windowSurface, YELLOW, box)
                pygame.draw.rect(windowSurface, DARKGREY, box, 1)

def drawBoard(board, color):
    grid = len(board)
    for x in range(grid):
        for y in range(grid):
            if board[x][y] == 10:
                box = pygame.Rect(x * (WINDOWWIDTH / grid), y * (WINDOWHEIGHT / grid), WINDOWHEIGHT / grid, WINDOWWIDTH / grid)
                pygame.draw.rect(windowSurface, color, box)
                pygame.draw.rect(windowSurface, DARKGREY, box, 1)
            else:
                box = pygame.Rect(x * (WINDOWWIDTH / grid), y * (WINDOWHEIGHT / grid), WINDOWHEIGHT / grid, WINDOWWIDTH / grid)
                pygame.draw.rect(windowSurface, WHITE, box)
                pygame.draw.rect(windowSurface, BLACK, box, 1)
                if not board[x][y] == 0:
                    drawText(board[x][y],box)

def createCover(grid):
    cover = []
    for i in range(grid):
        add = [0] * grid
        cover.append(add)
    coverRect = [[pygame.Rect(x * (WINDOWWIDTH / grid), y * (WINDOWHEIGHT / grid), WINDOWHEIGHT / grid,WINDOWWIDTH / grid) for y in range(grid)] for x in range(grid)]
    return [cover, coverRect]

def getBoardCopy(board):
    boardCopy = createBoard(len(board))
    for x in range(len(board)):
        for y in range(len(board)):
            boardCopy[x][y] = board[x][y]

    return boardCopy

def createBoard(grid):
    board = []
    for i in range(grid):
        add = [0] * grid
        board.append(add)
    return board

def addMines(grid, bombcount, x, y):
    while True:
        copyBoard = createBoard(grid)
        for k in range(bombcount):
            while True:
                i = random.randint(0,grid-1)
                j = random.randint(0,grid-1)
                if not copyBoard[j][i] == 10:
                    copyBoard[j][i] = 10
                    break
        copyBoard = analyzeBoard(copyBoard)
        if copyBoard[x][y] == 0:
            return copyBoard

def drawText(text, box):
    font = pygame.font.SysFont(None, TEXTSIZE)
    color = getColor(text)
    textobj = font.render(str(text), False, color)
    textrect = textobj.get_rect()
    textrect.centerx = box.centerx
    textrect.centery = box.centery
    windowSurface.blit(textobj, textrect)

def getColor(number):
    BLUE = (0, 0, 255)
    GREEN = (0, 128, 0)
    RED = (255, 0, 0)
    PURPLE = (75, 0, 130)
    MAROON = (80, 0, 0)
    TURQUOISE =  (95, 158, 160)
    BLACK = (0, 0, 0)
    GRAY = (150, 150, 150)
    if number == 1:
        return BLUE
    elif number == 2:
        return GREEN
    elif number == 3:
        return RED
    elif number == 4:
        return PURPLE
    elif number == 5:
        return MAROON
    elif number == 6:
        return TURQUOISE
    elif number == 7:
        return BLACK
    elif number == 8:
        return GRAY

def getFirstClick():
    while True:
        windowSurface.fill(WHITE)
        for clickEvent in pygame.event.get():
            if clickEvent.type == QUIT:
                pygame.quit()
                sys.exit()
            if clickEvent.type == MOUSEBUTTONUP:
                if clickEvent.button == 1:
                    for i in range(gridSize):
                        for j in range(gridSize):
                            pos = pygame.mouse.get_pos()
                            if coverBoardRect[j][i].collidepoint(pos):
                                coverBoard[j][i] = 1
                                return [j, i]

        drawCover(coverBoard)
        pygame.display.update()

def exposeZeros(board, cover):
    while True:
        coverCopy = getBoardCopy(cover)
        grid = len(board)
        for i in range(grid):
            for j in range(grid):
                if cover[j][i] == 1 and board[j][i] == 0:
                    right = left = down = up = downright = downleft = upright = upleft = True
                    if i == 0 and j == 0:
                        up = upright = upleft = left = downleft = False
                    elif j == 0 and i == grid - 1:
                        upleft = left = downleft = down = downright = False
                    elif i == grid - 1 and j == grid - 1:
                        upright = right = downright = down = downleft = False
                    elif j == grid - 1 and i == 0:
                        upleft = up = upright = right = downright = False
                    elif i == 0:
                        upleft = up = upright = False
                    elif j == 0:
                        upleft = left = downleft = False
                    elif i == grid - 1:
                        downleft = down = downright = False
                    elif j == grid - 1:
                        upright = right = downright = False
                    if right:
                        cover[j + 1][i] = 1
                    if downright:
                        cover[j + 1][i + 1] = 1
                    if upright:
                        cover[j + 1][i - 1] = 1
                    if left:
                        cover[j - 1][i] = 1
                    if downleft:
                        cover[j - 1][i + 1] = 1
                    if upleft:
                        cover[j - 1][i - 1] = 1
                    if down:
                        cover[j][i + 1] = 1
                    if up:
                        cover[j][i - 1] = 1
        if coverCopy == cover:
            break
    return cover

def analyzeBoard(board):
    grid = len(board)
    for i in range(grid):
        for j in range(grid):
            count = 0
            right = left = down = up = downright = downleft = upright = upleft = True
            if i == 0 and j == 0:
                up = upright = upleft = left = downleft = False
            elif j == 0 and i == grid - 1:
                upleft = left = downleft = down = downright = False
            elif i == grid-1 and j == grid - 1:
                upright = right = downright = down = downleft = False
            elif j == grid - 1 and i == 0:
                upleft = up = upright = right = downright = False
            elif i == 0:
                upleft = up = upright = False
            elif j == 0:
                upleft = left = downleft = False
            elif i == grid - 1:
                downleft = down = downright = False
            elif j == grid - 1:
                upright = right = downright = False
            if right:
                if board[j + 1][i] == 10:
                    count += 1
            if downright:
                if board[j + 1][i + 1] == 10:
                    count += 1
            if upright:
                if board[j + 1][i - 1] == 10:
                    count += 1
            if left:
                if board[j - 1][i] == 10 and left:
                    count += 1
            if downleft:
                if board[j - 1][i + 1] == 10:
                    count += 1
            if upleft:
                if board[j - 1][i - 1] == 10:
                    count += 1
            if down:
                if board[j][i + 1] == 10:
                    count += 1
            if up:
                if board[j][i - 1] == 10:
                    count += 1
            if not board[j][i] == 10:
                board[j][i] = count
    return board

def isGameWon(board, cover):
    won = True
    for y in range(len(board)):
        for x in range(len(board)):
            if board[x][y] == 10:
                if not cover[x][y] == 2:
                    won = False
            if cover[x][y] == 2:
                if not board[x][y] == 10:
                    won = False
    return won

def isGameLost(board, cover):
    lost = False
    for y in range(len(board)):
        for x in range(len(board)):
            if board[x][y] == 10:
                if cover[x][y] == 1:
                    lost = True
    return lost

while True:
    [gridSize, numOfBombs, TEXTSIZE] = chooseDifficulty()
    [coverBoard, coverBoardRect] = createCover(gridSize)
    [firstx, firsty] = getFirstClick()
    gameBoard = addMines(gridSize, numOfBombs, firstx, firsty)
    gameBoard = analyzeBoard(gameBoard)
    coverBoard = exposeZeros(gameBoard, coverBoard)
    while True:
        windowSurface.fill(WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    #optimize by calculating i and j and don't use collide point at all!
                    for a in range(gridSize):
                        for b in range(gridSize):
                            pos = pygame.mouse.get_pos()
                            if coverBoardRect[b][a].collidepoint(pos) and coverBoard[b][a] == 0:
                                coverBoard[b][a] = 1
                                if gameBoard[b][a] == 0:
                                    coverBoard = exposeZeros(gameBoard, coverBoard)
                elif event.button == 3:
                    for a in range(gridSize):
                        for b in range(gridSize):
                            pos = pygame.mouse.get_pos()
                            if coverBoardRect[b][a].collidepoint(pos):
                                if coverBoard[b][a] == 0:
                                    coverBoard[b][a] = 2
                                elif coverBoard[b][a] == 2:
                                    coverBoard[b][a] = 0
        drawBoard(gameBoard, RED)
        drawCover(coverBoard)
        if isGameWon(gameBoard, coverBoard):
            print('You Win')
            drawBoard(gameBoard, GREEN)
            pygame.display.update()
            waitForPlayerToPressKey()
            break
        if isGameLost(gameBoard, coverBoard):
            print('You Lose')
            drawBoard(gameBoard, RED)
            pygame.display.update()
            waitForPlayerToPressKey()
            break
        pygame.display.update()
