import pygame
import time
import random
 
pygame.init()

crash_sound = pygame.mixer.Sound("crash.wav")
car_sound= pygame.mixer.Sound("car.wav")
 
display_width = 800
display_height = 500
 
black = (0,0,0)
white = (255,255,255)
grey = (105,105,105)

red = (200,0,0)
green = (0,200,0)
yellow = (200,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)
bright_yellow = (255,255,0)

block_color = (255,0,0)
 
car_width = 100

pop=3

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('ESCAPE THE BOXES')
clock = pygame.time.Clock()
 
carImg = pygame.image.load('spc.png')
gameIcon = pygame.image.load('spc.png')

pygame.display.set_icon(gameIcon)

pause = False
#crash = True
    
 
def things_dodged(count):
    font = pygame.font.SysFont("Helvetica", 25)
    text = font.render("score : "+str(count), True, black)
    gameDisplay.blit(text,(0,0))
 
def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay,color, [thingx, thingy, thingw, thingh])
 
def car(x,y):
    gameDisplay.blit(carImg,(x,y))
 
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
 
last_10_scores = []

def crash(score):
    last_10_scores.append(score)
    if len(last_10_scores) > 10:
        last_10_scores.pop(0)  
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.Sound.stop(car_sound)
    largeText = pygame.font.SysFont("Helvetica", 115)
    TextSurf, TextRect = text_objects("BLASTED", largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    highest_score = max(last_10_scores, default=0)
    font = pygame.font.SysFont("Helvetica", 25)
    text = font.render("Highest Score: " + str(highest_score), True, black)
    gameDisplay.blit(text, (display_width - text.get_width() - 10, 10))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Easy", 100, 450, 100, 50, green, bright_green, game_loop)
        button("Medium", 250, 450, 100, 50, yellow, bright_yellow, medium)
        button("Hard", 400, 450, 100, 50, red, bright_red, hard)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)
        pygame.display.update()
        clock.tick(15)

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
    

def quitgame():
    pygame.quit()
    quit()

def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False
    

def paused():
    pygame.mixer.music.pause()
    largeText = pygame.font.SysFont("Helvetica",115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        

        button("Continue",150,450,100,50,green,bright_green,unpause)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)   



 

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(grey)
        largeText = pygame.font.SysFont("lucidasans",115)
        TextSurf, TextRect = text_objects("DODGE EM", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("Easy",100,450,100,50,green,bright_green,game_loop)
        button("Medium",250,450,100,50,yellow,bright_yellow,medium)
        button("Hard",400,450,100,50,red,bright_red,hard)
        button("Quit",550,450,100,50,red,bright_red,quitgame)
        

        pygame.display.update()
        clock.tick(15)
        

def hard():
    global pause
    pygame.mixer.Sound.play(car_sound)

    x = (display_width * 0.4)
    y = (display_height * 0.8)
 
    x_change = 0
 
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100
 
    thingCount = 1
 
    dodged = 0
 
    gameExit = False

    while not gameExit:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                    
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
 
        x += x_change
        gameDisplay.fill(grey)
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
 
 
        
        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)
        
 
        if x > display_width - car_width or x < 0:
            crash(dodged)

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            dodged += 1
            thing_speed += 5
            thing_width += (dodged * 1.2)
            
        if y < thing_starty+thing_height:
            if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                crash(dodged)
                  
        
        pygame.display.update()
        clock.tick(60)

def medium():
    global pause
    pygame.mixer.Sound.play(car_sound)

    x = (display_width * 0.4)
    y = (display_height * 0.8)
 
    x_change = 0
 
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100
 
    thingCount = 1
 
    dodged = 0
 
    gameExit = False

    while not gameExit:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                    
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
 
        x += x_change
        gameDisplay.fill(grey)
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
 
 
        
        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)
        
 
        if x > display_width - car_width or x < 0:
            crash(dodged)

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            dodged += 1
            thing_speed += 3
            thing_width += (dodged * 1.2)
            
        if y < thing_starty+thing_height:
            if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                crash(dodged) 
                  
        
        pygame.display.update()
        clock.tick(60)

def game_loop():
    global pause
    pygame.mixer.Sound.play(car_sound)

    x = (display_width * 0.4)
    y = (display_height * 0.8)

    x_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100

    thingCount = 1

    dodged = 0

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(grey)
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)

        thing_starty += thing_speed
        car(x, y)
        things_dodged(dodged)

        if x > display_width - car_width or x < 0:
            crash(dodged)

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 1.2)

        if y < thing_starty + thing_height:
            if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
                crash(dodged)

        pygame.display.update()
        clock.tick(60)




game_intro()
game_loop()
pygame.quit()
hard()
quit()

