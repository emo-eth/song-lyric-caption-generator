"""One-off Python script used to generate a database of Drake lyrics.
"""
import json
import os
import re
import sys

import nltk
from nltk.corpus import stopwords

import pylyrics3

__WORD_INDICES_FILE = "%s/word_indices.json"
__LYRICS_FILE = "%s/lyrics.json"

stopwords = set(stopwords.words("english"))


def get_words(line):
    words = set([word.lower() for word in nltk.word_tokenize(line)])
    return words.difference(stopwords)


def add_word_indices_to_dict(title, lines, word_to_indices):
    for i, line in enumerate(lines):
        words = get_words(line)

        for word in words:
            if not word_to_indices.get(word):
                word_to_indices[word] = {}

            if not word_to_indices[word].get(title):
                word_to_indices[word][title] = [i]
            else:
                word_to_indices[word][title].append(i)


def split_lines(lyrics):
    lines = [line.strip() for line in lyrics.split("\n")]
    return [line for line in lines
            if not re.match("^[\(\[].*[\)\]]$", line)]


def write_out_json(artist_name, word_to_indices, title_to_lines):
    folder_name = "data/" + artist_name.replace(" ", "_").lower()
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)
    with open(__WORD_INDICES_FILE % folder_name, "w") as f:
        f.write(json.dumps(word_to_indices))
    with open(__LYRICS_FILE % folder_name, "w") as f:
        f.write(json.dumps(title_to_lines))


def download_lyrics(artist_name):
    word_to_indices = {}
    title_to_lines = {}

    song_lyrics = pylyrics3.get_artist_lyrics("Drake")
    for title, lyrics in song_lyrics.items():
        lines = split_lines(lyrics)
        title_to_lines[title] = lines
        add_word_indices_to_dict(title, lines, word_to_indices)
    write_out_json(artist_name, word_to_indices, title_to_lines)


if __name__ == "__main__":
    global artist_name

    if len(sys.argv) < 2:
        print("Please specify the artist to download lyrics from.")
        print("Example usage: download_lyrics Drake")
        raise
    artist_name = sys.argv[1]
    download_lyrics(artist_name)
