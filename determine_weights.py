# Script to determine weights for determine_highest_weight_word

if __name__ == "__main__":
    import csv

    from utils import generate_word_list_from_url, convert_color_to_code
    from play import determine_word_positions
    from guesser import parse_input, determine_words, determine_a_good_guess

    # Test parameters
    freq_weights = [1]
    pos_weights = [0.900]

    # Generate word list
    list_of_words = generate_word_list_from_url(
        "https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt", 5, True
    )

    # Write header to weights file
    filename = 'weights.csv'
    with open(filename, 'w') as csvfile:
        row_writer = csv.writer(csvfile, delimiter=',')
        header = ["freq_weight", "pos_weight", "num_tests", "total_num_attempts", "average_attempts"]
        row_writer.writerow(header)

    for freq_weight in freq_weights:
        for pos_weight in pos_weights:
            test_num = 0
            total_attempts = 0
            for word in list_of_words:
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
                        guesses, freq_weight, pos_weight
                    )

                    # Compare guess to word
                    color_output, guessed = determine_word_positions(
                        word, proposed_guess
                    )

                    # Parse response to guess
                    output = convert_color_to_code(color_output)
                    incorrect_letters += parse_input(output, guess,
                                                     incorrect_positions)

                    # Generate new possibilies
                    guesses = determine_words(guesses, guess,
                                              incorrect_positions,
                                              incorrect_letters)

                test_num += 1
                total_attempts += num_guesses

            average_attempts = total_attempts / test_num
            print(f"Completed {test_num} test with (freq,pos) weights "
                  f"({freq_weight},{pos_weight}): "
                  f"{average_attempts} average attempts")
            with open(filename, 'a') as csvfile:
                row_writer = csv.writer(csvfile, delimiter=',')
                csv_row = [
                    freq_weight,
                    pos_weight,
                    test_num,
                    total_attempts,
                    average_attempts
                ]
                row_writer.writerow(csv_row)
