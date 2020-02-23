#!/usr/bin/python
# coding: utf-8

# Author: Amit
# Version: 2.0.0

import itunes
import sys
import os
import shutil
import time
import re
import subprocess
from collections import OrderedDict
from subprocess import call
from mediafile import MediaFile
from mutagen.flac import FLAC

# Global Variables
SUPPORTED_FORMATS = [".flac"]
WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
INPUT = []
OUTPUT = []
OPTIONS = []


def main():
    init()
    request_options()

    sys.stdout.write("\nSearching songs, please wait... ")

    filenames = get_paths()

    print str(len(filenames)) + " songs found"

    for index, filename in enumerate(filenames):
        if index > 0 and index % 15 == 0:
            time.sleep(70)  # To avoid iTunes Store API rate limiting timeout

        tag_song(filename)


def init():
    for index, argument in enumerate(sys.argv):
        if argument == "-i":
            i = index + 1

            while (i < len(sys.argv) and (os.path.isfile(sys.argv[i]) or os.path.isdir(sys.argv[i]))):
                INPUT.append(sys.argv[i])
                i += 1
        elif argument == "-o" and os.path.isdir(sys.argv[index + 1]):
            OUTPUT.append(sys.argv[index + 1])


def request_options():
    option = 1

    print "\nBefore continuing, it will be necessary for you to answer the following questions:"

    print "\n--- Automatic Tagging Behaviour ---"
    print "1. Disabled (Asks the user before tagging) <- Default"
    print "2. Enabled (Automatically tags each song with the best matching result)"

    option = raw_input("\nEnter selection: ") or 1
    option = int(option)

    if option == 2:
        OPTIONS.append("-A")

    option = 1

    print "\n--- Artwork Replacement ---"
    print "1. Disabled (Preserves each song's current artwork) <- Default"
    print "2. Enabled (Automatically switches each song's artwork for the best matching result)"

    option = raw_input("\nEnter selection: ") or 1
    option = int(option)

    if option == 1:
        OPTIONS.append("-p")


def get_paths():
    filenames = []

    if len(INPUT) == 0:
        INPUT.append("./")

    for current_input in INPUT:
        if os.path.isdir(current_input):
            for root, directories, files in os.walk(current_input):
                for file in files:
                    if os.path.splitext(file)[1] in SUPPORTED_FORMATS:
                        filenames.append(os.path.join(root, file))
        elif os.path.splitext(current_input)[1] in SUPPORTED_FORMATS:
            filenames.append(current_input)

    filenames = list(OrderedDict.fromkeys(filenames))

    return filenames


def tag_song(filename):
    print "\n--- Current file: " + os.path.basename(filename) + " ---"

    if "-q" in OPTIONS:
        query = [raw_input("Search query: ")]
    else:
        query = guess_title(filename)

    sys.stdout.write("\nSearching track: " + '"' + capitalize_string(query[0]))

    if len(query) > 1:
        sys.stdout.write(" - ")
        artists = query[1:]

        if len(artists) > 2:
            for index, artist in enumerate(artists):
                sys.stdout.write(artist)

                if index == len(artists) - 2:
                    sys.stdout.write(" & ")
                elif index != len(artists) - 1:
                    sys.stdout.write(", ")
        else:
            sys.stdout.write(artists[0])

    print("\"")

    if len(itunes.search_song(" ".join(query))) == 0:
        print "\nSong not found :("
    else:
        response = "y"

        while response == "y":
            tags = get_tags(filename, [" ".join(query)])
            print_tags(tags)
            response = write_tags(filename, tags)

            if response == "y":
                OPTIONS.append('-q')
                OPTIONS.append('-l')

    query = []


def guess_title(filename):
    query = []
    f = MediaFile(filename)
    sanitized_filename = sanitize(filename)

    ext = os.path.splitext(filename)[1]
    if ext in SUPPORTED_FORMATS:
        sanitized_filename = re.sub(
            " +", " ", sanitized_filename.replace(ext, "")).strip()

    if f.title != None:
        query.append(sanitize(f.title))

    if f.artist != None:
        if "&" in f.artist:
            query.extend(f.artist.split(" & "))
        elif "," in f.artist:
            query.append(f.artist.split(", ")[0])
        elif ";" in f.artist:
            query.append(f.artist.split(";")[0])
        elif "\\\\" in f.artist:
            query.append(f.artist.split("\\\\")[0])
        else:
            query.append(f.artist)

    if f.title == None and f.artist == None:
        query = sanitized_filename.split(" - ")

    return query


