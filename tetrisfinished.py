#------------------------------------------------------------------------------------------------------------
#Importing Libraries
from operator import truediv
import pygame
import random
import sys

#Initialising Pygame Font Globally
pygame.font.init()

#Declaring Global Variables
#Window Size Variable
winWidth = 800
winHeight = 650

#Declaring Play Area within Window
plyAreaWidth = 300  #The width of the play area is 10 blocks by 300/30 = 10
plyAreaHeight = 600 #The height of the play area is 20 blocks by 600/30 = 20

#Declaring the size of each block in a shape
blockSize = 30

#The extreme of the screens are declared for sizing later
tpLftX = (winWidth - plyAreaWidth) // 2
tpLftY = winHeight - plyAreaHeight


#------------------------------------------------------------------------------------------------------

#Declaring shapes and rotations

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

i = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

j = [['.....',
      '.0...',
      '.00..',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '.....',
      '.....'],
     ['.....',
      '.....',
      '..00.',
      '...0.',
      '.....'],
     ['.....',
      '.....',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

#Global shapes variable
#List of available shapes for randomising
shapes = [S, Z, I, i, O, J, j, L, T]
#Shape colours has each index correspond with the shape you want that colour to be attributed too
shpColours = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (0, 165, 165), (255, 255, 0), (255, 165, 0), (255, 100, 5), (0, 0, 255), (128, 0, 128)]


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Define class and game functions

#Define class piece which attriputes the pieces game attributes to keep track
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shpColours[shapes.index(shape)]
        self.rotation = 0


#Create grid is used to format the game to work on a grid
def gridGeneration(usedPos={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in usedPos:
                c = usedPos[(j,i)]
                grid[i][j] = c
    return grid



#So convertShapesFormatting takes the shapes specified above and turns them into datat that the computer
#can understand is for pygame. We use enumerate 
def convertShapesFormatting(shape):
    positions = []
    #format is used to determine which set of rotation the the program is actually formatting from the list
    format = shape.shape[shape.rotation % len(shape.shape)]

    #This iterates through the line according to formate and enumarates the data so the computer can use it4
    #By assigning positions for the data
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    #This data formats the positions so they can be displayed on screen
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    #Return positions data to use in game
    return positions


#Valid square is the function to check for space valididty while playing the game
def validSquare(shape, grid):
    #clearSpaces scans the grid for colour blank then adds them to the list but to get this data we
    #have to use a two dimensional list when we really want a 1 dimensional list
    clearSpaces = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    #This line of code flattens out 2 dimensional list and creates a 1 dimensional list
    clearSpaces = [j for sub in clearSpaces for j in sub]

    #We format the shape so the comouter can use it
    formatted = convertShapesFormatting(shape)

    #This goes through formatted and if it isn't valid return false if it gets through the list and it is valid
    #Return true
    for pos in formatted:
        if pos not in clearSpaces:
            if pos[1] > -1:
                return False
    return True


#Game over is the function we use to check if the game is over
def gameOver(positions):
    for pos in positions:
        x, y = pos
        #all we're doing here is checking that the current positions do not exceed the playable
        #are and if it is return that the game is now over
        if y < 1:
            return True
    return False

#This is the function which randomises which shape the player will get next
def randomShape():
    return Piece(5, 0, random.choice(shapes))

#Text middle is referenced when we want to put text in the middle of the screen
def textMiddle(surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (tpLftX + plyAreaWidth /2 - (label.get_width()/2), tpLftY + plyAreaHeight/2 - label.get_height()/2))

#Set of main menu text
def textMain1(surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (tpLftX + plyAreaWidth /2 - (label.get_width()/2), tpLftY + plyAreaHeight/16 - label.get_height()))

def textMain2(surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (tpLftX + plyAreaWidth /2 - (label.get_width()/2), tpLftY + plyAreaHeight/7 - label.get_height()))

def textMain3(surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (tpLftX + plyAreaWidth /8 - (label.get_width()/1.5), tpLftY + plyAreaHeight/5 - label.get_height()/2))

def textMain4(surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (tpLftX + plyAreaWidth /4.2 - (label.get_width()/2), tpLftY + plyAreaHeight/3.5 - label.get_height()/2))

def textMain5(surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (tpLftX + plyAreaWidth /3.15 - (label.get_width()/2), tpLftY + plyAreaHeight/2.75 - label.get_height()/2))

def textMain6(surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (tpLftX + plyAreaWidth /4 - (label.get_width()/2), tpLftY + plyAreaHeight/2.25 - label.get_height()/2))

def textMain7(surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (tpLftX + plyAreaWidth /2.5 - (label.get_width()/2), tpLftY + plyAreaHeight/1.9 - label.get_height()/2))

def buttonPlay(surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (tpLftX + plyAreaWidth /8 - (label.get_width()/0.5), tpLftY + plyAreaHeight/1.25 - label.get_height()/2))

def buttonConfigure(surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (tpLftX + plyAreaWidth /2 - (label.get_width()/2), tpLftY + plyAreaHeight/1.25 - label.get_height()/2))

def buttonQuit(surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (tpLftX + plyAreaWidth /0.85 - (label.get_width()/2), tpLftY + plyAreaHeight/1.25 - label.get_height()/2))        


#visual grid creates a grid for the player to see while playing the game
def visualGrid(surface, grid):
    sx = tpLftX
    sy = tpLftY

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*blockSize), (sx+plyAreaWidth, sy+ i*blockSize))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*blockSize, sy),(sx + j*blockSize, sy + plyAreaHeight))


