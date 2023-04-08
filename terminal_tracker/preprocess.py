import pandas as pd
import datetime
import pytz


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