def get_tags(filename, query):
    option = 0

    if "-l" in OPTIONS:
        results = itunes.search_song(" ".join(query), limit=10)

        for index, result in enumerate(results):
            sys.stdout.write("\n" + str(index + 1) + ". Title: " + result.get_name() + ", Album: " +
                             result.get_album().get_name() + ", Artists: " + result.get_artist().get_name())
            if index == 0:
                print " <- Default"
            else:
                print ""

        option = raw_input("\nEnter selection: ") or 1

        option = int(option) - 1

        if option < 0 or option > len(results):
            option = 0

    track = itunes.search_song(" ".join(query))[option]
    album = track.get_album()
    tags = {
        "title": track.get_name(),
        "album_title": album.get_name(),
        "artists": [track.get_artist().get_name()],
        "release_date": track.get_release_date(),
        "track_number": str(track.get_disc_number()) + "/" + str(album.get_track_count()),
        "genre": track.get_genre(),
        "album_artist": album.get_artist().get_name(),
        "disc_number": "1/1",
        "duration": track.get_duration()
    }

    return correct_tags(filename, tags)


def correct_tags(filename, tags):
    mix_version = re.search(
        "(\boriginal\b|\bextended\b||\binstrumental\b)", filename.lower())
    artists = tags["artists"][0]
    tags["artists"] = []

    if mix_version != None and len(mix_version.group(1)) > 0:
        mix_version = mix_version.group(1)

        if "(" in tags["title"]:
            tags["title"] += " ["
        else:
            tags["title"] += " ("
        tags["title"] += capitalize_string(mix_version)

        mix_type = re.search(
            "(\bmix\b|\bedit\b|\bversion\b)", filename.lower())

        if mix_type != None:
            mix_type = capitalize_string(mix_type.group(1))
            tags["title"] += " " + mix_type

        if ")" in tags["title"]:
            tags["title"] += "]"
        else:
            tags["title"] += ")"

    if "extended mix" in filename.lower() and "extended mix" not in clean(lowerCase(tags["title"])):
        if "(" and ")" in tags["title"]:
            tags["title"] += " [Extended Mix]"
        else:
            tags["title"] += " (Extended Mix)"
    elif "original mix" in filename.lower() and "original mix" not in clean(lowerCase(tags["title"])) and tags["total_tracks"] != 1:
        if "(" and ")" in tags["title"]:
            tags["title"] += " [Original Mix]"
        else:
            tags["title"] += " (Original Mix)"
    elif "instrumental mix" in filename.lower() and "instrumental mix" not in clean(lowerCase(tags["title"])) and tags["total_tracks"] != 1:
        if "(" and ")" in tags["title"]:
            tags["title"] += " [instrumental Mix]"
        else:
            tags["title"] += " (instrumental Mix)"

    if "extended mix" in filename.lower() and tags["track_number"] == 1 and tags["total_tracks"] == 1:
        tags["track_number"] = 2
        tags["total_tracks"] = 2

    if ", " in artists:
        tags["artists"].extend(artists.split(", "))

    if "&" in artists:
        tags["artists"].extend(artists.split(" & "))

    if ", " not in artists and "&" not in artists:
        tags["artists"] = [artists]

    if "feat." in tags["title"]:
        featured_artist = re.search(r"\(feat. (.+)\)", tags["title"])

        if featured_artist != None:
            featured_artist = featured_artist.group(1)
            tags["artists"].append(featured_artist)

    if "remix" in filename.lower():
        remixer = re.search(
            r"(?:(?:\(|\[)([\w ]*) remix(?:\)|\])[\w -.]*)$", filename.lower())

        if remixer != None:
            if "remix" not in clean(lowerCase(tags["title"])):
                if "(" in tags["title"]:
                    tags["title"] += "[" + \
                        capitalize_string(remixer.group(1)) + "]"
                else:
                    tags["title"] += "(" + \
                        capitalize_string(remixer.group(1)) + ")"

            tags["artists"].append(capitalize_string(remixer.group(1)))

    # Get the track's genre from Beatport
    title = tags["title"]

    if mix_version != None and len(mix_version.group(1)) > 0:
        title += mix_version

    artist = tags["artists"][0]
    p = subprocess.Popen(
        ["./get-genre-beatport.exe", title, artist], stdout=subprocess.PIPE)
    genre = p.stdout.read().strip()

    if genre != "null":
        tags["genre"] = genre

    if tags["genre"] == "Urbano latino":
        tags["genre"] = "Reggaetón"

    if "Alternative" in tags["genre"]:
        tags["genre"] = tags["genre"].replace("Alternative", "Indie")

    if " - Single" in tags["album_title"]:
        tags["album_title"].replace(" - Single", "")

    if " - EP" in tags["album_title"]:
        tags["album_title"] = tags["album_title"].replace(" - EP", "")

    if " - LP" in tags["album_title"]:
        tags["album_title"] = tags["album_title"].replace(" - LP", "")

    return tags