#This function is for when a player get's a tetris 
def playerTetris(grid, locked):

    detect = 0
    #it detectss each row in the grid and if any row doesn't have a blank square you add it to detect
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            detect += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    #this deletes all the rows from the list 
    if detect > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + detect)
                locked[newKey] = locked.pop(key)

    return detect


#Next shape area both draws the next shape but displays what the next shape will be according to the generated
#next shape
def nextShapeArea(shape, surface):
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = tpLftX + plyAreaWidth + 50
    sy = tpLftY + plyAreaHeight/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    #this convers the shape into a displayable format in the top left corner
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*blockSize, sy + i*blockSize, blockSize, blockSize), 0)

    surface.blit(label, (sx + 10, sy - 30))


#If a new highscore is achieved this edits the scores.txt text file to edit that score
def newHighScore(nscore):
    score = highScore()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


#Highscore fetches the highscore frim the scores.txt text file
def highScore():
    with open('scores.txt', 'r') as value:
        lines = value.readlines()
        score = lines[0].strip()

    return score

#playable window is the function which sets all the elements for the visable game
def playableWindow(surface, grid, score=0, bestScore = 0, numLines = 0):
    #this sets the background fill
    surface.fill((0, 0, 0))

    #tile word values
    pygame.font.init()
    font = pygame.font.SysFont('arial', 45)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (tpLftX + plyAreaWidth / 2 - (label.get_width() / 2), 0))

    #Current score for the game
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = tpLftX + plyAreaWidth + 50
    sy = tpLftY + plyAreaHeight/2 - 100

    surface.blit(label, (sx + 20, sy + 160))
    
    #This displays the highscore
    label = font.render('High Score: ' + bestScore, 1, (255,255,255))

    sx = tpLftX - 250
    sy = tpLftY + 150

    surface.blit(label, (sx + 20, sy + 160))

    #Displays Number of lines
    label = font.render('Number of Lines= ' + str(numLines), 1, (255, 255, 255))
    surface.blit(label, (sx+20, sy+100))

    #Display Group Number
    label = font.render('Group Number: 8', 1, (255, 255, 255))
    surface.blit(label, (sx+20, sy+40))

    #Display Player
    label = font.render('Type = Player', 1, (255, 255, 255))
    surface.blit(label, (sx+20, sy-50))


    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (tpLftX + j*blockSize, tpLftY + i*blockSize, blockSize, blockSize), 0)

    pygame.draw.rect(surface, (255, 0, 0), (tpLftX, tpLftY, plyAreaWidth, plyAreaHeight), 5)

    #Draws the grid
    visualGrid(surface, grid)


