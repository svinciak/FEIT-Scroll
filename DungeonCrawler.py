import tkinter as tk
import random as rnd
from tkinter import messagebox
from tkinter import font as tkfont


def onStartup():
    win = tk.Tk()
    win.title("Dungeon Crawler")
    win.geometry("960x640")
    createMenu(win)
    return win

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
    scoresButton = tk.Button(buttonsFrame, text="SKÓRE", command=show_scores, **buttonConfig)
    optionsButton = tk.Button(buttonsFrame, text="NASTAVENIA", command=show_options, **buttonConfig)
    helpButton = tk.Button(buttonsFrame, text="POMOC", command=show_help, **buttonConfig)
    aboutButton = tk.Button(buttonsFrame, text="O HRE", command=show_about, **buttonConfig)
    
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
    except Exception as e:
        print("Chyba pri načítaní obrázka LOGO")

def show_scores():
    messagebox.showinfo("Skóre", "Najvyššie zahrané skóre")

def show_options():
    messagebox.showinfo("Nastavenia", "Nastavenia hry ešte nie sú pridané")

def show_help():
    messagebox.showinfo("Pomoc", "Návod na hru si prečítaj online : )")

def show_about():
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
selectedLetters = []
clickedOrder = []

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
    
    
    current_word = ""
    for btn in clickedOrder:
        current_word += btn['text'].lower()
    print("Current word:", current_word)
        
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
        )
        # zachova 2 hodnoty: aktualnePismeno, tlacidlo ->buttonClick(aktualnePismeno, tlacidlo)
        l = letter
        b = btn
        btn.config(command=lambda l=letter, b=btn: buttonClick(l, b))
        letterButtons.append(btn)
    
def draw():
    # vykresli pismena
    i = 1
    for b in letterButtons:
        b.grid(row=0, column=i, padx=5)
        i+=1

def createGame():
    global game, enemyFrame,statsFrame, textFrame, lettersFrame, actionFrame
    
    # framy
    game = tk.Tk()
    game.title("Dungeon Crawler - Hra")
    game.geometry("1000x700")
    
    enemyFrame = tk.Frame(game, bg="red", width=250, height=175)
    enemyFrame.grid(row=0, column=0, sticky="nsew")
    statsFrame = tk.Frame(game, bg="yellow")
    statsFrame.grid(row=0, column=1, sticky="nsew")
    textFrame = tk.Frame(game, bg="white")
    textFrame.grid(row=0, column=2, sticky="nsew")
    lettersFrame = tk.Frame(game, bg="black", height=200)
    lettersFrame.grid(row=1, column=0, columnspan=2, sticky="nsew")
    actionFrame = tk.Frame(game, bg="blue")
    actionFrame.grid(row=1, column=2, sticky="nsew")
    
    game.grid_rowconfigure(0, weight=3)
    game.grid_rowconfigure(1, weight=1)
    game.grid_columnconfigure(0, weight=1)
    game.grid_columnconfigure(1, weight=1)
    game.grid_columnconfigure(2, weight=1)
    
    # tlacidla na pismena
    letters = generateLetters()
    makeLetterButoons()

#-------#
# START #
#-------#

def startGame(menuWin):
    menuWin.destroy()
    createGame()
    draw()
    game.mainloop()



# Spustenie aplikácie
window = onStartup()
window.mainloop()