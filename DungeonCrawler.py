import tkinter as tk
import random as rnd
from tkinter import messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk
from winsound import PlaySound

############
### MENU ###
############
def createMenu(win):
    # FRAME NA POZADIE 
    bgFrame = tk.Frame(win)
    bgFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    try:
        bgImg = tk.PhotoImage(file="sprites/feitImg.png")
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
    # TODO definovat buttonConfig implicitne
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

def startGame(menuWin):
    PlaySound('gameStart.wav', 1)
    menuWin.after(1000)
    menuWin.destroy()
    createMap()
    #createGame()  

def showScores():
    PlaySound('buttonClick.wav', 1)
    messagebox.showinfo("Skóre", "Najvyššie zahrané skóre")

def showOptions():
    PlaySound('buttonClick.wav', 1)
    messagebox.showinfo("Nastavenia", "Nastavenia hry si zmeň v zdrojovom kode")

def showHelp():
    PlaySound('buttonClick.wav', 1)
    messagebox.showinfo("Pomoc", "V tejto hre je tvojou úlohou skladať platné slová z ponúkaných písmen, aby si porazil nepriateľov v dungeonoch. Každé správne slovo poškodí nepriateľa a získaš zaň XP (skúsenostné body). Postupne tak môžeš prejsť všetky levely.")

def showAbout():
    PlaySound('buttonClick.wav', 1)
    messagebox.showinfo("O hre", "Semestrálna práca (Letný semester) - Marek Kerata")

#------#
# MAPA #
#------#
def createMap():
    levelWin = tk.Tk()
    levelWin.title("Level Selection")

    menuCanvas = tk.Canvas(levelWin, bg='red', width=500, height=500)
    menuCanvas.pack()
    
    level1Button = tk.Button(levelWin, text='Level 1', font=('Arial', 30), command=lambda: startLevel(levelWin, 1))
    menuCanvas.create_window(250, 150, window=level1Button)

    if dungeonLevel  >= 2:
        level2Button = tk.Button(levelWin, text='Level 2', font=('Arial', 30), command=lambda: startLevel(levelWin, 2))
        menuCanvas.create_window(250, 250, window=level2Button)
    else:
        menuCanvas.create_text(250, 250, text="Level 2 zamknutý", font=('Arial', 30))

    if dungeonLevel  >= 3:
        level3Button = tk.Button(levelWin, text='Level 3', font=('Arial', 30), command=lambda: startLevel(levelWin, 3))
        menuCanvas.create_window(250, 350, window=level3Button)
    else:
        menuCanvas.create_text(250, 350, text="Level 3 zamknutý", font=('Arial', 30))
    
    # nastavit cez return ako cislo mapy, a potom vytvorit game
    
def startLevel(levelWin, level):
    global unlockedLevels, dungeonLevel, enemyCount
    dungeonLevel = level
    enemyCount = level + 1
    levelWin.destroy()
    createGame(level)


#-----#
# HRA #
#-----#

#----------#
# PREMENNE #
#----------#


dungeonLevel = 1 
unlockedLevels = 1
playerHealth = 100
score = 100
enemyCount = 1
frameImgs = []
usedWords = []
letters = []
letterButtons = []
actionButtons = []
selectedLetters = []
clickedOrder = []
enemies = []
batImgs = []
slimeImgs = []
animationID = None  
currentImg = 0     
enemy = None  
xp = 0
helpUnlocked = False
wordsGuessed = 0



def makeActionButtons():
    global actionButtons, helpButton
    actionButtons = []

    submitButton = tk.Button(
        actionFrame,
        text="Potvrď slovo",
        bg='green',
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
        bg='blue',
        font=("ARIAL", 14),
        width=12,
        height=1,
        command=shuffleLetters
    ).grid(row=0, column=2, padx=5, pady=10)
    actionButtons.append(jumbleButton)

    helpButton = tk.Button(
        actionFrame,
        text="Pomoc",
        bg='white' if helpUnlocked else 'gray',
        font=("ARIAL", 14),
        width=12,
        height=1,
        command=finishWord,
        state = tk.NORMAL if helpUnlocked else tk.DISABLED
    )
    helpButton.grid(row=0, column=3, padx=5, pady=10)
    actionButtons.append(helpButton)

