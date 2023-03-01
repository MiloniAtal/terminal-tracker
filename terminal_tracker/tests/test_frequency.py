from terminal_tracker import FrequencyFile
from unittest.mock import Mock


ff = FrequencyFile("terminal_tracker/tests/zsh_test.txt", False, "zsh")

def test_most_frequent():
    most_frequent_expected = "dune exec -- bin/main.exe -l lib/test.mc > output\n"
    most_frequent = ff.find_most_frequent()
    assert(most_frequent == most_frequent_expected)
    

def test_most_frequent_start():
    most_frequent_expected = "git"
    most_frequent = ff.find_most_frequent_start()
    assert(most_frequent == most_frequent_expected)

def test_top_full():
    top_expected = [("dune exec -- bin/main.exe -l lib/test.mc > output\n",3), ("lli output\n",2)]
    top = ff.find_top_full(2)
    assert(top == top_expected)

def test_start_full():
    top_expected = [("git",5),("dune",3)]
    top = ff.find_top_start(2)
    assert(top == top_expected)

def test_recommend_alias():
    alias_expected = "dune exec -- bin/main.exe -l lib/test.mc > output\n"
    alias = ff.recommend_alias()
    assert(alias ==  alias_expected)