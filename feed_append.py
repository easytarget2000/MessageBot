import configparser
import re
import sys

no_params_exit_code = -1
similarity_abort_exit_code = -9
verbose = False
punctuation_regex = r'[^\w\s]'


def main():
    arguments = sys.argv
    if len(arguments) < 2:
        print("ERROR: No String provided.")
        quit(no_params_exit_code)

    new_line_raw = ' '.join(arguments[1:])
    new_line = "\"" + new_line_raw + "\""

    config = configparser.ConfigParser()
    config.read("config.ini")
    files_config = config["Files"]

    feed_filename = files_config["feed_file"]
    feed_shuffled_filename = files_config["feed_file_shuffled"]

    feed_file = prepare_file(feed_filename)
    shuffled_feed_file = prepare_file(feed_shuffled_filename)

    append_line_if_needed(new_line, feed_file, shuffled_feed_file)
    quit(0)


def find_similar_lines(lines, other_line, sensitivity=0.8):
    similar_lines = []
    for line in lines:
        comparison_value = compare_strings(line, other_line)

        if comparison_value >= sensitivity:
            similar_lines.append(line)
            if verbose:
                print("Comparing 1) " + line + " with 2) " + other_line + ": " + str(comparison_value))

    return similar_lines


def compare_strings(string_1, string_2):
    string_1_words = extract_words(string_1)
    string_2_words = extract_words(string_2)

    match_counter = 0
    for string_1_word in string_1_words:
        if string_1_word in string_2_words:
            match_counter += 1

    return float(match_counter) / float(len(string_2_words))


def extract_words(string):
    cleaned_string = string.lower()
    cleaned_string = re.sub(punctuation_regex, '', cleaned_string)
    return cleaned_string.split(' ')


def append_line(line, opened_file):
    print("Appending " + line + " to " + opened_file.name + ".")
    opened_file.writelines("\n" + line)

    opened_file.seek(0)
    num_of_lines = len(opened_file.readlines())
    print("Feed file now contains " + str(num_of_lines) + " lines.")
    print()


def append_line_if_needed(new_line, feed_file, shuffled_feed_file):
    feed_lines = feed_file.readlines()
    similar_lines = find_similar_lines(feed_lines, new_line)
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


def prepare_file(file_name):
    # open(file_name, "w+")
    return open(file_name, "r+")


main()
