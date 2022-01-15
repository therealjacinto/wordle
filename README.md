# wordle
Wordle game like https://www.powerlanguage.co.uk/wordle/

## Setup Locally
This code utilizes a python environment. Using `venv` or `conda`, install the `requirements.txt` packages before running the code.

### Conda
* Install conda environment
```sh
conda create -n wordle python=3.8.10 -y
```
* Install pip packages:
```sh
conda activate wordle
pip install -r requirements.txt
```

## Run Game
```sh
python play.py
```
- Begin when prompted for your guess.
- Once you press `Enter`, your guess is submitted and the results are returned
    - A **white** letter means the letter is not in the word.
    - A **blue**/**purple** letter means the letter exists at least once in the word, but not at this location.
    - A **green** letter means the letter exists at this location.
- Input another guess and repeat until you guess the word.

## Run Guesser
```sh
python guesser.py
```
- You will be prompted to try a word as a guess. You must first reply with a `Y` or a `N`. This is in case the generated word might not be an actual word. Most words are actual words, however if you look at the list of words from [this site](https://www.mit.edu/~ecprice/wordlist.100000), they are not all real words.
- Once you have a word you responded with `Y` (a word you have tried), you can input the results using the following format:
    - The letter followed by the result of that letter. Use **0** for an incorrect letter, a **1** for a letter that is in the word but is in the wrong position, and a **2** for a letter in the correct position.
    - An example string might look something like: `A0R1O2S0E0` for the word `AROSE` where the `A` and `E` are incorrect letters, the `R` is a letter that exists in the word but is at the wrong position, and the `O` is at the correct position.
- Repeat this until the guesser guesses a final word, or runs out of guesses.

## Run Benchmarking
```sh
python benchmark.py
```
If you make changes to the algorithm, you can test those changes by running the benchmarking script. This script tests the guesser against the wordle game until stopped. It will print out and output to a csv (`results.csv`) information like the time it took to guess and the number of attempts it made.