#min 3 znaky, musi byt vo wordList, nesmie byt pouzite, da sa urobit z dostupnych pismen
def submitWord():
    global usedWords, letters, clickedOrder, selectedLetters, playerHealth, wordsGuessed
    print("POTVRD SLOVO TLACIDIELKO BOLO STLACENE")
    currentWord = ""
    
    for b in clickedOrder:
        currentWord += b['text'].lower()
    if isValidWord(currentWord):
        print("Platné slovo:", currentWord)
        usedWords.append(currentWord)
        wordsGuessed += 1
        damageEnemy(currentWord)
        
        if (playerHealth+20) <= 100:
            playerHealth += 20
        else:
            playerHealth = 100
            
        for b in clickedOrder:
            b.config(state='normal')
            b.grid(row=0, column=letterButtons.index(b)+1, padx=5)
        
        clickedOrder = []
        selectedLetters = []
        
        if wordsGuessed >= 3:
            wordsGuessed = 0 
            messagebox.showinfo("Info", "Uhádol si 3 slová! Generujem nové písmená.")
            generateLetters()
            usedWords = []
            makeLetterButtons()
            drawLetters()
            
        if not canMakeWords(letters, wordList, usedWords):
            messagebox.showinfo("Info", "Uhádol si všetky možné slová! Pridávam nové písmená.")
            generateLetters()
            makeLetterButtons()
            drawLetters()
    else:
        print("Neplatné slovo")
        resetLetters()

def resetLetters():
    global selectedLetters, clickedOrder
    print("RESET LETTERS TLACIDIELKO BOLO STLACENE")
    selectedLetters.clear()
    
    for b in clickedOrder:
        if b in letterButtons:
            b.config(state='normal')
            b.grid(row=0, column=letterButtons.index(b)+1, padx=5)
    
    clickedOrder.clear()
    print("pismenka obnovene do povodneho stavu")
    
def shuffleLetters():
    print("JUMBLE LETTERS TLACIDIELKO BOLO STLACENE")
    rnd.shuffle(letterButtons)
    drawLetters()
    resetLetters()

def finishWord():
    global xp
    possibleWords = []
    
    if xp >= 100:
        xp -= 100
        updateXpText()
    else:
        messagebox.showinfo("Nedostatok XP", "Nemáš dostatok XP na použitie pomoci!")
        return
    
    for word in wordList:
        if len(word) < 3:
            continue
        tempLetters = letters.copy()
        isValid = True
        for letter in word:
            if letter in tempLetters:
                tempLetters.remove(letter)
            else:
                isValid = False
                break
        if isValid and word not in usedWords:
            possibleWords.append(word)
    
    if possibleWords:
        possibleWords.sort(key=len, reverse=True)
        suggestedWord = possibleWords[0]
        messagebox.showinfo("Pomoc", "Slovo: " + suggestedWord)
    else:
        messagebox.showinfo("Pomoc", "Žiadne nové slová sa nedajú vytvoriť z týchto písmen")

def loadImgs():
    global batImgs, slimeImgs
    global frameImgs

    batImgs = []
    slimeImgs = []
    try:
        for i in range(15):
            img = Image.open(f"sprites/bat/bat{i}.png")
            batImgs.append(ImageTk.PhotoImage(img, master=game))
        
        #frameImgs.append(Image.open("sprites/enemyFrameBg.png"))
        #print("nacitane")

        print("nacitavanie obrazkov Slime")
        for i in range(6):
            img = Image.open(f"sprites/slime/slime{i}.png")
            slimeImgs.append(ImageTk.PhotoImage(img, master=game))
    except Exception as e:
        print("chyba pri nacitani obrazkov: " + str(e))

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
        
def makeLetterButtons():
    global letterButtons
    for btn in letterButtons:
        btn.destroy()
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
    
