# Potter Duel
# Author: Mark Link II
# Date: 12/02/19

import pygame
import random


# Returns the awarded trophy amount given the winner and loser's current trophy count
def getTrophyPlus(winner, loser):
    dif = winner - loser
    if dif > 10:
        return 10
    elif dif > 0:
        return 20 - dif
    elif dif == 0:
        return 20
    elif 0 > dif > -10:
        return abs(dif) + 20
    else:
        return 30


# Checks for collision between spell and other entity
def getSpellCollision(x1, x2, y1, y2, radius, width, height):
    if x1 + radius > x2 and x1 - radius < x2 + width:
        if y1 - radius < y2 + height and y1 + radius > y2:
            return True
    return False


# Checks for collision of two non spell entities
def getCollision(x1, y1, x2, y2, width1, width2, height1, height2):
    for i in range(x1, x1+width1):
        if x2 <= i <= x2+width2:
            for j in range(y1, y1+height1):
                if y2 <= j <= y2+height2:
                    return True
    return False


SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600

PLAYER_WIDTH = 97
PLAYER_HEIGHT = 124

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)

# Initializers
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.font.init()
pygame.display.set_caption("Potter Duel")

# Fonts
testFont = pygame.font.SysFont('Times New Roman', 70)
titleFont = pygame.font.SysFont('Times New Roman', 90)
escFont = pygame.font.SysFont('Comic Sans MS', 15)
selectFont = pygame.font.SysFont('Elephant', 30)
howtoplayfont = pygame.font.SysFont('Times New Roman', 20)
backFont = pygame.font.SysFont('Times New Roman', 30)

# Graphics
smallSheet = pygame.image.load('Graphics/transSheet.png').convert_alpha()
smallSheet = pygame.transform.scale(smallSheet, (500, 500))
sheet = pygame.image.load('Graphics/transSheet1.png').convert_alpha()
sheet = pygame.transform.scale(sheet, (1200, 1200))
sheet1 = pygame.image.load('Graphics/transSheet2.png').convert_alpha()
sheet1 = pygame.transform.scale(sheet1, (1200, 1200))
icon1 = pygame.image.load('Graphics/spell1.jpg').convert_alpha()
icon1 = pygame.transform.scale(icon1, (45, 50))
icon2 = pygame.image.load('Graphics/spell2.png').convert_alpha()
icon2 = pygame.transform.scale(icon2, (45, 45))
icon3 = pygame.image.load('Graphics/spell3.png').convert_alpha()
icon3 = pygame.transform.scale(icon3, (50, 50))
menubg = pygame.image.load('Graphics/menuBG.jpg').convert_alpha()
menubg = pygame.transform.scale(menubg, (1100, 600))
bg = pygame.image.load('Graphics/bg.jpg').convert_alpha()
bg = pygame.transform.scale(bg, (1100, 600))
hpack = pygame.image.load('Graphics/hpack.png').convert_alpha()
hpack = pygame.transform.scale(hpack, (50, 50))
greenspell = pygame.image.load('Graphics/greenspell.png').convert_alpha()
greenspell = pygame.transform.scale(greenspell, (40, 40))
redspell = pygame.image.load('Graphics/redspell.png').convert_alpha()
redspell = pygame.transform.scale(redspell, (40, 40))
bluespellL = pygame.image.load('Graphics/bluespellL.png').convert_alpha()
bluespellL = pygame.transform.scale(bluespellL, (40, 40))
bluespellR = pygame.image.load('Graphics/bluespellR.png').convert_alpha()
bluespellR = pygame.transform.scale(bluespellR, (40, 40))
htpbg = pygame.image.load('Graphics/htpBG.jpg').convert_alpha()
htpbg = pygame.transform.scale(htpbg, (1100, 600))
keyboard = pygame.image.load('Graphics/keys.jpg').convert_alpha()
keyboard = pygame.transform.scale(keyboard, (500, 200))
shield = pygame.image.load('Graphics/shield.png').convert_alpha()
shield = pygame.transform.scale(shield, (50, 50))

# SFX
fireSound = pygame.mixer.Sound("Sounds/fire.wav")
fireSound.set_volume(0.5)
iceSound = pygame.mixer.Sound("Sounds/ice.wav")
iceSound.set_volume(0.6)
spellSound = pygame.mixer.Sound("Sounds/spell.wav")
spellSound.set_volume(0.5)
healthSound = pygame.mixer.Sound("Sounds/health.wav")
healthSound.set_volume(0.5)
hitSound = pygame.mixer.Sound("Sounds/oof.wav")
hitSound.set_volume(0.11)
buttonSound = pygame.mixer.Sound("Sounds/button.aiff")
buttonSound.set_volume(0.6)
shieldHit = pygame.mixer.Sound("Sounds/shieldHit.wav")
shieldHit.set_volume(0.35)
shieldUp = pygame.mixer.Sound("Sounds/shieldUp.flac")
shieldUp.set_volume(0.35)

# Boundary variable
difference = 0

# Character info
p1x = 170
p1y = 425
preJumpY1 = p1y
p2x = 820
p2y = 425
preJumpY2 = p2y
vel = 12
hp1 = 100
hp2 = 100

# Spell info
spellWidth = 20
spellVel = 40
s1p1x = 0
s2p1x = 0
s3p1x = 0
s1p2x = 0
s2p2x = 0
s3p2x = 0
s1p1y = 0
s2p1y = 0
s3p1y = 0
s1p2y = 0
s2p2y = 0
s3p2y = 0

# for jump mechanics
forceConst = 80
jumpCount1 = 9
jumpCount2 = 9
forceDiff1 = 0
forceDiff2 = 0

# makes this thing run
run = True

# Screen checkers
onMatchScreen = False
beginMatch = False
onMenu = True
gameOver = False
onHowToPlay = False
GameOver = False

# Jump checkers
isJump1 = False
isJump2 = False
forceDown1 = False
forceDown2 = False

# Spell selected
spell1P1 = True
spell2P1 = False
spell3P1 = False
spell1P2 = True
spell2P2 = False
spell3P2 = False

# Spell being used
spell1P1Fire = False
spell2P1Fire = False
spell3P1Fire = False
spell1P2Fire = False
spell2P2Fire = False
spell3P2Fire = False

# Spell direction
spell1P1Left = False
spell2P1Left = False
spell3P1Left = False
spell1P2Left = False
spell2P2Left = False
spell3P2Left = False
spell1P1Right = False
spell2P1Right = False
spell3P1Right = False
spell1P2Right = False
spell2P2Right = False
spell3P2Right = False

# Spell effects
frozen1 = False
frozen2 = False
fire1 = False
fire2 = False
useFreezeTimer1 = False
useFreezeTimer2 = False
useFireTimer1 = False
useFireTimer2 = False
freezeDuration = 1.5
fireDuration = 5
fireDamage = 4
fd1p1 = False
fd2p1 = False
fd3p1 = False
fd4p1 = False
fd5p1 = False
fd1p2 = False
fd2p2 = False
fd3p2 = False
fd4p2 = False
fd5p2 = False

# Health pack info
healthPackOnMap = False
hpx = random.randint(0, 1050)
hpy = 50

# Shield info
shieldx = random.randint(0, 1050)
shieldy = 50
shieldOnMap = False
shieldInInv1 = False
shieldInInv2 = False
shieldDuration = 4
useShieldTimer = False

# Temporary trophy count
tempCount = 0

# Players moving left or right
left1 = False
left2 = True
right1 = True
right2 = False

# Start game timer
gameStart = False
useGameStartTimer = False
timer = 4
timeElapsedStart = 0

# Load Music
loadMenuMusic = False
loadGameMusic = False
loadWinMusic = False

# Character selection P1
char1P1 = True
char2P1 = False
char3P1 = False
char4P1 = False
char5P1 = False
char6P1 = False
char7P1 = False
char8P1 = False

# Character selection P2
char1P2 = False
char2P2 = True
char3P2 = False
char4P2 = False
char5P2 = False
char6P2 = False
char7P2 = False
char8P2 = False

drawP1x = 15
drawP1y = 175

drawP2x = 127
drawP2y = 175

