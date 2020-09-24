
from tkinter import *
from Classes import *

def game():
    global endEvent
    if board.endEvent==False:
        #Check
        if stop == False:
            blue.move1()
            #2 Player
            if board.pType == "2-Player":
                red.move1()
                #Move
                if blue.headCollide == False and red.headCollide==False:
                    blue.move2()
                    red.move2()

            #1 Player
            elif blue.headCollide == False:
                blue.move2()
        root.after(board.speed, game)

    ##End Sequence
    else:
        if board.pType == "2-Player":
            if blue.headCollide == True and red.headCollide==True:
                endEvent="Both Lose"
                endMenu()

            else:
                endEvent=board.endEvent
                if blue.both or red.both == True:   #Due to "Head Head" collision not triggering a death of both snakes
                    red.death+=1
                    blue.death+=1
                    red.loss+=1
                    blue.loss+=1
                endMenu()
        else:
            endEvent="You Lose"
            endMenu()

root = Tk()
root.title("Snake")
root.geometry("600x600+250+20")

#Variables
stop = False
endEvent=None
count=None



def pause(event):
    global stop
    stop = not stop

#Classes
board = Board(root, bgcol="Black")
grid = Grid(board)
border = Border(board, grid)
food = Food(board, grid,"white")
blue = Snake(board,grid,food,"#55bbff" ,"Blue", 100, 300,direction="r", snakeLen=10)

red = Snake(board,grid,food,"#ffbb55" ,"Red", 500, 300,direction="l", snakeLen=10)

#Bindings
root.bind("<Up>", red.dirUp)
root.bind("<Down>", red.dirDown)
root.bind("<Left>", red.dirLeft)
root.bind("<Right>", red.dirRight)

root.bind("<w>", blue.dirUp)
root.bind("<s>", blue.dirDown)
root.bind("<a>", blue.dirLeft)
root.bind("<d>", blue.dirRight)

root.bind("<p>", pause)


def restart():
    global count
    #Clears
    board.canvas.delete("all")

    #Board
    board.resetSelf()

    #Grid
    grid.resetSelf()

    #Wall
    border.restartSelf()

    #Snakes
    blue.resetSelf()
    if board.pType == "2-Player":
        red.resetSelf()
    else:       #Single Player
        board.canvas.delete(red)

    #Wait
    count = board.canvas.create_text(310, 300, anchor='center',fill="White", font=('Arial', 100))
    root.after(600,countDown('3'))
    root.after(600,countDown('2'))
    root.after(600,countDown('1'))
    countDown('GO')
    board.canvas.delete(count)

    #Food
    food.restartSelf()

    #Start Game
    root.after(400,game())

def countDown(num):
    global count
    board.canvas.itemconfig(count,text=str(num))
    root.update_idletasks()

#Menu Functions
def startMenu():
    #Clears
    global mode
    board.canvas.delete("menu")
    if blue.activeMod or red.activeMod or board.activeMod != []:
        modWindow(40, 30)

    title = board.canvas.create_text(310, 200, text="Welcome to Snake",anchor='center',
                                     fill="White", font=('Arial', 40),tag="menu")

    options = GeneralButton(root,board,"Options",lambda: optionsMenu(startMenu),160,450)
    start = GeneralButton(root,board,"Start",restart,450,450)
    mode = GeneralButton(root,board,"Currently: "+board.pType,lambda:board.pTypeToggle(mode),220,490)
    mode.button.configure(width = 25)

def endMenu():
    global endEvent
    #Clears
    board.canvas.delete("menu")

    if blue.activeMod or red.activeMod or board.activeMod != []:
        modWindow(40,30)

    title = board.canvas.create_text(310, 200, text="Game Over\n"+str(endEvent),justify=CENTER,
                                     anchor='center',fill="White", font=('Arial', 40), tag="menu")

    options = GeneralButton(root,board,"Options",lambda: optionsMenu(endMenu),160,450)
    results = GeneralButton(root,board,"Results",resultsMenu,305,450)
    reset = GeneralButton(root,board,"Restart",restart,450,450)
    mode = GeneralButton(root,board,"Currently: "+board.pType,lambda:board.pTypeToggle(mode),220,490)
    mode.button.configure(width = 25)

def optionsMenu(parent):
    #Clears
    board.canvas.delete("menu")
    #Settings
    sColours = ["Blue", "Red", "Purple", "Green", "Orange", "Silver", "Yellow"]
    speedOptList = ["Fast", "Normal", "Slow"]
    sLenList = ["Short", "Normal", "Long", "Infinite"]

    title = board.canvas.create_text(130, 110, text="Options",justify=CENTER,
                                     anchor='w',fill="White", font=('Arial', 40), tag="menu")

    #Drop Down
    speedOpt = OptionsDropDown(root, board, board, speedOptList, "Set Speed",130, 150)
    if board.pType == "2-Player":
        sColRed = OptionsDropDown(root,board,red,sColours,"Right's Colour",130,270)
        sLenRed = OptionsDropDown(root,board,red,sLenList, "Right's Starting Length", 130, 310)
        sColBlue = OptionsDropDown(root,board,blue,sColours,"Left's Colour",130,190)
        sLenBlue = OptionsDropDown(root,board,blue,sLenList, "Left's Starting Length", 130, 230)
    else:
        sColBlue = OptionsDropDown(root,board,blue,sColours,"Snake's Colour",130,190)
        sLenBlue = OptionsDropDown(root,board,blue,sLenList, "Snake's Starting Length", 130, 230)

    back = GeneralButton(root,board,"Back",parent,450,450)

def resultsMenu():
    #Clears
    board.canvas.delete("menu")
    if board.pType == "2-Player":
        blueStat = Results(root,board,blue,170,100)
        redStat = Results(root,board,red,430,100)
    else:
        blueStat = Results(root,board,blue,300,100)

    back = GeneralButton(root,board,"Back",endMenu,450,450)

def modWindow(xpos,ypos):
    activeMods=[]

    checkEmpty(blue.activeMod,activeMods)
    checkEmpty(red.activeMod,activeMods)
    checkEmpty(board.activeMod,activeMods)

    title = board.canvas.create_text(xpos, ypos, text="Modifiers",justify=CENTER,
                                 anchor='nw',fill="White", font=('Arial', 15), tag="menu")

    mod = board.canvas.create_text(xpos, ypos+22, text=
                                   activeMods
                                   ,justify=CENTER,
                                 anchor='nw',fill="White", font=('Arial', 10), tag="menu")

def checkEmpty(alist,blist):
    if alist != []:
        blist.append(alist)

#StartProg
startMenu()
root.mainloop()
