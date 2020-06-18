# Slide Puzzle
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import pygame, sys, random
from pygame.locals import *
import puzzle as pz

# Create the constants (go ahead and experiment with different values)
board_size = 4  # number of rows/columns in the board
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHTBLUE = (0, 50, 255)
DARKTURQUOISE = (3, 54, 73)
GREEN = (0, 204, 0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * board_size + (board_size - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * board_size + (board_size - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # Store the option buttons and their rectangles in OPTIONS.
    RESET_SURF, RESET_RECT = makeText('Reset', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    NEW_SURF, NEW_RECT = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    SOLVE_SURF, SOLVE_RECT = makeText('Solve', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

    genBoard = generateNewPuzzle(4)
    mainBoard = pz.copy_board(genBoard)
    msg = 'Click tile or press arrow keys to slide.'  # contains the message to show in the upper left corner.
    drawBoard(mainBoard, msg)

    while True:  # main game loop
        slideTo = None  # the direction, if any, a tile should slide

        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    # check if the user clicked on an option button
                    if RESET_RECT.collidepoint(event.pos):
                        mainBoard = pz.copy_board(genBoard)  # clicked on Reset button
                        drawBoard(mainBoard, msg)

                    elif NEW_RECT.collidepoint(event.pos):
                        genBoard = generateNewPuzzle(16)  # clicked on New Game button
                        mainBoard = pz.copy_board(genBoard)
                        drawBoard(mainBoard, msg)

                    elif SOLVE_RECT.collidepoint(event.pos):
                        solution = pz.solve(mainBoard)
                        resetAnimation(mainBoard, solution)  # clicked on Solve button
                else:
                    # check if the clicked tile was next to the blank spot

                    blanky, blankx = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN

            elif event.type == KEYUP:
                # check if the user pressed a key to slide a tile
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN

        if slideTo:
            # slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 8)  # show slide on screen
            mainBoard = makeMove(mainBoard, slideTo)
            drawBoard(mainBoard, msg)
            # allMoves.append(slideTo)  # record the slide
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP):  # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event)  # put the other KEYUP event objects back


def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space.
    return pz.loc_space(board)


def makeMove(board, move):
    blankx, blanky = getBlankPosition(board)
    tileX, tileY = blankx, blanky
    if move == UP:
        tileX += 1
    elif move == DOWN:
        tileX -= 1
    elif move == LEFT:
        tileY += 1
    elif move == RIGHT:
        tileY -= 1

    if tileX in range(len(board)) and tileY in range(len(board)):
        print(f'Moving ... {tileX},{tileY}')
        return pz.result(board, action=(tileX, tileY))
    else:
        print(f'Ignoring ... {tileX},{tileY}')
    return board


def isValidMove(board, move):
    return True
    # blankx, blanky = getBlankPosition(board)
    # return (move == UP and blanky != len(board[0]) - 1) or \
    #        (move == DOWN and blanky != 0) or \
    #        (move == LEFT and blankx != len(board) - 1) or \
    #        (move == RIGHT and blankx != 0)


def getRandomMove(board, lastMove=None):
    # start with a full list of all four moves
    validMoves = [UP, DOWN, LEFT, RIGHT]

    # remove moves from the list as they are disqualified
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    # return a random move from the list of remaining moves
    return random.choice(validMoves)


def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, space_number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    # print(f'Tile: {tilex},{tiley} = {number}')
    left, top = getLeftTopOfTile(tiley, tilex)
    # print(f'Co-orfinates: {left},{top}')

    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    if number != space_number:
        textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
        textRect = textSurf.get_rect()
        textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
        DISPLAYSURF.blit(textSurf, textRect)
    else:
        baseSurf = DISPLAYSURF.copy()
        pygame.draw.rect(baseSurf, BGCOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
        DISPLAYSURF.blit(baseSurf, (0, 0))


def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)
    print(f'drawBoard: {board}')
    for tilex in range(len(board)):
        for tiley in range(len(board)):
            number = board[tilex][tiley]
            space_number = len(board) ** 2
            drawTile(tilex, tiley, number, space_number)

    left, top = getLeftTopOfTile(0, 0)
    width = board_size * TILESIZE
    height = board_size * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)


def slideAnimation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.
    print(f'slideAnimation {direction}')
    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        tileX = blankx + 1
        tileY = blanky
    elif direction == DOWN:
        tileX = blankx - 1
        tileY = blanky
    elif direction == LEFT:
        tileX = blankx
        tileY = blanky + 1
    elif direction == RIGHT:
        tileX = blankx
        tileY = blanky - 1
    print(f'Sloding tile {(tileX, tileY)}')
    # prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    movex, movey = tileY, tileX
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    number = board[tileX][tileY]
    space_number = len(board) ** 2
    for i in range(0, TILESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, number, space_number, 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, number, space_number, 0, i)
        if direction == LEFT:
            drawTile(movex, movey, number, space_number, -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, number, space_number, i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateNewPuzzle(numSlides):
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    board = pz.starting_board(board_size, numSlides)
    # drawBoard(board, '')
    # pygame.display.update()
    return board


def resetAnimation(board, solution):
    # make all of the moves in allMoves in reverse.
    mainboard = pz.copy_board(board)
    slide_crumb = None
    for tileX, tileY in solution:
        print(f'Solving ... {mainboard}')
        blankx, blanky = getBlankPosition(mainboard)
        if tileY < blanky:
            slideTo = RIGHT
        elif tileY > blanky:
            slideTo = LEFT
        elif tileX > blankx:
            slideTo = UP
        elif tileX < blankx:
            slideTo = DOWN

        if slide_crumb is None:
            slide_crumb = f'{slideTo}'
        else:
            slide_crumb += f' -- {slideTo}'
        mainboard = makeMove(mainboard, slideTo)
        drawBoard(mainboard, f'{slide_crumb}')
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
