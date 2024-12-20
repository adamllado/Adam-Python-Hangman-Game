import random
import csv

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
    guess = ''
    
    while number_of_guesses != 0:
        guess = input("")
                            
if __name__ == "__main__":
    HangManGame()