def drawLetters():
    i = 1
    for b in letterButtons:
        b.grid(row=0, column=i, padx=5)
        i+=1

def canMakeWords(currentLetters, wordList, usedWords):
    availableLetters = currentLetters.copy()
    possibleWords = []
    
    for word in wordList:
        if word in usedWords or len(word) < 3:
            continue
            
        tmpLetters = availableLetters.copy()
        valid = True
        for letter in word:
            if letter in tmpLetters:
                tmpLetters.remove(letter)
            else:
                valid = False
                break
                
        if valid:
            possibleWords.append(word)
    
    return len(possibleWords) > 0

# TODO nevyuzita funkcia 
def generateLettersOUTDATED():
    global dungeonLevel, letters
    letters = []
    letterCount = 5 + dungeonLevel * 2
    
    while len(letters) < letterCount:
        newLetter = chr(rnd.randint(97, 122))
        #if newLetter not in letters and newLetter not in ["x", "w", "q"]:
        if newLetter not in ["x", "w", "q"]:
            letters.append(newLetter)
    print("vytvorene pismena:", letters)

def generateLetters():
    global dungeonLevel, letters
    
    letters = []
    letterCount = 5 + dungeonLevel * 2
    word = rnd.choice([w for w in wordList if len(w) <= letterCount])
    letters = list(word)
    
    #+random pismena
    while len(letters) < letterCount:
        letters.append(chr(rnd.randint(97, 122)))  # a-z
    
    rnd.shuffle(letters)
    print("vygenerovane pismena:", letters, "base slovo:", word)
    
def updateGameAfterWord(word):
    global letters, clickedOrder, selectedLetters
    
    for char in word:
        if char in letters:
            letters.remove(char)
            
    newLettersCount = 2 + dungeonLevel // 2
    for i in range(newLettersCount):
        letters.append(chr(rnd.randint(97, 122)))
    
    clickedOrder = []
    selectedLetters = []
    
    #reset ui
    makeLetterButtons()
    drawLetters()
    
def isValidWord(word):
    if len(word) < 3:
        return False
    if word not in wordList:
        messagebox.showinfo("Info", "Slovo nie je v zozname slov.")
        return False
    if word in usedWords:
        messagebox.showinfo("Info", "Slovo už bolo použité")
        return False

    return True 
  
def draw():
    pass
    
def createEnemies(level, enemyType=None):
    global enemy, animationID
    
    enemyTypes = ["bat", "slime"]

    if enemyType is None:
        enemyType = rnd.choice(enemyTypes)
    
    if animationID:
        enemyCanvas.after_cancel(animationID)
        animationID = None
    enemyCanvas.delete("enemy")
    
    firstImg = batImgs[0] 
    enemyHp = 70
    match enemyType:
        case "bat":  
            firstImg = batImgs[0]
            enemyHp = 50
            posX = 150
            posY = 150
            logText("Stretol netopiera")
        case "slime":
            firstImg = slimeImgs[0]
            enemyHp = 80
            posX = 130
            posY = 200
            logText("Stretol si slajma")
        case _ :
            enemyHp = 50
            firstImg = batImgs[0]
            posX = 150
            posY = 150
            logText("Stretol si netopiera")
            
    enemy = {
        "type": enemyType,
        "hp": enemyHp+(30*level),
        "sound": "este neni, napotom",
        "id": enemyCanvas.create_image(posX, posY, image=firstImg, tags="enemy")
    }
    enemies.append(enemy)
    animateEnemies()

def animateEnemies():
    global currentImg, animationID
    
    if not enemy:
        return
    
    imgList = []
    if enemy["type"] == "bat":
        imgList = batImgs
    elif enemy["type"] == "slime":
        imgList = slimeImgs
    else:
        imgList = slimeImgs
        
        
    currentImg = (currentImg + 1) % len(imgList)
    enemyCanvas.itemconfig(enemy["id"], image=imgList[currentImg])
    # 100ms = 10 FPS
    
    if enemy["type"] == "bat":
        animationID = enemyCanvas.after(100, animateEnemies)
    else:
        animationID = enemyCanvas.after(170, animateEnemies)

