from argparse import ArgumentParser


def argumentparser():
    """This function will help to make the library run most commands directly from the command line

    Todo:
        * Make it usable and complete

    """
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", help="Path to history file")
    parser.add_argument("-s", "--shell", choices=["bash", "zsh"], default="zsh", help="The shell being used")
    parser.add_argument("-t", "--time", type=bool, default=False, help="Is time being stored in the history file")
    args = parser.parse_args()
    return args
