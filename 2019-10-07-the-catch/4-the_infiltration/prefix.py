#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Initiation ritual challenge - solve it and you can join us.
"""

import sys
import argparse

def get_args():
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

def conclude(code):
	"""
	Undocumented function
	"""
	res = ''
	last = ''
	for i, v in enumerate(code):
		if i % 2 == 0:
			res += code[i] + last
		last = v
	code = res
	return code

def finetune(code):
	code = code[:int(len(code) / 2)] + code[int(len(code) / 2):]
	return code

def finish(code):
	"""
	Undocumented function
	"""
	res = ''
	for i, v in enumerate(code):
		if i % 2 == 0:
			res += v
	code = res
	return code

def convert(init):
