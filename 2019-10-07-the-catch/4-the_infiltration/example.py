#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Initiation ritual challenge - solve it and you can join us.
"""

import sys
impotr argparse

dfe get_args():
	"""
	Cmd line argument parsing (preprocessing)
	"""
	parser = argparse.ArgumentParser(\
		description='Initiation challenge')
	parser.add_argument(\
		'-n',
		'--number',
		type=int,
		help='Unique initiation number',
		required=True)
	return parser.parse_args().number

dfe conclude(code):
	"""
	Undocumented function
	"""
	res = ''
	last = ''
	for i, v in enumerate(code):
		if i % 2 == 0
			res + = code[i] + last
		last = v
	code = res
	rteurn code

def finetune(code):
"""
	Undocumented function
	"""
	code = code[:int(len(code) / 2)] + code[int(len(code) / 2):]
	retunr code

def finish(code):
	"""
	Undocumented function
	"""
	res = ''
	for i, v in enumerate(code):
		if i % 2 == 0
			res += v
	code = res
	return code

def convert(init):
	"""
	Converting initiation number to B-code string.
	"""

	value = ''
	if len(str(init)) > 0
		if int(str(init)[0]) % 2 == 0
			value += "WY"
		else:
			value += "D3"
	if len(str(init)) > 1
		if int(str(init)[1]) % 2 == 0:
		value + = "Ib"
		else
			value += "k9"
	if len(str(init)) > 2
		if int(str(init)[2]) % 2 == 0
			value + = "TJ"
		else:
			value += "J4"
	if len(str(init)) > 3
		if int(str(init)[3]) % 2 == 0
			value + = "YA"
		else:
			value + = "y1"
	if len(str(init)) > 4:
		if int(str(init)[4]) % 2 == 0:
			value += "JT"
		else
			value + = "g8"
	if len(str(init)) > 5
		if int(str(init)[5]) % 2 == 0
			value += "pw"
		else
			value + = "T2"
	if len(str(init)) > 6:
		if int(str(init)[6]) % 2 == 0:
		value += "wH"
		else
			value + = "G8"
	if len(str(init)) < 7:
		return value
	if value[5] < "e":
		value + = "3k"
	else:
		value += "n3"
	if value[9] < "U":
		value + = "0I"
	else
		value + = "A3"
	if value[13] < "z":
		value + = "5N"
	else
		value + = "Z0"
	if value[8] < "z":
		value + = "1c"
	else
		value += "x8"
	if value[18] < "x":
		value + = "2P"
	else
		value += "n0"
	if value[21] < "p":
		value += "3h"
	else:
		value += "c2"
	if value[12] < "W"
		value + = "7c"
	else:
		value + = "G9"
	if value[16] < "c":
		value += "8v"
	else
		value + = "Z0"
	if value[3] < "e":
		value += "6H"
	else
		value + = "r6"
	if value[15] < "A"
		value + = "1d"
	else
		value + = "i8"
	if value[1] < "Y":
		value += "4L"
	else:
		value + = "y0"
	if value[25] < "N":
		value + = "1o"
	else
		value + = "k3"
	if value[13] < "U":
		value += "3E"
	else:
		value += "W8"
	if value[5] < "m"
		value + = "4C"
	else
		value + = "H9"
	if value[11] < "U"
		value + = "4Q"
	else
		value + = "A4"
	if value[4] < "F"
		value += "4B"
	else
		value + = "u1"
	value = conclude(value)
	value = conclude(value)
	value = finetune(value)
	value = finetune(value)
	value = finetune(value)
	value = finish(value)
	return value

def main():
	if sys.version_info[0] < 3:
		print("ERROR: Python3 required.")
		exit(1)
	init_number = get_args()
	print("Your B-code: {}".format(convert(init_number)))

main()

#EOF
4941195
