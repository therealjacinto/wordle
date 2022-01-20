# Script to determine weights for determine_highest_weight_word

if __name__ == "__main__":
    import random
    import time
    import csv

    from utils import generate_word_list_from_file, convert_color_to_code
    from play import determine_word_positions
    from guesser import parse_input, determine_words, determine_a_good_guess

    # Test parameters
    freq_weight_start = 0.1
    freq_weight_end = 1
    freq_weight_step = 0.1

    pos_weight_start = 1
    pos_weight_end = 100
    pos_weight_step = 5

    num_tests = 300

    # Generate word list
    list_of_words = generate_word_list_from_file("word.list")

    # Write header to weights file
    filename = 'weights.csv'
    with open(filename, 'w') as csvfile:
        row_writer = csv.writer(csvfile, delimiter=',')
        header = ["freq_weight", "pos_weight", "num_tests", "average_attempts"]
        row_writer.writerow(header)

    while freq_weight_start < freq_weight_end:
        while pos_weight_start < pos_weight_end:
            test_num = 0
            total_attempts = 0
            while test_num < num_tests:
                word = random.choice(list_of_words)

                # Initialize character info
                guesses = list_of_words
                guess = ["", "", "", "", ""]
                incorrect_positions = ["", "", "", "", ""]
                incorrect_letters = ""
                guesses = list_of_words
                num_guesses = 0
                guessed = False

                while not guessed:
                    # Generate a guess from posibilities
                    num_guesses += 1
                    proposed_guess = determine_a_good_guess(
                        guesses, freq_weight_start, pos_weight_start
                    )

                    # Compare guess to word
                    color_output, guessed = determine_word_positions(word,
                                                                     proposed_guess)

                    # Parse response to guess
                    output = convert_color_to_code(color_output)
                    incorrect_letters += parse_input(output, guess,
                                                     incorrect_positions)

                    # Generate new possibilies
                    guesses = determine_words(guesses, guess, incorrect_positions,
                                              incorrect_letters)

                test_num += 1
                total_attempts += num_guesses

            average_attempts = total_attempts / num_tests
            print(f"Completed {num_tests} with (freq,pos) weights "
                  f"({freq_weight_start},{pos_weight_start}): "
                  f"{average_attempts} average attempts")
            with open(filename, 'a') as csvfile:
                row_writer = csv.writer(csvfile, delimiter=',')
                csv_row = [
                    freq_weight_start,
                    pos_weight_start,
                    num_tests,
                    average_attempts
                ]
                row_writer.writerow(csv_row)

            pos_weight_start += pos_weight_step
        freq_weight_start += freq_weight_step
