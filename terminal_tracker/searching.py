class SearchFile:
    """This is a simple search class
    Attributes:
        file (str): path to the history file
    Todo:
        * Move to using the Preprocessing class
    """

    def __init__(self, file):
        self.file = file

    def find(self, a):
        """Finds all commands containing the word

        Args:
            a (str): word

        Returns:
            list: commands containing the word
        """
        commands = []
        for line in open(self.file, "r"):
            if a in line:
                commands.append(line.replace('\n', ''))
        return commands

    def latest(self, a):
        """Finds the latest command containing the word

        Args:
            a (str): word
        Returns:
            str: the latest command containing the word
        """
        for line in reversed(list(open(self.file))):
            if a in line:
                return line.replace('\n', '')

    def latest_iterator(self, a):
        """Iterator that finds the latest commands containing the word

        Args:
            a (str): word
        Yields:
            str: commands
        """
        for line in reversed(list(open(self.file))):
            if a in line:
                yield line.replace('\n', '')

    def using_latest_iterator(self, a):
        """Printing the latest commands containing the word

        Args:
            a (str): word
        """
        for command in self.latest_iterator(a):
            print(command)
