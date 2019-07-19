import pygame
import time
import random

pygame.init()

pygame.display.set_caption("QuickTravel")

#Initalizing board and block variables
window_length = 500
window_width = 500
window = pygame.display.set_mode((window_width, window_length))

#Initalizing button colors
GREEN = (0, 200, 0)
LIGHT_GREEN = (0, 255 ,0)
RED = (200, 0, 0)
LIGHT_RED = (255, 0, 0)
YELLOW = (200, 200, 0)
LIGHT_YELLOW = (255, 255, 0)
GRAY = (192, 192, 192)
WHITE = (255, 255, 255)

#Button class
class button():
    #Constructor
    def __init__(self, color, light_color, x_pos, y_pos, width, height, txt):
        self.color = color
        self.light_color = light_color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.txt = txt
    
    #Called to see if the mouse is currently hovering over the button
    def hovering(self):
        mouse = pygame.mouse.get_pos()
        #If mouse is on button...
        if self.x_pos + self.width > mouse[0] > self.x_pos and self.y_pos + self.height > mouse[1] > self.y_pos:
            return True
        else:
            return False

    #Draws the button on the screen, draws in a different shade if the mouse is hovering on it to simulate interactiveness
    def draw(self, window):
        if self.hovering():
            pygame.draw.rect(window, self.light_color, (self.x_pos, self.y_pos, self.width, self.height))
        else:
            pygame.draw.rect(window, self.color, (self.x_pos, self.y_pos, self.width, self.height))

        #Drawing text over rectangle
        font = pygame.font.SysFont('arial', 25)
        txt = font.render(self.txt, 1, (0, 0, 0))

        #Define center so we know where to put text
        x_center = self.x_pos + ((self.width/2) - (txt.get_width()/2))
        y_center = self.y_pos + ((self.height/2) - (txt.get_height()/2))

        #Write text onto window
        window.blit(txt, (x_center, y_center))


#Returns a list of the top 5 from the high scores text file. Enter parameter 'p' for the players, 's' for the scores
def getTop5(choice):
    scores = open("HighScores.txt", 'r')
    tempScores = []
    tempPlayers = []
    lines = scores.readlines()
    for line in lines:
        sections = line.split()
        tempPlayers.append(sections[1])
        tempScores.append(sections[3])       
    scores.close()
    if choice == 'p':
        return tempPlayers
    else:
        return tempScores

#Initialize scores and players by retreiving info from text file using above methods
highScores = getTop5('s')
highScorePlayers = getTop5('p')

#Rewrite the high scores text file, updating new scores/players
def rewriteHighScores(scoreList, playerList):
    file = open("HighScores.txt", 'w')
    for i in range(1, 6):
        file.write(str(i) + '. ' + str(playerList[i-1]) + " - " + str(scoreList[i-1]) + '\n')


#Given a current score, updates the list of high scores if the score belongs there
#Returns the index of the new score so we can add the new name, -1 otherwise
def updateHS(curScore, scores):
    for i in range(0, 5):
        if curScore > int(scores[i]):
            for j in range(4, i, -1):
                scores[j] = scores[j-1]
            scores[i] = curScore
            return i
    return -1

#Shifts entries back to update players on high scoreboard
def updateHSPlayers(playerIndex, playersList, playerName):
    for i in range(4, playerIndex, -1):
        playersList[i] = playersList[i-1]
    playersList[playerIndex] = playerName

def game_intro():
    easyButton = button(GREEN, LIGHT_GREEN, 200, 100, 100, 50, 'Easy')
    medButton = button(YELLOW, LIGHT_YELLOW, 200, 200, 100, 50, 'Medium')
    hardButton = button(RED, LIGHT_RED, 200, 300, 100, 50, 'Hard')
    customButton = button(GRAY, WHITE, 200, 400, 100, 50, 'Custom')

    keepGoing = True

    while keepGoing:
        window.fill((0, 0, 0))

        #Drawing Title
        title_font = pygame.font.SysFont('TT Supermolot Neue', 70)
        title = title_font.render('QuickTravel', 1, (0, 255, 0))
        window.blit(title, (115, 25))
       
        #Drawing Buttons
        easyButton.draw(window)
        medButton.draw(window)
        hardButton.draw(window)
        customButton.draw(window)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                pygame.quit()
                quit()
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            if easyButton.hovering():
                return 'Easy'
            if medButton.hovering():
                return 'Medium'
            if hardButton.hovering():
                return 'Hard'
            if customButton.hovering():
                return 'Custom'


def playGame(difficulty):
    #Height and width of player block
    width = 50
    height = 50

    #Initial position of player block
    x_pos = 230
    y_pos = 420

    #Initalize obstacle position and player score
    obstacle_y = -1
    score = -1

    #Initialize movement speed and opening sizes depending on selected difficulty
    if difficulty == 'Easy':
        obstacle_speed = 9
        openingSize = 150
        move = 10
    elif difficulty == 'Medium':
        obstacle_speed = 12
        openingSize = 140
        move = 12
    elif difficulty == 'Hard':
        obstacle_speed = 15
        openingSize = 130
        move = 15
    else:
        #Difficulty is custom, look for user input
        obstacle_speed = int(input('Please enter the desired speed of your block below: \n'))
        openingSize = int(input('Please enter the desired size of openings below: \n'))
        move = int(input('Please enter your desired lateral move speed below: \n'))

    play = True
    while play:
        #Provides option to quit using red X in corner
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
    
        #Key controls
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            x_pos -= move
        if key[pygame.K_RIGHT]:
            x_pos += move
    
        #Resets and redraws screen each moment to simulate movement
        window.fill(0)
        block = pygame.draw.rect(window, (0, 255, 0), (x_pos, y_pos, width, height))

        #Draw obstacles and change y value so they drop on the screen
        #Once obstacle is off screen, we reset it and change the x values of the obstacle (Top left corner is what its based on)
        if obstacle_y < 0 or obstacle_y > window_length:
            obstacle_y = 0
            obstacle_length = window_width-openingSize
            left_pos = random.randint(-obstacle_length, 0)
            right_pos = left_pos + obstacle_length + openingSize
            score += 1
    
        #Move obstacle down the screen, continously drawing them lower
        obstacle_y += obstacle_speed
        obstacleLeft = pygame.draw.rect(window, (150, 0 ,0), (left_pos, obstacle_y, obstacle_length, 10))
        obstacleRight = pygame.draw.rect(window, (150, 0 ,0), (right_pos, obstacle_y, obstacle_length, 10))
   
        #Update display
        pygame.display.update()

        #If block collides with obstacle, end game, display score
        if pygame.Rect.colliderect(block, obstacleLeft) == True or pygame.Rect.colliderect(block, obstacleRight) == True:
            play = False
       
            #Print high scores, updates board if there is a new one
            print("Score: " + str(score))
            file1 = open("HighScores.txt","r")
            print("High Scores:")
            nameInd = updateHS(score, highScores)
            #If user got high score, have them enter their name and the board will update
            if nameInd != -1:
                print('You got a high score! Please enter you name below:\n')
                playerName = input('Name: ')
                updateHSPlayers(nameInd, highScorePlayers, playerName)
            rewriteHighScores(highScores, highScorePlayers)
            print('Updated Leaderboard:\n')
            print(file1.read())

#game_intro() will allow user to select difficulty, then return that to playGame and start
Difficulty = game_intro()
playGame(Difficulty)

pygame.quit()