"""
CodeMaster
CS50 Python Final Project by Amanda Flood
October 2022

An implementation of the classic 'Mastermind' game which inspired Wordle, using voice recognition.
The computer sets a hidden four-colour code and the player must guess this code within ten tries.
Each guess receives feedback in the form of white pegs, indicating the number of warm (right colour
wrong place) or hot (right colour right place) placements.
The code set by the computer is drawn from six colours, and can contain any number of colour repetitions.

The player can choose to make their guesses using verbal speech or keyboard input.

"""

import re
import random
import os

# used for mic input and speech recognition
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import soundfile

# frame rate p/sec and seconds
fs = 44100
seconds = 8

# used for ASCII art title text
from pyfiglet import Figlet
figlet = Figlet()
figlet.setFont(font='standard')


def main():
    '''
        Runs the game from first to last
    '''
    clear_screen()
    # ask if player wants letterl feedback as well as colour feedback
    check_letter_use()
    # ask if player wants to use spoken input
    verbal = check_speech_input()

    # start game
    # user can play over and over if required
    while True:
        wins = play(verbal)
        if wins >= 1:
            print(f'You win in {wins} goes! Well done!\n')
        else:
            print('Sorry. Game over!\n')

        # check if user wants to play again
        if play_again(input('Would you like to play again? (Y/N): ')):
            continue
        else:
            break


def play(verbal: bool) -> int:
    """
        Implements the logic for playing one game of CodeMaster
        Returns -1 if game lost, or the number of goes taken if game won
    """
    # introduce the game
    clear_screen()
    
    print('Welcome to CodeMaster! The computer has set a code using four coloured pegs, and it\'s your task to guess it.\n\
There are six possible colours to choose from, and there may be any number of colour repetitions in the code.\n\
\nYou have ten chances to guess the code correctly. Good luck!\n')

    # to store player guesses and their corresponding results
    guesses = []
    results = []

    # set a 4 colour code
    code = generate_code()

    # Play game until player wins or 10 wrong guesses made
    while True:
        if verbal == True:
            guess = get_verbal_guess()
            guesses.append(guess)
        else:
            # get a guess from the player, and add it to the history of guesses
            guess = get_guess()
            guesses.append(guess)

        # evaluate the guess and append the result to the history of results
        result = get_result(guess, code)
        results.append(result)

        # display full list of guesses alongside results
        display_results(guesses, results, code)

        # if player wins, return number of goes taken
        if result == (4, 0):
            return len(guesses)

        # if player loses, return -1
        if len(guesses) == 10 and result != (4, 0):
            return -1


def generate_code() -> str:
    """
        Generates a random colour code and returns it as a string
    """
    codemaster = []
    for _ in range(4):
        codemaster.append(random.choice(['R', 'G', 'W', 'Y', 'B', 'P']))
    return ''.join(codemaster)


def get_verbal_guess() -> str:
    """
        Uses Google speech recognition to parse the user's verbal input into a code
        Checks the code and if valid returns it to the play() function
    """
    # string showing acceptable colour names, each rendered in the appropriate colour
    colour_codes = colour.red + 'Red ' + colour.yellow + 'Yellow ' + colour.green + 'Green ' + colour.white + 'White ' + colour.cyan + 'Blue ' + colour.magenta + 'Purple' + colour.end

    while True:
        s = input(f'Press Enter when ready to guess from "{colour_codes}"')

        print(f'You have eight seconds to say your four colour guess:\n')
        # 8 sec recording, save as .wav file
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        print('Thanks!\n')
        write('output.wav', fs, myrecording)

        # convert file into a PCM wav using soundfile
        data, samplerate = soundfile.read('output.wav')
        soundfile.write('new.wav', data, samplerate, subtype='PCM_16')

        # create recognizer with speech_recognition module sr
        r = sr.Recognizer()

        # create audio file to pass to speech recognition
        spoken = sr.AudioFile('new.wav')
        with spoken as source:
            audio = r.record(source)

        # get a string of the recorded words from google
        try:
            s = r.recognize_google(audio).lower()
        except:
            # if no string of words exists
            print(f'Try waiting a second and then speak clearly, using four of the colour words below')
            # debug print(s)
            continue

        guess = []

        # split verbal string into individual words and go through in order,
        # adding colour initials to the guess
        wordlist = s.split(' ')
        for word in wordlist:
            if word in ('red', 'yellow', 'blue', 'green', 'white', 'pink', 'purple'):
                guess.append(word[0])

        # turn guessed code into a string
        guess = ''.join(guess).upper()

        # guess is valid
        if guess and check_valid(guess):
            return guess
        else:
            print(f'Try waiting a second then speak clearly, using four of the colour words below')
            #debug print(s)
            continue


