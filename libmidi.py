#!/usr/bin/python3
# (C) 22nd-24th April 2020 Joel Schneider
# Extracts meta information from smf/.mid files
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

import os
global DEBUG, MIDI_HEADER
MIDI_HEADER = b'MThd\x00\x00\x00\x06'

def dbg(info, msg=b'', msg2=b''):
	if DEBUG:
		print(info, b'\r', msg, b'\t', msg2)

def smfmeta(filename):
	fp = open(filename, 'rb')
	data = fp.read()
	fp.close()
	if data[:8] != MIDI_HEADER:
		dbg("Not a midi file\n")
		return False

	#https://stackoverflow.com/a/2104107
	file_length = os.stat(filename).st_size
	
	position = 8
	length = 1
	dbg("File data:\n")
	dbg(data)
	options = { b'text':  b'\xFF\x01', b'copyright':  b'\xFF\x02', b'sequence':  b'\xFF\x03', b'instrument':  b'\xFF\x04', b'lyric':  b'\xFF\x05', b'marker':  b'\xFF\x06', b'cue':  b'\xFF\x07', b'time signature':  b'\xFF\x58\x04', b'key signature':  b'\xFF\x58\x02' }
	for i in options:
		options[i] = []
	while position <= file_length:
		length = 1
		position += 1
		sub_str = data[position:position+length]
		if sub_str == b'\xFF':
			result = get_MIDI_field_data(data, position)
			if result != (None, None):
				dbg(result)
				options[result[0]].append(result[1])
	options[b'filename'] = [str.encode(filename)]
	options[b'file size'] = [str.encode(str(file_length))]
	#for i in options:
	#	print(i, options[i])
	return options

def get_MIDI_field_data(data, start_position):
	sub_str = data[start_position:start_position+1]
	options = { b'text':  b'\xFF\x01', b'copyright':  b'\xFF\x02', b'sequence':  b'\xFF\x03', b'instrument':  b'\xFF\x04', b'lyric':  b'\xFF\x05', b'marker':  b'\xFF\x06', b'cue':  b'\xFF\x07', b'time signature':  b'\xFF\x58\x04', b'key signature':  b'\xFF\x58\x02' }
	#for i in options:
	#	print(i, options[i])
	position = start_position
	if sub_str == b'\xFF':
		for opt in options:
			if data[position:position+2] == options[opt]:
				dbg("Found sequence")
				for i in range(len(data)-position):
					if data[position+i:position+i+1] == b'\x00': # End of sequence
						result = opt, data[position+3:position+i]
						return result
	return None, None
