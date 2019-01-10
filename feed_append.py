import configparser
import re
import sys

no_params_exit_code = -1
similarity_abort_exit_code = -9
punctuation_regex = r"\n|[^\w\s]"
spaces_and_short_words_regex = r"\s.?.\s|\s"


def main():
    arguments = sys.argv
    if len(arguments) < 2:
        print("ERROR: No String provided.")
        quit(no_params_exit_code)

    new_line_raw = ' '.join(arguments[1:])
    new_line = "\"" + new_line_raw + "\""

    config = configparser.ConfigParser()
    config.read("config.ini")

    options_config = config["Options"]
    verbose = options_config.get("verbose", False)

    files_config = config["Files"]

    feed_filename = files_config["feed_file"]
    feed_shuffled_filename = files_config["feed_file_shuffled"]

    feed_file = prepare_file(feed_filename)
    shuffled_feed_file = prepare_file(feed_shuffled_filename)

    append_line_if_needed(new_line, feed_file, shuffled_feed_file, verbose)
    quit(0)


def append_line_if_needed(new_line, feed_file, shuffled_feed_file, verbose=False):
    feed_lines = feed_file.readlines()
    similar_lines = find_similar_lines(feed_lines, new_line, verbose=verbose)
    if len(similar_lines) > 0:

        similar_lines_joined = ''.join(similar_lines)

        print(feed_file.name + " already contains these lines that are similar:\n" + similar_lines_joined + "\n")
        print("Do you wish to add " + new_line + "? y/n")
        input_string = input().lower()
        if input_string != "y" and input_string != "Y":
            quit(similarity_abort_exit_code)
        print()

    append_line(new_line, feed_file)
    feed_file.close()
    append_line(new_line, shuffled_feed_file)
    shuffled_feed_file.close()


def find_similar_lines(lines, other_line, sensitivity=0.8, verbose=False):
    similar_lines = []
    other_line_words = extract_long_words(other_line)

    for line in lines:
        line_words = extract_long_words(line)
        comparison_value = compare_string_lists(line_words, other_line_words)
        if verbose:
            print("Comparing 1) " + line + " with 2) " + other_line + ": " + str(comparison_value))

        if comparison_value >= sensitivity:
            similar_lines.append(line)

    return similar_lines


def compare_string_lists(string_1_words, string_2_words):
    match_counter = 0
    for string_1_word in string_1_words:

        if string_1_word in string_2_words:
            match_counter += 1

    return float(match_counter) / float(len(string_2_words))


def extract_long_words(string):
    cleaned_string = string.lower()
    cleaned_string = re.sub(punctuation_regex, "", cleaned_string)
    words = re.split(spaces_and_short_words_regex, cleaned_string)
    return words


def append_line(line, opened_file):
    opened_file.readlines()
    print("Appending " + line + " to " + opened_file.name + ".")
    opened_file.writelines("\n" + line)

    opened_file.seek(0)
    num_of_lines = len(opened_file.readlines())
    print("Feed file now contains " + str(num_of_lines) + " lines.")
    print()


def prepare_file(file_name):
    # open(file_name, "w+")
    return open(file_name, "r+", encoding="utf-8")


main()
