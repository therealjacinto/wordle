from utils import UPPER_LETTERS, bcolors


def convert_color_to_code(output: str) -> str:
    out = ""
    output = output.replace(bcolors.ENDC, "")
    for i, char in enumerate(output):
        if char in UPPER_LETTERS:
            if i < 5:
                out += char + "0"
            elif output[i - len(bcolors.OKGREEN):i] == bcolors.OKGREEN:
                out += char + "2"
            elif output[i - len(bcolors.OKBLUE):i] == bcolors.OKBLUE:
                out += char + "1"
            else:
                out += char + "0"
    return out


def remove_formatting(input: str) -> str:
    return input.replace(bcolors.ENDC, "").replace(bcolors.OKGREEN, "").replace(bcolors.OKBLUE, "")

if __name__ == "__main__":
    import random
    import time
    import csv

    from word_list import get_word_list
    from play import determine_word_positions
    from tools import parse_input, determine_words, determine_a_good_guess

    list_of_words = get_word_list(
        "https://www.mit.edu/~ecprice/wordlist.100000", 5, True
    )
    while True:
        order = []
        word = random.choice(list_of_words)

        initial_guess = "AROSE"
        guess = ["", "", "", "", ""]
        incorrect_positions = ["", "", "", "", ""]
        incorrect_letters = ""
        guesses = list_of_words
        num_guesses = 1

        start = time.perf_counter()
        output, guessed = determine_word_positions(word, initial_guess)

        # Force second guess as CLINT
        # if not guessed:
        #     order.append(output)
        #     output = convert_color_to_code(output)

        #     incorrect_letters += parse_input(output, guess, incorrect_positions)
        #     second_guess = "CLINT"
        #     num_guesses += 1

        #     output, guessed = determine_word_positions(word, second_guess)

        while not guessed:
            order.append(output)
            output = convert_color_to_code(output)

            incorrect_letters += parse_input(output, guess, incorrect_positions)
            guesses = determine_words(guesses, guess, incorrect_positions, incorrect_letters)
            proposed_guess = determine_a_good_guess(guesses)
            num_guesses += 1
            
            output, guessed = determine_word_positions(word, proposed_guess)

        end = time.perf_counter()
        print(f"{output}: guessed in {end - start} seconds with {num_guesses} attempts: {' '.join(order)}")

        with open('results.csv', 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            csv_row = [remove_formatting(output), end - start, num_guesses]
            for item in order:
                csv_row.append(remove_formatting(item))
            spamwriter.writerow(csv_row)
