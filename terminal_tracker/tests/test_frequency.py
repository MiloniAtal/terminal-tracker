from terminal_tracker import FrequencyFile
from unittest.mock import patch, mock_open

file = "terminal_tracker/tests/zsh_test.txt"


def test_command_freq():
    file_content_mock = """lli output
lli output
git status
git stash"""
    fake_file_path = file
    with patch("builtins.open", mock_open(read_data=file_content_mock)) as mock_file:
        ff = FrequencyFile(file, False, "zsh")
        actual = ff.start_command_freq
        expected = {"lli": 2, "git": 2}
        assert actual == expected
        actual = ff.full_command_freq
        expected = {"lli output": 2, "git status": 1, "git stash": 1}
        assert actual == expected
        mock_file.assert_called_with(fake_file_path, 'r')
        assert mock_file.call_count == 2


def test_sorted():
    file_content_mock = """lli output
lli output
git status
git stash
git stash"""
    fake_file_path = file
    with patch("builtins.open", mock_open(read_data=file_content_mock)) as mock_file:
        ff = FrequencyFile(file, False, "zsh")
        actual = ff.full_command_sorted
        expected = [("lli output", 2), ("git stash", 2), ("git status", 1)]
        assert actual == expected
        actual = ff.start_command_sorted
        expected = [("git", 3), ("lli", 2)]
        assert actual == expected
        mock_file.assert_called_with(fake_file_path, 'r')
        assert mock_file.call_count == 2

        top_full = ff.find_most_frequent()
        top_start = ff.find_most_frequent_start()
        assert top_full == "lli output"
        assert top_start == "git"


def test_top():
    file_content_mock = """lli output
lli output
git status
git stash
git stash"""
    fake_file_path = file
    with patch("builtins.open", mock_open(read_data=file_content_mock)) as mock_file:
        ff = FrequencyFile(file, False, "zsh")
        actual = ff.find_top_full(1)
        expected = [("lli output", 2)]
        assert actual == expected
        actual = ff.find_top_full(100)
        expected = [("lli output", 2), ("git stash", 2), ("git status", 1)]
        assert actual == expected
        actual = ff.find_top_start(1)
        expected = [("git", 3)]
        assert actual == expected
        actual = ff.find_top_start(100)
        expected = [("git", 3), ("lli", 2)]
        assert actual == expected


@patch('builtins.print')
@patch('terminal_tracker.frequency.FrequencyFile.find_top_start')
@patch('terminal_tracker.frequency.FrequencyFile.find_top_full')
def test_print_top(mock_full, mock_start, mock_print):
    mock_full.return_value = [("lli output", 1)]
    mock_start.return_value = [("lli", 1)]
    file_content_mock = """lli output"""
    fake_file_path = file
    with patch("builtins.open", mock_open(read_data=file_content_mock)) as mock_file:
        ff = FrequencyFile(file, False, "zsh")
        ff.print_top("full", 10)
        assert mock_print.call_args.args == ("Freq: 1 -> lli output",)
        ff.print_top("start", 10)
        assert mock_print.call_args.args == ("Freq: 1 -> lli",)
        ff.print_top("s", 1)
        assert mock_print.call_args.args == ("Type not supported",)


@patch('terminal_tracker.frequency.FrequencyFile.find_top_full')
def test_recommend_alias(mock_full):
    mock_full.return_value = [("dune exec -- bin/main.exe -l lib/test.mc > output", 3), ("lli output", 2)]
    file_content_mock = """dune exec -- bin/main.exe -l lib/test.mc > output
dune exec -- bin/main.exe -l lib/test.mc > output
dune exec -- bin/main.exe -l lib/test.mc > output
lli output
lli output"""
    fake_file_path = file
    with patch("builtins.open", mock_open(read_data=file_content_mock)) as mock_file:
        ff = FrequencyFile(file, False, "zsh")
        alias_expected = "dune exec -- bin/main.exe -l lib/test.mc > output"
        alias = ff.recommend_alias()
        assert alias == alias_expected


ff = FrequencyFile("terminal_tracker/tests/zsh_test.txt", False, "zsh")


def test_most_frequent():
    most_frequent_expected = "dune exec -- bin/main.exe -l lib/test.mc > output"
    most_frequent = ff.find_most_frequent()
    assert most_frequent == most_frequent_expected


def test_most_frequent_start():
    most_frequent_expected = "git"
    most_frequent = ff.find_most_frequent_start()
    assert most_frequent == most_frequent_expected


def test_top_full():
    top_expected = [("dune exec -- bin/main.exe -l lib/test.mc > output", 3), ("lli output", 2)]
    top = ff.find_top_full(2)
    assert top == top_expected


def test_start_full():
    top_expected = [("git", 5), ("dune", 3)]
    top = ff.find_top_start(2)
    assert top == top_expected


def test_recommend_alias():
    alias_expected = "dune exec -- bin/main.exe -l lib/test.mc > output"
    alias = ff.recommend_alias()
    assert alias == alias_expected
