from typing import Tuple, List, Dict

from utils import bcolors

def determine_word_positions(word: str, guess: str, dirty_case: bool = False) -> Tuple[bool, str]:
    output = ""
    guessed = True
    for i, char in enumerate(guess):
        word_char = word[i]
        if dirty_case:
            char = char.upper()
            word_char = word_char.upper()
        if char == word_char:
            output += f"{bcolors.OKGREEN}{char}{bcolors.ENDC}"
        elif char in word:
            output += f"{bcolors.OKBLUE}{char}{bcolors.ENDC}"
            guessed = False
        else:
            output += f"{char}"
            guessed = False
    return output, guessed


def take_guess(prompt: str = "") -> str:
    guess = input(prompt)
    while len(guess) != 5:
        print("Your guess is the incorrect length. It must be 5 characters. "
              "Try again:")
        guess = input()
    return guess


if __name__ == "__main__":
    from word_list import get_word_list
    import random

    list_of_words = get_word_list(
        "https://www.mit.edu/~ecprice/wordlist.100000", 5, True
    )
    while True:
        word = random.choice(list_of_words)
        guess = take_guess("Guess the new word: ")
        output, guessed = determine_word_positions(word, guess.upper())

        while not guessed:
            print(output)
            guess = take_guess()
            output, guessed = determine_word_positions(word, guess.upper())
        print("Correct!")
        print(output)
