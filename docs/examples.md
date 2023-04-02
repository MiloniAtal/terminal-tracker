
# Examples

## Getting started notebooks

- [Frequent Commands](https://github.com/MiloniAtal/terminal-tracker/tree/main/terminal_tracker/examples/Frequency.ipynb)
- [Time and Tags](https://github.com/MiloniAtal/terminal-tracker/tree/main/terminal_tracker/examples/TagTime.ipynb)
- [Searching](https://github.com/MiloniAtal/terminal-tracker/tree/main/terminal_tracker/examples/Searching.ipynb)

## Most Frequently Used

```
from terminal_tracker import FrequencyFile
ff = FrequencyFile("zsh_history_file.txt", timeframe=False, shell="zsh")

# Finding the most frequent start command
most_frequent_start_command = ff.find_most_frequent_start()

# Find the top 5 most frequently used start commands
top_frequent_commands = ff.find_top_full(5)

# Printing utility
ff.print_top(type="full", N=10)

# Alias findinf
alias_command = ff.recommend_alias()
```
 
## Tags

```
from terminal_tracker import Tags
tg = Tags("zsh_history_file.txt", timeframe=False, shell="zsh")

# Search for "project", get the dataframe
project_df = tg.search_df("project")

# Search for "project", get the commands
project_command_list = tg.search("project")
```

## Time Analysis

```
from terminal_tracker import TimeAnalysis
tg = TimeAnalysis("zsh_history_file.txt", shell="zsh")

# Search for "2023-02-18", get the dataframe
date_df = tg.search_day("2023-02-18")

```

## Searching

```
from terminal_tracker import SearchFile
sf = SearchFile("bash_history_file.txt")

# Search for "name", get the list of commands
command_list = sf.find("name")

# Search for "name", get the latest command
command = sf.latest("name")

# Using the latest iterator
for command in sf.latest_iterator("name"):
   print(command)

```

## Preprocessor
```
from terminal_tracker import Preprocessing
prep = Preprocessing("bash_history_file.txt", shell="bash")
```
