import random
import csv

#Function that updates the Hangman gamestate taking the index of the find function into account.
#If the guessed letter is found in the randomWord, the index will not be -1 and we won't decrement number_of_guesses
#But if index is = -1, we will decrement number_of_guesses
#We will print out the corresponding hangman gamestate based on the # of remaining guesses
#We will also return the number_of_guesses which will update the number of tries left for the user in the while loop
def HangManImageUpdate(index, number_of_guesses):
    if index != -1:
        pass
    else:
        number_of_guesses -= 1
    
    
    if number_of_guesses == 5:
        print("""
                /|HANGMAN
              O/ |Guess the Word
                 |Or Leave Him Hanging
                 |\n""")
         
    elif number_of_guesses == 4:
        print("""
                /|HANGMAN
              O/ |Guess the Word
             /   |Or Leave Him Hanging
                 |\n""")
          
    elif number_of_guesses == 3:
        print("""
                /|HANGMAN
              O/ |Guess the Word
             /|  |Or Leave Him Hanging
                 |\n""")
        
    elif number_of_guesses == 2:
        print("""
                /|HANGMAN
              O/ |Guess the Word
             /|\ |Or Leave Him Hanging
                 |\n""")
        
    elif number_of_guesses == 1:
        print("""
                /|HANGMAN
              O/ |Guess the Word
             /|\ |Or Leave Him Hanging
             /   |\n""")
        
    elif number_of_guesses == 0:
        restart = input("""
                /|HANGMAN
              O/ |Game Over
             /|\ |Try Again?
             / \ |\n
         
         [yes/no]: """)
        if restart == 'yes':
            HangManGame()
        else:
            print("Thanks for Playing!")

        
    return number_of_guesses
        
#Function Prints out the current state of the guessed word
#Takes guessedWord as the argument, holding the current state of the guessed word 
def HangManWordUpdate(guessedWord):
    #for loop that prints out some whitespace for better look
    for i in range(10):
        print(" ", end="")
    #for loop that prints out guessedWord
    for item in guessedWord:
        print(item + " ", end="")
    print("\n")

#Function that creates a list guessedWord holding the current state of the guessed word
#We first add a number of underscores to guessedWord based on the length of the randomWord
#We then print out guessedWord each time we call the function 
def HangManWordSetUp(randomWord):
    guessedWord = list()
    #for loop that prints out some whitespace
    for i in range(10):
        print(" ", end="")
    #hold the length of randomWord
    length = len(randomWord)
    i = 0
    #while loop that adds underscores
    while i < length:
        guessedWord += "_"
        i += 1
    #for loop to print out guessedWord
    for item in guessedWord:
        print(item + " ", end="")
    print("\n")
    
    return guessedWord

#Function that finds duplicate instances of a letter in a word 
#This allows us to print multiple instances of a letter for one guess
def find_nth(haystack: str, needle: str, n: int) -> int:
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

#Main function holding the game logic for our Hangman Game
def HangManGame():
    #Print starting game state and opening screen
    print("""
             /|HANGMAN
           O/ |Guess the Word
              |Or Leave Him Hanging
              |Let's Begin!\n""")

    #open and read our csv file which holds 100 unique words to randomly choose from
    #add the words to a list which we can call the random choice function on
    with open('hangmanWords.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        HangmanWordList = list()
        for word in reader:
            HangmanWordList.append(word)
    
    #randomWord holds an str that pulls a random word from the HangmanWordList and pops that word
    #from the list so that we return a str and not a list value    
    randomWord = 'banana'
    
    #guessedWord is a list that holds the current state of the guessed word
    guessedWord = HangManWordSetUp(randomWord)
    
    #initialize number_of_guesses to 5, the number of guessed allowed per game
    number_of_guesses = 5
    
    #initialize correct_guesses to 0
    correct_guesses = 0
    
    #While loop holding the main game logic, stops when number_of_guesses != 0 or correct_guesses != len(randomWord)
    while number_of_guesses != 0 and correct_guesses-1 != len(randomWord):
        #initialize guess to empty string
        guess = ''
        
        #intialize duplicates to 0 which determines if there are duplicate letters for a guess within the random word
        duplicates = 0
        
        #input for guess
        guess = input(f"You have {number_of_guesses} guesses\nEnter a letter A-Z: ")
        #make guess lowercase
        guess = guess.lower()
        #Holds the index of the guessed letter in the randomWord
        index = randomWord.find(guess)
        
        #for loop that checks if there are duplicate letters of the guessed letter
        for letter in randomWord:
            if letter == guess:
                duplicates += 1
        #Conditional statement that checks if duplicates > 1
        #If so, then use the find_nth function and add all instances of the duplicate letter to the guessedWord list
        if duplicates > 1:
            while duplicates > 0:
                #Set index == the last instance of the duplicate letter, working backwards
                index = find_nth(randomWord, guess, duplicates)
                #Replace the underscore in guessedWord with the correct letter guessed
                guessedWord[index] = guess
                #decrement duplicates
                duplicates -= 1
                #increment correct_guesses
                correct_guesses += 1
            #Update number_of_guesses and call HangManImageUpdate to update current game state
            number_of_guesses = HangManImageUpdate(index, number_of_guesses)
            #Update current guessedWord list and print out the word state logic
            HangManWordUpdate(guessedWord)
            #if user wins, ask to restart game
            if correct_guesses == len(randomWord):
                restart = input("Play Again?\n[yes/no]: ")
                if restart == 'yes':
                    HangManGame()
                else:
                    print("Thanks for Playing!")
        #Conditional if guessed letter is correct but there is only 1 instance of that letter
        elif index != -1 and duplicates == 1:
            #Replace the underscore in guessedWord with the correct letter guessed
            guessedWord[index] = guess
            #Update number_of_guesses and call HangManImageUpdate to update current game state
            number_of_guesses = HangManImageUpdate(index, number_of_guesses)
            #Update current guessedWord list and print out the word state logic
            HangManWordUpdate(guessedWord)
            #increment correct_guesses
            correct_guesses += 1
            #if user wins, ask to restart game
            if correct_guesses == len(randomWord):
                restart = input("Play Again?\n[yes/no]: ")
                if restart == 'yes':
                    HangManGame()
                else:
                    print("Thanks for Playing!")
        #Conditional logic for when the user makes an incorrect guess
        else:
            number_of_guesses = HangManImageUpdate(index, number_of_guesses)
            HangManWordUpdate(guessedWord)
                 
#Main function to call the HangManGame           
if __name__ == "__main__":
    HangManGame()