def damageEnemy(word):
    global xp, helpUnlocked, dungeonLevel, enemyCount
    
    #finishWord()
    dmg = 10*len(word)
    
    xpGain = 50 + (dungeonLevel * 20)
    xp += xpGain
    logText(f"Získal si {xpGain} XP!", "yellow")
    updateXpText()
    print("XP: " + str(xp))
    
    if not helpUnlocked and xp >= 100:
        helpUnlocked = True
        logText("Pomoc tlacidlo bolo odomknute!", "green")
        
        helpButton.config(bg='white', state=tk.NORMAL)
        
    currentEnemy = enemies[-1]
    currentEnemy["hp"]-=dmg
    print(currentEnemy["hp"])
    updateEnemyHeatlh(currentEnemy["hp"])
    updateHealthText()
    logText(giveEnemyName(currentEnemy) + " stratil " + str(dmg) + " bodov zo života")
    
    if currentEnemy["hp"] <= 0:
        #print("netopierik zomrel :((")
        healPlayer(20)
        #messagebox.showinfo("sadge", "netopierik zomrel :((")
        logText(f"Porazil si {giveEnemyName(currentEnemy)}!", "red")
        
        destroyEnemy(currentEnemy)
        enemyCount -= 1
        
        if enemyCount > 0:
            createEnemies(dungeonLevel)
            updateEnemyHeatlh(enemies[-1]["hp"])
            updateHealthText()
        else:
            
            if dungeonLevel < 3:
                dungeonLevel += 1
                messagebox.showinfo("Level dokončený", f"Postúpil si na level {dungeonLevel}!")
                game.destroy()
                createMap()
            else:
                messagebox.showinfo("Gratulujem!", "Dokončil si všetky levely!")
                game.destroy()
        
def updateXpText():
    global xpLab, helpButton
    xpLab.config(text=str(xp) + "/100")
    
    
def updateEnemyHeatlh(health):
    for i in range(5):
        remainingHealth = health - (i * 20)
        if remainingHealth >= 20:
            newImage = heartImages['FULL']# full heart - 20 HP
        elif remainingHealth >= 10:
            newImage = heartImages['HALF']# half heart - 10 HP
        else:
            newImage = heartImages['EMPTY']# empty heart - 0 HP
            
        enemyHearts[i].config(image=newImage)
        enemyHearts[i].image = newImage

def destroyEnemy(enemy):
    global animationID
    if animationID:
        enemyCanvas.after_cancel(animationID)
        animationID = None
        
    enemyCanvas.delete(enemy["id"])
    if enemy in enemies:
        enemies.remove(enemy)
    
def healPlayer(amount):
    global playerHealth
    if (playerHealth+amount) > 100:
        playerHealth = 100
    else:
        playerHealth += amount
        
def decreasePlayerHealth():
    global playerHealth, healthDecreaseTimer
    
    if playerHealth > 0:
        playerHealth -= 5 
        print(f"player health: {playerHealth}")
        
        # TODO: updatnut playerhealth displej
        
    if playerHealth <= 0:
        print("skapal si")
        if healthDecreaseTimer:
            game.after_cancel(healthDecreaseTimer)
            healthDecreaseTimer = None
        PlaySound(None, 0)  # Zastavi všetky zvuky
        messagebox.showinfo("Koniec hry", "Zomrel si!")
        game.destroy()
        return
        
    updatePlayerHealth(playerHealth)
    healthDecreaseTimer = game.after(5000, decreasePlayerHealth)

