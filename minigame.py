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

#Returns a list of the 5 highest scores from the text file
def getHighScores():
    scores = open("HighScores.txt", 'r')
    highScores = []
    lines = scores.readlines()
    for line in lines:
        for section in line.split():
            if section.isdigit():
                highScores.append(int(section))
    return highScores

##Need to initiliaze these things using the text file in order to keep scores through multiple plays
highScores = getHighScores()
highScorePlayers = [' ', ' ', ' ', ' ', ' ']

#Rewrite the high scores text file, updating new scores/players
def rewriteHighScores(scores, players):
    file = open("HighScores.txt", 'w')
    for i in range(1, 6):
        file.write(str(i) + '. ' + str(players[i-1]) + " - " + str(scores[i-1]) + '\n')



#Given a current score, updates the list of high scores if the score belongs there
#Returns the index of the new score so we can add the new name, -1 otherwise
def updateHighScore(curScore, scores):
    for i in range(0, 5):
        if curScore > scores[i]:
            for j in range(4, i, -1):
                scores[j] = scores[j-1]
            scores[i] = curScore
            return i
    return -1


play = True

while play:
    #pygame.time.delay(100)

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
        nameInd = updateHighScore(score, highScores)
        if nameInd != -1:
            print('You got a high score! Please enter you name below:\n')
            playerName = input('Name: ')
            highScorePlayers[nameInd] = playerName
        rewriteHighScores(highScores, highScorePlayers)
        print(file1.read())

pygame.quit()