def get_guess() -> str:
    """
        Asks the player to guess the code using text input, and returns the first valid guess as a string
    """
    # string showing acceptable colour initials, each rendered in the appropriate colour
    colour_codes = colour.red + 'R ' + colour.yellow + 'Y ' + colour.green + 'G ' + colour.white + 'W ' + colour.cyan + 'B ' + colour.magenta + 'P ' + colour.end

    # Get user input in the form of four colours
    while True:
        i = input('Your 4 colour code (' + colour_codes + '): ').strip().upper()
        # check if input is valid
        if check_valid(i):
            return i
        else:
            print('Please input 4 colour codes from this set: ' + colour_codes)
            continue


def check_valid(s: str) -> bool:
    """
        Takes in a string and checks if it is a valid 4 letter colour code
        Returns a bool
    """
    # using regex to check string
    matches = re.search(r'^[RGWYPB]{4}', s)
    if matches and len(s) == 4:
        return True
    else:
        return False


def get_result(guess: str, code: str) -> tuple:
    """
        Compares the player's guess to the hidden code and returns a tuple containing
        the number of hot (right colour correctly placed) and warm (right colour incorrectly placed) guesses
    """
    # Separate guess and code strings into lists of characters
    code_list = [*code]
    guess_list = [*guess]

    hot = 0
    warm = 0

    # populate dictionaries to count the distribution of colours in guess and code
    map_code = {}
    map_guess = {}
    for c in code_list:
        map_code[c] = map_code.get(c, 0) + 1
    for g in guess_list:
        map_guess[g] = map_guess.get(g, 0) + 1

    # check for hot matches and remove them from the codemap dictionary and the guess list
    for i in range(4):
        if guess_list[i] == code_list[i]:
            hot = hot + 1
            map_code[guess_list[i]] = map_code[guess_list[i]] - 1
            guess_list[i] = ''

    # then check the guess list again, this time looking for warm matches and removing them
    for j in range(4):
        if guess_list[j] in map_code and map_code[guess_list[j]] >= 1:
                warm = warm + 1
                map_code[guess_list[j]] = map_code[guess_list[j]] - 1

    result = (hot, warm)
    return result


def display_results(guesses: list, results: list, code: str):
    """
        Prints out every guess made so far beside its corresponding result
    """
    guessed_colours = {
        'P' : colour.magenta + counter.rect,
        'B' : colour.cyan + counter.rect,
        'W' : colour.white + counter.rect,
        'G' : colour.green + counter.rect,
        'Y' : colour.yellow + counter.rect,
        'R' : colour.red + counter.rect
    }

    #clear terminal and print a header
    clear_screen()

    print(counter.hot + '= a correct colour in the correct position    ', end ='')
    print(counter.warm + '= a correct colour in the wrong position\n')

    # display all the guesses
    for i in range(len(guesses)):
        # if user indicated they want it, print user's code in letters
        if wants_letters == True:
            print(guesses[i] + '   ', end = '')
        # print out the guess in coloured blocks
        for c in guesses[i]:
            print(guessed_colours[c] + ' ', end='')
        print(colour.end + '   ', end='')
        # then print the result
        for j in range(results[i][0]):
            print(counter.hot, end='')
        for k in range(results[i][1]):
            print(counter.warm, end = '')
        print('')
    print('')

    if len(guesses) == 10:
        if wants_letters == True:
            print(code + '   ', end = '')
        # print out the code in coloured blocks
        for c in code:
            print(guessed_colours[c] + ' ', end='')
        print(colour.end + '\n')


def check_letter_use():
    """
        Checks if player wants to see letter feedback, in case of colour-blindness / English
        as a second language
    """
    s = input('\nWelcome! Would you like to see letters displayed as well as colours? (Y/N) ').strip().lower()
    global wants_letters
    wants_letters = False
    # use regex to accept any answer beginning with y, otherwise a no is assumed
    matches = re.search(r'^y.*', s)
    if matches:
        wants_letters = True


def check_speech_input() -> bool:
    '''
        Asks player if they want speech input, returning y/n
    '''
    s = input('Would you like to use speech recognition to make your guesses? (Y/N) ').strip().lower()
    # assume initial y is a yes, otherwise no
    matches = re.search(r'^y.*', s)
    if matches:
        return True
    return False


def play_again(s: str) -> bool:
    """
        Checks if player would like another game, returning True or False
    """
    s = s.lower().strip()
    # use regex to find an initial y - otherwise assume a no
    ymatches = re.search('^y.*', s)
    if ymatches:
        return True
    else:
        return False


def clear_screen():
    """Clears screen for all terminal types and prints CodeMaster header"""
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')
    print(colour.blue + figlet.renderText('CodeMaster') + colour.end)


class colour:
    """ANSI escape sequences to colour the terminal output text"""
    magenta = '\033[95m'
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    white = '\033[97m'
    end = '\033[0m'


class counter:
    """Unicode characters for the colour rectangles and the feedback pegs"""
    warm = '\u25cf '
    hot = '\u25c9 '
    rect = '\u25ae'



if __name__ == '__main__':
    main()
