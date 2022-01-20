# Script to benchmark the the guesser algorithm against the wordle game.

if __name__ == "__main__":
    import random
    import time
    import csv

    from utils import generate_word_list_from_file, convert_color_to_code, \
        remove_formatting
    from play import determine_word_positions
    from guesser import parse_input, determine_words, determine_a_good_guess

    # Generate word list
    list_of_words = generate_word_list_from_file("word.list")
    # Write header to benchmark file
    filename = 'results.csv'
    with open(filename, 'w') as csvfile:
        row_writer = csv.writer(csvfile, delimiter=',')
        header = ["word", "guessing_time (s)","num_attempts","guesses"]
        row_writer.writerow(header)

    while True:
        order = []
        word = random.choice(list_of_words)

        # Initialize character info
        guesses = list_of_words
        guess = ["", "", "", "", ""]
        incorrect_positions = ["", "", "", "", ""]
        incorrect_letters = ""
        guesses = list_of_words
        num_guesses = 0
        guessed = False

        start = time.perf_counter()
        while not guessed:
            # Generate a guess from posibilities
            num_guesses += 1
            proposed_guess = determine_a_good_guess(guesses)

            # Compare guess to word
            color_output, guessed = determine_word_positions(word,
                                                             proposed_guess)
            order.append(color_output)

            # Parse response to guess
            output = convert_color_to_code(color_output)
            incorrect_letters += parse_input(output, guess,
                                             incorrect_positions)

            # Generate new possibilies
            guesses = determine_words(guesses, guess, incorrect_positions,
                                      incorrect_letters)

        end = time.perf_counter()
        print(f"{color_output}: guessed in {end - start} seconds with "
              f"{num_guesses} attempts: {' '.join(order)}")

        with open(filename, 'a') as csvfile:
            row_writer = csv.writer(csvfile, delimiter=',')
            csv_row = [
                remove_formatting(color_output),
                end - start,
                num_guesses
            ]
            for item in order:
                csv_row.append(remove_formatting(item))
            row_writer.writerow(csv_row)
