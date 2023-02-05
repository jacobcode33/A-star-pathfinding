import time
import winsound
from graphics import *
import random
import keyboard
import csv

def refresh():
    canvas.update()
    for item in canvas.items[:]: # clears drawing
        item.undraw()

def draw():
    for o in range (len(wallsd)): # draws snake
        wall = wallsd[o]
        wall.setFill("black")
        wall.draw (canvas)
    for o in range (len(checked)):
        seen = (Rectangle(Point(((checked[o][0]-1)*(screenwidth/tileswidth)),((checked[o][1]-1)*((screenheight/tilesheight)))), Point(((checked[o][0])*(screenwidth/tileswidth)),((checked[o][1])*((screenheight/tilesheight))))))
        if checkedF1[o] == 99999:
            seen.setFill("lightblue")
        else:
            seen.setFill("lightgreen")
        seen.draw(canvas)
    start = (Rectangle(Point(((startpoint[0]-1)*(screenwidth/tileswidth)),((startpoint[1]-1)*((screenheight/tilesheight)))), Point(((startpoint[0])*(screenwidth/tileswidth)),((startpoint[1])*((screenheight/tilesheight))))))
    end = (Rectangle(Point(((endpoint[0]-1)*(screenwidth/tileswidth)),((endpoint[1]-1)*((screenheight/tilesheight)))), Point(((endpoint[0])*(screenwidth/tileswidth)),((endpoint[1])*((screenheight/tilesheight))))))
    start.setFill("green")
    end.setFill("red")
    start.draw(canvas)
    end.draw(canvas)
    
    refresh()

def make():
    startpoint.append(random.randint(1,tileswidth))
    startpoint.append(random.randint(1,tilesheight))
    endpoint.append(random.randint(1,tileswidth))
    endpoint.append(random.randint(1,tilesheight))

    count = 0
    while count < 100 and len(checked) < (tileswidth*tilesheight):
        point = []
        point.append(random.randint(1,tileswidth))
        point.append(random.randint(1,tilesheight))
        if not point in walls and point != startpoint and point != endpoint:
            draw() # watch as the walls are created (optional)
            walls.append(point)
            wallsd.append(Rectangle(Point(((point[0]-1)*(screenwidth/tileswidth)),((point[1]-1)*((screenheight/tilesheight)))), Point(((point[0])*(screenwidth/tileswidth)),((point[1])*((screenheight/tilesheight))))))
            count = count + 1

def search(spread):
    global done
    index = checkedF1.index(min(checkedF1))
    point = checked[index]
    for i in range(4):
        if i == 0:
            newpoint = [point[0],point[1]+1]
        if i == 1:
            newpoint = [point[0],point[1]-1]
        if i == 2:
            newpoint = [point[0]+1,point[1]]
        if i == 3:
            newpoint = [point[0]-1,point[1]]
        if newpoint not in walls:
            if newpoint not in checked:
                checked.append(newpoint)
                checkedG.append(checkedG[len(checked)-2]+spread)
                checkedH.append(abs(newpoint[0]-endpoint[0])+abs(newpoint[1]-endpoint[1]))
                checkedF1.append(checkedG[len(checked)-1]+checkedH[len(checked)-1])
                checkedF2.append(checkedG[len(checked)-1]+checkedH[len(checked)-1])
            elif checkedF1[checked.index(newpoint)] != 99999 and checkedF2[checked.index(newpoint)] > ((abs(newpoint[0]-startpoint[0])+abs(newpoint[1]-startpoint[1]))+(abs(newpoint[0]-endpoint[0])+abs(newpoint[1]-endpoint[1]))):
                checkedG[checked.index(newpoint)] += spread
                checkedF2[checked.index(newpoint)] = (checkedG[checked.index(newpoint)]+checkedH[checked.index(newpoint)])
                checkedF1[checked.index(newpoint)] = (checkedG[checked.index(newpoint)]+checkedH[checked.index(newpoint)])
            if newpoint == endpoint:
                done = True
        checkedF1[index] = 99999

tileswidth = 30
tilesheight = 30
screenwidth = 600
screenheight = 600

canvas = GraphWin("snake", 700, 700, autoflush = False)
canvas.setBackground ("white")

while True:
    startpoint = []
    endpoint = []
    walls = []
    wallsd = []
    checked = []
    checkedG = [] # manhatten distance from startpoint
    checkedH = [] # manhatten distance from endpoint
    checkedF1 = [] # fake version of F2 where it does not allow for the same tile to be checked twice
    checkedF2 = [] # sum of G&H for prioritising where to check
    make()
    checked.append(startpoint)
    checkedG.append(0) # manhatten distance from startpoint
    checkedH.append(abs(startpoint[0]-endpoint[0])+abs(startpoint[1]-endpoint[1])) # manhatten distance from endpoint
    checkedF1.append(abs(startpoint[0]-endpoint[0])+abs(startpoint[1]-endpoint[1])) # fake version of F2 where it does not allow for the same tile to be checked twice
    checkedF2.append(abs(startpoint[0]-endpoint[0])+abs(startpoint[1]-endpoint[1])) # total value for which it wants to check
    
    done = False
    count = 0
    while not done:
        search(0.35) # the higher the spread the more likely to find the fastest route but it will take longer to find
        draw()
