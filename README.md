CODEMASTER
CS50 Python Final Project
by Amanda Flood, October 2022

GAMEPLAY

A command-line implementation of the classic 'Mastermind' game, with the option of speech recognition input.

The computer sets a secret four-colour code and the player must guess this code within ten tries.
Each player guess receives feedback in the form of white pegs, indicating the number of warm (right colour wrong place) or hot (right colour right place) guesses.
The code set by the computer is drawn from six colours, and can contain any number of colour repetitions.

The player can choose to use speech recognition or text input to make their guesses.


PROJECT OVERVIEW

I wanted to make a game that would challenge my coding skills, be fun to play, and look good in the terminal shell.

I also wanted to give it a fun spin by implementing a speech recognition option for player input.


CHALLENGES

The major challenge was programme design. I wanted clear design logic which would be easy to read for others. I 'divided and conquered' by writing the game in pseudocode and assigning a function to each step.

Minor challenges included how to present the game in a clear and attractive manner, how to get player input, language and colour-blindness issues, and how to mark the player's guess against the hidden code.


DESIGN

The major challenge was designing a logical programme which could be easily read by others.

I implemented a separate play() function containing the logic for one game.
In main(), I implemented a while True loop so that the player could play repeatedly if they wished.

For a single game, the pseudocode logic is as follows:

- Generate the hidden code
= For up to ten turns, get the player's guess by text or spoken word
- Check the validity of the player's guess, and prompt again if it's not suitable
- Compare the validated guess against the code and calculate the number of warm and hot guesses made
- Display all guesses to date alongside their results, for player review
- Determine whether the player has won or lost the game

I separated each of these processes out into a function:

generate_code() - returns a randomly selected code

check_valid() - checks whether the player's guess meets the requirement of 4 valid colours

get_guess() - gets text input from command line, reprompts for invalid guesses and returns the first valid guess

get_verbal_guess() - gets spoken input, parses it, reprompts for invalid codes and returns the first validated guess

check_result() - compares player's guess against the hidden code and returns a tuple of (hot, warm) guesses

display_guesses() - clears screen and displays all guesses with their results

play() - conducts a single game and returns either win or lose to the main() function

I documented each function with type hints, docstrings and comments to ensure readability.

I used classes for ANSI escape sequence strings (colours) and Unicode sequence strings (counters), to make the setting of colour and counter more usable/readable.



PRESENTATION AND EASE OF PLAY

This was my second consideration. A game should be attractive and easy to play, with clear feedback given to the player.

Using the terminal created some constraints, and I thought about implementing the game in pygame. However, I've never worked with the command line, and wanted to create something in the terminal that looked good even given the constraints.

I used bright colours with a high contrast to one another, a clear layout, and simple Unicode characters to make the game as clean and attractive as possible.

I used ANSI escape string sequences to set text colour, and Unicode character strings for the coloured counters and feedback pegs.

It was not possible to increase the terminal font size programmatically - I did try. The player can do it themselves
if their shell allows.

Playing the game while scrolling down the command line worked, but was a bit messy-looking.
I decided clearing the terminal screen and setting a standard header would be most attractive and give the clearest feedback to the player.



PLAYER INPUT - SPOKEN AND TEXT

The original game of MasterMind is played with coloured pegs only, with no speech necessary.
However, in the terminal the user can only input text to the command line, raising the issue of how to ask for the player's guess.

I decided to give the player two options: standard text input, or verbal input using speech recognition.

Standard text input expects the first initial of the colour's name in English as the player's input.
To make it easier, the game presents a text prompt with each code initial displayed in the appropriate colour.

Verbal input expects the spoken English words for the colours. The game uses the speech_recognition module and Google to parse spoken input, searching it for the appropriate colours and converting them into a four letter code.



ACCESSIBILITY ISSUES - LANGUAGE AND COLOUR-BLINDNESS

Using text input creates a language issue that the original game doesn't bring up. Using the initials of the six colours in the guess is only simple/intuitive if English is your first language. For instance, a French player would associate 'j' with yellow (from 'jaune') and might find it hard to remember 'y'.

For colour blind players, showing only plain blocks of colour in display_guesses could cause confusion, e.g. between the red and green counters.

Seeing the player's text input displayed alongside the colours would solve both problems - the player would then have the option of solving the code using string characters rather than colours.
The display looks more crowded this way, so I decided to make it a separate option rather than implementing it as standard.

The very start of the game therefore checks if the player wants to see the letter codes displayed alongside the colours.

For speech recognition input, the player is instructed every time which English words to use, and the words are again shown in their appropriate colours.




LIBRARIES USED

re:                 to parse player's input and check the validity of inputted codes

random:             to generate the hidden code

os:                 to clear the terminal screen for play

pyfiglet:           to display a pretty 'CodeMaster' title

speech_recognition: to parse the player's spoken input

sounddevice:        to record the player's speech from the mic

scipy:              to write the resulting .wav file to disk

soundfile:          to translate the .wav file into a PCM .wav file acceptable to speech_recognition
