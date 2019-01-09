import configparser
import datetime
import random
import tweepy


def main():
	config = configparser.ConfigParser()
	config.read("config.ini")
	files_config = config["Files"]

	feed_filename = files_config["feed_file"]

	feed_lines = open(feed_filename, "r+").readlines()

	message = construct_message(feed_lines)
	print()
	print(message)


def construct_message(feed_lines):
	message = "\""
	num_of_mixed_lines = random.randrange(3, 7)
	num_of_feed_lines = len(feed_lines)
	beginning_of_sentence = True

	for line_index in range(0, num_of_mixed_lines):
		random_line_index = random.randrange(0, num_of_feed_lines)
		random_line = feed_lines[random_line_index]
		random_line = random_line.replace("\n", "").replace("\"", "")

		print(str(line_index) + " ##: " + random_line)

		words_in_line = random_line.split(' ')
		num_of_words_in_line = len(words_in_line)
		if num_of_words_in_line == 1:
			num_of_words_from_line = 1
		else:
			num_of_words_from_line = random.randrange(1, num_of_words_in_line)

		print("Taking " + str(num_of_words_from_line) + " words.")

		word_range_start = 0
		word_range_end = num_of_words_from_line

		for word_index in range(word_range_start, word_range_end):
			word = words_in_line[word_index]

			if beginning_of_sentence:
				word = word.capitalize()
			else:
				word = lowercase_optionally(word)

			if len(message) > 1:
				word = ' ' + word

			beginning_of_sentence = end_of_sentence(word)

			if len(message) + len(word) <= 140:
				message += word
			else:
				break

	return message + ".\""


def allow_case_change(word):
	return word != "I" and word != "I'm" and word != "I've" and word != "I'll"


def lowercase_optionally(word):
	if allow_case_change(word):
		return word.lower()
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
