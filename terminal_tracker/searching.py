from collections import defaultdict
from operator import itemgetter
import pandas as pd

class Preprocessing:
    def __init__(self, file, timeframe=False, shell="zsh"):
        self.file = file
        self.timeframe = timeframe
        self.shell = shell
        self.df = self.convert()

    def convert(self):
        # Separate tags also
        # Multiline not handeled correctly
        if(self.shell == "zsh"):
            data = []
            if(self.timeframe):
                for line in open(self.file, "r"):
                    sep = line.split(";")
                    if(len(sep)==2):
                        time = sep[0][2:-2]
                        command = sep[1][:-1]
                        command_start = command.split(" ")[0]
                        command_options = command[len(command_start)+1:] 
                        data.append([command, time, command_start, command_options])
                    else:
                        print("Ignoring:"+ str(line))
                columns = ["Command", "Time", "Main Command", "Arguments"]
            else:
                for command in open(self.file, "r"):
                    command_start = command.split(" ")[0]
                    command_options = command[len(command_start)+1:] 
                    data.append([command, command_start, command_options])
                columns = ["Command", "Main Command", "Arguments"]
            df = pd.DataFrame(data, columns=columns)
        
        if(self.shell == "bash"):
            print("Not Implemented")
        return df

class FrequencyFile:
    def __init__(self, file, timeframe=False, shell="zsh"):
        self.file = file
        self.timeframe = timeframe
        self.shell = shell
        self.full_command_freq = self.calc_full_command_freq()
        self.start_command_freq = self.calc_start_command_freq()
        self.full_command_sorted = sorted(self.full_command_freq.items(), key = itemgetter(1), reverse = True)
        self.start_command_sorted = sorted(self.start_command_freq.items(), key = itemgetter(1), reverse = True)

    def calc_full_command_freq(self):
        command_frequency = defaultdict(lambda: 0)

        for line in open(self.file, "r"):
            command_frequency[line] += 1
        return command_frequency
    
    def calc_start_command_freq(self):
        command_frequency = defaultdict(lambda: 0)
        for line in open(self.file, "r"):
            words = line.split(" ")
            command_frequency[words[0]] += 1
        return command_frequency

    def find_most_frequent(self):
        return max(self.full_command_freq)

    def find_most_frequent_start(self):
        return max(self.start_command_freq)

    def find_top_full(self, t=10):
        return self.full_command_sorted[:t]
    
    def find_top_start(self, t=10):
        return self.start_command_sorted[:t]

    def print_top(self, type="full", N=10):
        if(type == "full"):
            top_full = self.find_top_full(N)
            for t in top_full:
                print(t[0])
        elif(type == "start"):
            top_start = self.find_start_full(N)
            for t in top_start:
                print(t[0])
        else:
            print("Type not supported")

class SearchFile:
    def __init__(self, file):
        self.file = file

    def find(self, a):
        commands = []
        for line in open(self.file, "r"):
            if(a in line):
                commands.append(line)
        return commands

    def latest(self, a):
        for line in reversed(list(open(self.file))):
            if(a in line):
                return line
        return "Not found"

    def latest_iterator(self, a):
        for line in reversed(list(open(self.file))):
            if(a in line):
                yield line

    def using_latest_iterator(self, a):
        for command in self.latest_iterator(a):
            print(command)

if __name__ == "__main__":
    file = "./history_files/zsh_history_timeframe.txt"
    prep = Preprocessing(file, True)
    print(prep.df)
    
    