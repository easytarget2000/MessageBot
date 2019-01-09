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

def decision(probability):
    return random.random() < probability

def clean(string):
	string = string.replace("\n", "").replace("\"", "")
	string = string.replace(".", "")
	string = string.replace("!", "")
	return string.replace("?", "")

###

feed_file = open(FEED_FILENAME, "r")
tweet = ""
lines = feed_file.readlines()
num_of_mixed_lines = random.randrange(2, 9)
num_of_lines = len(lines)
beginning_of_sentence = True

for i in xrange(0, num_of_mixed_lines):
	random_line_index = random.randrange(0, num_of_lines)
	random_line = lines[random_line_index]
	random_line = clean(random_line)

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
		word = words_in_line[j].lower()

		if len(tweet) > 1:
			if decision(0.1):
				word = "\n" + word
			else:
				word = ' ' + word

		if len(tweet) + len(word) <= 140:
			tweet += word
		else:
			break

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

print("\nNew Twitter status:\n" + tweet + "\n\n" + str(datetime.datetime.now().time()))