# TODO: Settings
allMusic = True
allSFX = True

# How to Play flags
hoverOverHTP = False
hoverOverBack = False
hoverOverStart = False

fileData = []
try:
    trophyFile = open("trophyFile.txt", "r")
except FileNotFoundError:
    trophyFile = open("trophyFile.txt", "w")
    for i in range(0, 2):
        trophyFile.write('0\n')
    trophyFile.close()
    trophyFile = open("trophyFile.txt", "r")
    for i in range(0, 2):
        line = trophyFile.readline()
        fileData.append(float(line))
else:
    for i in range(0, 2):
        line = trophyFile.readline()
        fileData.append(float(line))
trophyCount1 = fileData[0]
trophyCount2 = fileData[1]

while run:
    # Grabbing characters from sheet
    if char1P1:
        drawP1x = 15
        drawP1y = 175
    if char2P1:
        drawP1x = 127
        drawP1y = 175
    if char3P1:
        drawP1x = 15
        drawP1y = 755
    if char4P1:
        drawP1x = 127
        drawP1y = 755
    if char5P1:
        drawP1x = 575
        drawP1y = 175
    if char6P1:
        drawP1x = 463
        drawP1y = 175
    if char7P1:
        drawP1x = 351
        drawP1y = 900
    if char8P1:
        drawP1x = 463
        drawP1y = 320
    if char1P2:
        drawP2x = 15
        drawP2y = 175
    if char2P2:
        drawP2x = 127
        drawP2y = 175
    if char3P2:
        drawP2x = 15
        drawP2y = 755
    if char4P2:
        drawP2x = 127
        drawP2y = 755
    if char5P2:
        drawP2x = 575
        drawP2y = 175
    if char6P2:
        drawP2x = 463
        drawP2y = 175
    if char7P2:
        drawP2x = 351
        drawP2y = 900
    if char8P2:
        drawP2x = 463
        drawP2y = 320
    # Game start timer
    if onMatchScreen and not gameStart:
        if not useGameStartTimer:
            useGameStartTimer = True
            gameStartTime = pygame.time.get_ticks()
        else:
            timeElapsedStart = timer - ((pygame.time.get_ticks()-gameStartTime)/1000)
            if timeElapsedStart <= 0:
                gameStart = True
                useGameStartTimer = False
    # Fail-safe for falling under map
    if p1y > 425:
        p1y = 425
    if p2y > 425:
        p2y = 425
    pygame.time.delay(38)
    # Timer for shield
    if shieldInInv1 and not useShieldTimer:
        useShieldTimer = True
        shieldTime = pygame.time.get_ticks()
    elif shieldInInv1 and useShieldTimer:
        timeElapsedShield = shieldDuration - ((pygame.time.get_ticks()-shieldTime)/1000)
        if timeElapsedShield <= 0:
            useShieldTimer = False
            shieldInInv1 = False
            shieldOnMap = False
            shield1Active = False
            shieldx = random.randint(0, 1050)
            shieldy = 50
    if shieldInInv2 and not useShieldTimer:
        useShieldTimer = True
        shieldTime = pygame.time.get_ticks()
    elif shieldInInv2 and useShieldTimer:
        timeElapsedShield = shieldDuration - ((pygame.time.get_ticks() - shieldTime) / 1000)
        if timeElapsedShield <= 0:
            useShieldTimer = False
            shieldInInv2 = False
            shieldOnMap = False
            shield1Active = False
            shieldx = random.randint(0, 1050)
            shieldy = 50
    # Timer for freeze spell
    if frozen2 and not useFreezeTimer1:
        useFreezeTimer1 = True
        freezeTime1 = pygame.time.get_ticks()
    elif frozen2 and useFreezeTimer1:
        timeElapsed1 = freezeDuration - ((pygame.time.get_ticks()-freezeTime1)/1000)
        if timeElapsed1 <= 0:
            frozen2 = False
            useFreezeTimer1 = False
    if frozen1 and not useFreezeTimer2:
        useFreezeTimer2 = True
        freezeTime2 = pygame.time.get_ticks()
    elif frozen1 and useFreezeTimer2:
        timeElapsed2 = freezeDuration - ((pygame.time.get_ticks()-freezeTime2)/1000)
        if timeElapsed2 <= 0:
            frozen1 = False
            useFreezeTimer2 = False
    # Timer for fire spell
    if fire1 and not useFireTimer1:
        useFireTimer1 = True
        fireTime1 = pygame.time.get_ticks()
    elif fire1 and useFireTimer1:
        timeElapsedF1 = fireDuration - ((pygame.time.get_ticks()-fireTime1)/1000)
        if int(timeElapsedF1) == 0 and not fd1p1 and not shieldInInv1:
            hp1 -= fireDamage
            fd1p1 = True
        if int(timeElapsedF1) == 1 and not fd2p1 and not shieldInInv1:
            hp1 -= fireDamage
            fd2p1 = True
        if int(timeElapsedF1) == 2 and not fd3p1 and not shieldInInv1:
            hp1 -= fireDamage
            fd3p1 = True
        if int(timeElapsedF1) == 3 and not fd4p1 and not shieldInInv1:
            hp1 -= fireDamage
            fd4p1 = True
        if int(timeElapsedF1) == 4 and not fd5p1 and not shieldInInv1:
            hp1 -= fireDamage
            fd5p1 = True
        if timeElapsedF1 <= 0:
            fd1p1 = False
            fd2p1 = False
            fd3p1 = False
            fd4p1 = False
            fd5p1 = False
            fire1 = False
            useFireTimer1 = False
    if fire2 and not useFireTimer2:
        useFireTimer2 = True
        fireTime2 = pygame.time.get_ticks()
    elif fire2 and useFireTimer2:
        timeElapsedF2 = fireDuration - ((pygame.time.get_ticks()-fireTime2)/1000)
        if int(timeElapsedF2) == 0 and not fd1p2 and not shieldInInv2:
            hp2 -= fireDamage
            fd1p2 = True
        if int(timeElapsedF2) == 1 and not fd2p2 and not shieldInInv2:
            hp2 -= fireDamage
            fd2p2 = True
        if int(timeElapsedF2) == 2 and not fd3p2 and not shieldInInv2:
            hp2 -= fireDamage
            fd3p2 = True
        if int(timeElapsedF2) == 3 and not fd4p2 and not shieldInInv2:
            hp2 -= fireDamage
            fd4p2 = True
        if int(timeElapsedF2) == 4 and not fd5p2 and not shieldInInv2:
            hp2 -= fireDamage
            fd5p2 = True
        if timeElapsedF2 <= 0:
            fd1p2 = False
            fd2p2 = False
            fd3p2 = False
            fd4p2 = False
            fd5p2 = False
            fire2 = False
            useFireTimer2 = False
    keys = pygame.key.get_pressed()
    # Move player 1 right
    if keys[pygame.K_d] and p1x < SCREEN_WIDTH - PLAYER_WIDTH - vel and not frozen1 and onMatchScreen and gameStart:
        right1 = True
        left1 = False
        p1x += vel
    # Boundary for player 1 right
    elif keys[pygame.K_d] and p1x >= SCREEN_WIDTH - PLAYER_WIDTH - vel and not frozen1 and onMatchScreen:
        right1 = True
        left1 = False
        difference = (p1x+vel+PLAYER_WIDTH) - SCREEN_WIDTH
        p1x += vel - difference
    # Move player 1 left
    if keys[pygame.K_a] and p1x - vel >= 0 and not frozen1 and onMatchScreen and gameStart:
        left1 = True
        right1 = False
        p1x -= vel
    # Move player 1 left
    if keys[pygame.K_a] and p1x - vel < 0 and not frozen1 and onMatchScreen:
        left1 = True
        right1 = False
        p1x = 0
    # Move player 2 right
    if keys[pygame.K_RIGHT] and p2x < SCREEN_WIDTH - PLAYER_WIDTH - vel and not frozen2 and onMatchScreen and gameStart:
        right2 = True
        left2 = False
        p2x += vel
    # Boundary for player 2 right
    elif keys[pygame.K_RIGHT] and p2x >= SCREEN_WIDTH - PLAYER_WIDTH - vel and not frozen2 and onMatchScreen:
        right2 = True
        left2 = False
        difference = (p2x + vel + PLAYER_WIDTH) - SCREEN_WIDTH
        p2x += vel - difference
    # Move player 2 left
    if keys[pygame.K_LEFT] and p2x - vel >= 0 and not frozen2 and onMatchScreen and gameStart:
        left2 = True
        right2 = False
        p2x -= vel
    # Boundary for player 2 left
    elif keys[pygame.K_LEFT] and p2x - vel < 0 and not frozen2 and onMatchScreen:
        right2 = False
        left2 = True
        p2x = 0
    # Cancel jump player 1
    if keys[pygame.K_s] and isJump1 and onMatchScreen:
        if frozen1:
            isJump1 = False
            forceDown1 = False
            p1y = preJumpY1
        else:
            isJump1 = False
            forceDown1 = True
            jumpCount1 = 9
    # Cancel jump player 2
    if keys[pygame.K_DOWN] and isJump2 and onMatchScreen:
        if frozen2:
            isJump2 = False
            forceDown2 = False
            p2y = preJumpY2
        else:
            isJump2 = False
            forceDown2 = True
            jumpCount2 = 9
    # Player 1 jump
    if keys[pygame.K_w] and onMatchScreen:
        if not isJump1 and not forceDown1 and not frozen1 and gameStart:
            isJump1 = True
            preJumpY1 = p1y
    # Player 2 jump
    if keys[pygame.K_UP] and onMatchScreen:
        if not isJump2 and not forceDown2 and not frozen2 and gameStart:
            isJump2 = True
            preJumpY2 = p2y
    # Select spell 1 Player 1
    if keys[pygame.K_1] and onMatchScreen and not GameOver and gameStart:
        spell1P1 = True
        spell2P1 = False
        spell3P1 = False
    # Select spell 2 Player 1
    if keys[pygame.K_2] and onMatchScreen and not GameOver and gameStart:
        spell1P1 = False
        spell2P1 = True
        spell3P1 = False
    # Select spell 3 Player 1
    if keys[pygame.K_3] and onMatchScreen and not GameOver and gameStart:
        spell1P1 = False
        spell2P1 = False
        spell3P1 = True
    # Select spell 1 Player 2
    if keys[pygame.K_RCTRL] and onMatchScreen and not GameOver and gameStart:
        spell1P2 = True
        spell2P2 = False
        spell3P2 = False
    # Select spell 2 Player 2
    if keys[pygame.K_PERIOD] and onMatchScreen and not GameOver and gameStart:
        spell1P2 = False
        spell2P2 = True
        spell3P2 = False
    # Select spell 3 Player 2
    if keys[pygame.K_SLASH] and onMatchScreen and not GameOver and gameStart:
        spell1P2 = False
        spell2P2 = False
        spell3P2 = True
    # Jump mechanics player 1
    if isJump1:
        if frozen1:
            isJump1 = False
            p1y = preJumpY1
        else:
            if jumpCount1 >= -9:
                p1y -= (jumpCount1 * abs(jumpCount1)) * 0.9
                jumpCount1 -= 1
            else:
                isJump1 = False
                jumpCount1 = 9
    # Jump mechanics player 2
    if isJump2:
        if frozen2:
            isJump2 = False
            p2y = preJumpY2
        else:
            if jumpCount2 >= -9:
                p2y -= (jumpCount2 * abs(jumpCount2)) * 0.9
                jumpCount2 -= 1
            else:
                isJump2 = False
                jumpCount2 = 9
    # Cancel Jump mechanics player 1
    if forceDown1:
        if frozen1:
            forceDown1 = False
            p1y = preJumpY1
        else:
            if p1y < preJumpY1 and p1y + forceConst > preJumpY1:
                forceDiff1 = (forceConst + p1y) - preJumpY1
                p1y += forceConst - forceDiff1
            elif p1y < preJumpY1:
                p1y += forceConst
            else:
                forceDown1 = False
    # Cancel Jump mechanics player 2
    if forceDown2:
        if frozen2:
            forceDown2 = False
            p2y = preJumpY2
        else:
            if p2y < preJumpY2 and p2y + forceConst > preJumpY2:
                forceDiff2 = (forceConst + p2y) - preJumpY2
                p2y += forceConst - forceDiff2
            elif p2y < preJumpY2:
                p2y += forceConst
            else:
                forceDown2 = False

    # Spell shoot mechanics Player 1
    if spell1P1Fire:
        if spell1P1Right:
            if s1p1x + spellWidth < SCREEN_WIDTH:
                s1p1x += spellVel
            else:
                spell1P1Fire = False
                s1p1y = 0
        elif spell1P1Left:
            if s1p1x > 0:
                s1p1x -= spellVel
            else:
                spell1P1Fire = False
                s1p1y = 0
    if spell2P1Fire:
        if spell2P1Right:
            if s2p1x + spellWidth < SCREEN_WIDTH:
                s2p1x += spellVel
            else:
                spell2P1Fire = False
                s2p1y = 0
        elif spell2P1Left:
            if s2p1x > 0:
                s2p1x -= spellVel
            else:
                spell2P1Fire = False
                s2p1y = 0
    if spell3P1Fire:
        if spell3P1Right:
            if s3p1x + spellWidth < SCREEN_WIDTH:
                s3p1x += spellVel
            else:
                spell3P1Fire = False
                s3p1y = 0
        elif spell3P1Left:
            if s3p1x > 0:
                s3p1x -= spellVel
            else:
                spell3P1Fire = False
                s3p1y = 0

    # Spell shoot mechanics Player 2
    if spell1P2Fire:
        if spell1P2Left:
            if s1p2x > 0:
                s1p2x -= spellVel
            else:
                spell1P2Fire = False
                s1p2y = 0
        elif spell1P2Right:
            if s1p2x + spellWidth < SCREEN_WIDTH:
                s1p2x += spellVel
            else:
                spell1P2Fire = False
                s1p2y = 0
    if spell2P2Fire:
        if spell2P2Left:
            if s2p2x > 0:
                s2p2x -= spellVel
            else:
                spell2P2Fire = False
                s2p2y = 0
        elif spell2P2Right:
            if s2p2x + spellWidth < SCREEN_WIDTH:
                s2p2x += spellVel
            else:
                spell2P2Fire = False
                s2p2y = 0
    if spell3P2Fire:
        if spell3P2Left:
            if s3p2x > 0:
                s3p2x -= spellVel
            else:
                spell3P2Fire = False
                s3p2y = 0
        elif spell3P2Right:
            if s3p2x + spellWidth < SCREEN_WIDTH:
                s3p2x += spellVel
            else:
                spell3P2Fire = False
                s3p2y = 0
    # Return to menu after game is over
    if keys[pygame.K_ESCAPE] and GameOver:
        onMenu = True
        onMatchScreen = False
        GameOver = False
    for event in pygame.event.get():
        # Checks for mouse hover position
        x, y = pygame.mouse.get_pos()
        if onMenu and 178 >= x >= 50 and 92 >= y >= 42:
            hoverOverHTP = True
        elif onMenu:
            hoverOverHTP = False
        if onHowToPlay and 1050 >= x >= 1050-128 and 92 >= y >= 42:
            hoverOverBack = True
        elif onHowToPlay:
            hoverOverBack = False
        if onMenu and 675 >= x >= 425 and 425 >= y >= 325:
            hoverOverStart = True
        elif onMenu:
            hoverOverStart = False
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            # Shoot spell player 1
            if event.key == pygame.K_f and onMatchScreen and not GameOver and gameStart:
                # Spell 1
                if spell1P1 and not spell1P1Fire and not frozen1:
                    spellSound.play()
                    if right1:
                        spell1P1Right = True
                        spell1P1Left = False
                    elif left1:
                        spell1P1Left = True
                        spell1P1Right = False
                    spell1P1Fire = True
                    s1p1x = p1x + (PLAYER_WIDTH / 2)
                    s1p1y = p1y + (PLAYER_HEIGHT / 2)
                # Spell 2
                elif spell2P1 and not spell2P1Fire and not frozen1 and not frozen2:
                    iceSound.play()
                    if right1:
                        spell2P1Right = True
                        spell2P1Left = False
                    elif left1:
                        spell2P1Left = True
                        spell2P1Right = False
                    spell2P1Fire = True
                    s2p1x = p1x + (PLAYER_WIDTH / 2)
                    s2p1y = p1y + (PLAYER_HEIGHT / 2)
                # Spell 3
                elif spell3P1 and not spell3P1Fire and not frozen1 and not fire2:
                    fireSound.play()
                    if right1:
                        spell3P1Right = True
                        spell3P1Left = False
                    elif left1:
                        spell3P1Left = True
                        spell3P1Right = False
                    spell3P1Fire = True
                    s3p1x = p1x + (PLAYER_WIDTH / 2)
                    s3p1y = p1y + (PLAYER_HEIGHT / 2)
            # Shoot spell player 2
            if event.key == pygame.K_RSHIFT and onMatchScreen and not GameOver and gameStart:
                # Spell 1
                if spell1P2 and not spell1P2Fire and not frozen2:
                    spellSound.play()
                    if right2:
                        spell1P2Right = True
                        spell1P2Left = False
                    elif left2:
                        spell1P2Left = True
                        spell1P2Right = False
                    spell1P2Fire = True
                    s1p2x = p2x + (PLAYER_WIDTH / 2)
                    s1p2y = p2y + (PLAYER_HEIGHT / 2)
                # Spell 2
                elif spell2P2 and not spell2P2Fire and not frozen2 and not frozen1:
                    iceSound.play()
                    if right2:
                        spell2P2Right = True
                        spell2P2Left = False
                    elif left2:
                        spell2P2Left = True
                        spell2P2Right = False
                    spell2P2Fire = True
                    s2p2x = p2x + (PLAYER_WIDTH / 2)
                    s2p2y = p2y + (PLAYER_HEIGHT / 2)
                # Spell 3
                elif spell3P2 and not spell3P2Fire and not frozen2 and not fire1:
                    fireSound.play()
                    if right2:
                        spell3P2Right = True
                        spell3P2Left = False
                    elif left2:
                        spell3P2Left = True
                        spell3P2Right = False
                    spell3P2Fire = True
                    s3p2x = p2x + (PLAYER_WIDTH / 2)
                    s3p2y = p2y + (PLAYER_HEIGHT / 2)
        if event.type == pygame.MOUSEBUTTONDOWN:
            xPress, yPress = pygame.mouse.get_pos()
            # Back button on HTP screen
            if onHowToPlay:
                if 1050 >= xPress >= 1050-128 and 92 >= yPress >= 42:
                    hoverOverBack = False
                    onHowToPlay = False
                    onMenu = True
            # Buttons on menu screen
            if onMenu:
                # HTP Button
                if 178 >= xPress >= 50 and 92 >= yPress >= 42:
                    hoverOverHTP = False
                    onMenu = False
                    onHowToPlay = True
                # Start Button
                if 675 >= xPress >= 425 and 425 >= yPress >= 325:
                    onMenu = False
                    onMatchScreen = True
                    hoverOverStart = False
                # Character selection buttons below
                if 105 >= xPress >= 55 and 480 >= yPress >= 430 and not char1P2:
                    buttonSound.play()
                    char1P1 = False
                    char2P1 = False
                    char3P1 = False
                    char4P1 = False
                    char5P1 = False
                    char6P1 = False
                    char7P1 = False
                    char8P1 = False
                    char1P1 = True
                if 175 >= xPress >= 125 and 480 >= yPress >= 430 and not char2P2:
                    buttonSound.play()
                    char1P1 = False
                    char2P1 = False
                    char3P1 = False
                    char4P1 = False
                    char5P1 = False
                    char6P1 = False
                    char7P1 = False
                    char8P1 = False
                    char2P1 = True
                if 235 >= xPress >= 195 and 480 >= yPress >= 430 and not char3P2:
                    buttonSound.play()
                    char1P1 = False
                    char2P1 = False
                    char3P1 = False
                    char4P1 = False
                    char5P1 = False
                    char6P1 = False
                    char7P1 = False
                    char8P1 = False
                    char3P1 = True
                if 305 >= xPress >= 265 and 480 >= yPress >= 430 and not char4P2:
                    buttonSound.play()
                    char1P1 = False
                    char2P1 = False
                    char3P1 = False
                    char4P1 = False
                    char5P1 = False
                    char6P1 = False
                    char7P1 = False
                    char8P1 = False
                    char4P1 = True
                if 105 >= xPress >= 55 and 550 >= yPress >= 500 and not char5P2:
                    buttonSound.play()
                    char1P1 = False
                    char2P1 = False
                    char3P1 = False
                    char4P1 = False
                    char5P1 = False
                    char6P1 = False
                    char7P1 = False
                    char8P1 = False
                    char5P1 = True
                if 175 >= xPress >= 125 and 550 >= yPress >= 500 and not char6P2:
                    buttonSound.play()
                    char1P1 = False
                    char2P1 = False
                    char3P1 = False
                    char4P1 = False
                    char5P1 = False
                    char6P1 = False
                    char7P1 = False
                    char8P1 = False
                    char6P1 = True
                if 235 >= xPress >= 195 and 550 >= yPress >= 500 and not char7P2:
                    buttonSound.play()
                    char1P1 = False
                    char2P1 = False
                    char3P1 = False
                    char4P1 = False
                    char5P1 = False
                    char6P1 = False
                    char7P1 = False
                    char8P1 = False
                    char7P1 = True
                if 315 >= xPress >= 265 and 550 >= yPress >= 500 and not char8P2:
                    buttonSound.play()
                    char1P1 = False
                    char2P1 = False
                    char3P1 = False
                    char4P1 = False
                    char5P1 = False
                    char6P1 = False
                    char7P1 = False
                    char8P1 = False
                    char8P1 = True

                if 835 >= xPress >= 785 and 480 >= yPress >= 430 and not char1P1:
                    buttonSound.play()
                    char1P2 = False
                    char2P2 = False
                    char3P2 = False
                    char4P2 = False
                    char5P2 = False
                    char6P2 = False
                    char7P2 = False
                    char8P2 = False
                    char1P2 = True
                if 905 >= xPress >= 855 and 480 >= yPress >= 430 and not char2P1:
                    buttonSound.play()
                    char1P2 = False
                    char2P2 = False
                    char3P2 = False
                    char4P2 = False
                    char5P2 = False
                    char6P2 = False
                    char7P2 = False
                    char8P2 = False
                    char2P2 = True
                if 975 >= xPress >= 925 and 480 >= yPress >= 430 and not char3P1:
                    buttonSound.play()
                    char1P2 = False
                    char2P2 = False
                    char3P2 = False
                    char4P2 = False
                    char5P2 = False
                    char6P2 = False
                    char7P2 = False
                    char8P2 = False
                    char3P2 = True
                if 1045 >= xPress >= 995 and 480 >= yPress >= 430 and not char4P1:
                    buttonSound.play()
                    char1P2 = False
                    char2P2 = False
                    char3P2 = False
                    char4P2 = False
                    char5P2 = False
                    char6P2 = False
                    char7P2 = False
                    char8P2 = False
                    char4P2 = True
                if 835 >= xPress >= 785 and 550 >= yPress >= 500 and not char5P1:
                    buttonSound.play()
                    char1P2 = False
                    char2P2 = False
                    char3P2 = False
                    char4P2 = False
                    char5P2 = False
                    char6P2 = False
                    char7P2 = False
                    char8P2 = False
                    char5P2 = True
                if 905 >= xPress >= 855 and 550 >= yPress >= 500 and not char6P1:
                    buttonSound.play()
                    char1P2 = False
                    char2P2 = False
                    char3P2 = False
                    char4P2 = False
                    char5P2 = False
                    char6P2 = False
                    char7P2 = False
                    char8P2 = False
                    char6P2 = True
                if 975 >= xPress >= 925 and 550 >= yPress >= 500 and not char7P1:
                    buttonSound.play()
                    char1P2 = False
                    char2P2 = False
                    char3P2 = False
                    char4P2 = False
                    char5P2 = False
                    char6P2 = False
                    char7P2 = False
                    char8P2 = False
                    char7P2 = True
                if 1045 >= xPress >= 995 and 550 >= yPress >= 500 and not char8P1:
                    buttonSound.play()
                    char1P2 = False
                    char2P2 = False
                    char3P2 = False
                    char4P2 = False
                    char5P2 = False
                    char6P2 = False
                    char7P2 = False
                    char8P2 = False
                    char8P2 = True
    # On menu screen
    if onMenu:
        trophyAwarded = False
        loadGameMusic = False
        loadWinMusic = False
        if not loadMenuMusic:
            pygame.mixer.stop()
            pygame.mixer.music.load("Sounds/Harry_Potter_Theme_Song_Hedwigs_Theme.ogg")
            pygame.mixer.music.play(-1, 82.5)
            pygame.mixer.music.set_volume(0.5)
            loadMenuMusic = True
        win.blit(menubg, (0, 0))
        pygame.draw.rect(win, (165, 137, 96), (849, 340, 134, 32))
        pygame.draw.rect(win, (165, 137, 96), (771, 370, 300, 31))
        pygame.draw.rect(win, (165, 137, 96), (116, 340, 136, 32))
        pygame.draw.rect(win, (165, 137, 96), (33, 370, 300, 31))
        pygame.draw.rect(win, BLACK, (420, 320, 260, 110))
        if hoverOverStart:
            pygame.draw.rect(win, (205, 180, 18), (425, 325, 250, 100))
        else:
            pygame.draw.rect(win, GOLD, (425, 325, 250, 100))
        pygame.draw.rect(win, BLACK, (285, 190, 510, 110))
        pygame.draw.rect(win, (200, 200, 200), (290, 195, 500, 100))
        titleFont1 = titleFont.render("Potter Duel", False, BLACK)
        pSelect = selectFont.render("Player 1", False, (40, 30, 3))
        win.blit(pSelect, (123, 335))
        pSelect1 = selectFont.render("Character Selection", False, (40, 30, 3))
        win.blit(pSelect1, (32, 370))
        p2Select = selectFont.render("Player 2", False, (40, 30, 3))
        win.blit(p2Select, (853, 335))
        win.blit(pSelect1, (772, 370))
        win.blit(titleFont1, (332, 190))
        startFont = testFont.render("Start", False, (90, 90, 90))
        win.blit(startFont, (475, 333))
        p1x = 170
        p1y = 425
        preJumpY1 = p1y
        p2x = 820
        p2y = 425
        preJumpY2 = p2y
        hp1 = 100
        hp2 = 100
        gameStart = False
        useGameStartTimer = False
        if not hoverOverHTP:
            pygame.draw.rect(win, (165, 137, 96), (50, 42, 128, 50))
        else:
            pygame.draw.rect(win, (122, 100, 70), (50, 42, 128, 50))
        htpH = howtoplayfont.render("How", False, WHITE)
        win.blit(htpH, (95, 42))
        htpT = howtoplayfont.render("to", False, WHITE)
        win.blit(htpT, (105, 55))
        htpP = howtoplayfont.render("Play", False, WHITE)
        win.blit(htpP, (97, 68))
        if char1P1:
            pygame.draw.rect(win, (101, 77, 42), (51, 426, 58, 58))
        if char2P1:
            pygame.draw.rect(win, (101, 77, 42), (121, 426, 58, 58))
        if char3P1:
            pygame.draw.rect(win, (101, 77, 42), (191, 426, 58, 58))
        if char4P1:
            pygame.draw.rect(win, (101, 77, 42), (261, 426, 58, 58))
        if char5P1:
            pygame.draw.rect(win, (101, 77, 42), (51, 496, 58, 58))
        if char6P1:
            pygame.draw.rect(win, (101, 77, 42), (121, 496, 58, 58))
        if char7P1:
            pygame.draw.rect(win, (101, 77, 42), (191, 496, 58, 58))
        if char8P1:
            pygame.draw.rect(win, (101, 77, 42), (261, 496, 58, 58))

        if char4P2:
            pygame.draw.rect(win, (101, 77, 42), (991, 426, 58, 58))
        if char3P2:
            pygame.draw.rect(win, (101, 77, 42), (921, 426, 58, 58))
        if char2P2:
            pygame.draw.rect(win, (101, 77, 42), (851, 426, 58, 58))
        if char1P2:
            pygame.draw.rect(win, (101, 77, 42), (781, 426, 58, 58))
        if char8P2:
            pygame.draw.rect(win, (101, 77, 42), (991, 496, 58, 58))
        if char7P2:
            pygame.draw.rect(win, (101, 77, 42), (921, 496, 58, 58))
        if char6P2:
            pygame.draw.rect(win, (101, 77, 42), (851, 496, 58, 58))
        if char5P2:
            pygame.draw.rect(win, (101, 77, 42), (781, 496, 58, 58))

        for i in range(0, 4):
            pygame.draw.rect(win, (165, 137, 96), (55+i*70, 430, 50, 50))
            pygame.draw.rect(win, (165, 137, 96), (55+i*70, 500, 50, 50))
            pygame.draw.rect(win, (165, 137, 96), (785+i*70, 430, 50, 50))
            pygame.draw.rect(win, (165, 137, 96), (785+i*70, 500, 50, 50))

        win.blit(smallSheet, (58, 428), (5, 71, 43, 52))
        win.blit(smallSheet, (788, 428), (5, 71, 43, 52))
        win.blit(smallSheet, (129, 428), (53, 71, 43, 52))
        win.blit(smallSheet, (859, 428), (53, 71, 43, 52))
        win.blit(smallSheet, (198, 428), (5, 313, 43, 52))
        win.blit(smallSheet, (928, 428), (5, 313, 43, 52))
        win.blit(smallSheet, (269, 428), (53, 313, 43, 52))
        win.blit(smallSheet, (999, 428), (53, 313, 43, 52))

        win.blit(smallSheet, (58, 498), (238, 71, 43, 52))
        win.blit(smallSheet, (788, 498), (238, 71, 43, 52))
        win.blit(smallSheet, (129, 498), (192, 71, 43, 52))
        win.blit(smallSheet, (859, 498), (192, 71, 43, 52))
        win.blit(smallSheet, (198, 498), (145, 374, 43, 52))
        win.blit(smallSheet, (928, 498), (145, 374, 43, 52))
        win.blit(smallSheet, (269, 498), (192, 132, 43, 52))
        win.blit(smallSheet, (999, 498), (192, 132, 43, 52))
        right1 = True
        left2 = True

    if beginMatch:
        pygame.draw.rect(win, BLACK, (10, 10, 10, 10))
    if onHowToPlay:
        win.blit(htpbg, (0, 0))
        if not hoverOverBack:
            pygame.draw.rect(win, (165, 137, 96), (1050-128, 42, 128, 50))
        else:
            pygame.draw.rect(win, (122, 100, 70), (1050-128, 42, 128, 50))
        back = backFont.render("Back", False, WHITE)
        win.blit(back, (955, 48))
        p1HTP = backFont.render("Player 1", False, (67, 52, 32))
        win.blit(p1HTP, (230, 250))
        p2HTP = backFont.render("Player 2", False, (67, 52, 32))
        win.blit(p2HTP, (780, 250))
        howtoplay = titleFont.render("How to Play", False, (67, 52, 32))
        win.blit(howtoplay, (280, 10))
        win.blit(keyboard, (25, 290))
        win.blit(keyboard, (575, 290))
        pygame.draw.rect(win, (2, 68, 9), (280, 115, 140, 70))
        pygame.draw.rect(win, (117, 0, 0), (425, 115, 140, 70))
        pygame.draw.rect(win, BLACK, (570, 115, 140, 70))
        pygame.draw.rect(win, (2, 68, 9), (121, 373, 26, 23))
        pygame.draw.rect(win, (2, 68, 9), (98, 401, 26, 23))
        pygame.draw.rect(win, (2, 68, 9), (129, 402, 26, 23))
        pygame.draw.rect(win, (2, 68, 9), (163, 402, 26, 23))
        pygame.draw.rect(win, (2, 68, 9), (1005, 458, 27, 13))
        pygame.draw.rect(win, (2, 68, 9), (1006, 472, 27, 13))
        pygame.draw.rect(win, (2, 68, 9), (974, 472, 27, 13))
        pygame.draw.rect(win, (2, 68, 9), (1038, 472, 27, 13))
        pygame.draw.rect(win, (117, 0, 0), (196, 402, 25, 22))
        pygame.draw.rect(win, (117, 0, 0), (999, 429, 66, 24))
        pygame.draw.rect(win, BLACK, (70, 345, 25, 21))
        pygame.draw.rect(win, BLACK, (104, 345, 25, 21))
        pygame.draw.rect(win, BLACK, (138, 345, 25, 21))
        pygame.draw.rect(win, BLACK, (939, 459, 26, 25))
        pygame.draw.rect(win, BLACK, (931, 430, 25, 21))
        pygame.draw.rect(win, BLACK, (964, 431, 25, 21))
        w = howtoplayfont.render('W', False, WHITE)
        win.blit(w, (124, 373))
        a = howtoplayfont.render('A', False, WHITE)
        win.blit(a, (104, 401))
        s = howtoplayfont.render('S', False, WHITE)
        win.blit(s, (135, 402))
        d = howtoplayfont.render('D', False, WHITE)
        win.blit(d, (169, 402))
        f = howtoplayfont.render('F', False, WHITE)
        win.blit(f, (202, 402))
        o = howtoplayfont.render('1', False, WHITE)
        win.blit(o, (76, 345))
        tw = howtoplayfont.render('2', False, WHITE)
        win.blit(tw, (109, 345))
        th = howtoplayfont.render('3', False, WHITE)
        win.blit(th, (144, 345))
        up = howtoplayfont.render('^', False, WHITE)
        win.blit(up, (1014, 457))
        left = howtoplayfont.render('<-', False, WHITE)
        win.blit(left, (978, 468))
        down = howtoplayfont.render('v', False, WHITE)
        win.blit(down, (1014, 465))
        right = howtoplayfont.render('->', False, WHITE)
        win.blit(right, (1042, 468))
        shift = howtoplayfont.render('shift', False, WHITE)
        win.blit(shift, (1013, 429))
        ctrl = howtoplayfont.render('ctrl', False, WHITE)
        win.blit(ctrl, (939, 459))
        dot = howtoplayfont.render('>', False, WHITE)
        win.blit(dot, (936, 430))
        slash = howtoplayfont.render('?', False, WHITE)
        win.blit(slash, (969, 431))
        cm = howtoplayfont.render("Character", False, WHITE)
        win.blit(cm, (305, 125))
        cm = howtoplayfont.render("Movement", False, WHITE)
        win.blit(cm, (305, 150))
        cm = howtoplayfont.render("Shoot", False, WHITE)
        win.blit(cm, (470, 125))
        cm = howtoplayfont.render("Spell", False, WHITE)
        win.blit(cm, (470, 150))
        cm = howtoplayfont.render("Select", False, WHITE)
        win.blit(cm, (615, 125))
        cm = howtoplayfont.render("Spell", False, WHITE)
        win.blit(cm, (615, 150))

    if onMatchScreen:
        if not loadGameMusic and not GameOver:
            loadMenuMusic = False
            loadWinMusic = False
            pygame.mixer.stop()
            pygame.mixer.music.load("Sounds/fight.mp3")
            pygame.mixer.music.play(-1, 68)
            pygame.mixer.music.set_volume(0.3)
            loadGameMusic = True
        if not loadWinMusic and GameOver:
            loadGameMusic = False
            loadMenuMusic = False
            pygame.mixer.stop()
            pygame.mixer.music.load("Sounds/win.mp3")
            pygame.mixer.music.play(-1, 12)
            loadWinMusic = True
        win.blit(bg, (0, 0))
        p1Font = escFont.render("Player 1", False, WHITE)
        if not gameStart and useGameStartTimer:
            timeFont = titleFont.render(str(int(timeElapsedStart)), False, WHITE)
            duelFont = titleFont.render("DUEL!", False, RED)
            if int(timeElapsedStart) >= 1:
                win.blit(timeFont, (520, 200))
            elif 0.9 > timeElapsedStart > 0.1:
                win.blit(duelFont, (410, 200))
        p2Font = escFont.render("Player 2", False, WHITE)
        win.blit(p1Font, (110, 6))
        win.blit(p2Font, (750, 6))
        # Health Bars
        if shieldInInv1:
            pygame.draw.rect(win, GOLD, (76, 26, 308, 38))
        if shieldInInv2:
            pygame.draw.rect(win, GOLD, (716, 26, 308, 38))
        pygame.draw.rect(win, RED, (80, 30, 300, 30))
        pygame.draw.rect(win, RED, (720, 30, 300, 30))
        if hp1 > 0:
            pygame.draw.rect(win, GREEN, (80, 30, hp1*3, 30))
        if hp2 > 0:
            pygame.draw.rect(win, GREEN, (720+(300-(hp2*3)), 30, hp2*3, 30))
        # Selected Spells
        if spell1P1:
            pygame.draw.rect(win, WHITE, (119, 79, 49, 49))
        if spell2P1:
            pygame.draw.rect(win, WHITE, (206, 79, 49, 49))
        if spell3P1:
            pygame.draw.rect(win, WHITE, (291, 79, 49, 49))
        if spell1P2:
            pygame.draw.rect(win, WHITE, (759, 79, 49, 49))
        if spell2P2:
            pygame.draw.rect(win, WHITE, (759+87, 79, 49, 49))
        if spell3P2:
            pygame.draw.rect(win, WHITE, (758+87+87, 79, 49, 49))
        win.blit(icon1, (121, 81), (0, 0, 45, 45))
        win.blit(icon2, (208, 81), (0, 0, 45, 45))
        win.blit(icon3, (293, 81), (2, 2, 45, 45))
        win.blit(icon1, (761, 81), (0, 0, 45, 45))
        win.blit(icon2, (759+87+2, 81), (0, 0, 45, 45))
        win.blit(icon3, (759+87+86+2, 81), (2, 2, 45, 45))
        if not GameOver and not useGameStartTimer:
            if not healthPackOnMap:
                if pygame.time.get_ticks() % 50 == 0:
                    healthPackOnMap = True
            if healthPackOnMap:
                if hpy < 499:
                    hpy += 10
                win.blit(hpack, (hpx, hpy))
        if not GameOver and not useGameStartTimer:
            if not shieldOnMap and not shieldInInv1 and not shieldInInv2:
                if pygame.time.get_ticks() % 100 == 0:
                    shieldOnMap = True
            if shieldOnMap:
                if shieldy < 499:
                    shieldy += 8
                win.blit(shield, (shieldx, shieldy))
        # Draw Player 1
        if hp1 > 0:
            if right1:
                if frozen1:
                    pygame.draw.rect(win, (145, 212, 255), (p1x-1, p1y-1, PLAYER_WIDTH+2, PLAYER_HEIGHT+2))
                if fire1:
                    if pygame.time.get_ticks() % 3 == 0:
                        pygame.draw.rect(win, RED, (p1x - 1, p1y - 1, PLAYER_WIDTH + 2, PLAYER_HEIGHT + 2))
                win.blit(sheet, (p1x, p1y), (drawP1x, drawP1y, PLAYER_WIDTH, PLAYER_HEIGHT))
            elif left1:
                if frozen1:
                    pygame.draw.rect(win, (145, 212, 255), (p1x-1, p1y-1, PLAYER_WIDTH+2, PLAYER_HEIGHT+2))
                if fire1:
                    if pygame.time.get_ticks() % 3 == 0:
                        pygame.draw.rect(win, RED, (p1x - 1, p1y - 1, PLAYER_WIDTH + 2, PLAYER_HEIGHT + 2))
                win.blit(sheet1, (p1x, p1y), (drawP1x, drawP1y, PLAYER_WIDTH, PLAYER_HEIGHT))
        elif hp1 <= 0 and hp2 <= 0:
            drawFont = testFont.render("It's a Draw!", False, BLACK)
            drawFont1 = testFont.render("It's a Draw!", False, GOLD)
            if pygame.time.get_ticks() % 3 == 0:
                win.blit(drawFont, (365, 200))
            else:
                win.blit(drawFont1, (365, 200))
            GameOver = True
            pygame.draw.rect(win, (140, 140, 140), (435, 290, 210, 30))
            escape = escFont.render("Press 'Esc' to Return", False, BLACK)
            win.blit(escape, (465, 295))
        else:
            GameOver = True
            if right2 and GameOver:
                win.blit(sheet, (p2x, p2y), (drawP2x, drawP2y, PLAYER_WIDTH, PLAYER_HEIGHT))
            elif left2 and GameOver:
                win.blit(sheet1, (p2x, p2y), (drawP2x, drawP2y, PLAYER_WIDTH, PLAYER_HEIGHT))
            P2WinBlack = testFont.render("Player 2 Wins!", False, BLACK)
            P2WinGold = testFont.render("Player 2 Wins!", False, GOLD)
            if pygame.time.get_ticks() % 3 == 0:
                win.blit(P2WinBlack, (350, 200))
            else:
                win.blit(P2WinGold, (350, 200))
            pygame.draw.rect(win, (140, 140, 140), (435, 290, 210, 30))
            escape = escFont.render("Press 'Esc' to Return", False, BLACK)
            win.blit(escape, (465, 295))
        # Draw Player 2
        if hp2 > 0:
            if right2 and not GameOver:
                if frozen2:
                    pygame.draw.rect(win, (145, 212, 255), (p2x-1, p2y-1, PLAYER_WIDTH+2, PLAYER_HEIGHT+2))
                if fire2:
                    if pygame.time.get_ticks() % 3 == 0:
                        pygame.draw.rect(win, RED, (p2x-1, p2y-1, PLAYER_WIDTH+2, PLAYER_HEIGHT+2))
                win.blit(sheet, (p2x, p2y), (drawP2x, drawP2y, PLAYER_WIDTH, PLAYER_HEIGHT))
            elif left2 and not GameOver:
                if frozen2:
                    pygame.draw.rect(win, (145, 212, 255), (p2x-1, p2y-1, PLAYER_WIDTH+2, PLAYER_HEIGHT+2))
                if fire2:
                    if pygame.time.get_ticks() % 3 == 0:
                        pygame.draw.rect(win, RED, (p2x-1, p2y-1, PLAYER_WIDTH+2, PLAYER_HEIGHT+2))
                win.blit(sheet1, (p2x, p2y), (drawP2x, drawP2y, PLAYER_WIDTH, PLAYER_HEIGHT))
            if right2 and useGameStartTimer:
                right2 = False
                left2 = True
        elif hp2 <= 0 and hp1 <= 0:
            drawFont = testFont.render("It's a Draw!", False, BLACK)
            drawFont1 = testFont.render("It's a Draw!", False, GOLD)
            if pygame.time.get_ticks() % 3 == 0:
                win.blit(drawFont, (365, 200))
            else:
                win.blit(drawFont1, (365, 200))
            GameOver = True
            pygame.draw.rect(win, (140, 140, 140), (435, 290, 210, 30))
            escape = escFont.render("Press 'Esc' to Return", False, BLACK)
            win.blit(escape, (465, 295))
        else:
            P1WinBlack = testFont.render("Player 1 Wins!", False, BLACK)
            P1WinGold = testFont.render("Player 1 Wins!", False, GOLD)
            if pygame.time.get_ticks() % 3 == 0:
                win.blit(P1WinBlack, (350, 200))
            else:
                win.blit(P1WinGold, (350, 200))
            pygame.draw.rect(win, (140, 140, 140), (435, 290, 210, 30))
            escape = escFont.render("Press 'Esc' to Return", False, BLACK)
            win.blit(escape, (465, 295))
            GameOver = True
        if GameOver:
            if onMatchScreen:
                # Award trophies
                if hp1 > 0 and not trophyAwarded and onMatchScreen:
                    trophyCount = getTrophyPlus(trophyCount1, trophyCount2)
                    trophyCount1 += trophyCount
                    if trophyCount > trophyCount2:
                        tempCount = trophyCount2
                        trophyCount2 = 0
                    else:
                        tempCount = trophyCount
                        trophyCount2 -= trophyCount
                    trophyAwarded = True
                elif hp2 > 0 and not trophyAwarded and onMatchScreen:
                    trophyCount = getTrophyPlus(trophyCount2, trophyCount1)
                    trophyCount2 += trophyCount
                    if trophyCount > trophyCount1:
                        tempCount = trophyCount1
                        trophyCount1 = 0
                    else:
                        tempCount = trophyCount
                        trophyCount1 -= trophyCount
                    trophyAwarded = True
                elif hp2 <= 0 and hp1 <= 0:
                    trophyAwarded = True
                # Show trophy count
                text_width, text_height = selectFont.size("Total: " + str(int(trophyCount1)))
                pygame.draw.rect(win, (104, 62, 0), (300, 350, text_width, text_height))
                text_width, text_height = selectFont.size("Total: " + str(int(trophyCount2)))
                pygame.draw.rect(win, (104, 62, 0), (670, 350, text_width, text_height))
                if hp1 > 0 >= hp2:
                    plusT = selectFont.render("+" + str(trophyCount), False, GOLD)
                    text_width, text_height = selectFont.size("+" + str(trophyCount))
                    pygame.draw.rect(win, (104, 62, 0), (320, 300, text_width, text_height))
                    win.blit(plusT, (320, 300))
                    minusT = selectFont.render("-" + str(int(tempCount)), False, GOLD)
                    text_width, text_height = selectFont.size("-" + str(int(tempCount)))
                    pygame.draw.rect(win, (104, 62, 0), (690, 300, text_width, text_height))
                    win.blit(minusT, (690, 300))
                elif hp2 > 0 >= hp1:
                    plusT = selectFont.render("+" + str(trophyCount), False, GOLD)
                    text_width, text_height = selectFont.size("+" + str(trophyCount))
                    pygame.draw.rect(win, (104, 62, 0), (690, 300, text_width, text_height))
                    win.blit(plusT, (690, 300))
                    minusT = selectFont.render("-" + str(int(tempCount)), False, GOLD)
                    text_width, text_height = selectFont.size("-" + str(int(tempCount)))
                    pygame.draw.rect(win, (104, 62, 0), (320, 300, text_width, text_height))
                    win.blit(minusT, (320, 300))
                p1Trophy = selectFont.render("Total: " + str(int(trophyCount1)), False, GOLD)
                win.blit(p1Trophy, (300, 350))
                p2Trophy = selectFont.render("Total: " + str(int(trophyCount2)), False, GOLD)
                win.blit(p2Trophy, (670, 350))
            # Reset everything
            shieldOnMap = False
            healthPackOnMap = False
            hpx = random.randint(0, 1050)
            shieldx = random.randint(0, 1050)
            hpy = 50
            shieldy = 50
            fire1 = False
            frozen1 = False
            fire2 = False
            frozen2 = False
            s1p1x = 0
            s2p1x = 0
            s3p1x = 0
            s1p2x = 0
            s2p2x = 0
            s3p2x = 0
            s1p1y = 0
            s2p1y = 0
            s3p1y = 0
            s1p2y = 0
            s2p2y = 0
            s3p2y = 0
            spell1P1 = True
            spell1P2 = True
            spell2P1 = False
            spell2P2 = False
            spell3P1 = False
            spell3P2 = False

        # Draw Spells
        if spell1P1Fire:
            win.blit(greenspell, (s1p1x, s1p1y))
        if spell2P1Fire:
            win.blit(bluespellR, (s2p1x, s2p1y))
        if spell3P1Fire:
            win.blit(redspell, (s3p1x, s3p1y))
        if spell1P2Fire:
            win.blit(greenspell, (s1p2x, s1p2y))
        if spell2P2Fire:
            win.blit(bluespellL, (s2p2x, s2p2y))
        if spell3P2Fire:
            win.blit(redspell, (s3p2x, s3p2y))

        # Shield Collisions
        if getCollision(shieldx, shieldy, p1x, p1y, 50, PLAYER_WIDTH, 50, PLAYER_HEIGHT) and getCollision(shieldx, shieldy, p2x, p2y, 50, PLAYER_WIDTH, 50, PLAYER_HEIGHT):
            shieldOnMap = False
            shieldx = random.randint(0, 1050)
            shieldy = 50
        elif getCollision(shieldx, shieldy, p1x, p1y, 50, PLAYER_WIDTH, 50, PLAYER_HEIGHT) and not GameOver:
            shieldUp.play()
            shieldOnMap = False
            shieldInInv1 = True
            shieldx = random.randint(0, 1050)
            shieldy = 50
        elif getCollision(shieldx, shieldy, p2x, p2y, 50, PLAYER_WIDTH, 50, PLAYER_HEIGHT) and not GameOver:
            shieldUp.play()
            shieldOnMap = False
            shieldInInv2 = True
            shieldx = random.randint(0, 1050)
            shieldy = 50

        # Health Pack Collisions
        if getCollision(hpx, hpy, p1x, p1y, 50, PLAYER_WIDTH, 50, PLAYER_HEIGHT) and getCollision(hpx, hpy, p2x, p2y, 50, PLAYER_WIDTH, 50, PLAYER_HEIGHT) and hp1 != 100 and hp2 != 100:
            healthPackOnMap = False
            hpx = random.randint(0, 1050)
            hpy = 50
        elif getCollision(hpx, hpy, p1x, p1y, 50, PLAYER_WIDTH, 50, PLAYER_HEIGHT) and hp1 != 100 and not GameOver:
            if 100 > hp1 > 85:
                healthSound.play()
                healthPackOnMap = False
                hp1 = 100
                hpx = random.randint(0,1050)
                hpy = 50
            elif 85 >= hp1 > 0:
                healthSound.play()
                healthPackOnMap = False
                hp1 += 15
                hpx = random.randint(0,1050)
                hpy = 50
        elif getCollision(hpx, hpy, p2x, p2y, 50, PLAYER_WIDTH, 50, PLAYER_HEIGHT) and hp2 != 100 and not GameOver:
            if 100 > hp2 > 85:
                healthSound.play()
                healthPackOnMap = False
                hp2 = 100
                hpx = random.randint(0,1050)
                hpy = 50
            elif 85 >= hp2 > 0:
                healthSound.play()
                healthPackOnMap = False
                hp2 += 15
                hpx = random.randint(0,1050)
                hpy = 50

        # P1 to P2 Spell Collisions
        if getSpellCollision(s1p1x, p2x, s1p1y, p2y, spellWidth, PLAYER_WIDTH, PLAYER_HEIGHT):
            if shieldInInv2:
                shieldHit.play()
                spell1P1Fire = False
                s1p1x = 0
                s1p1y = 0
            else:
                hitSound.play()
                spell1P1Fire = False
                hp2 -= 10
                s1p1x = 0
                s1p1y = 0
        if getSpellCollision(s2p1x, p2x, s2p1y, p2y, spellWidth, PLAYER_WIDTH, PLAYER_HEIGHT):
            if shieldInInv2:
                shieldHit.play()
                spell2P1Fire = False
                s2p1x = 0
                s2p1y = 0
            else:
                hitSound.play()
                spell2P1Fire = False
                frozen2 = True
                hp2 -= 5
                s2p1x = 0
                s2p1y = 0
        if getSpellCollision(s3p1x, p2x, s3p1y, p2y, spellWidth, PLAYER_WIDTH, PLAYER_HEIGHT):
            if shieldInInv2:
                shieldHit.play()
                spell3P1Fire = False
                s3p1x = 0
                s3p1y = 0
            else:
                hitSound.play()
                spell3P1Fire = False
                fire2 = True
                s3p1x = 0
                s3p1y = 0

        # P2 to P1 Spell Collisions
        if getSpellCollision(s1p2x, p1x, s1p2y, p1y, spellWidth, PLAYER_WIDTH, PLAYER_HEIGHT):
            if shieldInInv1:
                shieldHit.play()
                spell1P2Fire = False
                s1p2x = 0
                s1p2y = 0
            else:
                hitSound.play()
                spell1P2Fire = False
                hp1 -= 10
                s1p2x = 0
                s1p2y = 0
        if getSpellCollision(s2p2x, p1x, s2p2y, p1y, spellWidth, PLAYER_WIDTH, PLAYER_HEIGHT):
            if shieldInInv1:
                shieldHit.play()
                spell2P2Fire = False
                s2p2x = 0
                s2p2y = 0
            else:
                hitSound.play()
                spell2P2Fire = False
                frozen1 = True
                hp1 -= 5
                s2p2x = 0
                s2p2y = 0
        if getSpellCollision(s3p2x, p1x, s3p2y, p1y, spellWidth, PLAYER_WIDTH, PLAYER_HEIGHT):
            if shieldInInv1:
                shieldHit.play()
                spell3P2Fire = False
                s3p2x = 0
                s3p2y = 0
            else:
                hitSound.play()
                spell3P2Fire = False
                fire1 = True
                s3p2x = 0
                s3p2y = 0

        # Spell on Spell collisions
        if getSpellCollision(s1p1x, s1p2x, s1p1y, s1p2y, spellWidth*2, spellWidth*2, spellWidth):
            spell1P1Fire = False
            s1p1x = 0
            s1p1y = 0
            s1p2x = 0
            s1p2y = 0
            spell1P2Fire = False
        if getSpellCollision(s1p1x, s2p2x, s1p1y, s2p2y, spellWidth*2, spellWidth*2, spellWidth):
            spell1P1Fire = False
            s1p1x = 0
            s1p1y = 0
            s2p2x = 0
            s2p2y = 0
            spell2P2Fire = False
        if getSpellCollision(s1p1x, s3p2x, s1p1y, s3p2y, spellWidth*2, spellWidth*2, spellWidth):
            spell1P1Fire = False
            s1p1x = 0
            s1p1y = 0
            s3p2x = 0
            s3p2y = 0
            spell1P3Fire = False
        if getSpellCollision(s2p1x, s1p2x, s2p1y, s1p2y, spellWidth*2, spellWidth*2, spellWidth):
            spell2P1Fire = False
            s2p1x = 0
            s2p1y = 0
            s1p2x = 0
            s1p2y = 0
            spell1P2Fire = False
        if getSpellCollision(s2p1x, s2p2x, s2p1y, s2p2y, spellWidth*2, spellWidth*2, spellWidth):
            spell2P1Fire = False
            s2p1x = 0
            s2p1y = 0
            s2p2x = 0
            s2p2y = 0
            spell2P2Fire = False
        if getSpellCollision(s2p1x, s3p2x, s2p1y, s3p2y, spellWidth*2, spellWidth*2, spellWidth):
            spell2P1Fire = False
            s2p1x = 0
            s2p1y = 0
            s3p2x = 0
            s3p2y = 0
            spell3P2Fire = False
        if getSpellCollision(s3p1x, s1p2x, s3p1y, s1p2y, spellWidth*2, spellWidth*2, spellWidth):
            spell3P1Fire = False
            s3p1x = 0
            s3p1y = 0
            s1p2x = 0
            s1p2y = 0
            spell1P2Fire = False
        if getSpellCollision(s3p1x, s2p2x, s3p1y, s2p2y, spellWidth*2, spellWidth*2, spellWidth):
            spell3P1Fire = False
            s3p1x = 0
            s3p1y = 0
            s2p2x = 0
            s2p2y = 0
            spell2P2Fire = False
        if getSpellCollision(s3p1x, s3p2x, s3p1y, s3p2y, spellWidth*2, spellWidth*2, spellWidth):
            spell3P1Fire = False
            s3p1x = 0
            s3p1y = 0
            s3p2x = 0
            s3p2y = 0
            spell3P2Fire = False

    pygame.display.update()

newFileData = [trophyCount1, trophyCount2]
with open("trophyFile.txt", "w") as file:
    for i in newFileData:
        file.write(str(i) + '\n')

pygame.quit()
