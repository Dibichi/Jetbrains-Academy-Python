import random

def hangman():
    x = 0
    print('H A N G M A N\n')
    wordList = ['python', 'java', 'kotlin', 'javascript']
    letterList = []
    randomWord = random.choice(wordList)
    guessWord = '-' * (len(randomWord))

    while guessWord != randomWord:
        index = 0
        print(guessWord)
        userInput = input('Input a letter:')
        if userInput in letterList:
            print('You already typed this letter\n')
            continue
        elif len(userInput) > 1:
            print('You should input a single letter\n')
            continue
        elif userInput.isascii() is False or userInput.islower() is False:
            print('It is not an ASCII lowercase letter\n')
            continue
        else:
            letterList.append(userInput)
        
        if userInput in randomWord:
            while True:
                try:
                    index = randomWord.index(userInput, index)
                except:
                    break
                
                guessWord = guessWord[:index] + userInput + guessWord[index + 1:]
                index += 1
        else:
            print('No such letter in the word')
            x += 1

        if x == 8:
            print('You are hanged!')
            break
        
        print('\n')
    else:
        print(randomWord)
        print('You guessed the word!\nYou survived!')

while True:
    playGame = input('Type "play" to play the game, "exit" to quit:')
    if playGame == "play":
        hangman()
    elif playGame == "exit":
        break
