# Class for logger
# Singelton class for logging idented progress

from logging import Logger
from constants import IDENT


class __Logger():

    current_ident = ""

    def enter_level(self):
        self.current_ident = "   " + self.add_ident

    def exit_level(self):

        if len(self.current_ident) < len(IDENT):
            self.current_ident = ""
        else:
            self.current_ident = self.current_ident[len(IDENT):]

    def print_progress(self, message):
        print(f"{self.current_ident}{message}")

    def print_warning(self, message):
        print(f"Warning: {message}")

    def print_error(self, message):
        print(f"Error: {message}")


# Singleton
Logger = __Logger()