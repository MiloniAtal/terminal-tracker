from collections import defaultdict
from operator import itemgetter


class FrequencyFile:
    """This class helps to calculate the frequencies of the commands

    Attributes:
        file (str): path to the history file
        timeframe (bool): whether time values are present in the history file
        shell (str): "zsh" or "bash"
        full_command_freq (dic): Frequency of each "full" command
        start_command_freq (dic): Frequency of each "start" command
        full_command_freq (list): Frequency of each "full" command in order of decreasing frequency
        start_command_freq (dic): Frequency of each "start" command in order of decreasing frequency

    Todo:
        * Only works with files without timeframe and tags
    """

    def __init__(self, file, timeframe=False, shell="zsh"):
        self.file = file
        self.timeframe = timeframe
        self.shell = shell
        self.full_command_freq = self.calc_full_command_freq()
        self.start_command_freq = self.calc_start_command_freq()
        self.full_command_sorted = sorted(self.full_command_freq.items(), key=itemgetter(1), reverse=True)
        self.start_command_sorted = sorted(self.start_command_freq.items(), key=itemgetter(1), reverse=True)

    def calc_full_command_freq(self):
        """
        Calculates the frequency of each "full" command

        Returns:
            dic: Frequency of each "full" command
        """
        command_frequency = defaultdict(lambda: 0)
        for line in open(self.file, "r"):
            command_frequency[line.replace('\n', '')] += 1
        return command_frequency

    def calc_start_command_freq(self):
        """
        Calculates the frequency of each "start" command

        Returns:
            dic: Frequency of each "start" command
        """
        command_frequency = defaultdict(lambda: 0)
        for line in open(self.file, "r"):
            words = line.split(" ")
            command_frequency[words[0]] += 1
        return command_frequency

    def find_most_frequent(self):
        """
        Finds the most frequent "full" command

        Returns:
            str: most frequent "full" command
        """
        return self.full_command_sorted[0][0]

    def find_most_frequent_start(self):
        """
        Finds the most frequent "start" command

        Returns:
            str: most frequent "start" command
        """
        return self.start_command_sorted[0][0]

    def find_top_full(self, t=10):
        """
        Finds the top "t" most frequent "full" command

        Args:
            t (int): Number of commands

        Returns:
            list: top "t" most frequent "full" command
        """
        if t > len(self.full_command_sorted):
            return self.full_command_sorted
        return self.full_command_sorted[:t]

    def find_top_start(self, t=10):
        """
        Finds the top "t" most frequent "start" command

        Args:
            t (int): Number of commands

        Returns:
            list: top "t" most frequent "start" command
        """
        if t > len(self.start_command_sorted):
            return self.start_command_sorted
        return self.start_command_sorted[:t]

    def print_top(self, type="full", N=10):
        """
        Helper function to print the most frequent commands

        Args:
            N (int): Number of commands
            type (str): "full" or "start"
        """
        if type == "full":
            top_full = self.find_top_full(N)
            for t in top_full:
                print("Freq: " + str(t[1]) + " -> " + str(t[0]))
        elif type == "start":
            top_start = self.find_top_start(N)
            for t in top_start:
                print("Freq: " + str(t[1]) + " -> " + str(t[0]))
        else:
            print("Type not supported")

    def recommend_alias(self, weight_freq=0.5, weight_len=0.5):
        """
        Recommends functions that should have an alias based on length and
        frequency of command usage

        Args:
            weight_freq (float): Weight given to frequency of command
            weight_len (float): Weight given to lenght of command
        """
        top = self.find_top_full()
        max_score = 0
        max_command = ""
        for value in top:
            t, f = value
            score = len(t) * weight_len + f * weight_freq
            if score > max_score:
                max_score = score
                max_command = t
        return max_command
