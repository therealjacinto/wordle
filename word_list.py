from typing import List

import requests


def get_word_list(url: str, length: int) -> List[str]:
    list_of_words = []

    response = requests.get(url)
    if response.status_code == 200:
        words = response.text.splitlines()
        for word in words:
            if len(word) == length:
                list_of_words.append(word)

    return list_of_words
