import configparser
import datetime
import random
import tweepy


def main():
	config = configparser.ConfigParser()
	config.read("config.ini")
	files_config = config["Files"]

	feed_filename = files_config["feed_file"]

	feed_file = open(feed_filename, "r")
	feed_lines = feed_file.readlines()
	print(construct_message(feed_lines))


def construct_message(feed_lines):
	message = "\""
	num_of_mixed_lines = random.randrange(2, 6)
	num_of_lines = len(feed_lines)
	beginning_of_sentence = True

	for i in xrange(0, num_of_mixed_lines):
		random_line_index = random.randrange(0, num_of_lines)
		random_line = feed_lines[random_line_index]
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

			if len(message) > 1:
				word = ' ' + word

			beginning_of_sentence = end_of_sentence(word)

			if len(message) + len(word) <= 64:
				message += word
			else:
				break

	if beginning_of_sentence:
		mixed_line = message
	else:
		mixed_line = message + ".\""

	return message

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


def send_tweet(tweet, twitter_config):
	auth = tweepy.OAuthHandler(twitter_config["twitter_consumer_key"], twitter_config["twitter_consumer_secret"])
	auth.set_access_token(twitter_config["twitter_access_key"], twitter_config["twitter_access_secret"])
	api = tweepy.API(auth)
	api.update_status(status=tweet)

	time = datetime.datetime.now().time()
	print("Sent:\n" + tweet + str(time))
	print()


main()