def drawEnemyHealth():
    global enemyHearts, heartImages
    try:
        enemyHearts = []
        heartImages = {
            'FULL' : ImageTk.PhotoImage(Image.open("sprites/heartFULL.png")),
            'HALF' : ImageTk.PhotoImage(Image.open("sprites/heartHALF.png")),
            'EMPTY' : ImageTk.PhotoImage(Image.open("sprites/heartEMPTY.png"))
        }
    
        heart1Label = tk.Label(statsFrame, image=heartImages['FULL'], bd=0, highlightthickness=0, relief='flat')
        heart1Label.place(x=16, y=12)
        enemyHearts.append(heart1Label)
    
        heart2Label = tk.Label(statsFrame, image=heartImages['FULL'], bd=0, highlightthickness=0, relief='flat')
        heart2Label.place(x=16, y=68)
        enemyHearts.append(heart2Label)
        
        heart3Label = tk.Label(statsFrame, image=heartImages['FULL'], bd=0, highlightthickness=0, relief='flat')
        heart3Label.place(x=16, y=124)
        enemyHearts.append(heart3Label)
        
        heart4Label = tk.Label(statsFrame, image=heartImages['FULL'], bd=0, highlightthickness=0, relief='flat')
        heart4Label.place(x=16, y=180)
        enemyHearts.append(heart4Label)
        
        heart5Label = tk.Label(statsFrame, image=heartImages['FULL'], bd=0, highlightthickness=0, relief='flat')
        heart5Label.place(x=16, y=236)
        enemyHearts.append(heart5Label)
      
    except Exception:
        print("chyba pri nacitani heart img") 

def updatePlayerHealth(health):
    for i in range(5):
        remainingHealth = health - (i * 20)
        if remainingHealth >= 20:
            newImage = playerHeartImages['FULL'] # full heart - 20 HP
        elif remainingHealth >= 10:
            newImage = playerHeartImages['HALF'] # half heart - 10 HP
        else:
            newImage = playerHeartImages['EMPTY'] # empty heart - 0 HP
            
        playerHearts[i].config(image=newImage)
        playerHearts[i].image = newImage
    
    updateHealthText()

def drawPlayerHealth():
    global playerHearts, playerHeartImages
    try:
        playerHearts = []
        playerHeartImages = {
            'FULL' : ImageTk.PhotoImage(Image.open("sprites/playerHeartFULL.png")),
            'HALF' : ImageTk.PhotoImage(Image.open("sprites/playerHeartHALF.png")),
            'EMPTY' : ImageTk.PhotoImage(Image.open("sprites/heartEMPTY.png"))
        }
        
        heart1Label = tk.Label(statsFrame, image=playerHeartImages['FULL'], bd=0, highlightthickness=0, relief='flat')
        heart1Label.place(x=540, y=12)
        playerHearts.append(heart1Label)
    
        heart2Label = tk.Label(statsFrame, image=playerHeartImages['FULL'], bd=0, highlightthickness=0, relief='flat')
        heart2Label.place(x=540, y=68)
        playerHearts.append(heart2Label)
        
        heart3Label = tk.Label(statsFrame, image=playerHeartImages['FULL'], bd=0, highlightthickness=0, relief='flat')
        heart3Label.place(x=540, y=124)
        playerHearts.append(heart3Label)
        
        heart4Label = tk.Label(statsFrame, image=playerHeartImages['FULL'], bd=0, highlightthickness=0, relief='flat')
        heart4Label.place(x=540, y=180)
        playerHearts.append(heart4Label)
        
        heart5Label = tk.Label(statsFrame, image=playerHeartImages['FULL'], bd=0, highlightthickness=0, relief='flat')
        heart5Label.place(x=540, y=236)
        playerHearts.append(heart5Label)
        
    except Exception:
        print("chyba pri nacitani obrazkov srdiecka (hrac) ")

def healthText():
    global enemyHealthText, playerHealthText
    currentEnemy = enemies[-1]
    enemyHealthText = tk.Label(
        statsFrame,
        text="Život: " + str(currentEnemy["hp"]),
        font=('ARIAL', 35),
        bg='#7F7F7F',
        fg='red'
        )
    playerHealthText = tk.Label(
        statsFrame, 
        text = ("Život: " + str(playerHealth)),
        font = ('ARIAL', 35), 
        bg = '#7F7F7F', 
        fg = 'cyan'
        )
    
    enemyHealthText.place(x=295, rely=0.12, anchor='ne')
    playerHealthText.place(x=310,  rely=0.12, anchor='nw')
    
