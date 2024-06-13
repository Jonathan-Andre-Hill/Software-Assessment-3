import pygame
from sys import exit
import math
import random
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2) # fixes an issue with trying to get display resolution

pygame.init()

# Create window
screen = pygame.display.set_mode((pygame.display.get_desktop_sizes()[0]))
pygame.display.set_caption('Menu')
clock = pygame.time.Clock()
font = pygame.font.Font(None,50)
pygame.display.toggle_fullscreen()
clock.tick(60) # tickspeed/fpsvc

# Define Variables
screenResolution = str(pygame.display.get_desktop_sizes()[0])
screenWidth = int(screenResolution.strip('()').split(",")[0])
screenHeight = int(screenResolution.strip('()').split(",")[1])
screenMiddle = (screenWidth/2,screenHeight/2)

# PLAY TESTING VARIABLES
screenCenterX = (screenWidth/2)
screenCenterY = (screenHeight/2)
screenCenter = (screenCenterX,screenCenterY)
borderSize = 1000
gameActive = False
xMovement = 0
yMovement = 0
playerSpeed = 3
playerWidth = 0.05
playerHeight = 0.1

slimeSpeed = 1.5
slimeWidth = 0.05
slimeHeight = 0.1

floorWidth = 0.6
floorHeight = 0.8


# Adjustable Variables

# Menu Background Colours
mainMenuBackgroundColour = ('pink')
helpMenuBackgroundColour = ('green')
optionsMenuBackgroundColour = ('blue')

# Main Menu Buttons
mainMenuButtonsSizeX = 0.3
mainMenuButtonsSizeY = 0.1
mainMenuButtonsPosX = 0.5
mainMenuButtonsPosY = 0.675
mainMenuButtonsYSpacing = 0.15
mainMenuButtonsColour = ('blue')
mainMenuButtonsHoverColour = ('yellow')
mainMenuButtonsTextColour = ('white')
mainMenuButtonsFont = (pygame.font.get_default_font())
mainMenuButtonsFontSize = (30)

# Return To Main Menu Button
returnToMenuButtonSizeX = 0.1
returnToMenuButtonSizeY = 0.1
returnToMainMenuButtonPosX = 0.1
returnToMainMenuButtonPosY = 0.1
returnToMainMenuButtonColour = ('red')
returnToMainMenuButtonsHoverColour = ('yellow')
returnToMainMenuButtonsTextColour = ('white')
returnToMainMenuButtonFont = (pygame.font.get_default_font())
returnTMainMenuButtonFontSize = (15)


# Define Surfaces & Rectangles

# PLAY TESTING SURFACES & RECTANGLES
floorUscaledSurf = pygame.image.load('graphics/floor.png').convert_alpha()
floorSurf = pygame.transform.scale(floorUscaledSurf, (floorWidth*screenWidth, floorHeight*screenHeight))
floorRect = floorSurf.get_rect(center=(screenCenter))

leftSurf = pygame.Surface((borderSize,floorRect.height + borderSize*2))
leftRect = leftSurf.get_rect(center = ((screenWidth/2) - (floorRect.width/2) - (leftSurf.get_width()/2),(screenHeight/2)))
topSurf = pygame.Surface((floorRect.width + borderSize*2,borderSize))
topRect = topSurf.get_rect(center = ((screenWidth/2),(screenHeight/2) - (floorRect.height/2) - (topSurf.get_height()/2)))
rightSurf = pygame.Surface((borderSize,floorRect.height + borderSize*2))
rightRect = rightSurf.get_rect(center = ((screenWidth/2) + (floorRect.width/2) + (rightSurf.get_width()/2),(screenHeight/2)))
bottomSurf = pygame.Surface((floorRect.width + borderSize*2,borderSize))
bottomRect = bottomSurf.get_rect(center = ((screenWidth/2),(screenHeight/2) + (floorRect.height/2) + (bottomSurf.get_height()/2)))


gameEndText = font.render('Press Any Key To Start',True,'black')
gameEndRect = gameEndText.get_rect(center = (screenCenter))


# Classes

