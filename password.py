import os
import string
import random

# Lists of the 4 kinds of characters
UPPER_CHARS = string.ascii_uppercase      # A-Z
LOWER_CHARS = string.ascii_lowercase      # a-z
DIGIT_CHARS = string.digits               # 0-9
SPECIAL_CHARS = string.punctuation        # symbols like ! @ # $ %




def find_data_file(default_name, keyword):
    """Find a data file and return its path.

    default_name - the file name we expect (like 'toppasswords.txt')
    keyword      - a word that should be in the file name (like 'top')

    It looks in the current folder and in the folder of this program.
    First it tries the exact name, then any .txt file with the keyword
    in its name. If nothing is found, it just returns default_name.
    """
    this_folder = os.path.dirname(os.path.abspath(__file__))
    folders = [os.getcwd(), this_folder]

    for folder in folders:
        if os.path.isdir(folder):
            for name in os.listdir(folder):
                if name.lower() == default_name.lower():
                    return os.path.join(folder, name)

    # Next, try any .txt file with the keyword in the name
    for folder in folders:
        if os.path.isdir(folder):
            for name in os.listdir(folder):
                if keyword in name.lower() and name.lower().endswith(".txt"):
                    return os.path.join(folder, name)

    return default_name


# File names for the two lists
DICTIONARY_FILE = find_data_file("dictionary.txt", "dict")
TOP_PASSWORDS_FILE = find_data_file("toppasswords.txt", "top")



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
            line = line.strip()      

            if case_sensitive == False:
                line = line.lower()

            if line == word:
                found = True
                break                

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


def word_complexity(word):
    """Calculate the complexity score of a word, from 1 to 4.

    The score is how many of the 4 kinds of characters the word uses:
    upper case letters, lower case letters, digits, and special symbols.
    Example: 'abc' = 1, 'Abc' = 2, 'Abc1' = 3, 'Abc1!' = 4
    """
    complexity = 0

    if word_has_character(word, UPPER_CHARS):
        complexity = complexity + 1

    if word_has_character(word, LOWER_CHARS):
        complexity = complexity + 1

    if word_has_character(word, DIGIT_CHARS):
        complexity = complexity + 1

    if word_has_character(word, SPECIAL_CHARS):
        complexity = complexity + 1

    return complexity


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
    # Strength is a base score of 1 plus the complexity score
    complexity = word_complexity(password)
    strength = 1 + complexity

    # Tell the user how they did
    if strength == 5:
        print("Password is strong. It uses all 4 kinds of characters.")
    elif strength >= 3:
        print("Password is okay, but it could be stronger.")
    else:
        print("Password is weak. It does not use enough kinds of characters.")

    return strength



def show_meter(strength):
    """Draw a strength bar and a fun label for a score from 0 to 5."""
    labels = [
        "Wide open - a hacker would guess this in a blink!",
        "Very weak - a screen door on a submarine.",
        "Weak - getting there, keep going!",
        "Decent - a locked door, but not a vault.",
        "Pretty good - almost a fortress!",
        "Fortress - the cell tower of passwords!"
    ]

    filled = "#" * strength
    empty = "-" * (5 - strength)

    print("[" + filled + empty + "]  " + labels[strength])


def give_tips(password, min_length=10):
    """Print tips to help the user improve a password."""
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


