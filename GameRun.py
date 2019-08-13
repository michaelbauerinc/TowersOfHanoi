from stack import Stack
from node import Node
import pygame
import time
from time import sleep
import os
import sys

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

pygame.init()

display_width = 445
display_height = 550

black = (0, 0, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
run = True
choosingMode = False
start = False
moving = False
topDisk = None
currentDisk = None
previousStack = None
gameWin = False
gameWinNum = 0
turnCount = 0
num_disks = 0
screenContent = {}
message = ""

pygame.display.set_caption('TowersOfHanoi')
clock = pygame.time.Clock()


firstTower = Node(65)
secondTower = Node(189)
thirdTower = Node(313)

firstTower.set_next_node(secondTower)
secondTower.set_next_node(thirdTower)

secondTower.set_previous_node(firstTower)
thirdTower.set_previous_node(secondTower)

currentLocation = firstTower
nextLocation = currentLocation.get_next_node()
previousLocation = currentLocation.get_previous_node()
diskLocation = None


class Image(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    gameDisplay.blit(BackGround.image, BackGround.rect)
    largeText = pygame.font.Font('freesansbold.ttf', 15)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (460))
    gameDisplay.blit(TextSurf, TextRect)


def gameStart():
    global start
    global message
    global num_disks
    global gameWinNum
    global num_optimal_moves
    global screenContent
    start = True
    del screenContent[Three.image]
    del screenContent[Four.image]

    BottomDisk.rect.left = 34
    MiddleDisk.rect.left = 47
    ThirdDisk.rect.left = 58
    TopDisk.rect.left = 68

    num_optimal_moves = (2 ** num_disks) - 1
    message = "Optimal solution: {} moves. Goodluck!".format(num_optimal_moves)

    if num_disks == 4:
        screenContent[BottomDisk.image] = (BottomDisk.rect)
        screenContent[MiddleDisk.image] = (MiddleDisk.rect)
        screenContent[ThirdDisk.image] = (ThirdDisk.rect)
        screenContent[TopDisk.image] = (TopDisk.rect)
        left_stack.push(4)
        top = left_stack.top_item
        top.assign_image(BottomDisk)
        left_stack.push(3)
        top = left_stack.top_item
        top.assign_image(MiddleDisk)
        left_stack.push(2)
        top = left_stack.top_item
        top.assign_image(ThirdDisk)
        left_stack.push(1)
        top = left_stack.top_item
        top.assign_image(TopDisk)
        gameWinNum = left_stack.get_size()
        screenRefresh()
    else:
        screenContent[BottomDisk.image] = (BottomDisk.rect)
        screenContent[MiddleDisk.image] = (MiddleDisk.rect)
        screenContent[ThirdDisk.image] = (ThirdDisk.rect)
        left_stack.push(4)
        top = left_stack.top_item
        top.assign_image(BottomDisk)
        left_stack.push(3)
        top = left_stack.top_item
        top.assign_image(MiddleDisk)
        left_stack.push(2)
        top = left_stack.top_item
        top.assign_image(ThirdDisk)
        gameWinNum = left_stack.get_size()
        screenRefresh()
    message = "Choose disk to move."


def checkTower():
    global message
    global topDisk
    global diskLocation
    global left_stack
    global right_stack
    global middle_stack
    global currentLocation
    global moving
    global previousStack
    global diskToAnimate
    global topImage

    diskLocation = currentLocation

    if currentLocation == firstTower:
        topDisk = left_stack.peek()
        if not topDisk:
            message = "No disk on that tower."
        else:

            top = left_stack.get_top_node()
            diskToAnimate = top.get_image()
            topImage = top.get_image()
            topDisk = left_stack.pop()
            previousStack = left_stack
            message = "Move to where?"
            moving = True

    elif currentLocation == secondTower:
        topDisk = middle_stack.peek()
        if not topDisk:
            message = "No disk on that tower."
        else:

            top = middle_stack.get_top_node()
            diskToAnimate = top.get_image()
            topImage = top.get_image()
            topDisk = middle_stack.pop()
            previousStack = middle_stack
            message = "Move to where?"
            moving = True

    elif currentLocation == thirdTower:
        topDisk = right_stack.peek()
        if not topDisk:
            message = "No disk on that tower."
        else:

            top = right_stack.get_top_node()
            diskToAnimate = top.get_image()
            topImage = top.get_image()
            topDisk = right_stack.pop()
            previousStack = right_stack
            message = "Move to where?"
            moving = True

    screenRefresh()


def moveDisk():
    global message
    global topDisk
    global diskLocation
    global left_stack
    global right_stack
    global middle_stack
    global currentLocation
    global moving
    global previousStack
    global currentStack
    global top
    global topImage
    global gameWin
    global gameWinNum
    global turnCount
    global num_optimal_moves

    if currentLocation == diskLocation:
        previousStack.push(topDisk)
        top = previousStack.get_top_node()
        top.assign_image(topImage)
        message = "Disk already on that tower."
        moving = False
        screenRefresh()
        return

    elif currentLocation == firstTower and left_stack.peek() == None or currentLocation == firstTower and topDisk < left_stack.peek():
        currentStack = left_stack
        diskAnimation(diskToAnimate)
        left_stack.push(topDisk)
        top = left_stack.get_top_node()
        top.assign_image(topImage)
        message = "Choose disk to move."

    elif currentLocation == secondTower and middle_stack.peek() == None or currentLocation == secondTower and topDisk < middle_stack.peek():
        currentStack = middle_stack
        diskAnimation(diskToAnimate)
        middle_stack.push(topDisk)
        top = middle_stack.get_top_node()
        top.assign_image(topImage)
        message = "Choose disk to move."

    elif currentLocation == thirdTower and right_stack.peek() == None or currentLocation == thirdTower and topDisk < right_stack.peek():
        currentStack = right_stack
        diskAnimation(diskToAnimate)
        right_stack.push(topDisk)
        top = right_stack.get_top_node()
        top.assign_image(topImage)
        message = "Choose disk to move."

    else:
        message = "You can't place bigger disks on smaller ones."
        previousStack.push(topDisk)
        top = previousStack.get_top_node()
        top.assign_image(topImage)
        moving = False
        screenRefresh()
        return

    previousStack = None
    moving = False
    topDisk = None
    turnCount += 1

    if right_stack.get_size() == gameWinNum:
        gameWin = True
        message = "You win in {0} moves. Optimal number is {1}".format(
            turnCount, num_optimal_moves)
        screenRefresh()
        sleep(2.0)
        message = "Press space to play again."

    screenRefresh()

    print("DEBUG:")
    left_stack.print_items()
    middle_stack.print_items()
    right_stack.print_items()


def calculateSpacesToMove(diskTracker, spacesToMove=0, spacesToMoveNeg=0, firstFlag=False, secondFlag=False):
    if diskTracker == currentLocation and spacesToMoveNeg < 0:
        return spacesToMoveNeg
    elif diskTracker == currentLocation:
        return spacesToMove
    elif diskTracker == firstTower:
        diskTracker = diskTracker.get_next_node()
        spacesToMove += 1
        return calculateSpacesToMove(diskTracker, spacesToMove)
    elif diskTracker == secondTower and firstFlag:
        diskTracker = diskTracker.get_previous_node()
        spacesToMoveNeg -= 1
        return calculateSpacesToMove(diskTracker, spacesToMove, spacesToMoveNeg, firstFlag)
    elif diskTracker == secondTower:
        diskTracker = diskTracker.get_next_node()
        spacesToMove += 1
        secondFlag = True
        return calculateSpacesToMove(diskTracker, spacesToMove, spacesToMoveNeg, firstFlag, secondFlag)
    elif diskTracker == thirdTower and secondFlag:
        diskTracker = diskTracker.get_previous_node()
        firstFlag = True
        return calculateSpacesToMove(diskTracker, spacesToMove, spacesToMoveNeg, firstFlag, secondFlag)
    elif diskTracker == thirdTower:
        firstFlag = True
        diskTracker = diskTracker.get_previous_node()
        spacesToMoveNeg -= 1
        return calculateSpacesToMove(diskTracker, spacesToMove, spacesToMoveNeg, firstFlag)


def diskAnimation(disk):
    global diskLocation
    spacesToMovePos = 0
    spacesToMoveNeg = 0
    diskTracker = diskLocation
    diskTrackerNeg = diskLocation
    spacesToMove = calculateSpacesToMove(diskLocation)

    if spacesToMove == 1:
        xcoord = 124
    elif spacesToMove == 2:
        xcoord = 248
    elif spacesToMove == -1:
        xcoord = -124
    elif spacesToMove == -2:
        xcoord = -248
    if currentStack.get_size() == 0:
        diskToAnimate.rect.top = 292
    elif currentStack.get_size() == 1:
        diskToAnimate.rect.top = 262
    elif currentStack.get_size() == 2:
        diskToAnimate.rect.top = 233
    elif currentStack.get_size() == 3:
        diskToAnimate.rect.top = 204

    diskToAnimate.rect.left += xcoord
    diskLocation = currentLocation


def screenRefresh():
    gameDisplay.blit(BackGround.image, BackGround.rect)
    message_display(message)
    for key, value in screenContent.items():
        gameDisplay.blit(key, value)
    pygame.display.update()


def resetPointer():
    global currentLocation
    global previousLocation
    global nextLocation

    Pointer.rect.left = previousLocation.get_value()
    currentLocation = currentLocation.get_previous_node()
    nextLocation = currentLocation.get_next_node()
    previousLocation = currentLocation.get_previous_node()
    Pointer.rect.left = previousLocation.get_value()
    currentLocation = currentLocation.get_previous_node()
    nextLocation = currentLocation.get_next_node()
    previousLocation = currentLocation.get_previous_node()


def restart_program():
    global choosingMode
    global start
    global moving
    global gameWin
    global screenContent
    global num_disks
    global turnCount

    if num_disks == 4:
        TopDisk.rect.left -= 68

    for i in range(num_disks):
        right_stack.pop()

    screenContent.clear()
    gameDisplay.blit(BackGround.image, BackGround.rect)
    message_display("Towers of Hanoi! Press space to play.")
    pygame.display.update()
    choosingMode = False
    start = False
    moving = False
    gameWin = False
    turnCount = 0
    resetPointer()


# ASSETS
BackGround = Image('background.png', [0, 0])
BottomDisk = Image("bottomdisk.png", [34, 292])
MiddleDisk = Image("middledisk.png", [47, 262])
ThirdDisk = Image("thirddisk.png", [58, 233])
TopDisk = Image("topdisk.png", [68, 204])
Pointer = Image("selecttriangle.png", [65, 90])
Three = Image("three.png", [44, 200])
Four = Image("four.png", [167, 200])


message_display("Towers of Hanoi! Press space to play.")
pygame.display.update()

stacks = []

left_stack = Stack("Left")
middle_stack = Stack("Middle")
right_stack = Stack("Right")


while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif not choosingMode:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    gameDisplay.blit(BackGround.image, BackGround.rect)
                    screenContent[Pointer.image] = (Pointer.rect)
                    screenContent[Three.image] = (Three.rect)
                    screenContent[Four.image] = (Four.rect)
                    message = "Choose number of disks to play with."
                    screenRefresh()
                    choosingMode = True
        elif choosingMode and not start:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and currentLocation != thirdTower:
                    Pointer.rect.left = nextLocation.get_value()
                    currentLocation = currentLocation.get_next_node()
                    nextLocation = currentLocation.get_next_node()
                    previousLocation = currentLocation.get_previous_node()
                    screenRefresh()
                elif event.key == pygame.K_LEFT and currentLocation != firstTower:
                    Pointer.rect.left = previousLocation.get_value()
                    currentLocation = currentLocation.get_previous_node()
                    nextLocation = currentLocation.get_next_node()
                    previousLocation = currentLocation.get_previous_node()
                    screenRefresh()
                elif event.key == pygame.K_SPACE and currentLocation == firstTower:
                    num_disks = 3
                    gameStart()
                elif event.key == pygame.K_SPACE and currentLocation == secondTower:
                    num_disks = 4
                    gameStart()
        elif choosingMode and start and not gameWin:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and currentLocation != thirdTower:
                    Pointer.rect.left = nextLocation.get_value()
                    currentLocation = currentLocation.get_next_node()
                    nextLocation = currentLocation.get_next_node()
                    previousLocation = currentLocation.get_previous_node()
                    screenRefresh()
                elif event.key == pygame.K_LEFT and currentLocation != firstTower:
                    Pointer.rect.left = previousLocation.get_value()
                    currentLocation = currentLocation.get_previous_node()
                    nextLocation = currentLocation.get_next_node()
                    previousLocation = currentLocation.get_previous_node()
                    screenRefresh()
                elif event.key == pygame.K_SPACE and not moving:
                    checkTower()
                    print(str(currentLocation.get_value()))
                elif event.key == pygame.K_SPACE and moving:
                    moveDisk()
                    print(str(currentLocation.get_value()))
        elif choosingMode and start and gameWin:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    restart_program()
