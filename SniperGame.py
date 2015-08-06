import pygame
import time
import pygame.mixer
import random
from PIL import Image

pygame.init()

# Images
ICON = pygame.image.load("logo.png")
IMG_SM_CITY = pygame.image.load("City.png")
IMG_AIM = pygame.image.load("aim.png")
IMG_SCOPE = pygame.image.load("scope.png")
IMG_SM_CRIMINAL = pygame.image.load("sm_criminal.png")
IMG_LG_CRIMINAL = pygame.image.load("lg_criminal.png")
IMG_SM_SPLASH = pygame.image.load("sm_splash.png")
IMG_LG_SPLASH = pygame.image.load("lg_splash.png")
IMG_LEFT_ARROW = pygame.image.load("left_arrow.png")
IMG_RIGHT_ARROW = pygame.image.load("right_arrow.png")

# Fonts
SMALL_FONT = pygame.font.SysFont("comicsansms", 25, True) 
MEDIUM_FONT = pygame.font.SysFont("comicsansms", 50, True) 
LARGE_FONT = pygame.font.SysFont("comicsansms", 80, True)

# Colors
WHITE = (255,255,255)
BLACK= (0,0,0)
RED = (255,0,0)
GREEN = (0,100,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
DARK_BLUE = (0,0,30)

# Sounds
sniperShot = pygame.mixer.Sound("sniperShot.wav")

# Variables
NAME = "Sniper"
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600 
FPS = 30

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_icon(ICON)
pygame.display.set_caption(NAME) 
clock = pygame.time.Clock()

pygame.mouse.set_visible(False) # Disable default cursor

def getTextSurface(text, color, size):
    # Draw text on a new Surface
    if size == "small":
        textSurface = SMALL_FONT.render(text, True, color) 
    elif size == "medium":
        textSurface = MEDIUM_FONT.render(text, True, color)
    elif size == "large":
        textSurface = LARGE_FONT.render(text, True, color)
    return textSurface, textSurface.get_rect()

def blitText(msg, color, x_displace=0, y_displace=0, size="small"):
    # Draw surface on another surface
    textSurf, textRect = getTextSurface(msg, color, size)
    textRect.center = (DISPLAY_WIDTH/2) + x_displace, (DISPLAY_HEIGHT/2) + y_displace
    gameDisplay.blit(textSurf, textRect) 

def updateScore(score):
    text = SMALL_FONT.render("Score: "+str(score), True, YELLOW)
    gameDisplay.blit(text, [20,10])

def blackOut():
	gameDisplay.fill(RED)

# def reduceHealth(health):
# 	x = health[0] + 10
# 	y = health[1]
# 	width = health[2] - 10
# 	height = health[3]

# 	r = pygame.draw.rect(gameDisplay, RED, (x, y, width, height))
# 	return r

def checkGetHit(health):
	player = round(random.randrange(0, 300))
	target = round(random.randrange(0, 300))
	if target == player:
		blackOut()
		return health - 10
	return health

def generateTarget(target):
	BRIGHT_WINDOW = (211, 188, 95, 255)
	DARK_WINDOW = (108, 83, 83, 255)
	image = Image.open("City.png")
	repeat = True
	error = False

	if onScope:
		img_criminal = IMG_LG_CRIMINAL
	else:
		img_criminal = IMG_SM_CRIMINAL

	while repeat:
		targetPositionX = round(random.randrange(0, IMG_SM_CITY.get_rect()[2] - target.size[0]))
		targetPositionY = round(random.randrange(0, DISPLAY_HEIGHT - target.size[1]))
		x = targetPositionX - city.x
		y = targetPositionY - city.y 

		try:
			pixelColor = image.getpixel((x,y))

			# Get location
			if pixelColor == BRIGHT_WINDOW:
				print("BRIGHT_WINDOW")
				location = BRIGHT_WINDOW
				repeat = False
			elif pixelColor == DARK_WINDOW:
				print("DARK_WINDOW")
				location = DARK_WINDOW
				repeat = False
		except:
			pass

	onFloor = False
	onLeft = False

	try:
		while not onFloor:
			y += 1
			pixelColor = image.getpixel((x,y))

			if not pixelColor == location:
				onFloor = True

		y -= 1
	except:
		y = 475
		
	try: 
		while not onLeft:
			x -= 1
			pixelColor = image.getpixel((x,y))

			if not pixelColor == location:
				onLeft = True	

		x += 1
	except:
		x = 49
		pass

	return x + city.x, y + city.y - img_criminal.get_rect()[3]

def checkHitTarget(target):
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

					# Hold the splash image for a short period of time
					while timer > pygame.time.get_ticks():
						gameDisplay.blit(splash, (target.x, target.y))
						pygame.display.update()

					targetPositionX, targetPositionY = generateTarget(target)
					return True
				else:
					targetPositionX = target.x
					targetPositionY = target.y
				return False
			except:
				pass

def runGame():
	global city
	global onScope
	global score
	global hit
	hit = False
	gameExit = False
	gameOver = False
	onScope = False
	mouseCursor = IMG_AIM.convert_alpha() # Add image on cursor
	disp_x = 0
	score = 0
	healthPoint = 100

	city = gameDisplay.blit(IMG_SM_CITY, (0, 68))
	criminal = gameDisplay.blit(IMG_SM_CRIMINAL, (49, 475))
	city_position_x = city.x 
	targetPositionX, targetPositionY = generateTarget(criminal)
	criminal_position_x = targetPositionX

	while not gameExit:	
		# Get mouse cursor position
		cursorX,cursorY = pygame.mouse.get_pos()
		cursorX -= mouseCursor.get_width()/2 
		cursorY -= mouseCursor.get_height()/2

		if onScope:
			img_criminal = IMG_LG_CRIMINAL
		else:
			img_criminal = IMG_SM_CRIMINAL
		
		# Move background depending on cursor's X position
		if onScope:
			if cursorX > -50:
				disp_x = -10
			elif cursorX < - DISPLAY_WIDTH + 50:
				disp_x = 10
			else:
				disp_x = 0
		else:
			if cursorX > DISPLAY_WIDTH - 50: # Move right
				disp_x = -10
			elif cursorX < 50:
				disp_x = 10
			else:
				disp_x = 0
		city_position_x  = city_position_x  + disp_x

		# Make sure the city background can be seen on the window
		if city_position_x  > 0:
			city_position_x  = 0
			disp_x = 0
		elif city_position_x  < - IMG_SM_CITY.get_rect()[2] + DISPLAY_WIDTH:
			city_position_x  = - IMG_SM_CITY.get_rect()[2] + DISPLAY_WIDTH
			disp_x = 0 

		criminal_position_x = criminal_position_x + disp_x

		gameDisplay.fill(DARK_BLUE)			
		city = gameDisplay.blit(IMG_SM_CITY, (city_position_x,68))

		criminal = gameDisplay.blit(img_criminal, (targetPositionX + city_position_x, targetPositionY))  	

		# Show where player should move the mouse to find the criminal if criminal goes off screen
		if targetPositionX + city_position_x < 0:
			left_arrow = gameDisplay.blit(IMG_LEFT_ARROW, (10, DISPLAY_HEIGHT/2 - IMG_LEFT_ARROW.get_rect()[2]/2))
		elif targetPositionX + city_position_x > DISPLAY_WIDTH:
			right_arrow = gameDisplay.blit(IMG_RIGHT_ARROW, (DISPLAY_WIDTH - IMG_LEFT_ARROW.get_rect()[2] - 10, DISPLAY_HEIGHT/2 - IMG_RIGHT_ARROW.get_rect()[2]/2))

		# Update health Point
		healthPoint = checkGetHit(healthPoint)
		print(healthPoint)

		# Draw healthBar
		pygame.draw.rect(gameDisplay, BLACK, [DISPLAY_WIDTH - 220,15,200,40])

		if not healthPoint == 0:
			pygame.draw.rect(gameDisplay, RED, [DISPLAY_WIDTH - 215,20,190*(healthPoint/100),30])
		else:
			pygame.draw.rect(gameDisplay, BLACK, [DISPLAY_WIDTH - 220,15,200,40]) # Hide red bar
			gameOver = True
		updateScore(score) # Update score

		# Draw cursor with scope
		gameDisplay.blit(mouseCursor,(cursorX,cursorY)) 

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if pygame.key.get_pressed()[pygame.K_LALT] and pygame.key.get_pressed()[pygame.K_F4]:
					pygame.quit()
					quit()
				elif event.key == pygame.K_a:
					blackOut()
			elif event.type == pygame.MOUSEBUTTONUP:
				# If mouse left click is pressed
				if event.button == 1: 
					sniperShot.play()

					# Sniper Recoil
					x,y = pygame.mouse.get_pos()
					pygame.mouse.set_pos([x,y-10])

					try:
						# If criminal is hit
						if checkHitTarget(criminal):
							# Update target position 
							targetPositionX, targetPositionY = generateTarget(criminal)
							score += 1
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