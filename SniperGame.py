import pygame
import time
import pygame.mixer
import random
from PIL import Image

pygame.init()

# Images
IMG_AIM = pygame.image.load("aim.png")
IMG_SCOPE = pygame.image.load("scope.png")
IMG_SM_CRIMINAL = pygame.image.load("sm_criminal.png")
IMG_LG_CRIMINAL = pygame.image.load("lg_criminal.png")
IMG_SM_SPLASH = pygame.image.load("sm_splash.png")
IMG_LG_SPLASH = pygame.image.load("lg_splash.png")

# Colors
WHITE = (255,255,255)
BLACK= (0,0,0)
RED = (255,0,0)
GREEN = (0,100,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

# Sounds
sniperShot = pygame.mixer.Sound("sniperShot.wav")

# Variables
NAME = "Sniper"
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600 
FPS = 30
Hit = False

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption(NAME) 
clock = pygame.time.Clock()

pygame.mouse.set_visible(False) # Disable default cursor

def getType(object):
	return object.__class__.__name__

def generateTarget(target):
    targetPositionX = round(random.randrange(0, DISPLAY_WIDTH - target.size[0]))
    targetPositionY = round(random.randrange(0, DISPLAY_HEIGHT - target.size[1]))
    return targetPositionX, targetPositionY

def checkHitTarget(target, onScope):

	if not onScope:
		image = Image.open("sm_criminal.png")
		splash = IMG_SM_SPLASH
	else:
		image = Image.open("lg_criminal.png")
		splash = IMG_LG_SPLASH

	# Get mouse position
	mouseX,mouseY = pygame.mouse.get_pos()

	# Check for collision
	if mouseX >= target.x and mouseX <= target.x + target.size[0]:
		if mouseY >= target.y and mouseY <= target.y + target.size[1]:
			x = mouseX - target.x 
			y = mouseY - target.y

			try:
				# Check alpha color of the specific pixel 	
				if image.getpixel((x,y))[3] > 0:
					print("Hit!")
					timer = pygame.time.get_ticks() + 200
					# Hold the splash image for a period of time
					while timer > pygame.time.get_ticks():
						gameDisplay.blit(splash, (target.x, target.y))
						pygame.display.update()

					targetPositionX, targetPositionY = generateTarget(target)
				else:
					targetPositionX = target.x
					targetPositionY = target.y
				return targetPositionX, targetPositionY
			except:
				pass

def runGame():
	gameExit = False
	gameOver = False
	onScope = False
	mouseCursor = IMG_AIM.convert_alpha() # Add image on cursor

	criminal = gameDisplay.blit(IMG_SM_CRIMINAL, (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2))
	targetPositionX, targetPositionY = generateTarget(criminal)

	while not gameExit:		
		gameDisplay.fill(WHITE)

		if onScope:
			criminal = gameDisplay.blit(IMG_LG_CRIMINAL, (targetPositionX, targetPositionY))
		else:
			criminal = gameDisplay.blit(IMG_SM_CRIMINAL, (targetPositionX, targetPositionY))

		# NOTE: Make sure cursor image is drawn after all game images
		cursorX,cursorY = pygame.mouse.get_pos()
		cursorX -= mouseCursor.get_width()/2 
		cursorY -= mouseCursor.get_height()/2
		gameDisplay.blit(mouseCursor,(cursorX,cursorY)) 

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if pygame.key.get_pressed()[pygame.K_LALT] and pygame.key.get_pressed()[pygame.K_F4]:
					pygame.quit()
					quit()
			elif event.type == pygame.MOUSEBUTTONUP:
				# If mouse left click is pressed
				if event.button == 1: 
					sniperShot.play()

					# Sniper Recoil
					x,y = pygame.mouse.get_pos()
					pygame.mouse.set_pos([x,y-10])

					# Update target position 
					try:
						targetPositionX, targetPositionY = checkHitTarget(criminal, onScope)
					except:
						pass

					if onScope: 
						mouseCursor = IMG_AIM.convert_alpha()
						onScope = False

				# If mouse right click is pressed
				elif event.button == 3:

					if onScope:
						mouseCursor = IMG_AIM.convert_alpha()
						onScope = False
					else:	
						mouseCursor = IMG_SCOPE.convert_alpha()
						onScope = True

		pygame.display.update()
		clock.tick(FPS)

	pygame.quit()
	quit()

runGame()