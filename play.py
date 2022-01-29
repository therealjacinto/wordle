from typing import Tuple

from utils import bcolors


def determine_word_positions(word: str, guess: str) -> Tuple[str, bool]:
    """Color string based on position information and return result."""
    output = ""
    guessed = True

    for i, char in enumerate(guess):
        word_char = word[i]
        if char == word_char:
            # Correct position
            output += f"{bcolors.OKGREEN}{char}{bcolors.ENDC}"
        elif char in word:
            # Incorrect position but exists in word
            output += f"{bcolors.OKBLUE}{char}{bcolors.ENDC}"
            guessed = False
        else:
            # Not a correct letter
            output += f"{char}"
            guessed = False

    return output, guessed


def take_guess(force_upper: bool = True) -> str:
    """Take input from user and handle mistakes."""
    guess = input()

    # Check for incorrect length
    while len(guess) != 5:
        print("Your guess is the incorrect length. It must be 5 characters. "
              "Try again:")
        guess = input()

    # Keep input at uppercase
    if force_upper:
        return guess.upper()
    else:
        return guess


if __name__ == "__main__":
    import random

    from utils import generate_word_list_from_file    

    # Generate list of words
    list_of_words = generate_word_list_from_file("word.list")

    # Play game forever
    game_number = 1
    while True:
        word = random.choice(list_of_words)
        attempt = 1
        guessed = False

        print("[Game {}] Guess the new word: ".format(game_number))
        while not guessed:
            guess = take_guess()
            output, guessed = determine_word_positions(word, guess)
            print("[Attempt {}]: {}".format(attempt, output))
            attempt += 1
        print("Yay, You guessed the word!")
        game_number += 1
