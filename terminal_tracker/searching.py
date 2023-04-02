from collections import defaultdict
from operator import itemgetter
import pandas as pd
import datetime
from argparse import ArgumentParser
import pytz


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


class Preprocessing:
    """
    This class helps in preprocessing the history files

    Attributes:
        file (str): path to the history file
        timeframe (bool): whether time values are present in the history file
        shell (str): "zsh" or "bash"
        df (pandas.DataFrame):
            Columns:
                Command(str), Main Command (str), Arguments (str), Tags (str)
            Optional Columns:
                Time (str), Pretty Time (datetime.datetime)
    """

    def __init__(self, file, timeframe=False, shell="zsh"):
        self.file = file
        self.timeframe = timeframe
        self.shell = shell
        self.df = self._convert()

    def _convert(self):
        if self.timeframe:
            return self._convert_timeframe()
        else:
            return self._convert_no_timeframe()

    def _convert_no_timeframe(self):
        data = []
        for command in open(self.file, "r"):
            command = command.replace('\n', '')
            command_start = command.split(" ")[0]
            command_rest = command[len(command_start) + 1 :]
            index = command_rest.find("#")
            if index == -1:
                command_options = command_rest.replace('\n', '')
                tags = ""
            else:
                command_options = command_rest[: (index - 1)]
                # Last line error
                tags = command_rest[index + 1 :].replace('\n', '')
            data.append([command, command_start, command_options, tags])
        columns = ["Command", "Main Command", "Arguments", "Tags"]
        df = pd.DataFrame(data, columns=columns)
        return df

    def _convert_timeframe(self):
        if self.shell == "zsh":
            data = self._convert_timeframe_zsh()
        elif self.shell == "bash":
            data = self._convert_timeframe_bash()
        columns = ["Command", "Time", "Pretty Time", "Main Command", "Arguments", "Tags"]
        df = pd.DataFrame(data, columns=columns)
        return df

    def _convert_timeframe_zsh(self):
        data = []
        for line in open(self.file, "r"):
            sep = line.split(";")
            if len(sep) == 2:
                # TODO: Currently assumes Unix timestamp
                time = sep[0][2:].split(":")[0]
                if ":" in time:
                    # TODO: remove?
                    print(line)
                pretty_time = datetime.datetime.fromtimestamp(int(time), tz=pytz.utc)
                command = sep[1][:].replace('\n', '')
                command_start = command.split(" ")[0]
                command_rest = command[len(command_start) + 1 :]
                index = command_rest.find("#")
                if index == -1:
                    command_options = command_rest
                    tags = ""
                else:
                    command_options = command_rest[: (index - 1)]
                    # Last line error
                    tags = command_rest[index + 1 :]
                data.append([command, time, pretty_time, command_start, command_options, tags])
            # Multiline not handeled correctly
            else:
                print("Ignoring:" + str(line))
        return data

    def _convert_timeframe_bash(self):
        data = []
        prev = False
        for line in open(self.file, "r"):
            if line[0] == "#":
                prev = True
                time = line[1:].replace('\n', '')
            else:
                if prev:
                    # TODO: Currently assumes Unix timestamp
                    prev = False
                    pretty_time = datetime.datetime.fromtimestamp(int(time), tz=pytz.utc)
                else:
                    time = "No"
                    pretty_time = "No"
                command = line.replace('\n', '')
                command_start = command.split(" ")[0]
                command_rest = command[len(command_start) + 1 :]
                index = command_rest.find("#")
                if index == -1:
                    command_options = command_rest
                    tags = ""
                else:
                    command_options = command_rest[: (index - 1)]
                    # Last line error
                    tags = command_rest[index + 1 :]
                data.append([command, time, pretty_time, command_start, command_options, tags])
        return data


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


class Tags:
    """This class helps to search commands with certain tags

    Attributes:
        prep (Preprocessing): Preprocessing the file using the Preprocessing class
        df (pandas.DataFrame):
            Preprocessed dataframe
            Columns:
                Command(str), Main Command (str), Arguments (str), Tags (str)
            Optional Columns:
                Time (str), Pretty Time (datetime.datetime)
    """

    def __init__(self, file, timeframe, shell):
        self.prep = Preprocessing(file, timeframe, shell)
        self.df = self.prep.df

    def search_df(self, a):
        """
        Searches for commands with tag "a" in history file and get the entire information

        Args:
            a (str): Tag

        Returns:
            pandas.Dataframe: Dataframe with only rows with commands containing the tag
        """
        return self.df[self.df["Tags"].str.contains(a, case=False, na=False)]

    def search(self, a):
        """
        Searches for commands with tag "a" in history file and get only the commands

        Args:
            a (str): Tag

        Returns:
            list: Commands containing the tag "a"
        """
        df = self.search_df(a)
        return df["Command"].values.tolist()


class TimeAnalysis:
    """This class helps to search commands with certain tags

    Attributes:
        prep (Preprocessing): Preprocessing the file using the Preprocessing class
        df (pandas.DataFrame):
            Preprocessed dataframe
            Columns:
                Command(str), Main Command (str), Arguments (str), Tags (str),
                Time (str), Pretty Time (datetime.datetime)

    Todo:
        * reject files with no timeframe
    """

    def __init__(self, file, shell):
        self.prep = Preprocessing(file, True, shell)
        self._df_raw = self.prep.df
        self.df = self._remove_no_time_rows()

    def _remove_no_time_rows(self):
        return self._df_raw[self._df_raw["Pretty Time"] != "No"].reset_index(drop=True)

    def search_day(self, day):
        """Finds commands that were executed on the given day

        Args:
            day (str): Day in 2023-02-18 format

        Returns:
            pandas.DataFrame: Dataframe containing rows that were executed on the day

        """
        return self.df[self.df['Pretty Time'].astype(str).str.contains(day)].reset_index(drop=True)


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


if __name__ == "__main__":
    args = argumentparser()
    # file = "./history_files/bash_history_timeframe.txt"
    prep = Preprocessing(args.file, args.time, args.shell)
    # print(prep.df)
    # ta = TimeAnalysis(file, "bash")
    # print(ta.remove_no_time_rows())
    # print(ta.search_day('2023-02-18'))
    # print(tags.search("NLP"))
    # freq = FrequencyFile(file)
    # freq.print_top()
    # print(freq.recommend_alias())