def print_tags(tags):
    print "\nTitle: " + tags["title"]
    print "Album: " + tags["album_title"]
    print "Artists: ",

    if len(tags["artists"]) > 1:
        for index, artist in enumerate(tags["artists"]):
            sys.stdout.write(artist)

            if index == len(tags["artists"]) - 2:
                sys.stdout.write(" & ")
            elif index != len(tags["artists"]) - 1:
                sys.stdout.write(", ")
    else:
        sys.stdout.write(tags["artists"][0])

    print "\nRelease Date: " + tags["release_date"]
    print "Track Number: " + str(tags["track_number"])
    print "Genre: " + tags["genre"]
    print "Album Artist: " + tags["album_artist"]
    print "Disc Number: " + str(tags["disc_number"])
    minutes = int(tags["duration"] / 60)
    seconds = int(tags["duration"] / 60 % 1 * 100)
    print "Duration: " + str(minutes) + "m " + str(seconds) + "s"

    """
	print "\nAvailable Artworks:"
	artworks = track.get_artwork()
	for index, artwork in enumerate(artworks):
		print "Artwork #" + str(index + 1) + " (" + str(artwork) + "x" + str(artwork) + "):"
		print artworks[artwork] + "\n"
	"""


def write_tags(filename, tags):
    f1 = MediaFile(filename)
    writeTags = "y"
    showMoreOptions = "n"

    if not "-A" in OPTIONS:
        writeTags = raw_input("\nWrite tags? (y/n): ")

    if writeTags == "y":
        print "\nWriting tags..."

        # Deletes current tags from the song
        f1.delete()

        date = tags["release_date"].split("-")
        f1.title = tags["title"]
        f1.album = tags["album_title"]
        # f1.artist = tags["artists"]
        f1.year = date[0]
        f1.month = date[1]
        f1.day = date[2]
        # f1.track = tags["track_number"]
        # f1.tracktotal = tags["total_tracks"]
        # f1.disc = str(tags["disc_number"])
        # f1.disctotal = tags["total_discs"]
        f1.genre = tags["genre"]
        f1.albumartist = tags["album_artist"]

        # Drops "Album Artist" Tag
        f1.__dict__["mgfile"].pop("album artist")
        
        os.chdir(os.path.dirname(filename))

        if not "-p" in OPTIONS:
            f1.art = get_artwork(
                filename, (tags["album_title"], tags["album_artist"]))

        f1.save()

        f2 = FLAC(filename)
        f2["Artist"] = tags["artists"]
        f2["tracknumber"] = [str(tags["track_number"])]
        f2["discnumber"] = [str(tags["disc_number"])]

        f2.save()

        print "Tags written successfully!"

        filename_ext = os.path.splitext(filename)[1]
        title = f1.title + " - " + f1.albumartist + filename_ext

        if not os.path.isfile(title):
            os.rename(filename, title)

        if os.path.isfile("./cover.jpg"):
            os.remove("./cover.jpg")
        
        if len(OUTPUT) != 0:
            dest = os.path.join(OUTPUT[0], os.path.basename(filename))
            
            if os.path.exists(dest):
                os.remove(dest)

            shutil.move(filename, OUTPUT[0])

    if writeTags == "n" and not "-A" in OPTIONS:
        showMoreOptions = raw_input("\nShow more options? (y/n): ")

    return showMoreOptions


def get_artwork(filename, query):
    print "\nSearching artwork..."
    call([os.path.join(WORKING_DIR, "./itunes-artwork-downloader.exe"),
          " ".join(query), "-q", "1500"])

    if os.path.isfile("./cover.jpg"):
        art_filename = open("./cover.jpg", "rb")

        return art_filename.read()


def sanitize(text):
    return re.sub(" +", " ", re.sub("(?:\boriginal\b|\bextended\b||\binstrumental\b) (?:\bmix\b|\bedit\b|\bversion\b)", "", re.sub(r"\(?feat\.? [\w ]+\)?", "", os.path.basename(text.replace("_", " "))), flags=re.IGNORECASE)).strip()


def capitalize_string(text):
    words = text.split(" ")
    result = ""

    for word in words:
        word = re.sub(" +", " ", word)

        if word[0] == "(" or word[0] == "[":
            result += word[0] + word[1:].capitalize()
        else:
            result += word.capitalize()

        result += " "

    return result.strip()


def lowerCase(text):
    text = text.split(" ")

    for index, term in enumerate(text):
        text[index] = term.lower()

    return " ".join(text)


if __name__ == '__main__':
    main()
