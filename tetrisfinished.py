
# - Implement a design tactic through highscores



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

#Attribute for extended mode 
global Extended
Extended = 0

global fallTime
fallTime = 0

global playerType
playerType = 0

#20
global gridHeight
gridHeight = 20





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
shapes = [S, Z, I, O, J, L, T]
exShapes = [S, Z, I, i, O, J, j, L, T]
#Shape colours has each index correspond with the shape you want that colour to be attributed too
exShpColours = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (0, 165, 165), (255, 255, 0), (255, 165, 0), (255, 100, 5), (0, 0, 255), (128, 0, 128)]
shpColours = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Define class and game functions

#Define class piece which attriputes the pieces game attributes to keep track
class Piece(object):
    global Extended
    def __init__(self, x, y, shape):
        if Extended == 0:
            self.x = x
            self.y = y
            self.shape = shape
            self.color = shpColours[shapes.index(shape)]
            self.rotation = 0
        else:
            self.x = x
            self.y = y
            self.shape = shape
            self.color = exShpColours[exShapes.index(shape)]
            self.rotation = 0



#Create grid is used to format the game to work on a grid
def gridGeneration(usedPos={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(gridHeight)]

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
    clearSpaces = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(gridHeight)]
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
    global Extended
    if Extended == 1:
        return Piece(5, 0, random.choice(exShapes))
    else:
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

def buttonScores(surface, text, size, color):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (tpLftX + plyAreaWidth /2 - (label.get_width()/2), tpLftY + plyAreaHeight/1.25 - label.get_height()/0.45))        


#visual grid creates a grid for the player to see while playing the game
def visualGrid(surface, grid):
    sx = tpLftX
    sy = tpLftY

    divisableBoard = 20/gridHeight 

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*blockSize), (sx+plyAreaWidth, sy+ i*blockSize))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*blockSize, sy),(sx + j*blockSize, sy + plyAreaHeight/divisableBoard))