def estimate_crack_time(password, strength):
    """Print a fun guess of how long brute force would take.

    We count how many different characters could be in each spot (the
    'pool'), then work out how many guesses it takes on average. We pretend
    a computer can make 10 billion guesses every second.
    This is only a rough, fun estimate!
    """
    if strength == 0:
        print("Crack time: instantly - it is on a list hackers already have.")
        return

    # How many characters could be used in each spot?
    pool = 0
    if word_has_character(password, LOWER_CHARS):
        pool = pool + 26
    if word_has_character(password, UPPER_CHARS):
        pool = pool + 26
    if word_has_character(password, DIGIT_CHARS):
        pool = pool + 10
    if word_has_character(password, SPECIAL_CHARS):
        pool = pool + len(SPECIAL_CHARS)
    if pool == 0:
        pool = 1        # password only has spaces or other odd characters

    # On average a hacker finds it after trying half of all the guesses
    guesses = (pool ** len(password)) // 2
    seconds = guesses // 10000000000

    minute = 60
    hour = 60 * minute
    day = 24 * hour
    year = 365 * day

    if seconds < 1:
        text = "less than a second"
    elif seconds < minute:
        text = str(seconds) + " seconds"
    elif seconds < hour:
        text = str(seconds // minute) + " minutes"
    elif seconds < day:
        text = str(seconds // hour) + " hours"
    elif seconds < year:
        text = str(seconds // day) + " days"
    elif seconds < year * 1000000:
        text = str(seconds // year) + " years"
    elif seconds < year * 14000000000:
        text = "millions of years"
    else:
        text = "longer than the age of the universe"

    print("Crack time (rough guess): " + text)


def make_passphrase(word_count=4):
    """Make a random passphrase from dictionary words.

    Example: Tiger-Cloud-Rocket-Maple42
    Picking random words makes it hard to guess, and a story like
    "tiger, cloud, rocket, maple" is easy for a person to remember.
    """
    # Read the dictionary and keep only words that are 4+ letters
    # and have only letters (no apostrophes etc.)
    good_words = []
    with open(DICTIONARY_FILE, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            line = line.strip()
            if len(line) >= 4 and line.isalpha():
                good_words.append(line)

    # Keep making passphrases until one is at least 16 characters long
    passphrase = ""
    while len(passphrase) < 16:
        chosen = random.sample(good_words, word_count)

        # Capitalize each word and join them with dashes
        for i in range(len(chosen)):
            chosen[i] = chosen[i].capitalize()
        passphrase = "-".join(chosen)

        # Add a random two digit number on the end
        passphrase = passphrase + str(random.randint(10, 99))

    return passphrase


def show_summary(checked, best_score):
    """Print a short summary of the session."""
    print()
    print("--- Session summary ---")
    print("Passwords checked: " + str(checked))

    if checked > 0:
        print("Best score: " + str(best_score) + " out of 5")
        if best_score == 5:
            print("You made a password fortress. Great job!")
        else:
            print("Next time, try for a 5 - long passphrases are the easy way!")


def check_files_exist():
    """Make sure both word files can be found.

    If a file is missing, ask the user to type its name instead of
    stopping the whole program.  Returns True when both files are ready,
    or False if the user gives up (by pressing Enter with no name).
    """
    global DICTIONARY_FILE
    global TOP_PASSWORDS_FILE

    while not os.path.isfile(DICTIONARY_FILE):
        print("Could not find the dictionary file '" + DICTIONARY_FILE + "'.")
        name = input("Type the dictionary file name (or press Enter to give up): ")
        if name.strip() == "":
            return False
        DICTIONARY_FILE = find_data_file(name.strip(), name.strip().lower())

    while not os.path.isfile(TOP_PASSWORDS_FILE):
        print("Could not find the top passwords file '" + TOP_PASSWORDS_FILE + "'.")
        name = input("Type the top passwords file name (or press Enter to give up): ")
        if name.strip() == "":
            return False
        TOP_PASSWORDS_FILE = find_data_file(name.strip(), name.strip().lower())

    return True


def main():
    """Let the user check passwords until they enter Q to quit."""
    print("=" * 50)
    print("      PASSWORD STRENGTH CHECKER")
    print("=" * 50)
    print("Strength goes from 0 (very weak) to 5 (very strong).")
    print("Type a password to check it, or:")
    print("   S = get a random passphrase idea")
    print("   Q = quit the program")
    print("Tip: don't type your REAL work password - try a similar one!")

    # Make sure the word files are there before we start
    if not check_files_exist():
        print("The word files are needed to check passwords. Goodbye!")
        return

    checked = 0          # how many passwords were checked
    best_score = 0       # the highest score so far
    keep_going = True

    while keep_going:
        print()
        password = input("Enter a password to check (S = suggest, Q = quit): ")

        # Commands are not case sensitive: q and Q both quit
        command = password.strip().lower()

        if command == "q":
            keep_going = False

        elif command == "s":
            idea = make_passphrase()
            print("How about this passphrase:  " + idea)
            print("Let's see how strong it is:")
            strength = password_strength(idea)
            show_meter(strength)
            estimate_crack_time(idea, strength)
            print("Don't use this exact one, make up your own!")

        else:
            strength = password_strength(password)
            show_meter(strength)
            estimate_crack_time(password, strength)

            checked = checked + 1
            if strength > best_score:
                best_score = strength

            # Only give tips if it is not a 5
            if strength < 5:
                give_tips(password)

    show_summary(checked, best_score)
    print("Thanks for using the Password Strength Checker. Stay secure!")


# Only run the program if this file is run directly.
# This lets other projects import password_strength() without starting the menu.
if __name__ == "__main__":
    main()