import pygame
import time
import random
from PIL import Image
import tkinter 

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
IMG_SPLATTER = pygame.image.load("splatter.png")
IMG_RELOAD = pygame.image.load("reload.png")
IMG_RELOAD_HOVER = pygame.image.load("reload2.png")
IMG_EXIT = pygame.image.load("exit.png")
IMG_EXIT_HOVER = pygame.image.load("exit2.png")

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

def exitGame():
	pygame.quit()
	quit()

def updateScore(score):
    text = SMALL_FONT.render("Score: "+str(score), True, YELLOW)
    gameDisplay.blit(text, [20,10])

def blackOut(color):
	gameDisplay.fill(color)

def checkGetHit(health):
	player = round(random.randrange(0, 300))
	target = round(random.randrange(0, 300))
	# player = round(random.randrange(0, 50))
	# target = round(random.randrange(0, 50))
	if target == player:
		blackOut(RED)
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
	disp_y = 0

	city = gameDisplay.blit(IMG_SM_CITY, (0, 68))
	criminal = gameDisplay.blit(IMG_SM_CRIMINAL, (49, 475))
	city_position_x = city.x 
	targetPositionX, targetPositionY = generateTarget(criminal)
	criminal_position_x = targetPositionX

	while not gameExit:	
		img_replay = IMG_RELOAD 
		img_exit = IMG_EXIT

		while gameOver:
			GAMEOVER_BUTTON = (49,255,8,255)
			GAMEOVER_BUTTON_HOVER = (35,184,6,255)
			pygame.mouse.set_visible(True) # Enable default cursor
			gameDisplay.fill(DARK_BLUE)
			gameDisplay.blit(IMG_SPLATTER, (DISPLAY_WIDTH/2 - IMG_SPLATTER.get_rect()[2]/2, DISPLAY_HEIGHT/2 - IMG_SPLATTER.get_rect()[3]/2))  	
			blitText("Press C to play again or Q to quit", YELLOW, y_displace=-260)
			blitText("GAME OVER", WHITE, x_displace=15, size="small")
			blitText(str(score), WHITE, size="medium", x_displace=15, y_displace=50)
			replay = gameDisplay.blit(img_replay, (20, 20))
			quit = gameDisplay.blit(img_exit, (720, 20))
			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exitGame()
				elif event.type == pygame.KEYDOWN:
					if pygame.key.get_pressed()[pygame.K_LALT] and pygame.key.get_pressed()[pygame.K_F4]:
						exitGame()
					elif event.key == pygame.K_c:
						healthPoint = 100
						score = 0
						gameOver = False
						targetPositionX, targetPositionY = generateTarget(criminal)
						city_position_x = 0
						pygame.display.update()
					elif event.key == pygame.K_q:
						exitGame()
				elif event.type == pygame.MOUSEBUTTONUP:
					# If mouse left click is pressed
					if event.button == 1: 
						posX, posY = pygame.mouse.get_pos()
						if replay.collidepoint((posX, posY)):
							image = Image.open("reload.png")
							x = posX - replay.x
							y = posY - replay.y
							if image.getpixel((x,y)) == GAMEOVER_BUTTON: 
								healthPoint = 100
								score = 0
								gameOver = False
								targetPositionX, targetPositionY = generateTarget(criminal)
								city_position_x = 0
								pygame.display.update()
						elif quit.collidepoint(pygame.mouse.get_pos()):
							image = Image.open("exit.png")
							x = posX - quit.x
							y = posY - quit.y
							if image.getpixel((x,y)) == GAMEOVER_BUTTON: 
								exitGame()
				elif event.type == pygame.MOUSEMOTION:
					posX, posY = pygame.mouse.get_pos()

					# If mouse collides with replay image
					if replay.collidepoint((posX, posY)):
						image = Image.open("reload.png")
						x = posX - replay.x
						y = posY - replay.y

						# Add hover on img_replay
						if image.getpixel((x,y)) == GAMEOVER_BUTTON:
							img_replay = IMG_RELOAD_HOVER
					# If mouse collides with quit image
					elif quit.collidepoint((posX, posY)):
						image = Image.open("exit.png")
						x = posX - quit.x
						y = posY - quit.y

						# Add hover on img_exit
						if image.getpixel((x,y)) == GAMEOVER_BUTTON:
							img_exit = IMG_EXIT_HOVER
					else:
						img_replay = IMG_RELOAD
						img_exit = IMG_EXIT

		# Get mouse cursor position
		cursorX,cursorY = pygame.mouse.get_pos()						
		cursorX -= mouseCursor.get_width()/2 
		cursorY -= mouseCursor.get_height()/2
		pygame.mouse.set_visible(False) # Disable default cursor

		if onScope:
			img_criminal = IMG_LG_CRIMINAL
			disp_y = -12
		else:
			img_criminal = IMG_SM_CRIMINAL
			if disp_y == -12:
				disp_y = 12
			else:
				disp_y = 0
		
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

		criminal = gameDisplay.blit(img_criminal, (targetPositionX + city_position_x, targetPositionY + disp_y))  	

		# Show where player should move the mouse to find the criminal if criminal goes off screen
		if targetPositionX + city_position_x < 0:
			left_arrow = gameDisplay.blit(IMG_LEFT_ARROW, (10, DISPLAY_HEIGHT/2 - IMG_LEFT_ARROW.get_rect()[2]/2))
		elif targetPositionX + city_position_x > DISPLAY_WIDTH:
			right_arrow = gameDisplay.blit(IMG_RIGHT_ARROW, (DISPLAY_WIDTH - IMG_LEFT_ARROW.get_rect()[2] - 10, DISPLAY_HEIGHT/2 - IMG_RIGHT_ARROW.get_rect()[2]/2))

		# Update health Point
		healthPoint = checkGetHit(healthPoint)

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
				exitGame()
			elif event.type == pygame.KEYDOWN:
				if pygame.key.get_pressed()[pygame.K_LALT] and pygame.key.get_pressed()[pygame.K_F4]:
					exitGame()
				# elif event.key == pygame.K_a:
				# 	blackOut(BLACK)
				# 	gameOver = True
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
							if onScope:
								targetPositionY += 12
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

	exitGame()

runGame()