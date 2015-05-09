'''
Convert Hunter's Trix FLAC downloads to lossless iTunes (ALAC/.m4a) audio, with metadata and convert art.

Correlate filenames in directory with track listings in data file `data.txt`,
then set as much FLAC metadata as possible, add cover art, convert to ALAC (.m4a)
and push to the "Automatically Add to iTunes" directory. iTunes does the rest.

Total time to process a show is about one minute, compared to 20 minutes when copying all metadata manually.

See https://github.com/shacker/trix for installation and usage notes.
'''

import re
import os
import sys
import fnmatch
import datetime
from shutil import move
from subprocess import call

# Tweak these:
dir = "/Users/yourname/Downloads/torrents/process"
itunes_dir = "/Volumes/something/Automatically Add to iTunes"

# Constants
genre = "Rock"
artist = "Grateful Dead"

# Ensure we have the data file and cover art ready. Bail if not.
if not os.path.isfile("data.txt"):
	print("Metadata text file must be named data.txt. Exiting.")
	sys.exit()

if not os.path.isfile("cover.jpg"):
	print("Cover art file must be named cover.jpg. Exiting.")
	sys.exit()


# ===========================================
# Generate album title - should end up like:
# Hunter's Trix -- Vol. 54 -- 03/09/81 -- Madison Square Garden - New York, NY

# Volume # isn't in the data file - prompt for intput
volume = raw_input("Volume: ")

# Open file in "universal" mode ("rt") to handle both Windows and Unix line endings
# First four lines should have this format:
# Grateful Dead
# Madison Square Garden
# New York, NY
# March 9, 1981

lines = [line.strip() for line in open('data.txt', 'rt')]
venue = lines[1]
location = lines[2]
raw_date = lines[3]

get_date = datetime.datetime.strptime(raw_date, "%B %d, %Y")
new_date = get_date.strftime("%m/%d/%y")
year = get_date.year
albumtitle = "Hunter's Trix Vol. {vol} -- {date} -- {ven} - {loc}".format(vol=volume, date=new_date, ven=venue, loc=location)

# Show isn't in the data file - have to extract it from one of the filenames.
# Find all .flac files in dir and grab the first, then strip it out.
fn = [f for f in os.listdir('.') if '.flac' in f][0]
show = re.search("gd(.*)d", fn).group().lstrip("gd").rstrip("d")

# Read in data file containing track names. Store each line starting with "d" as a list item
lines = [line.strip() for line in open('data.txt') if line[0] == "d" and " - " in line]

for line in lines:
	print("Found track specifier in data.txt: {L}".format(L=line))

	# Filenames will be like `gd92-03-20d1t07.flac`. We consider the identifier to be `d1t07`. Get start of line up to first space.
	identifier = re.search("^.*?\ ", line).group().strip()

	disc = line[1]  # 2nd character is always the disc number (unless there are more than 9 discs, but there aren't)

	# Get first occurence of "t" to find track number. Remove leading "t" and leading "0".
	track = re.search('t.*?\ ', line).group(0).strip().lstrip("t").lstrip("0")

	# Title is everything after " - "
	title = re.search("\ -\ .*$", line).group().lstrip(" - ").strip()

	# Predict filename
	filename = "gd{show}{identifier}.flac".format(show=show, identifier=identifier)
	print("Predicted filename {f}".format(f=filename))

	print("Identifier: '{i}', Disc: {d}, Track: {tr}, Title '{ti}'".format(i=identifier, d=disc, tr=track, ti=title))

	# Generate full path to file.
	filepath = "{d}/{f}".format(d=dir, f=filename)
	outpath = filepath.replace(".flac", ".m4a")
	
	# metaflac won't ovewrite data; erase anything present
	print("Removing old metadata from {f}".format(f=filename))
	call(["metaflac", "--remove-all-tags", filepath])

	# Write new metadata
	print("Writing new metadata to {f}".format(f=filename))
	call(["metaflac", "--set-tag=ARTIST={a}".format(a=artist), filepath])
	call(["metaflac", "--set-tag=DISCNUMBER={d}".format(d=disc), filepath])
	call(["metaflac", "--set-tag=TRACKNUMBER={t}".format(t=track), filepath])
	call(["metaflac", "--set-tag=TITLE={t}".format(t=title), filepath])
	call(["metaflac", "--set-tag=ALBUM={a}".format(a=albumtitle), filepath])
	call(["metaflac", "--set-tag=DATE={y}".format(y=year), filepath])
	call(["metaflac", "--set-tag=GENRE={g}".format(g=genre), filepath])

	# Convert to ALAC
	basefile = filename.replace(".flac", "")
	print("Converting to ALAC: {b}.flac -> {b}.m4a".format(b=basefile))
	call(["ffmpeg", "-i", filename, "-acodec", "alac", "-loglevel", "warning", outpath])

	# Add cover art
	call(["mp4art", "--add", "cover.jpg", outpath])

	print("")

# Move m4a files to iTunes 
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*.m4a'):
		print("Sending file {f} to iTunes".format(f=file))
		move(file, itunes_dir)

# Clean up the rest
files = os.listdir('.')
for filename in files:
	os.remove(os.path.join(dir, filename))
	print("Deleting {f}".format(f=filename))

print("Done.")
