import tkinter as tk
import random as rnd
from tkinter import messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk

# TODO: krajsie tlacidla, fixnut priehladnost(cez canvas nie Label), commit(pridanie ActionsFrame)

############
### MENU ###
############
def createMenu(win):
    # FRAME NA POZADIE 
    bgFrame = tk.Frame(win)
    bgFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    try:
        bgImg = tk.PhotoImage(file="uniza.png")
        bgLabel = tk.Label(bgFrame, image=bgImg, bg='black')
        bgLabel.image = bgImg
        bgLabel.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Chyba pri načítavaní obrázka")
        print(e)
        bgFrame.config(bg='blue')
    
    # FRAME NA TLACIDLA
    buttonsFrame = tk.Frame(win, bg='#333333', width=200)
    buttonsFrame.pack(side=tk.RIGHT, fill=tk.Y)
    buttonFont = tkfont.Font(family='Helvetica', size=14, weight='bold')
    buttonConfig = {
        'font': buttonFont,
        'width': 10,
        'height': 2,
        'bg': '#555555',
        'fg': 'white',
        'activeforeground': 'white', 
        'activebackground': '#777777', 
        'relief': tk.RAISED, 
        'borderwidth': 10
    }
    
    playButton = tk.Button(buttonsFrame, text="HRAJ", command=lambda: startGame(win), **buttonConfig)
    scoresButton = tk.Button(buttonsFrame, text="SKÓRE", command=showScores, **buttonConfig)
    optionsButton = tk.Button(buttonsFrame, text="NASTAVENIA", command=showOptions, **buttonConfig)
    helpButton = tk.Button(buttonsFrame, text="POMOC", command=showHelp, **buttonConfig)
    aboutButton = tk.Button(buttonsFrame, text="O HRE", command=showAbout, **buttonConfig)
    
    playButton.pack(pady=10)
    scoresButton.pack(pady=10)
    optionsButton.pack(pady=10)
    helpButton.pack(pady=10)
    aboutButton.pack(pady=10)
    
    try:
        logoImg = tk.PhotoImage(file="unizaLOGO.png")
        logoFrame = tk.Frame(buttonsFrame, bg='#333333')
        logoFrame.pack(side=tk.BOTTOM, fill=tk.X, pady=(0,10))
        
        logoLabel = tk.Label(logoFrame, image=logoImg, bg='#333333', borderwidth=0)
        logoLabel.image = logoImg
        logoLabel.pack(pady=5)
    except Exception:
        print("Chyba pri načítaní obrázka LOGO")

def showScores():
    messagebox.showinfo("Skóre", "Najvyššie zahrané skóre")

def showOptions():
    messagebox.showinfo("Nastavenia", "Nastavenia hry ešte nie sú pridané")

def showHelp():
    messagebox.showinfo("Pomoc", "Návod na hru si prečítaj online : )")

def showAbout():
    messagebox.showinfo("O hre", "Semestrálna práca Dungeon Crawler je hra vytvorená v Pythone využitím knižnice Tkinter. Vytvoril Kerata Marek.")

#-----#
# HRA #
#-----#

#----------#
# PREMENNE #
#----------#


dungeonLevel = 1 
playerHealth = 100
enemyList = []
letters = []
letterButtons = []
actionButtons = []
selectedLetters = []
clickedOrder = []
enemies = []
batImgs = []
animationID = None  
currentImg = 0     
enemy = None  


def makeActionButtons():
    global actionButtons
    actionButtons = []

    submitButton = tk.Button(
        actionFrame,
        text="Potvrď slovo",
        bg='yellow',
        font=("ARIAL", 14),
        width=12,
        height=1,
        command=submitWord
    ).grid(row=0, column=0, padx=5, pady=10)
    actionButtons.append(submitButton)

    resetButton = tk.Button(
        actionFrame,
        text="Obnov písmena",
        bg='yellow',
        font=("ARIAL", 14),
        width=12,
        height=1,
        command=resetLetters
    ).grid(row=0, column=1, padx=5, pady=10)
    actionButtons.append(resetButton)

    jumbleButton = tk.Button(
        actionFrame,
        text="Zamiešaj",
        bg='yellow',
        font=("ARIAL", 14),
        width=12,
        height=1,
        command=jumbleLetters
    ).grid(row=0, column=2, padx=5, pady=10)
    actionButtons.append(jumbleButton)

    helpButton = tk.Button(
        actionFrame,
        text="Pomoc",
        bg='yellow',
        font=("ARIAL", 14),
        width=12,
        height=1,
        command=finishWord
    ).grid(row=0, column=3, padx=5, pady=10)
    actionButtons.append(helpButton)

def submitWord():
    print("POTVRD SLOVO TLACIDIELKO BOLO STLACENE")
    
