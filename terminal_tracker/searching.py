from collections import defaultdict
from operator import itemgetter
import pandas as pd
import datetime
from argparse import ArgumentParser

def argumentparser():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file" , help="Path to history file")
    parser.add_argument("-s", "--shell", choices=["bash", "zsh"], default="zsh", help="The shell being used")
    parser.add_argument("-t","--time", type=bool, default=False, help="Is time being stored in the history file")
    args = parser.parse_args()
    return args

#remove_duplicates=False
class Preprocessing:
    def __init__(self, file, timeframe=False, shell="zsh"):
        self.file = file
        self.timeframe = timeframe
        self.shell = shell
        self.df = self.convert()

    def convert(self):
        if(self.timeframe):
            return self.convert_timeframe()
        else:
            return self.convert_no_timeframe()

    def convert_no_timeframe(self):
        data = []
        for command in open(self.file, "r"):
            command = command.replace('\n', '')
            command_start = command.split(" ")[0]
            command_rest = command[len(command_start)+1:] 
            index = command_rest.find("#")
            if(index==-1):
                command_options = command_rest.replace('\n', '')
                tags = ""
            else:
                command_options = command_rest[:(index-1)]
                #Last line error
                tags = command_rest[index+1:].replace('\n', '')
            data.append([command, command_start, command_options, tags])
        columns = ["Command", "Main Command", "Arguments", "Tags"]
        df = pd.DataFrame(data, columns=columns)
        return df
    
    def convert_timeframe(self):
        if(self.shell == "zsh"):
            data = self.convert_timeframe_zsh()
        elif(self.shell=="bash"):
            data = self.convert_timeframe_bash()
        columns = ["Command", "Time", "Pretty Time", "Main Command", "Arguments", "Tags"]
        df = pd.DataFrame(data, columns=columns)
        return df

    def convert_timeframe_zsh(self):
        data = []
        for line in open(self.file, "r"):
            sep = line.split(";")
            if(len(sep)==2):
                #TODO: Currently assumes Unix timestamp
                time = sep[0][2:].split(":")[0]
                if(":" in time):
                    print(line)
                pretty_time = datetime.datetime.fromtimestamp(int(time))
                command = sep[1][:].replace('\n', '')
                command_start = command.split(" ")[0]
                command_rest = command[len(command_start)+1:] 
                index = command_rest.find("#")
                if(index==-1):
                    command_options = command_rest
                    tags = ""
                else:
                    command_options = command_rest[:(index-1)]
                    #Last line error
                    tags = command_rest[index+1:]
                data.append([command, time, pretty_time, command_start, command_options, tags])
            # Multiline not handeled correctly     
            else:
                print("Ignoring:"+ str(line))
        return data
    
    def convert_timeframe_bash(self):
        data = []
        prev = False
        for line in open(self.file, "r"):
            if(line[0]=="#"):
                prev = True
                time = line[1:].replace('\n', '')
            else:
                if(prev):
                    #TODO: Currently assumes Unix timestamp
                    prev = False
                    pretty_time = datetime.datetime.fromtimestamp(int(time))
                else:
                    time = "No"
                    pretty_time = "No"
                command = line.replace('\n', '')
                command_start = command.split(" ")[0]
                command_rest = command[len(command_start)+1:] 
                index = command_rest.find("#")
                if(index==-1):
                    command_options = command_rest
                    tags = ""
                else:
                    command_options = command_rest[:(index-1)]
                    #Last line error
                    tags = command_rest[index+1:]
                data.append([command, time, pretty_time, command_start, command_options, tags])
        return data

#Only handles without timeframe, no tags?
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
        ff = self.full_command_freq
        return max(ff, key=lambda x:ff[x])

    def find_most_frequent_start(self):
        ff = self.start_command_freq
        return max(ff, key=lambda x:ff[x])

    def find_top_full(self, t=10):
        if(t > len(self.full_command_sorted)):
            return self.full_command_sorted
        return self.full_command_sorted[:t]
    
    def find_top_start(self, t=10):
        if(t > len(self.start_command_sorted)):
            return self.start_command_sorted
        return self.start_command_sorted[:t]

    def print_top(self, type="full", N=10):
        if(type == "full"):
            top_full = self.find_top_full(N)
            for t in top_full:
                print("Freq: " + str(t[1]) +  " -> " + str(t[0]))
        elif(type == "start"):
            top_start = self.find_start_full(N)
            for t in top_start:
                print(t[0])
        else:
            print("Type not supported")
    
    def recommend_alias(self, weight_freq=0.5, weight_len=0.5):
        top = self.find_top_full()
        max_score = 0
        max_command = ""
        for value in top:
            t, f = value
            print(t, f)
            score = len(t)*weight_len + f*weight_freq
            if(score > max_score):
                max_score = score
                max_command = t
        return max_command


class Tags:
    def __init__(self, file, timeframe, shell):
        self.prep = Preprocessing(file, timeframe, shell)
        self.df = self.prep.df

    def search_df(self, a):
        return self.df[self.df["Tags"].str.contains(a, case=False, na=False)]
    
    def search(self, a):
        df = self.search_df(a)
        return df["Command"].values.tolist()

class TimeAnalysis:
    #TODO: reject files with no timeframe
    def __init__(self, file, shell):
        self.prep = Preprocessing(file, True, shell)
        self.df_raw = self.prep.df
        self.df = self.remove_no_time_rows()
    
    def remove_no_time_rows(self):
        return self.df_raw[self.df_raw["Pretty Time"] != "No"]

    #TODO:day in 2023-02-18 format
    def search_day(self, day):
        return self.df[ self.df['Pretty Time'].astype(str).str.contains(day)]
    
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
    
    