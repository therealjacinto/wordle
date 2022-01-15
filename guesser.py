import random
from bisect import bisect_left
from typing import List, Dict

from utils import UPPER_LETTERS, list_to_word


def generate_guesses(
        guess: List[str], index: int, correct_letter_positions: List[str],
        incorrect_letter_positions: List[str], incorrect_letters: str,
        guesses: List[str], list_of_words: List[str]) -> List[str]:
    """Recursive function that populates the guesses list with guesses.
    
    This function recursively generates a word (starting from AAAAA to ZZZZZ)
    using previously determined information. A binary search tree is used for
    speeding up the generation that will stop generating a word if a word does
    not exists in list_of_words that starts with the word you are creating
    (e.g. if the first two letters are "CC" then it won't continue because
    there is no word that starts with "CC")

    Args:
        guess: list that is populated via recursion to add to guesses
        index: used to recursively keep track of character position
        correct_letter_positions: known correct letter positions
        incorrect_letter_positions: known letters that exist in the word, but
          are at the wrong position
        incorrect_letters: known letters that are not in the word
        guesses: list that is populated with all the generated guesses
        list_of_words: list of possible words
    """
    # Reached the end of the recursion
    if index == len(guess):
        guess_word = list_to_word(guess)

        # Only use guesses that utilize information from
        # incorrect_letter_positions
        for position in incorrect_letter_positions:
            for char in position:
                if char not in guess_word:
                    return

        # Only add words if they exist in list_of_words
        if guess_word in list_of_words:
            guesses.append(guess_word)
        return

    # Always fill in known positions
    if correct_letter_positions[index] != "":
        guess[index] = correct_letter_positions[index]
        generate_guesses(guess, index + 1, correct_letter_positions,
                         incorrect_letter_positions, incorrect_letters,
                         guesses, list_of_words)
    else:
        # Brute-force letter filling
        for letter in UPPER_LETTERS:
            # Ignore letters we know can't exist at this index
            if letter in incorrect_letters or \
                    letter in incorrect_letter_positions[index]:
                continue

            guess[index] = letter

            # Optimization: for indexes 2 and 3, check if there is even a
            # possibility that a word can be generated with the first few
            # characters you currently have. Uses a binary search tree to speed
            # up search. This assumes the list_of_words is already
            # alphabetically sorted.
            if index > 1 and index < 4:
                try:
                    guess_word = list_to_word(guess[:index + 1])
                    exists = list_of_words[
                        bisect_left(list_of_words, guess_word)
                    ].startswith(guess_word)
                    if not exists:
                        # Nothing with these starting characters exists. Skip
                        # this letter.
                        continue
                except IndexError:
                    # guess is greater than all entries in wordlist
                    continue

            # Recursive loop
            generate_guesses(guess, index + 1, correct_letter_positions,
                             incorrect_letter_positions, incorrect_letters,
                             guesses, list_of_words)


def determine_words(
        list_of_words: List[str], correct_letter_positions: List[str],
        incorrect_letter_positions: List[str],
        incorrect_letters: str) -> List[str]:
    """Call recursive function and return list."""
    # Initialize lists
    guess = ["", "", "", "", ""]
    guesses = []

    # Generation algorithm
    generate_guesses(guess, 0, correct_letter_positions,
                     incorrect_letter_positions, incorrect_letters, guesses,
                     list_of_words)

    return guesses


def determine_highest_weight_word(
        words: List[str], frequency_weights: Dict[str, int],
        position_frequencies: List[Dict[str, int]]) -> str:
    """Determine word weight based on frequency of character in list."""
    # Initialize counters
    largest_total = 0
    best_word = None

    # Determine word with the highest frequency character value
    for guess in words:
        total = 0
        for i, char in enumerate(guess):
            total += frequency_weights[char] * position_frequencies[i][char]
        if total > largest_total:
            largest_total = total
            best_word = guess
    return best_word


def determine_a_good_guess(guesses: List[str]) -> str:
    """Determine a good word to use for guess.
    
    This function takes into account words that have duplicate letters (given
    lower priority) and words with letters that are more likely to provide more
    information (are frequent in list of possible guesses).
    """
    if len(guesses) == 0:
        return

    # Initialize list of words with unique characters
    unique_char_guesses = []
    # Initialize dictionary of character frequency information
    frequency = {}
    # Initialize position of character frequency information
    character_position_frequency = [{}, {}, {}, {}, {}]

    # Iterate through list of guesses putting words with unique characters in
    # the unique_char_guesses list and adding the number of times each
    # character is used in all words and storing that in the frequency dict
    for guess in guesses:
        good_guess = True
        for i, char in enumerate(guess):
            if guess.count(char) > 1:
                good_guess = False
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1
            if char in character_position_frequency[i]:
                character_position_frequency[i][char] += 1
            else:
                character_position_frequency[i][char] = 1
        if good_guess:
            unique_char_guesses.append(guess)

    best_word = determine_highest_weight_word(unique_char_guesses, frequency,
                                              character_position_frequency)

    # best_word can be None if there exists no word without repeated letters
    if best_word is not None:
        return best_word

    # Dealer's choice
    word = random.choice(guesses)
    return word


def parse_input(user_input: str, correct_letter_positions: List[str],
                incorrect_letter_positions: List[str]) -> str:
    """Parse user input for character information."""
    i = 0
    incorrect_letters = ""

    while i < len(user_input):
        if int(user_input[i + 1]) == 0:
            # Letter doesn't exist in word
            incorrect_letters += user_input[i]
        elif int(user_input[i + 1]) == 1:
            # Letter exists in word, just not at this position
            incorrect_letter_positions[i // 2] += user_input[i]
        elif int(user_input[i + 1]) == 2:
            # Letter exists at this position
            correct_letter_positions[i // 2] = user_input[i]
        i += 2

    return incorrect_letters


if __name__ == "__main__":
    from utils import generate_word_list

    list_of_words = generate_word_list(
        "https://www.mit.edu/~ecprice/wordlist.100000", 5, True
    )

    # Try and guess
    guess = ["", "", "", "", ""]
    incorrect_positions = ["", "", "", "", ""]
    incorrect_letters = ""

    guesses = list_of_words
    while len(guesses) > 1:
        if len(guesses) < 10:
            print(guesses)
        y_n = "N"
        while y_n == "N" or y_n == "n":
            # Generate a guess
            proposed_guess = determine_a_good_guess(guesses)
            if proposed_guess is None:
                print("Out of options")
                exit()

            print(f"Try {proposed_guess}?")
            y_n = input("Y/n: ")

            # In case you want to reject this guess (not a real word)
            if y_n == "N" or y_n == "n":
                guesses.remove(proposed_guess)

        print(f"What was the result of {proposed_guess}? ")
        result = input()
        incorrect_letters += parse_input(result.upper(), guess,
                                         incorrect_positions)
        guesses = determine_words(guesses, guess, incorrect_positions,
                                  incorrect_letters)

    print(f"Word is: {guesses}")