def updateHealthText():
    currentEnemy = enemies[-1]
    enemyHealthText.config(text="Život: "+str(currentEnemy["hp"]))
    playerHealthText.config(text="Život: " + str(playerHealth))

def giveEnemyName(enemyType):
    match enemyType:
        case "bat":
            return "Netopier"
        case "slime":
            return "Slime"
        case _:
            Exception("giveEnemyType: nenasiel sa nazov, davam default")
            return "Netopier"

def logText(text, color="white"):
    textLog.config(state='normal')
    if color != "white":
        textLog.tag_config(color, foreground=color, font = ("ARIAL", 14, "bold"))
        textLog.insert(tk.END, text + "\n", color)
    else:
        textLog.insert(tk.END, text + "\n")
    textLog.see(tk.END)
    textLog.config(state='normal')

def statsText():
    global xpLab
    
    currentEnemy = enemies[-1]
    enemyName = tk.Label(
        statsFrame, 
        text="Nepriateľ: " + giveEnemyName(currentEnemy["type"]), 
        font = tkfont.Font(family='Helvetica', size=20, weight='bold'),
        bg="#7F7F7F", fg="cyan"
        )
    dungeonLvl = tk.Label(
        statsFrame,
        text="Dungeon level: " + str(dungeonLevel),
        font = tkfont.Font(family='Helvetica', size=20, weight='bold'),
        bg="#7F7F7F", fg="cyan"
        )
    scoreLab = tk.Label(
        statsFrame,
        text="Skóre: " + str(score),
        font = tkfont.Font(family='Helvetica', size=20, weight='bold'),
        bg="#7F7F7F", fg="yellow"
        )
    xpLab = tk.Label(
        statsFrame,
        text=f"XP: {xp}/100",
        font = tkfont.Font(family='Helvetica', size=20, weight='bold'),
        bg="#7F7F7F", fg="yellow"
        )
    enemyName.place(x=100, y=150)
    dungeonLvl.place(x=100, y=220)
    scoreLab.place(x=380, y=150)
    xpLab.place(x=380, y=220)
    
def loadWordList():
    global wordList
    wordList = []
    try:
        file = open("slovnik.txt", "r", encoding="utf-8")
        while True:
            line = file.readline()
            if not line:
                break
            
            strippedWord = line.strip().lower()
            if len(strippedWord) >= 3:
                wordList.append(strippedWord)
                
        file.close()
    except Exception as e:
        print(e)
        print("nenacitali sa slova")
        wordList = ['byt', 'strom', 'jaskyna', 'kuzlo', 'pismeno', 'hra', 'poklad', 'dungeon']

def endGame():
    global animationID, healthDecreaseTimer, game
    #game.after_cancel(animationID)
    #game.after_cancel(healthDecreaseTimer)
    #game.destroy()
    
    if animationID:
        game.after_cancel(animationID)
        animationID = None
        
    if healthDecreaseTimer:
        game.after_cancel(healthDecreaseTimer)
        healthDecreaseTimer = None
    PlaySound(None, 0)

    if game:
        game.destroy()
        game = None

