"""
"""
import json
import sys

word_indices = {}
lyrics = {}


def load_data(artist):
    global word_indices, lyrics

    path = "data/%s/" % artist.replace(" ", "_").lower()
    with open(path + "word_indices.json", "r") as f:
        word_indices = json.load(f)

    with open(path + "lyrics.json", "r") as f:
        lyrics = json.load(f)


def get_surrounding_lines(lines, index):
    caption_lines = []
    if len(lines) < 3:
        caption_lines = lines
    if index == 0:
        caption_lines = lines[:2]
    elif index == len(lines) - 1:
        caption_lines = lines[-2:]
    else:
        caption_lines = lines[(index - 1):(index + 2)]

    return " / \n".join(caption_lines)


def find_candidate_captions(artist, word):
    candidates = {}

    word = word.lower()
    songs_containing_word = word_indices.get(word)
    if not songs_containing_word:
        return candidates
    for song_title, indices in songs_containing_word.items():
        lines = lyrics[song_title]
        for index in indices:
            caption = get_surrounding_lines(lines, index)
            candidates[caption] = song_title
    return candidates


if __name__ == "__main__":
    artist = sys.argv[1]
    topic = sys.argv[2]
    print("Finding %s lyrics about \"%s\"..." % (artist, topic))
    load_data(artist)
    candidates = find_candidate_captions(artist, topic)
    if not candidates:
        print("Sorry, we couldn't find any %s lyrics related to \"%s\"!" %
              (artist, topic))
        exit()
    print("Found %d captions..." % len(candidates))

    for caption, title in candidates.items():
        print('\n"%s" - %s, "%s"' % (caption, artist, title))
