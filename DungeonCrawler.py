import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
import random as rn

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

##########
## GAME ##
##########

def createGame():
    game = tk.Tk()
    game.title("Dungeon Crawler - Hra")
    game.geometry("1000x700")
    
    enemyFrame = tk.Frame(game, bg="red", width=250, height=175)
    enemyFrame.grid(row=0, column=0, sticky="nsew")
    enemyImg = tk.PhotoImage(file="marci2.png")
    enemyImg = enemyImg.subsample(9,9)
    enemyLabel = tk.Label(enemyFrame, image=enemyImg)
    enemyLabel.image = enemyImg
    enemyLabel.place(x=0, y=0, relwidth=1, relheight=1)

    statsFrame = tk.Frame(game, bg="yellow")
    statsFrame.grid(row=0, column=1, sticky="nsew")
    
    
    textFrame = tk.Frame(game, bg="white")
    textFrame.grid(row=0, column=2, sticky="nsew")
    
    
    lettersFrame = tk.Frame(game, bg="black", height=200)
    lettersFrame.grid(row=1, column=0, columnspan=2, sticky="nsew")
    
    
    actionFrame = tk.Frame(game, bg="blue")
    actionFrame.grid(row=1, column=2, sticky="nsew")
    actionImg = tk.PhotoImage(file="fredo1.png")
    actionImg = actionImg.subsample(7,7)
    actionLabel = tk.Label(actionFrame, image=actionImg)
    actionLabel.image = actionImg
    actionLabel.place(x=0, y=0, relwidth=1, relheight=1)
    
    
    game.grid_rowconfigure(0, weight=3)
    game.grid_rowconfigure(1, weight=1)
    game.grid_columnconfigure(0, weight=1)
    game.grid_columnconfigure(1, weight=1)
    game.grid_columnconfigure(2, weight=1)
    
    return game, enemyFrame, statsFrame, textFrame, lettersFrame, actionFrame

def startGame(menuWin):
    menuWin.destroy()
    game = createGame()
    game.mainloop()

def updateDisplay(window):
    
    pass


# Spustenie aplikácie
window = onStartup()
window.mainloop()