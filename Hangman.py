import random
import csv

def HangManWordSetUp(randomWord):
    setupString = list()
    for i in range(10):
        setupString += " "
    length = len(randomWord)
    i = 0
    while i < length:
        setupString += "_ "
        i += 1
    for item in setupString:
        print(item, end="")
    print("\n")

def HangManGame():
    print("""
             /|HANGMAN
           O/ |Guess the Word
              |Or Leave Him Hanging
              |Let's Begin!\n""")

    with open('hangmanWords.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        HangmanWordList = list()
        for word in reader:
            HangmanWordList.append(word)
            
    randomWord = str(random.choice(HangmanWordList))
    HangManWordSetUp(randomWord)
    guess = ''
    number_of_guesses = 5
    
    while number_of_guesses != 0:
        guess = input(f"You have {number_of_guesses} guesses\nEnter a letter A-Z: ")
        guess.lower()
        index = randomwWord.find(guess)
        if index != -1:
            
        
        
                            
if __name__ == "__main__":
    HangManGame()
