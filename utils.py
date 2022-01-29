from typing import List

import requests


class bcolors:
    """Terminal output color codes."""

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# List of uppercase letters
UPPER_LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                 "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
                 "Y", "Z"]


def generate_word_list_from_url(
        url: str, length: int = 5, force_upper: bool = True,
        force_alphabetical_sort: bool = True) -> List[str]:
    """Get list of words from url and formats them."""
    list_of_words = []

    response = requests.get(url)
    if response.status_code == 200:
        words = response.text.splitlines()
        for word in words:
            # Only use words of specified length
            if len(word) == length:
                # Apply formatting
                if force_upper:
                    list_of_words.append(word.upper())
                else:
                    list_of_words.append(word)
    # Sort words (useful for binary searches later on)
    if force_alphabetical_sort:
        list_of_words.sort()
    return list_of_words


def generate_word_list_from_file(filename: str, force_upper: bool = True,
                                 force_alphabetical_sort: bool = True):
    """Get list of words from file and formats them."""
    list_of_words = []
    with open(filename) as file:
        while (word := file.readline().rstrip()):
            if force_upper:
                # Apply formatting
                word = word.upper()
            list_of_words.append(word)
    # Sort words (useful for binary searches later on)
    if force_alphabetical_sort:
        list_of_words.sort()
    return list_of_words


def list_to_word(word_list: List[str]) -> str:
    """Convert list of chars to a string."""
    word = ""
    for char in word_list:
        word += char
    return word


def convert_color_to_code(output: str) -> str:
    """Convert string with color information to position information."""
    out = ""
    output = output.replace(bcolors.ENDC, "")

    for i, char in enumerate(output):
        if char in UPPER_LETTERS:
            # Avoid out of index errors
            if i < 5:
                out += char + "0"
            elif output[i - len(bcolors.OKGREEN):i] == bcolors.OKGREEN:
                # Character in correct position
                out += char + "2"
            elif output[i - len(bcolors.OKBLUE):i] == bcolors.OKBLUE:
                # Character in incorrect position
                out += char + "1"
            else:
                # Character not in word
                out += char + "0"
    return out


def remove_formatting(input: str) -> str:
    """Remove color information from string."""
    return input.replace(bcolors.ENDC, "")\
                .replace(bcolors.OKGREEN, "")\
                .replace(bcolors.OKBLUE, "")
