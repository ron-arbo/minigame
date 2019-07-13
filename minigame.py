import pygame
import time
import random
pygame.init()

window_length = 500
window_width = 500
window = pygame.display.set_mode((window_width, window_length))

pygame.display.set_caption("QuickTravel Minigame")

width = 50
height = 50
x_pos = 230
y_pos = 420
move = 10
obstacle_y = -1
openingSize = 150
score = -1

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

play = True
while play:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
    
    
    #Key controls
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        x_pos -= move
    if key[pygame.K_RIGHT]:
        x_pos += move
    
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
    obstacle_y += 8
    obstacleLeft = pygame.draw.rect(window, (150, 0 ,0), (left_pos, obstacle_y, obstacle_length, 10))
    obstacleRight = pygame.draw.rect(window, (150, 0 ,0), (right_pos, obstacle_y, obstacle_length, 10))
   
    pygame.display.update()

    #If block collides with obstacle, end game, display score
    if pygame.Rect.colliderect(block, obstacleLeft) == True or pygame.Rect.colliderect(block, obstacleRight) == True:
        play = False
        print("Score: " + str(score))
        file1 = open("HighScores.txt","r")
        
        print("High Scores:")
        nameInd = updateHS(score, highScores)
        if nameInd != -1:
            print('You got a high score! Please enter you name below:\n')
            playerName = input('Name: ')
            updateHSPlayers(nameInd, highScorePlayers, playerName)
        rewriteHighScores(highScores, highScorePlayers)
        print(file1.read())

pygame.quit()