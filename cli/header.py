from pyfiglet import print_figlet
from termcolor import colored


def header():
    print_figlet("IGDL", font="slant")

    print(colored("InstagramDL v0.1.0a", attrs=["bold"]))
    print("Download instagram posts, and stories - Made by fxrcha with love")
    print()
