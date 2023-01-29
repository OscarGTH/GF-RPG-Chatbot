import sys
import pgf
from utils import say

absmodule = "RPGChatbot"
AVAILABLE_LANGS = ["Eng"]

class RPGBot:
    def __init__(self, args) -> None:
        """ Initializes the chatbot. """
        
        # Initializing the GF and setting the language.
        grammar = pgf.readPGF(absmodule + ".pgf")
        langcode = "RPGChatbotEng"
        if len(sys.argv) > 1:
          if sys.argv[1] in AVAILABLE_LANGS:
            langcode = absmodule + sys.argv[1]
          else:
            say("Supplied language not available.", "program")

        self.language = grammar.languages[langcode]
        self.run_main_loop()
        pass

    def run_main_loop(self):
        """Contains main input loop of the program."""

        # Running endless loop
        while True:
            say("Player input:", "program")
            user_input = input()

            if user_input == "exit":
                break
            elif user_input == "help":
                self.help()
            else:
                self.parse_command(user_input)

    def parse_command(self, user_input):
        """ Parses the user command in GF format and returns the parse tree."""
        say("Parsing command.","program")

    def help(self):
        """Prints out the possible commands."""
        say("Possible commands/questions are the following: ", "program")


def start_game(args):
    # Initializing library that allows for colored command-line printing.

    say("\nWelcome to GF-RPG Text-based dungeon game!", "program")
    say(
        'Write "help" to see the list of the commands and "exit" to quit the program.\n',
        "program",
    )
    RPGBot(args)


if __name__ == "__main__":
    start_game(sys.argv)