class Button:
    def __init__(self, width, height, centerX, centerY, colour, hoverColour, text, fontType, fontSize, textColour):
        self.width = width*screenWidth
        self.height = height*screenHeight
        self.centerX = centerX*screenWidth
        self.centerY = centerY*screenHeight
        self.colour = colour
        self.hoverColour = hoverColour
        self.text = text
        self.font = pygame.font.Font(fontType, math.ceil((fontSize*screenWidth)/1000))
        self.textColour = textColour
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(self.colour)
        self.rect = self.surf.get_rect(center = (self.centerX, self.centerY))
        self.textSurf = self.font.render(self.text, True, self.textColour)
        self.textRect = self.textSurf.get_rect(center = (self.centerX, self.centerY))
    
    def checkHover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surf.fill(self.hoverColour)
            return(True)
        else:
            self.surf.fill(self.colour)
            return(False)
    
    def blit(self):
        screen.blit(self.surf, self.rect)
        screen.blit(self.textSurf, (self.textRect))

class Player:
    def __init__(self, width, height, playerSpeed, xMovement, yMovement):
        self.xMovement = xMovement
        self.yMovement = yMovement
        self.width = width*screenWidth
        self.height = height*screenHeight
        self.speed = (playerSpeed*screenWidth/1000)
        self.unscaledSurf = pygame.image.load('graphics/player.png').convert_alpha()
        self.surf = pygame.transform.scale(self.unscaledSurf, (self.width,self.height))
        self.startPos = (screenCenterX, screenCenterY)
        self.rect = self.surf.get_rect(center = self.startPos)
    
    def playerMovement(self):
            if self.rect.top >= floorRect.bottom and self.yMovement < 0:
                self.yMovement = 0
                floorRect.y += floorRect.height + self.rect.height
                leftRect.y += floorRect.height + self.rect.height
                topRect.y += floorRect.height + self.rect.height
                rightRect.y += floorRect.height + self.rect.height
                bottomRect.y += floorRect.height + self.rect.height
                slime.rect.y += floorRect.height + self.rect.height
            if self.rect.bottom <= floorRect.top and self.yMovement > 0:
                self.yMovement = 0
                floorRect.y -= floorRect.height + self.rect.height
                leftRect.y -= floorRect.height + self.rect.height
                topRect.y -= floorRect.height + self.rect.height
                rightRect.y -= floorRect.height + self.rect.height
                bottomRect.y -= floorRect.height + self.rect.height
                slime.rect.y -= floorRect.height + self.rect.height
            if self.rect.right <= floorRect.left and self.xMovement > 0:
                self.xMovement = 0
                floorRect.x -= floorRect.width + self.rect.width
                leftRect.x -= floorRect.width + self.rect.width
                topRect.x -= floorRect.width + self.rect.width
                rightRect.x -= floorRect.width + self.rect.width
                bottomRect.x -= floorRect.width + self.rect.width
                slime.rect.x -= floorRect.width + self.rect.width
            if self.rect.left >= floorRect.right and self.xMovement < 0:
                self.xMovement = 0
                floorRect.x += floorRect.width + self.rect.width
                leftRect.x += floorRect.width + self.rect.width
                topRect.x += floorRect.width + self.rect.width
                rightRect.x += floorRect.width + self.rect.width
                bottomRect.x += floorRect.width + self.rect.width
                slime.rect.x += floorRect.width + self.rect.width


            floorRect.y += self.yMovement
            floorRect.x += self.xMovement
            leftRect.y += self.yMovement
            leftRect.x += self.xMovement
            topRect.y += self.yMovement
            topRect.x += self.xMovement
            rightRect.y += self.yMovement
            rightRect.x += self.xMovement
            bottomRect.y += self.yMovement
            bottomRect.x += self.xMovement
            slime.rect.y += self.yMovement
            slime.rect.x += self.xMovement

            self.yMovement = 0
            self.xMovement = 0

