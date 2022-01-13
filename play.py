from typing import Tuple

from utils import bcolors

def determine_word_positions(word: str, guess: str) -> Tuple[bool, str]:
    output = ""
    guessed = True
    for i, char in enumerate(guess):
        char_upper = char.upper()
        word_upper = word[i].upper()
        if char_upper == word_upper:
            output += f"{bcolors.OKGREEN}{char_upper}{bcolors.ENDC}"
        elif char_upper in word.upper():
            output += f"{bcolors.OKBLUE}{char_upper}{bcolors.ENDC}"
            guessed = False
        else:
            output += f"{char_upper}"
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
    from random import choice

    list_of_words = get_word_list(
        "https://www.mit.edu/~ecprice/wordlist.10000", 5
    )
    while True:
        word = choice(list_of_words)
        guess = take_guess("Guess the new word: ")
        output, guessed = determine_word_positions(word, guess)

        while not guessed:
            print(output)
            guess = take_guess()
            output, guessed = determine_word_positions(word, guess)
        print("Correct!")
        print(output)