def resetLetters():
    global selectedLetters, clickedOrder
    print("RESET LETTERS TLACIDIELKO BOLO STLACENE")
    
    selectedLetters.clear()
    
    for b in clickedOrder:
        b.config(state='normal')
        print(b)
        b.grid(row=0, column=letterButtons.index(b)+1, padx=5)
    clickedOrder.clear()
    print("pismenka obnovene do povodneho stavu")
    

def jumbleLetters():
    print("JUMBLE LETTERS TLACIDIELKO BOLO STLACENE")

def finishWord():
    print("DOKONCI SLOVO TLACIDIELKO BOLO STLACENE")

## transparent imgs: https://stackoverflow.com/questions/56554692/unable-to-put-transparent-png-over-a-normal-image-python-tkinter/56555164#56555164
def loadImgs():
    global batImgs
    batImgs = []
    try:
        for i in range(15):
            img = Image.open(f"sprites/bat/bat{i}.png")
            batImgs.append(ImageTk.PhotoImage(img, master=game))
    except Exception as e:
        print("chyba pri nacitani obrazkov: " + str(e))

def generateLetters():
    global dungeonLevel, letters
    letters = []
    letterCount = 4 + dungeonLevel * 2
    
    for i in range(letterCount):
        l = chr(rnd.randint(97,122))
        letters.append(l)

def buttonClick(letterFromButton, button):
    print("klikol som tlacidlo: " + letterFromButton)
    selectedLetters.append(letterFromButton)
    clickedOrder.append(button)
    #zoradenie
    button.grid(row=1, column=len(clickedOrder), padx=5)
    button.config(state="disabled")
    
    currentWord = ""
    for btn in clickedOrder:
        currentWord += btn['text'].lower()
    print("Current word:", currentWord)
        
def makeLetterButoons():
    global letterButtons
    letterButtons = []
    for letter in letters:
        btn = tk.Button(
            lettersFrame,
            text=letter.upper(),
            font=("ARIAL", 18),
            width=3,
            height=1,
            state = 'normal'
        )
        # zachova 2 hodnoty: aktualnePismeno, tlacidlo ->buttonClick(aktualnePismeno, tlacidlo)
        btn.config(command=lambda l=letter, b=btn: buttonClick(l, b))
        letterButtons.append(btn)
    
def createEnemies():
    global enemy, animationID
    
    if animationID:
        enemyFrame.after_cancel(animationID)
    for widget in enemyFrame.winfo_children():
        widget.destroy()
    
    enemy = {
        "type": "bat",
        "hp": 100,
        "sound": "este neni, napotom",
        "label": tk.Label(enemyFrame)
    }
    enemy["label"].pack(pady=20)
    enemies.append(enemy)
    animateEnemies()

def animateEnemies():
    global currentImg, animationID
    
    if not batImgs or not enemy:
        return
    
    enemy["label"].config(image=batImgs[currentImg])
    currentImg = (currentImg + 1) % len(batImgs)
    
    # 100ms = 10 FPS
    animationID = enemyFrame.after(100, animateEnemies)

def drawLetters():
    i = 1
    for b in letterButtons:
        b.grid(row=0, column=i, padx=5)
        i+=1
        
def draw():
    pass

def createGame():
    global game, enemyFrame,statsFrame, textFrame, lettersFrame, actionFrame
    
    game = tk.Tk()
    game.title("FEIT Crawler - Hra")
    #game.geometry("800x700")
    
    # FRAMES-config
    enemyFrame = tk.Frame(game, bg="red", width=300, height=300)
    statsFrame = tk.Frame(game, bg="yellow", width=600, height=300)
    textFrame = tk.Frame(game, bg="white", width=900, height=100)
    lettersFrame = tk.Frame(game, bg="black", width=900, height=80)
    actionFrame = tk.Frame(game, bg="blue", width=900, height=80)
    enemyFrame.grid_propagate(False)
    statsFrame.grid_propagate(False)
    textFrame.grid_propagate(False)
    lettersFrame.grid_propagate(False)
    actionFrame.grid_propagate(False)
    enemyFrame.grid(row=0, column=0, sticky="nsew")
    statsFrame.grid(row=0, column=1, columnspan=2, sticky="nsew")
    textFrame.grid(row=1, column=0, columnspan=3, sticky="nsew")
    lettersFrame.grid(row=2, column=0, columnspan=3, sticky="nsew")
    actionFrame.grid(row=3, column=0, columnspan=3, sticky="nsew")
    
    # PISMENA-LettersFrame
    generateLetters()
    makeLetterButoons()
    loadImgs()
    drawLetters()
    
    # enemiesFrame
    createEnemies()
    
    # actionFrame
    makeActionButtons()
    
#-------#
# START #
#-------#

def startGame(menuWin):
    menuWin.destroy()
    createGame()  
    game.mainloop()
    
def onStartup():
    win = tk.Tk()
    win.title("Dungeon Crawler")
    win.geometry("960x640")
    createMenu(win)
    return win



# Spustenie aplikácie
window = onStartup()
window.mainloop()