#This function is for when a player get's a tetris 
def playerTetris(grid, locked, volume):
    pygame.mixer.init()
    tetrisSound = pygame.mixer.Sound("tetris.mp3")
    tetrisSound.set_volume(volume)
    detect = 0
    #it detectss each row in the grid and if any row doesn't have a blank square you add it to detect
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            pygame.mixer.Sound.play(tetrisSound)
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
def newHighScore(nscore, win):
    scores = []
    for x in range(0, 10):
        with open("scores.txt", 'r') as value:
            lines = value.readlines()
            scores.append(lines[x].strip())


    if nscore > int(scores[9]):
        topscore = -1
        for x in range(9):
            if nscore > int(scores[(x)]):
                topscore = x
        temp = scores[topscore]
        scores[9-topscore] = nscore
        nameScore = topscore
        input = False
        name = ""
        while input == False:
            win.fill((0, 0, 0))
            width = win.get_width()
            height = win.get_height()
            pygame.font.init()
            font = pygame.font.SysFont('arial', 40)
            textMiddle(win, "Name: ", 80, (255,255,255))
            pygame.draw.rect(win,(255, 255, 255),[width-265,height-315,180,50]) #extended
            label = font.render(name, 1, (0, 0, 0))
            win.blit(label, [width-235, height-315])

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()

                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_q:
                        if len(name) < 3:
                            name += "Q"
                    elif event.key == pygame.K_w:
                        if len(name) < 3:
                            name += "W"
                    elif event.key == pygame.K_e:
                        if len(name) < 3:
                            name += "E"
                    elif event.key == pygame.K_r:
                        if len(name) < 3:
                            name += "R"
                    elif event.key == pygame.K_t:
                        if len(name) < 3:
                            name += "T"
                    elif event.key == pygame.K_y:
                        if len(name) < 3:
                            name += "Y"
                    elif event.key == pygame.K_u:
                        if len(name) < 3:
                            name += "U"
                    elif event.key == pygame.K_i:
                        if len(name) < 3:
                            name += "I"
                    elif event.key == pygame.K_o:
                        if len(name) < 3:
                            name += "O"
                    elif event.key == pygame.K_p:
                        if len(name) < 3:
                            name += "P"
                    elif event.key == pygame.K_a:
                        if len(name) < 3:
                            name += "A"
                    elif event.key == pygame.K_s:
                        if len(name) < 3:
                            name += "S"
                    elif event.key == pygame.K_d:
                        if len(name) < 3:
                            name += "D"
                    elif event.key == pygame.K_f:
                        if len(name) < 3:
                            name += "F"
                    elif event.key == pygame.K_g:
                        if len(name) < 3:
                            name += "G"
                    elif event.key == pygame.K_h:
                        if len(name) < 3:
                            name += "H"
                    elif event.key == pygame.K_j:
                        if len(name) < 3:
                            name += "J"
                    elif event.key == pygame.K_k:
                        if len(name) < 3:
                            name += "K"
                    elif event.key == pygame.K_l:
                        if len(name) < 3:
                            name += "L"
                    elif event.key == pygame.K_z:
                        if len(name) < 3:
                            name += "Z"
                    elif event.key == pygame.K_x:
                        if len(name) < 3:
                            name += "X"
                    elif event.key == pygame.K_c:
                        if len(name) < 3:
                            name += "C"
                    elif event.key == pygame.K_v:
                        if len(name) < 3:
                            name += "V"
                    elif event.key == pygame.K_b:
                        if len(name) < 3:
                            name += "B"
                    elif event.key == pygame.K_n:
                        if len(name) < 3:
                            name += "N"
                    elif event.key == pygame.K_m:
                        if len(name) < 3:
                            name += "M"
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_RETURN:
                        if len(name) == 3:
                            print("INSIDE")
                            userNames = []
                            for x in range(0, 10):
                                with open("names.txt", 'r') as value:
                                    lines = value.readlines()
                                    userNames.append(lines[x].strip())
                            
                            nameTemp = userNames[9-nameScore]
                            userNames[9-nameScore] = name
                            nameScore -= 1
                            while nameScore != 0:
                                userNames[nameScore] = nameTemp
                                nameScore -= 1
                                nameTemp = userNames[nameScore]

                            with open('names.txt', 'w') as f:
                                for x in userNames:
                                    f.write(str(x) + '\n')
                            input = True






        topscore -= 1
        while topscore != 0:
            scores[topscore] = temp
            topscore -= 1
            temp = scores[topscore]
    with open('scores.txt', 'w') as f:
        for x in scores:
            f.write(str(x) + '\n')


#Highscore fetches the highscore frim the scores.txt text file
def highScore():
    with open('scores.txt', 'r') as value:
        lines = value.readlines()
        score = lines[0].strip()

    return score