#----------------------------------------------------------------------------------------------------------------------------------------------------------


#This is the main game loop
def main(win):
    #Set game variables
    bestScore = highScore()
    #Keeps track of the blocks that are placed down
    usedPositions = {}
    #Generate grid
    grid = gridGeneration(usedPositions)
    #Need to change the piece
    changePiece = False
    #Game over variable
    run = True
    #Declare currentPiece
    currentPiece = randomShape()
    #Declare the nextPiece
    nextPiece = randomShape()
    #Clock start for pygame, used to measure ticks
    clock = pygame.time.Clock()
    #Fall time is used for the constant speed the blocks fall
    fallTime = 0
    #Fall speed is the incrementing speed that the game will increase over time
    fallSpeed = 0.27
    #Level time is the time occured ingame so far
    lvlTime = 0
    #The score variable
    score = 0

    numLines=0

    #While the code is running
    while run:
        #grid generation parsing in the used positions
        grid = gridGeneration(usedPositions)
        #Increment the fall time according to the cock
        fallTime += clock.get_rawtime()
        #Increase leveltime
        lvlTime += clock.get_rawtime()
        #Increment the clock
        clock.tick()

        


        #To be updated with explanations I forgot and didn't wanna error check what I'm doing
        if lvlTime/1000 > 5:
            lvlTime = 0
            if lvlTime > 0.12:
                lvlTime -= 0.005

        if fallTime/1000 > fallSpeed:
            fallTime = 0
            currentPiece.y += 1
            if not(validSquare(currentPiece, grid)) and currentPiece.y > 0:
                currentPiece.y -= 1
                changePiece = True

        #detects if the user is pressing the x button on window frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            #This checks for the event.type of a key being pressed down
            if event.type == pygame.KEYDOWN:
                #From here the program checks if the correct event.key is being used to value a response
                #Afterwards it proceeds to move the piece down and check for validity if not valid reverse move
                #This process runs for all cardinal Directions
                if event.key == pygame.K_LEFT:
                    currentPiece.x -= 1
                    if not(validSquare(currentPiece, grid)):
                        currentPiece.x += 1
                if event.key == pygame.K_RIGHT:
                    currentPiece.x += 1
                    if not(validSquare(currentPiece, grid)):
                        currentPiece.x -= 1
                if event.key == pygame.K_DOWN:
                    currentPiece.y += 1
                    if not(validSquare(currentPiece, grid)):
                        currentPiece.y -= 1
                if event.key == pygame.K_UP:
                    currentPiece.rotation += 1
                    if not(validSquare(currentPiece, grid)):
                        currentPiece.rotation -= 1
                        


        #Assigns the shapes current position
        shapePosition = convertShapesFormatting(currentPiece)


        #This assigns the colour to the grid space when a shape is occupying it
        for i in range(len(shapePosition)):
            x, y = shapePosition[i]
            if y > -1:
                grid[y][x] = currentPiece.color

        #if the game needs to change piece update usedPositions and get the next piece then update score
        if changePiece:
            for pos in shapePosition:
                p = (pos[0], pos[1])
                usedPositions[p] = currentPiece.color
            currentPiece = nextPiece
            nextPiece = randomShape()
            changePiece = False
            score += playerTetris(grid, usedPositions) * 10
            numLines = score/10

        #Remake playable Window
        playableWindow(win, grid, score, bestScore, numLines)
        #Redisplay the next shape area
        nextShapeArea(nextPiece, win)
        #Update pygame display
        pygame.display.update()

        #Game over check
        if gameOver(usedPositions):
            textMiddle(win, "YOU LOST!", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            newHighScore(score)


def configureMenu(win):
    run = True
    while run:
        win.fill((0,0,0))
        width = win.get_width()
        height = win.get_height()

        pygame.draw.rect(win,(170, 170, 170),[width/1.60,height/1.26,140,40])

        pygame.font.init()
        #back
        font = pygame.font.SysFont('arial', 40)
        label = font.render('Back', 1, (0, 0, 1))
        win.blit(label, [width/1.5, height/1.27])

        #Size
        label = font.render('Game size: ', 1, (255, 255, 255))
        win.blit(label, [width-700, height-600])
        #Level
        label = font.render('Level: ', 1, (255, 255, 255))
        win.blit(label, [width-700, height-500])

        #Normal
        label = font.render('Mode: ', 1, (255, 255, 255))
        win.blit(label, [width-700, height-400])

        #Player
        label = font.render('Input: ', 1, (255, 255, 255))
        win.blit(label, [width-700, height-300])

        #Proto
        label = font.render('Prototype ', 1, (255, 255, 255))
        win.blit(label, [width-500, height-600])
        win.blit(label, [width-500, height-500])
        #Mode
        label = font.render('Normal', 1, (255, 255, 255))
        win.blit(label, [width-500, height-400])
        #Input
        label = font.render('Player', 1, (255, 255, 255))
        win.blit(label, [width-500, height-300])
        

        pygame.display.update()
        for event in pygame.event.get():
            #If quit then quit
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                pixel = win.get_at((x, y))
                if pixel == (170, 170, 170) or pixel == (0, 0, 1):
                    mainMenu(win)

        



#Main menu code will update code with fall stuff and ai later
def mainMenu(win):
    run = True
    while run:
        win.fill((0,0,0))
        width = win.get_width()
        height = win.get_height()

        textMain1(win, "Tetris: ", 50, (255, 255, 255))
        textMain2(win, "2805ICT : 2022", 40, (255, 0, 0))
        textMain3(win, "Group Members: ", 40, (255, 127, 0))
        textMain4(win, "James Sanders", 40, (255, 255, 0))
        textMain5(win, "Sam Snow Bollaan", 40, (0, 255, 0))
        textMain6(win, "Naveen Rodrigo", 40, (0, 255, 255))
        textMain7(win, "Tinotenda Mukondomi", 40, (128, 0, 128))

        pygame.draw.rect(win,(172, 170, 170),[width/1.5,height/1.27,140,40]) #quit
        pygame.draw.rect(win,(171, 170, 170),[width/2.60,height/1.27,180,40]) #configure
        pygame.draw.rect(win,(170, 170, 170),[width/6.8,height/1.27,140,40]) #play

        buttonPlay(win, "Play", 40, (0, 1, 0))
        buttonConfigure(win, "Configure", 36, (0, 0, 1))
        buttonQuit(win, "Quit", 40, (1, 0, 0)) 
        
        pygame.display.update()
        for event in pygame.event.get():
            #If quit then quit
            if event.type == pygame.QUIT:
                run = False
            #if any key then run main
            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                pixel = win.get_at((x, y))
                #play
                if pixel == (170, 170, 170) or pixel == (0, 1, 0):
                    main(win)
                #configure
                if pixel == (171, 170, 170) or pixel == (0, 0, 1):
                    configureMenu(win)
                #quit
                if pixel == (172, 170, 170) or pixel == (1, 0, 0):
                    pygame.quit()
        
    #Destroy current display
    pygame.display.quit()


#Declare window
win = pygame.display.set_mode((winWidth, winHeight))
#Give the window a name
pygame.display.set_caption('Tetris')
#Run main menu
mainMenu(win)

#-------------------------------------------------------------------------------------------------------------------------------------------------------