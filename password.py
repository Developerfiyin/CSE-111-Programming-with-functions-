
#
# This program lets employees type in passwords and see how strong they are.
# The strength is a number from 0 (very weak) to 5 (very strong).
#
# Files needed in the same folder as this program:
#   dictionary.txt    - about 70,000 words, one word per line
#   toppasswords.txt  - the top 1 million passwords, one per line
#
# OPTIONAL COMPONENT (added by me):
#   The function give_tips() looks at a password and tells the user which
#   kinds of characters are missing (upper case, lower case, digits, symbols)
#   and if the password is short. This helps employees learn HOW to make
#   their password better, which is the goal of this tool. It is only
#   called from the main program, so password_strength() still works
#   exactly as Sven designed it.

import string

# File names for the two lists
DICTIONARY_FILE = "dictionary.txt"
TOP_PASSWORDS_FILE = "toppasswords.txt"

# Lists of the 4 kinds of characters
UPPER_CHARS = string.ascii_uppercase      # A-Z
LOWER_CHARS = string.ascii_lowercase      # a-z
DIGIT_CHARS = string.digits               # 0-9
SPECIAL_CHARS = string.punctuation        # symbols like ! @ # $ %


def word_in_file(word, filename, case_sensitive=False):
    """Check if a word is in a file (one word per line).

    word           - the word to look for
    filename       - the name of the file to search
    case_sensitive - False means 'Apple' matches 'apple' (default)
                     True means the upper/lower case must match exactly

    Returns True if the word is found, otherwise False.
    """
    # If we are NOT case sensitive, change the word to lower case
    if case_sensitive == False:
        word = word.lower()

    found = False

    # Open the file and look at each line
    with open(filename, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            line = line.strip()      # remove the newline and extra spaces

            if case_sensitive == False:
                line = line.lower()

            if line == word:
                found = True
                break                # no need to keep looking

    return found


def word_has_character(word, character_list):
    """Check if a word has at least one character from character_list.

    word           - the word to check (a string)
    character_list - the characters we are looking for (a string or a list)

    Returns True if any character of the word is in character_list,
    otherwise False.
    """
    for letter in word:
        if letter in character_list:
            return True

    return False


def password_strength(password, min_length=10, strong_length=16):
    """Calculate how strong a password is, from 0 to 5.

    password      - the password to check
    min_length    - passwords shorter than this are not secure (default 10)
    strong_length - passwords this long or longer are strong (default 16,
                    which means "longer than 15 characters")

    Prints a message about the password and returns the strength number.
    """
    # Rule 1: dictionary word (case insensitive) -> strength 0
    if word_in_file(password, DICTIONARY_FILE, case_sensitive=False):
        print("Password is a dictionary word and is not secure.")
        return 0

    # Rule 2: top password list (case sensitive) -> strength 0
    if word_in_file(password, TOP_PASSWORDS_FILE, case_sensitive=True):
        print("Password is a commonly used password and is not secure.")
        return 0

    # Rule 3: too short -> strength 1
    if len(password) < min_length:
        print("Password is too short and is not secure.")
        return 1

    # Rule 4: long password -> strength 5
    if len(password) >= strong_length:
        print("Password is long, length trumps complexity this is a good password.")
        return 5

    # Rule 5: everything else is scored by complexity
    # Complexity = how many of the 4 kinds of characters are used
    complexity = 0

    if word_has_character(password, UPPER_CHARS):
        complexity = complexity + 1

    if word_has_character(password, LOWER_CHARS):
        complexity = complexity + 1

    if word_has_character(password, DIGIT_CHARS):
        complexity = complexity + 1

    if word_has_character(password, SPECIAL_CHARS):
        complexity = complexity + 1

    # Strength is a base score of 1 plus the complexity score
    strength = 1 + complexity

    # Tell the user how they did
    if strength == 5:
        print("Password is strong. It uses all 4 kinds of characters.")
    elif strength >= 3:
        print("Password is okay, but it could be stronger.")
    else:
        print("Password is weak. It does not use enough kinds of characters.")

    return strength


def give_tips(password, min_length=10):
    """OPTIONAL COMPONENT: print tips to help the user improve a password."""
    tips = []

    if len(password) < min_length:
        tips.append("Make it at least " + str(min_length) + " characters long.")

    if not word_has_character(password, UPPER_CHARS):
        tips.append("Add an upper case letter.")

    if not word_has_character(password, LOWER_CHARS):
        tips.append("Add a lower case letter.")

    if not word_has_character(password, DIGIT_CHARS):
        tips.append("Add a number.")

    if not word_has_character(password, SPECIAL_CHARS):
        tips.append("Add a special symbol like ! or #.")

    if len(tips) > 0:
        print("Tips to improve your password:")
        for tip in tips:
            print(" - " + tip)
        print("Remember: a password of 16 or more characters is always strong!")


def main():
    """Let the user check passwords until they choose to quit."""
    print("=== Password Strength Checker ===")
    print("Strength goes from 0 (very weak) to 5 (very strong).")

    keep_going = True

    while keep_going:
        print()
        password = input("Enter a password to check (or type 'quit' to exit): ")

        if password == "quit":
            keep_going = False
        else:
            try:
                strength = password_strength(password)
                print("Password strength: " + str(strength) + " out of 5")

                # Optional component: only give tips if it is not a 5
                if strength < 5:
                    give_tips(password)

            except FileNotFoundError:
                print("Error: could not find " + DICTIONARY_FILE + " or "
                      + TOP_PASSWORDS_FILE + ".")
                print("Make sure both files are in the same folder as this program.")
                keep_going = False

    print("Thanks for using the Password Strength Checker. Stay secure!")


# Only run the program if this file is run directly.
# This lets other projects import password_strength() without starting the menu.
if __name__ == "__main__":
    main()