def createGame(level):
    global game, enemyCanvas,statsFrame, textFrame, lettersFrame, actionFrame, textLog
    global playerHealth, enemies, usedWords, letters, clickedOrder, selectedLetters, letterButtons
    global xp, helpUnlocked, wordsGuessed
    
    playerHealth = 100
    enemies = []
    usedWords = []
    letters = []
    clickedOrder = []
    selectedLetters = []
    letterButtons = []
    helpUnlocked = False
    wordsGuessed = 0
    
    game = tk.Tk()
    game.title("FEIT Crawler - Hra")
    #game.geometry("800x700")
    
    def onGameClose():
        PlaySound(None, 0)
        game.destroy()
    game.protocol("WM_DELETE_WINDOW", onGameClose)
    
    loadImgs()
    loadWordList()
    
    # ENEMY CANVAS
    enemyCanvas = tk.Canvas(game, width=300, height=300, highlightthickness=0)
    enemyCanvas.grid(row=0, column=0, sticky="nsew")
    enemyCanvas.grid_propagate(False)
    enemyBgImg = ImageTk.PhotoImage(Image.open("sprites/enemyFrameBg.png"))
    enemyCanvas.background = enemyBgImg
    enemyCanvas.create_image(0, 0, anchor="nw", image=enemyBgImg)
    
    statsFrame = tk.Frame(game, bg="yellow", width=600, height=300)
    img = ImageTk.PhotoImage(Image.open("sprites/statsFrameBg.png"))
    textFrameBgLabel = tk.Label(statsFrame, fg='cyan', compound='center', image=img)
    textFrameBgLabel.image = img
    textFrameBgLabel.place(x=0, y=0, relwidth=1, relheight=1)
    
    # TEXT FRAME #
    textFrame = tk.Frame(game, width=900, height=100)
    textFrame.grid_propagate(False)
    
    bgImg = ImageTk.PhotoImage(Image.open("sprites/textFrameBg.png"))
    bgLabel = tk.Label(textFrame, image=bgImg)
    bgLabel.image = bgImg
    bgLabel.place(x=0, y=0, relwidth=1, relheight=1)
    
    logFrame = tk.Frame(textFrame, bg='#7F7F7F')
    logFrame.place(relx=0.5, rely=0.5, anchor="center", width=870, height=80)
    
    textScroll = tk.Scrollbar(logFrame)
    textLog = tk.Text(
        logFrame,
        wrap=tk.WORD,
        yscrollcommand=textScroll.set,
        bg='#7F7F7F',
        fg='white',
        font=('Arial', 16, 'bold'),
        padx=10,
        pady=5,
        state='normal',
        borderwidth=10
    )
    textScroll.config(command=textLog.yview)
    textLog.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    textScroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    # LETTERS FRAME #
    lettersFrame = tk.Frame(game, bg="black", width=900, height=100)
    img = ImageTk.PhotoImage(Image.open("sprites/lettersFrameBg.png"))
    textFrameBgLabel = tk.Label(lettersFrame, compound='center', image=img)
    textFrameBgLabel.image = img
    textFrameBgLabel.place(x=0, y=0, relwidth=1, relheight=1)
    
    # ACTION FRAME #
    actionFrame = tk.Frame(game, bg="blue", width=900, height=80)
    img = ImageTk.PhotoImage(Image.open("sprites/actionFrameBg.png"))
    textFrameBgLabel = tk.Label(actionFrame, compound='center', image=img)
    textFrameBgLabel.image = img
    textFrameBgLabel.place(x=0, y=0, relwidth=1, relheight=1)
    
    statsFrame.grid_propagate(False)
    textFrame.grid_propagate(False)
    lettersFrame.grid_propagate(False)
    actionFrame.grid_propagate(False)

    statsFrame.grid(row=0, column=1, columnspan=2, sticky="nsew")
    textFrame.grid(row=1, column=0, columnspan=3, sticky="nsew")
    lettersFrame.grid(row=2, column=0, columnspan=3, sticky="nsew")
    actionFrame.grid(row=3, column=0, columnspan=3, sticky="nsew")
    
    # SRDIECKA
    drawEnemyHealth()
    drawPlayerHealth()
    
    # PISMENA-LettersFrame
    generateLetters()
    makeLetterButtons()
    drawLetters()
    
    # enemiesFrame
    #createEnemies(level, "slime")
    for _ in range(enemyCount):
        createEnemies(level)
    
    # statsFrame texty
    healthText()
    statsText()
    
    # actionFrame
    makeActionButtons()
    
    # ostatne
    PlaySound('theme.wav', 1)
    decreasePlayerHealth()
    
#-------#
# START #
#-------#
    
def onStartup():
    win = tk.Tk()
    win.title("Dungeon Crawler")
    win.geometry("960x640")
    win.focus()
    createMenu(win)
    return win


# startup
root = onStartup()
root.mainloop()