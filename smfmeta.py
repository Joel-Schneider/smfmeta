#!/usr/bin/python3
# (C) 22nd-24th April 2020 Joel Schneider
# Displays meta information from smf/.mid files
# License: AGPL v3+ (see LICENSE.txt)
""" implementation from scratch of midi metadata extraction
Reverse engineering using public domain midis as examples
(for example, The Cyber Hymnal at www.hymntime.com/tch)
and comparing the output with:
	timidity -ig <midifile> (v 2.15.0)
	strings <midifile>
Then I found both of these:
http://www.personal.kent.edu/~sbirch/Music_Production/MP-II/MIDI/midi_file_format.htm
http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html

Thankfully they seem to match up reasonably well, although
some of the midis I've come across seem to use the 'wrong' fields...
"""

import sys, libmidi
global DEBUG, MIDI_HEADER
libmidi.DEBUG = False
MIDI_HEADER = b'MThd\x00\x00\x00\x06'

if sys.argv[1]  == "-v":
	libmidi.DEBUG = True
	filename = sys.argv[2]
else:
	filename = sys.argv[1]

options = libmidi.smfmeta(filename)

for item in options:
	print(item.decode(), ":\n\t", sep='', end='')
	for line in options[item]:
		print('"', line.decode(), '" ', sep='', end='')
	print()

