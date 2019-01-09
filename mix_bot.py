#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, tweepy, random, time, sys, os

###

CONSUMER_KEY = "AOjH1ZNMuFDfQ9acgPicxov7W"
CONSUMER_SECRET = "hjMQOAl5R8XfG2MoRkjHzfMoDd21Z6ZhHXJVNoofGPVxiizzhk"
ACCESS_KEY = "848111154090127360-ZXsHsJ9dGmdjUfl1IKDLZJaGIqwKgQr"
ACCESS_SECRET = "NAlR7j0HnYqWtQrIg4SCpptb0zSqSIS9Pbc0dgMxmOEOy"
FEED_FILENAME = "feed.txt"

###

def allow_case_change(word):
	return word != "I" and word != "I'm" and word != "I've" and word != "I'll"

def lowercase_optionally(word):
	if allow_case_change(word):
		return word.lower()
	else: 
		return word

def uppercase_optionally(word):
	if allow_case_change(word):
		return word.upper()
	else:
		return word

def end_of_sentence(word):
	return '.' in word or '!' in word or '?' in word

###

feed_file = open(FEED_FILENAME, "r")
return_line = "\""
lines = feed_file.readlines()
num_of_mixed_lines = random.randrange(2, 6)
num_of_lines = len(lines)
beginning_of_sentence = True

for i in xrange(0, num_of_mixed_lines):
	random_line_index = random.randrange(0, num_of_lines)
	random_line = lines[random_line_index]
	random_line = random_line.replace("\n", "").replace("\"", "")

	print(str(i) + " ##: " + random_line)

	words_in_line = random_line.split(' ')
	num_of_words_in_line = len(words_in_line)
	if num_of_words_in_line == 1:
		num_of_words_from_line = 1
	else:
		num_of_words_from_line = random.randrange(1, num_of_words_in_line)

	print("Taking " + str(num_of_words_from_line) + " words.")

	word_range_start = 0
	word_range_end = num_of_words_from_line

	for j in xrange(word_range_start, word_range_end):
		word = words_in_line[j]

		if beginning_of_sentence:
			word = uppercase_optionally(word)
			beginning_of_sentence = False
		else:
			word = lowercase_optionally(word)

		if len(return_line) > 1:
			word = ' ' + word

		beginning_of_sentence = end_of_sentence(word)

		if len(return_line) + len(word) <= 64:
			return_line += word
		else:
			break

if beginning_of_sentence:
	mixed_line = return_line
else:
	mixed_line = return_line + ".\""

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

print("\nNew Twitter status:\n" + mixed_line + " - " + str(datetime.datetime.now().time()))

