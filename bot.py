import argparse
import datetime
import os
import random
import sys
import tweepy

abort_exit_code = -2
missing_params_exit_code = -10

twitter_consumer_key = "gxkrFii3PpyEp4wrKRb9W9oor"
twitter_consumer_secret = "9cpbyxAaPybWqWAky1CToNqcTFUnXZITegKVF1XIXQjzdHmpeC"
twitter_access_key = "3059527421-4E9URrmgbgte2Pa5N5GLVzn6ZXbVzoRqxOdG7kF"
twitter_access_secret = "DjlyO5ctD4ArrRi1X0ClkpOGQT1I2jjtMxuAtrt5B2Boc"


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--force", help="Force send. Do not ask.", action="store_true")
	args, file_names = parser.parse_known_args()
	ask_before_sending = not args.force
	arguments = sys.argv

	if len(file_names) < 2:
		print "ERROR: Please provide a feed and shuffled feed filename."
		quit(missing_params_exit_code)

	feed_filename = arguments[1]
	feed_shuffled_filename = arguments[2]

	shuffled_feed_file = prepare_shuffled_feed(feed_shuffled_filename, feed_filename)

	post_random_line(shuffled_feed_file, ask_before_sending)


def prepare_shuffled_feed(shuffled_feed_filename, feed_filename):
	write_feed_shuffled = not os.path.isfile(shuffled_feed_filename) or os.stat(shuffled_feed_filename).st_size < 1

	if write_feed_shuffled:
		# If needed, shuffle the feed.
		print("Creating " + shuffled_feed_filename + ".")
		feed_lines = open(feed_filename, "r").readlines()
		random.shuffle(feed_lines)
	else:
		print (shuffled_feed_filename + " exists.")

	if write_feed_shuffled:
		# If needed, write the shuffled feed into a separate file.
		feed_shuffled = open(shuffled_feed_filename, "w+")
		feed_shuffled.writelines(feed_lines)
		feed_shuffled.close()

	return open(shuffled_feed_filename, "r")


def post_random_line(feed_file, ask_before_sending=True, remove_after=True):
	lines = feed_file.readlines()

	num_of_shuffled_lines = len(lines)
	print("Number of lines in feed: " + str(num_of_shuffled_lines) + "\n")
	num_of_shuffled_lines -= 1

	# Tweet a random line from the shuffled file.
	random_line_index = random.randrange(0, num_of_shuffled_lines)
	random_line = lines[random_line_index]

	if ask_before_sending:
		print "Do you wish to send this line? y/n\n" + random_line
		input_string = raw_input().lower()
		if input_string != "y" and input_string != "Y":
			quit(abort_exit_code)

	send_tweet(random_line)

	if remove_after:
		cleaned_lines = lines
		del cleaned_lines[random_line_index]
		feed_file.seek(0)
		feed_file.writelines(cleaned_lines)

	feed_file.close()


def send_tweet(tweet):
	auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
	auth.set_access_token(twitter_access_key, twitter_access_secret)
	api = tweepy.API(auth)
	api.update_status(status=tweet)

	time = datetime.datetime.now().time()
	print("Sent:\n" + tweet + str(time))
	print


main()
