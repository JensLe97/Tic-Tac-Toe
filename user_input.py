# ====== User Input ========

def range_question(question, number):
    """Asks the user to select a number beween 1 and number and returns it as int"""
    while True:
        print()
        usr_in = input(question)
        try:
            n = int(usr_in)
            if n in range(1, number + 1):
                return n
            else:
                print("Please choose a valid game mode!")
        except ValueError:
            print("Please enter a valid number!")

def yes_no_question(question):
    """Asks the user a given yes/no questions and returns "y" or "n" """
    while True:
        print()
        again = input(question)

        if again in ["y", "n"]:
            return again
        else:
            print("Please choose 'y' for yes or 'n' for no!")

def name_question(question):
    """Asks the user for an arbitrary name and returns it"""
    while True:
        print()
        name = input(question)

        if name.strip() and name.strip()[0].isalpha():
            return name.strip()
        else:
            print("Please choose a non-empty name starting with a letter!")