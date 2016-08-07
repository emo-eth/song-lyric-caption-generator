"""
"""
import json
import sys
from semspaces.space import SemanticSpace

NUM_SIMILAR_WORDS = 5
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


def find_candidate_captions(artist, topic):
    print("Finding %s lyrics about \"%s\"..." % (artist, topic))

    candidates = {}

    topic = topic.lower()
    songs_containing_word = word_indices.get(topic)
    if not songs_containing_word:
        print("Sorry, we couldn't find any %s lyrics related to \"%s\"!" %
              (artist, topic))
        return candidates
    for song_title, indices in songs_containing_word.items():
        lines = lyrics[song_title]
        for index in indices:
            caption = get_surrounding_lines(lines, index)
            candidates[caption] = song_title
    print("Found %d captions for %s..." % (len(candidates), topic))
    for caption, title in candidates.items():
        print('\n"%s" - %s, "%s"' % (caption, artist, title))
    print()
    return candidates


def load_space():
    print('Loading semantic space...')
    return SemanticSpace.from_csv('spaces/lemmas.w2v.gz')

if __name__ == "__main__":
    artist, topic = sys.argv[1:3]
    load_data(artist)
    # semantic space vars
    use_space = False  # whether or not to use/load semantic space
    semantic_space = None
    related_words = []
    if len(sys.argv) > 3:
        use_space = sys.argv[3]
    if use_space:
        semantic_space = load_space()
        try:
            # get (word, distance) tuples
            word_distances = semantic_space.most_similar([topic])[topic]
            # get the first n words from those tuples
            related_words = [word_dist[0] for word_dist
                             in word_distances[:NUM_SIMILAR_WORDS]
                             if word_dist[0] != topic]
            print('Found similar topics: ' + ', '.join(related_words))
        except ValueError:
            pass
    candidates = {}
    for topic in [topic] + related_words:
        candidates.update(find_candidate_captions(artist, topic))
