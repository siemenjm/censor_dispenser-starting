# These are the emails you will be censoring. The open() function is opening the text file that the emails are
# contained in and the .read() method is allowing us to save their contexts to the following variables:
email_one = open("email_one.txt", "r").read()
email_two = open("email_two.txt", "r").read()
email_three = open("email_three.txt", "r").read()
email_four = open("email_four.txt", "r").read()

# Words to be censored from email_two
proprietary_terms = ["she", "personality matrix", "sense of self", "self-preservation", "learning algorithm", "her", "herself"]

# Words censored after used more than once
negative_words = ["concerned", "behind", "danger", "dangerous", "alarming", "alarmed", "out of control", "help", "unhappy", "bad", "upset", "awful", "broken", "damage", "damaging", "dismal", "distressed", "distressed", "concerning", "horrible", "horribly", "questionable"]


# Censors word from input text
def censor_word(input, word):
    redacted = redact(word)
    input = input.replace(word, redacted)
    return input

# Censors word from list of words from input text
def censor_list(input, word_list):
    sorted_word_list = sort_list_by_element_length(word_list)
    for word in sorted_word_list:
        variants = word_variants(word)
        for variant in variants:
            input = censor_word(input, variant)
    return input

# Censors words from list (like function censor_list) and censors negative words after two or more uses
def censor_multiple_lists(input, word_list, negative_list):
    input_censored = censor_list(input, word_list)
    censored_split = input_censored.split()
    print(censored_split)
    negative_count = 0
    for i in range(len(censored_split)):
        if censored_split[i] in negative_list:
            negative_count += 1
            if negative_count > 1:
                censored_split[i] = redact(censored_split[i])
    joined_censored = " ".join(censored_split)
    return joined_censored

# Also censors words that come before AND after a term from the two lists
def final_censor(input, word_list, negative_list):
    input_censored = censor_multiple_lists(input, word_list, negative_list)
    censored_split = input_censored.split()
    censored_again_split = list(censored_split)
    index = 0
    while index < len(censored_split):
        if index == 0:
            if censored_split[index].find("#") != -1:
                after_censored = redact(censored_split[index + 1])
                censored_again_split[index + 1] = after_censored
        elif index == (len(censored_split) - 1):
            if censored_split[index].find("#") != -1:
                before_censored = redact(censored_split[index - 1])
                censored_again_split[index - 1] = before_censored
        else:
            if censored_split[index].find("#") != -1:
                before_censored = redact(censored_split[index - 1])
                censored_again_split[index - 1] = before_censored
                after_censored = redact(censored_split[index + 1])
                censored_again_split[index + 1] = after_censored
        index += 1
    joined_censored = " ".join(censored_again_split)
    return joined_censored

# Replaces word with #'s
def redact(word):
    redacted_string = ""
    for letter in word:
        if letter == " ":
            redacted_string += " "
        else:
            redacted_string += "#"
    return redacted_string

# Checks for other variants of censored words (cases)
def word_variants(word):
    lower = word.lower()
    upper = word.upper()
    title = word.title()
    # If word is actually a phrase as the from of a sentence, only capitalize first word.
    if word.find(" ") != -1:
        phrase = word.split()
        titled_phrase = phrase[0].title()
        phrase[0] = titled_phrase
        joined_phrase = " ".join(phrase)
        variants = [word, lower, upper, title, joined_phrase]
    else:
        variants = [word, lower, upper, title]
    return variants

# Returns length of a string
def string_length(string):
    return len(string)

# Sorts censored word list by length of word/phrase. For example, we want "herself" to be censored before "her",
# otherwise the censor function will see "###self" and not censor the "self" portion. Ordering from longest to shortest
# gets around this (I think).
def sort_list_by_element_length(input_list):
    input_list.sort(key=string_length)
    input_list.reverse()
    return input_list


# Uncomment lines below to run the program, good luck!!! (First program, go easy :))
#print(censor_word(email_one, "learning algorithms"))
#print(censor_list(email_two, proprietary_terms))
#print(censor_multiple_lists(email_three, proprietary_terms, negative_words))
#print(final_censor(email_four, proprietary_terms, negative_words))