class Slime:
    def __init__(self, width, height, slimeSpeed):
        self.width = width*screenWidth
        self.height = height*screenHeight
        self.speed = (slimeSpeed*screenWidth/1000)
        self.centerX = random.uniform(leftRect.right,rightRect.left)
        self.centerY = random.uniform(topRect.bottom,bottomRect.top)
        self.startPos = (self.centerX, self.centerY)
        self.unscaledSurf = pygame.image.load('graphics/slime.png').convert_alpha()
        self.surf = pygame.transform.scale(self.unscaledSurf, (self.width,self.height))
        self.rect = self.surf.get_rect(center = self.startPos)
                                                               
    def generateSpawnPoint(self):
        self.centerX = random.uniform(leftRect.right,rightRect.left)
        self.centerY = random.uniform(topRect.bottom,bottomRect.top)
        self.startPos = (self.centerX, self.centerY)
        self.rect = self.surf.get_rect(center = self.startPos)

    def slimeMovement(self):
            if player.rect.y < self.rect.y and (((player.rect.top) - (floorRect.top)) + ((floorRect.bottom) - (self.rect.top))) > ((self.rect.top) - (player.rect.bottom)):
                self.rect.y -= self.speed
            elif player.rect.y < self.rect.y:
                self.rect.y += self.speed
            if player.rect.y > self.rect.y and (((floorRect.bottom) - (player.rect.bottom)) + ((self.rect.bottom) - (floorRect.top))) > ((player.rect.top) - (self.rect.bottom)):
                self.rect.y += self.speed
            elif player.rect.y > self.rect.y:
                self.rect.y -= self.speed
            if player.rect.x < self.rect.x and (((player.rect.left) - (floorRect.left)) + ((floorRect.right) - (self.rect.left))) > ((self.rect.left) - (player.rect.right)):
                self.rect.x -= self.speed
            elif player.rect.x < self.rect.x:
                self.rect.x += self.speed
            if player.rect.x > self.rect.x and (((floorRect.right) - (player.rect.right)) + ((self.rect.right) - (floorRect.left))) > ((player.rect.left) - (self.rect.right)):
                self.rect.x += self.speed
            elif player.rect.x > self.rect.x:
                self.rect.x -= self.speed

            if self.rect.top >= floorRect.bottom:
                self.rect.y -= self.rect.height + floorRect.height
            if self.rect.bottom <= floorRect.top:
                self.rect.y += self.rect.height + floorRect.height
            if self.rect.right <= floorRect.left:
                self.rect.x += self.rect.width + floorRect.width
            if self.rect.left >= floorRect.right:
                self.rect.x -= self.rect.width + floorRect.width

    def checkCollision(self):
            if player.rect.colliderect(self.rect):
                return ("collision")


# Objects
playButton = Button(mainMenuButtonsSizeX, mainMenuButtonsSizeY, mainMenuButtonsPosX, mainMenuButtonsPosY - (1.5*mainMenuButtonsYSpacing), mainMenuButtonsColour, mainMenuButtonsHoverColour, "Play", mainMenuButtonsFont, mainMenuButtonsFontSize, mainMenuButtonsTextColour)
helpMenuButton = Button(mainMenuButtonsSizeX, mainMenuButtonsSizeY, mainMenuButtonsPosX, mainMenuButtonsPosY - (0.5*mainMenuButtonsYSpacing), mainMenuButtonsColour, mainMenuButtonsHoverColour, "Help", mainMenuButtonsFont, mainMenuButtonsFontSize, mainMenuButtonsTextColour)
optionsMenuButton = Button(mainMenuButtonsSizeX, mainMenuButtonsSizeY, mainMenuButtonsPosX, mainMenuButtonsPosY + (0.5*mainMenuButtonsYSpacing), mainMenuButtonsColour, mainMenuButtonsHoverColour, "Options", mainMenuButtonsFont, mainMenuButtonsFontSize, mainMenuButtonsTextColour)
mainMenuButton = Button(returnToMenuButtonSizeX, returnToMenuButtonSizeY, returnToMainMenuButtonPosX, returnToMainMenuButtonPosY, returnToMainMenuButtonColour, returnToMainMenuButtonsHoverColour, "Main Menu", returnToMainMenuButtonFont, returnTMainMenuButtonFontSize, returnToMainMenuButtonsTextColour)
quitButton = Button(mainMenuButtonsSizeX, mainMenuButtonsSizeY, mainMenuButtonsPosX, mainMenuButtonsPosY + (1.5*mainMenuButtonsYSpacing), mainMenuButtonsColour, mainMenuButtonsHoverColour, "Quit", mainMenuButtonsFont, mainMenuButtonsFontSize, mainMenuButtonsTextColour)

