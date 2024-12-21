import random
import csv
import os
from openai import OpenAI
from dotenv import load_dotenv


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
    
    if number_of_guesses == 6:
        print("""
                /|HANGMAN
               / |Guess the Word
                 |Or Leave Him Hanging
                 |\n""")
        
    elif number_of_guesses == 5:
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

#Function that calls a free API which will generate a hint for the randomWord chosen by the game
#Takes randomWord as a parameter to tell the function what random word has been chosen
#The prompt ensures that the randomWord will not be revealed to the user in the response
#And we limit the response to the 10 tokens.
def AI_Hint_Generator(randomWord):
    #Site where API is pulled from
    base_url = "https://api.aimlapi.com/v1"
    load_dotenv()
    OPEN_API_KEY = os.environ.get('OPEN_API_KEY')
    system_prompt = f"You give hints about words for a game called Hangman. Give concise but helpful answers and DO NOT use {randomWord} in the response."
    user_prompt = f"Give me a hint for the word {randomWord}. Do not use {randomWord} in the sentence."

    api = OpenAI(api_key=OPEN_API_KEY, base_url=base_url)
    
    try:
        completion = api.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=10,
        )
        
        response = completion.choices[0].message.content
        
        #Conditional and looping logic to ensure that all instances of the randomWord is not found in the hint
        if randomWord in response:
            response = response.replace(randomWord, "__")
                
        print("Hint:", response)
        return response
    
    except:
        print("You are out of API requests for the hour.\nKeep playing.")

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
            / |Guess the Word
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
    randomWord = random.choice(HangmanWordList).pop()
    
    #Function that uses a free AI API to generate a hint for the user based on the randomWord given
    hintMessage = AI_Hint_Generator(randomWord)
    
    #guessedWord is a list that holds the current state of the guessed word
    guessedWord = HangManWordSetUp(randomWord)
    
    #initialize number_of_guesses to 6, the number of guessed allowed per game
    number_of_guesses = 6
    
    #initialize correct_guesses to 0
    correct_guesses = 0
    
    #list that holds the letters that have already been guessed 
    already_guessed = [" "]
    
    
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
        
        #Checking if the guess is in already_guessed, and passing the main game loop if it is.
        if guess in already_guessed:
            print(f"\n|||Already Guessed {guess.title()}|||")
        else:
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
                #increment correct_guesses
                correct_guesses += 1
                #if user wins, ask to restart game
                if correct_guesses == len(randomWord):
                    restart = input("Play Again?\n[yes/no]: ")
                    if restart == 'yes':
                        HangManGame()
                    else:
                        print("Thanks for Playing!")
                        
        #########################################################################################################################
        ####### Functions and statements that happen in every conditional statment and loop: Put at end of inner game logic #####
        #########################################################################################################################
        
        #Update number_of_guesses and call HangManImageUpdate to update current game state
        number_of_guesses = HangManImageUpdate(index, number_of_guesses)
        #Update current guessedWord list and print out the word state logic
        HangManWordUpdate(guessedWord)
        #Print the message hint for the user each loop
        print("Hint:", hintMessage)
        #Add guessed letter to already guessed list
        already_guessed.append(guess)
            
                 
#Main function to call the HangManGame           
if __name__ == "__main__":
    HangManGame()
