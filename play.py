from typing import Tuple

from utils import bcolors

def determine_word_positions(word: str, guess: str) -> Tuple[bool, str]:
    output = ""
    guessed = True
    for i, char in enumerate(word):
        char_upper = char.upper()
        guess_upper = guess[i].upper()
        if char_upper == guess_upper:
            output += f"{bcolors.OKGREEN}{guess_upper}{bcolors.ENDC}"
        elif char_upper in guess.upper():
            output += f"{bcolors.OKBLUE}{guess_upper}{bcolors.ENDC}"
            guessed = False
        else:
            output += f"{guess_upper}"
            guessed = False
    return output, guessed


if __name__ == "__main__":
    from word_list import get_word_list
    from random import choice

    list_of_words = get_word_list(
        "https://www.mit.edu/~ecprice/wordlist.10000", 5
    )
    while True:
        word = choice(list_of_words)
        guess = input("Guess the new word: ")
        output, guessed = determine_word_positions(word, guess)

        while not guessed:
            print(output)
            guess = input()
            output, guessed = determine_word_positions(word, guess)
        print("Correct!")
        print(output)