#playable window is the function which sets all the elements for the visable game
def playableWindow(surface, grid, score=0, bestScore = 0, numLines = 0):
    #this sets the background fill
    global playerType
    global gridHeight
    divisableHeight = 20/gridHeight
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

    if playerType == 1:
        displayType = "AI"
    else:
        displayType = "Player"

    #Display Player
    label = font.render('Type = ' + displayType, 1, (255, 255, 255))
    surface.blit(label, (sx+20, sy-50))


    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (tpLftX + j*blockSize, tpLftY + i*blockSize, blockSize, blockSize), 0)

    pygame.draw.rect(surface, (255, 0, 0), (tpLftX, tpLftY, plyAreaWidth, plyAreaHeight/divisableHeight), 5)

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
    global fallTime
    #Fall speed is the incrementing speed that the game will increase over time
    fallSpeed = 0.27
    #Level time is the time occured ingame so far
    lvlTime = 0
    #The score variable
    score = 100
    selfComplete = False

    numLines=0

    #Set up music to play
    musicPlaying = 1
    volume = 0.2
    pygame.mixer.init()
    pygame.mixer.music.load("gameTheme.mp3")
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)
    placeSound = pygame.mixer.Sound("placeBlock.mp3")

    width = win.get_width()
    height = win.get_height()

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
                pygame.mixer.Sound.play(placeSound)
                changePiece = True


        if playerType == 1:
            if (random.randint(0, 8)) == 0:
                move = random.randint(0, 3)
                if move == 0:
                    currentPiece.x -= 1
                    if not(validSquare(currentPiece, grid)):
                        currentPiece.x += 1
                elif move == 1:
                    currentPiece.x += 1
                    if not(validSquare(currentPiece, grid)):
                        currentPiece.x -= 1
                elif move == 2:
                    currentPiece.y += 1
                    if not(validSquare(currentPiece, grid)):
                        currentPiece.y -= 1
                elif move == 3:
                    currentPiece.rotation += 1
                    if not(validSquare(currentPiece, grid)):
                        currentPiece.rotation -= 1
                else:
                    pass


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
                if playerType == 0:
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

                if event.key == pygame.K_m:
                    if musicPlaying == 1:
                        musicPlaying = 0
                        volume = 0
                        pygame.mixer.music.pause()
                        placeSound.set_volume(volume)
                    else:
                        volume = 0.2
                        pygame.mixer.music.unpause()
                        placeSound.set_volume(volume)

                elif event.key == pygame.K_ESCAPE:
                    end = True
                    while end:
                        textMiddle(win, "End Game?", 80, (255,255,255))
                        pygame.draw.rect(win,(172, 170, 170),[width/1.5,height/1.27,140,40]) #No
                        pygame.draw.rect(win,(170, 170, 170),[width/6.8,height/1.27,140,40]) #Yes
                        buttonPlay(win, "Yes", 40, (0, 1, 0))
                        buttonQuit(win, "No", 40, (1, 0, 0))

                        
                        pygame.display.update()

                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    end = False

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                (x, y) = pygame.mouse.get_pos()
                                pixel = win.get_at((x, y))
                                if pixel == (170, 170, 170) or pixel == (0, 1, 0):
                                    selfComplete = True
                                    end = False
                                if pixel == (172, 170, 170) or pixel == (1, 0, 0):
                                    end = False


                elif event.key == pygame.K_p:
                    pause = True
                    while pause:
                        textMiddle(win, "Pause", 80, (255,255,255))
                        
                        pygame.display.update()

                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                    pause = False 

                
                        


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
            score += playerTetris(grid, usedPositions, volume) * 10
            numLines = score/10

        #Remake playable Window
        playableWindow(win, grid, score, bestScore, numLines)
        #Redisplay the next shape area
        nextShapeArea(nextPiece, win)
        #Update pygame display
        pygame.display.update()

        #Game over check
        if gameOver(usedPositions) or selfComplete == True:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("gameOver.mp3")
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(1)
            textMiddle(win, "YOU LOST!", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            newHighScore(score, win)


def configureMenu(win):
    run = True
    global playerType
    global Extended
    global fallTime
    global gridHeight

    if Extended == 0:
        modeDisplay = "Normal"
        modeFont = pygame.font.SysFont('arial', 40)
    else:
        modeDisplay = "Extended"
        modeFont = pygame.font.SysFont('arial', 32)

    if playerType == 0:
        modePlayer = "Player"
    else:
        modePlayer = "AI"


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

        #Grid Number
        label = font.render(str(gridHeight), 1, (255, 255, 255))
        win.blit(label, [width-425, height-600])
        #Grid Height
        label = font.render('Board Height: ', 1, (255, 255, 255))
        win.blit(label, [width-700, height-600])
        pygame.draw.rect(win,(170, 173, 170),[width-360,height-595,40,40]) #Up arrow
        label = font.render(('▲ '), 1, (0, 3, 0))
        win.blit(label, [width-354, height-600])
        pygame.draw.rect(win,(170, 174, 170),[width-485,height-595,40,40]) #Down arrow
        label = font.render('▼'  , 1, (0, 4, 0))
        win.blit(label, [width-478, height-600])

        #Level
        label = font.render('Level: ', 1, (255, 255, 255))
        win.blit(label, [width-700, height-500])

        #Normal
        label = font.render('Mode: ', 1, (255, 255, 255))
        win.blit(label, [width-700, height-400])

        #Player
        label = font.render('Input: ', 1, (255, 255, 255))
        win.blit(label, [width-700, height-300])

        #Level
        label = font.render(('Level: ' + str(fallTime)), 1, (255, 255, 255))
        win.blit(label, [width-500, height-500])
        pygame.draw.rect(win,(170, 171, 170),[width-550,height-497,40,40]) #Down arrow
        pygame.draw.rect(win,(170, 172, 170),[width-360,height-497,40,40]) #Up arrow
        label = font.render(('▲ '), 1, (0, 2, 0))
        win.blit(label, [width-354, height-500])
        label = font.render('▼'  , 1, (0, 1, 0))
        win.blit(label, [width-544, height-500])
        

        #Mode
        pygame.draw.rect(win,(173, 170, 170),[width-518,height-397,140,40]) #extended
        label = modeFont.render(modeDisplay, 1, (0, 0, 0))
        win.blit(label, [width-500, height-400])

        #Input
        pygame.draw.rect(win,(172, 170, 170),[width-523,height-296,140,40]) #player
        label = font.render(modePlayer, 1, (0, 0, 0))
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
                elif pixel == (173, 170, 170):
                    if Extended == 0:
                        Extended = 1
                    else:
                        Extended = 0
                elif pixel == (172, 170, 170):
                    if playerType == 1:
                        playerType = 0
                    else:
                        playerType = 1
                elif pixel == (170, 171, 170) or pixel == (0, 1, 0):
                    if fallTime > 0:
                        fallTime -= 1
                elif pixel == (170, 172, 170) or pixel == (0, 2, 0):
                    if fallTime < 100:
                        fallTime += 1
                elif pixel == (170, 173, 170) or pixel == (0, 3, 0):
                    if gridHeight < 20:
                        gridHeight += 1
                elif pixel == (170, 174, 170) or pixel == (0, 4, 0):
                    if gridHeight > 0:
                        gridHeight -= 1
                configureMenu(win)


        
def score(win):
    run = True

    

    while run:
        win.fill((0, 0, 0))
        width = win.get_width()
        height = win.get_height()
        pygame.font.init()
        font = pygame.font.SysFont('arial', 40)

        pygame.draw.rect(win,(170, 170, 170),[width/1.60,height/1.26,140,40])
        font = pygame.font.SysFont('arial', 40)
        label = font.render('Back', 1, (0, 0, 1))
        win.blit(label, [width/1.5, height/1.27])

        spacing = 600

        for x in range(9):
            with open('names.txt', 'r') as value:
                lines = value.readlines()
                name = lines[x].strip()
            label = font.render(name + ":", 1, (255, 255, 255))
            win.blit(label, [width-700, height-spacing])
            spacing -= 50

        spacing = 600

        for x in range(9):
            with open('scores.txt', 'r') as value:
                lines = value.readlines()
                score = lines[x].strip()
            label = font.render((str(score)), 1, (255, 255, 255))
            win.blit(label, [width-600, height-spacing])
            spacing -= 50



        pygame.display.update()
        for event in pygame.event.get():
            #If quit then quit
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                pixel = win.get_at((x, y))
                if pixel == (170, 170, 170) or pixel == (0, 0, 1):
                    mainMenu(win)
    pygame.display.quit()

        




#Main menu code will update code with fall stuff and ai later
def mainMenu(win):
    pygame.mixer.init()
    pygame.mixer.music.load("mainTheme.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
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
        pygame.draw.rect(win,(173, 170, 170),[width/2.46,height/1.5,140,40]) #Scores

        buttonPlay(win, "Play", 40, (0, 1, 0))
        buttonConfigure(win, "Configure", 36, (0, 0, 1))
        buttonQuit(win, "Quit", 40, (1, 0, 0)) 
        buttonScores(win, "Scores", 40, (0, 1, 1))
        
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
                    pygame.mixer.music.stop()
                #configure
                if pixel == (171, 170, 170) or pixel == (0, 0, 1):
                    configureMenu(win)
                #scores
                if pixel == (173, 170, 170) or pixel == (0, 1, 1):
                    score(win)
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
#------------------------------------------------------------------------------------------------------------------------------------------