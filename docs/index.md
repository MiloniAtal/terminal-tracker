

# Welcome to terminal-tracker's documentation!

    
## Overview

This tools helps with analysing, filtering and segregrating your command history. It also provides functions to support storing of this history in a better format, that can be used share with people or used in future. It recommends commands (based of length of command and frequency of use) that should have an alias. 

## Main features
- Recommends commands that should have an alias. 
- It provides support for both zsh and bash shells. 
- Nice format to store and share history

## Installing

```
pip install terminal-tracker
```

## Dependencies

- pandas
- pytz

## Usage

```
from terminal_tracker import FrequencyFile
ff = FrequencyFile("zsh_history_file.txt", timeframe=False, shell="zsh")
most_frequent_command = ff.find_most_frequent()

```

## Configurations

These congifurations will help you to better store your history:

### zsh 

These should be added to /.zshrc

```
export HISTFILE=~/.zsh_history
export HISTFILESIZE=1000000000      # big big history
export HISTSIZE=1000000000          # big big history
setopt INC_APPEND_HISTORY           # append to history, don't overwrite it
setopt EXTENDED_HISTORY
setopt HIST_FIND_NO_DUPS            # no duplicate entries
setopt HIST_IGNORE_ALL_DUPS         # no duplicate entries
setopt interactivecomments
```

### bash

These should be added to /.bashrc

```
export HISTCONTROL=ignoredups:erasedups  # no duplicate entries
export HISTSIZE=100000                   # big big history
export HISTFILESIZE=100000               # big big history
shopt -s histappend                      # append to history, don't overwrite it

# Save and reload the history after each command finishes
export PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND"
```

## Coverage and Tests

Tests and coverage can be run using these simple make commands
```
make coverage
make test
``` 

## Contributing to terminal_tracker

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.


```eval_rst
.. toctree::
   :maxdepth: 4
   :caption: Contents:

   modules
   examples

   
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```
