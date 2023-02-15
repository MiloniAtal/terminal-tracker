from collections import defaultdict

def find( a, file):
    commands = []
    for line in open(file, "r"):
        if(a in line):
            commands.append(line)
    return commands

def latest(a, file):
    for line in reversed(list(open(file))):
        if(a in line):
            return line
    return "Not found"

def latest_iterator(a, file):
    for line in reversed(list(open(file))):
        if(a in line):
            yield line

def using_latest_iterator(a, file):
    for command in latest_iterator(a, file):
        print(command)

def frequency_full_command(file):
    command_frequency = defaultdict(lambda: 0)
    for line in open(file, "r"):
        command_frequency[line] += 1
    return command_frequency

def frequency_start_command(file):
    command_frequency = defaultdict(lambda: 0)
    for line in open(file, "r"):
        words = line.split(" ")
        command_frequency[words[0]] += 1
    return command_frequency

def find_most_frequent(file):
    freqs = frequency_full_command(file)
    return max(freqs)

def find_most_frequent_start(file):
    freqs = frequency_start_command(file)
    return max(freqs)
    
def find_top(file, t=10):
    return "Not implemented yet"

if __name__ == "__main__":
    file = "./history_files/zsh_history.txt"
    print(find_most_frequent_start(file))
    
    