# Play Testing Objects
player = Player(playerWidth, playerHeight, playerSpeed, xMovement, yMovement)
slime = Slime(slimeWidth, slimeHeight, slimeSpeed)
slime2 = Slime(slimeWidth, slimeHeight, slimeSpeed)

# Sprite Groups


# Functions
def MainMenu():
    while True:
        for event in pygame.event.get():
            # event Loop
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Impuls Inputs
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_h:
                    HelpMenu()
                if event.key == pygame.K_o:
                    OptionsMenu()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.checkHover() == True:
                    Play()
                if helpMenuButton.checkHover() == True:
                    HelpMenu()
                if optionsMenuButton.checkHover() == True:
                    OptionsMenu()
                if quitButton.checkHover() == True:
                    pygame.quit()
                    exit()
                        

        # Constant Inputs
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_w]:


        # Draw Screen
        screen.fill(mainMenuBackgroundColour)
        playButton.checkHover()
        playButton.blit()
        helpMenuButton.checkHover()
        helpMenuButton.blit()
        optionsMenuButton.checkHover()
        optionsMenuButton.blit()
        quitButton.checkHover()
        quitButton.blit()
        pygame.display.update() # updates the display

def HelpMenu():
    while True:
        for event in pygame.event.get():
            # event Loop
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Impuls Inputs
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mainMenuButton.checkHover() == True:
                    MainMenu()
                        
        # Constant Inputs
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_w]:


        # Draw Screen
        screen.fill(helpMenuBackgroundColour)
        mainMenuButton.checkHover()
        mainMenuButton.blit()
        pygame.display.update() # updates the display

def OptionsMenu():
    while True:
        for event in pygame.event.get():
            # event Loop
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Impuls Inputs
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mainMenuButton.checkHover() == True:
                    MainMenu()
                        
        # Constant Inputs
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_w]:


        # Draw Screen
        screen.fill(optionsMenuBackgroundColour)
        mainMenuButton.checkHover()
        mainMenuButton.blit()
        pygame.display.update() # updates the display

def Play():
    global screenCenter
    global borderSize
    global gameActive
    global xMovement
    global yMovement
    while True:
        for event in pygame.event.get():
            # event Loop
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Impuls Inputs
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MainMenu()

            if gameActive == False:
                slime.rect.center = slime.startPos
                slime.generateSpawnPoint()
                floorRect.center = screenCenter
                player.rect.center = screenCenter
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    gameActive = True

        if gameActive:
            # Constant Inputs
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player.yMovement = +player.speed
            if keys[pygame.K_a]:
                player.xMovement = +player.speed
            if keys[pygame.K_s]:
                player.yMovement = -player.speed
            if keys[pygame.K_d]:
                player.xMovement = -player.speed

            # Player Logic
            player.playerMovement()

            # slime Logic
            if slime.checkCollision() == ('collision'):
                gameActive = False

            slime.slimeMovement()


            # Draw Screen
            screen.fill('black')
            screen.blit(floorSurf,floorRect)

            # player.draw(screen)
            screen.blit(player.surf,player.rect)
            screen.blit(slime.surf,slime.rect)

            screen.blit(leftSurf,leftRect)
            screen.blit(topSurf,topRect)
            screen.blit(rightSurf,rightRect)
            screen.blit(bottomSurf,bottomRect)
        else:
            screen.fill('Green')
            player.rect = player.surf.get_rect(center = (screenCenter))
            player.rect.center = ((screenWidth/2,(screenHeight/2)+screenHeight*0.1))
            leftRect.center = ((screenWidth/2) - (floorRect.width/2) - (leftSurf.get_width()/2),(screenHeight/2))
            topRect.center = ((screenWidth/2),(screenHeight/2) - (floorRect.height/2) - (topSurf.get_height()/2))
            rightRect.center = ((screenWidth/2) + (floorRect.width/2) + (rightSurf.get_width()/2),(screenHeight/2))
            bottomRect.center = ((screenWidth/2),(screenHeight/2) + (floorRect.height/2) + (bottomSurf.get_height()/2))
            screen.blit(player.surf,player.rect)
            screen.blit(gameEndText,gameEndRect)

        pygame.display.update() # updates the display



MainMenu()