"""One-off Python script used to generate a database of Drake lyrics."""
import lyrics

__CSV_OUT_PATH = "drake_lyrics.csv"

song_lyrics = lyrics.get_artist_lyrics("Drake")
for song in song_lyrics:
	lines = song[1].split("\n")
	