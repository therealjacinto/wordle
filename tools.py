import random
from bisect import bisect_left
from typing import List, Dict

from utils import UPPER_LETTERS


def find_word_with_letters(list_of_chars: List[str], list_of_words: List[str], dirty_case: bool = False) -> List[str]:
    found_words = []
    for word in list_of_words:
        found_word = True
        if dirty_case:
            word = word.upper()
        for char in list_of_chars:
            if dirty_case:
                char = char.upper()
            if char not in word:
                found_word = False
                break
        if found_word:
            found_words.append(word)
    return found_words


def get_frequency(list_of_words: List[str]) -> Dict[str, int]:
    output = {}
    for word in list_of_words:
        for char in word:
            char = char.upper()
            if char in output:
                output[char] += 1
            else:
                output[char] = 1
    return output


def list_to_word(word_list: List[str]) -> str:
    word = ""
    for char in word_list:
        word += char
    return word


def is_word(guess: str, list_of_words: List[str]) -> bool:
    word = list_to_word(guess)
    return word in list_of_words


def generate_guesses(guess: List[str], index: int, correct_letter_positions: List[str], incorrect_letter_positions: List[str], incorrect_letters: str, guesses: List[str], list_of_words: List[str]) -> List[str]:
    if index == len(guess):
        guess_word = list_to_word(guess)
        for position in incorrect_letter_positions:
            for char in position:
                if char not in guess_word:
                    return
        if guess_word in list_of_words:
            guesses.append(guess_word)
        return
    if correct_letter_positions[index] != "":
        guess[index] = correct_letter_positions[index]
        generate_guesses(guess, index + 1, correct_letter_positions, incorrect_letter_positions, incorrect_letters, guesses, list_of_words)
    else:
        for letter in UPPER_LETTERS:
            if letter in incorrect_letters or letter in incorrect_letter_positions[index]:
                continue
            guess[index] = letter
            if index > 1 and index < 4:
                try:
                    guess_word = list_to_word(guess[:index + 1])
                    exists = list_of_words[bisect_left(list_of_words, guess_word)].startswith(guess_word)
                    if not exists:
                        continue
                except IndexError:
                    continue
            generate_guesses(guess, index + 1, correct_letter_positions, incorrect_letter_positions, incorrect_letters, guesses, list_of_words)


def determine_words(list_of_words: List[str], correct_letter_positions: List[str], incorrect_letter_positions: List[str], incorrect_letters: str) -> List[str]:
    # First guesses
    if all(char == "" for char in correct_letter_positions) and all(char == "" for char in incorrect_letter_positions) and len(incorrect_letters) == 0:
        return ["CLEAT", "IRONS"]
    
    # Build word
    guess = ["", "", "", "", ""]
    guesses = []
    generate_guesses(guess, 0, correct_letter_positions, incorrect_letter_positions, incorrect_letters, guesses, list_of_words)
    return guesses


def determine_a_good_guess(guesses: List[str]) -> str:
    if len(guesses) == 0:
        return
    
    unique_char_guesses = []
    frequency = {}
    for guess in guesses:
        good_guess = True
        for char in guess:
            if guess.count(char) > 1:
                good_guess = False
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1
        if good_guess:
            unique_char_guesses.append(guess)
    
    largest_total = 0
    best_word = ""
    for guess in unique_char_guesses:
        total = 0
        for char in guess:
            total += frequency[char]
        if total > largest_total:
            largest_total = total
            best_word = guess

    if largest_total > 0:
        return best_word

    # Dealer's choice
    word = random.choice(guesses)
    return word


def parse_input(user_input: str, correct_letter_positions: List[str], incorrect_letter_positions: List[str]) -> str:
    i = 0
    incorrect_letters = ""
    while i < len(user_input):
        if int(user_input[i + 1]) == 0:
            incorrect_letters += user_input[i]
        elif int(user_input[i + 1]) == 1:
            incorrect_letter_positions[i // 2] += user_input[i]
        elif int(user_input[i + 1]) == 2:
            correct_letter_positions[i // 2] = user_input[i]
        i += 2
    return incorrect_letters


if __name__ == "__main__":
    from word_list import get_word_list

    list_of_words = get_word_list(
        "https://www.mit.edu/~ecprice/wordlist.100000", 5, True
    )
    
    # Print out letter frequencies
    # import json
    # print(json.dumps(dict(sorted(get_frequency(list_of_words).items(), key=lambda item: item[1], reverse=True))))

    # Find a word with the letters provided
    #print(find_word_with_letters(["A", "E", "L", "T", "C"], list_of_words))
    #print(find_word_with_letters(["S", "O", "I", "R", "N"], list_of_words))

    # Try and guess
    guess = ["", "", "", "", ""]
    incorrect_positions = ["", "", "", "", ""]
    incorrect_letters = ""

    result = input("What was the result of AROSE/CLEAT?: ")
    incorrect_letters += parse_input(result, guess, incorrect_positions)
    result = input("What was the result of CLINT/IRONS?: ")
    incorrect_letters += parse_input(result, guess, incorrect_positions)

    guesses = determine_words(list_of_words, guess, incorrect_positions, incorrect_letters)
    while len(guesses) > 1:
        proposed_guess = determine_a_good_guess(guesses)
        print(f"Try {proposed_guess}?")
        y_n = input("Y/n: ")
        while y_n == "N" or y_n == "n":
            guesses.remove(proposed_guess)
            proposed_guess = determine_a_good_guess(guesses)
            if proposed_guess is None:
                print("Out of options")
                exit()
            print(f"Try {proposed_guess}?")
            y_n = input("Y/n: ")
        result = input(f"What was the result of {proposed_guess}? ")
        incorrect_letters += parse_input(result, guess, incorrect_positions)
        guesses = determine_words(guesses, guess, incorrect_positions, incorrect_letters)

    print(f"Good job! The word was {guesses}")
