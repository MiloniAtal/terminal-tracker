from terminal_tracker import Export
from unittest.mock import patch, mock_open
import pandas as pd
import datetime
import pytz
import pytest

file = "terminal_tracker/tests/zsh_test.txt"


def test_sort_by_main():
    file_content_mock = """lli output #PLT
dune exec -- bin/main.exe -l lib/test.mc > output"""
    with patch("builtins.open", mock_open(read_data=file_content_mock)):
        e = Export(file, False, "zsh")
        e.sort_by("Start Command")
        actual = e.df
        columns = ["Command", "Main Command", "Arguments", "Tags"]
        data = [
            [
                "dune exec -- bin/main.exe -l lib/test.mc > output",
                "dune",
                "exec -- bin/main.exe -l lib/test.mc > output",
                "",
            ],
            ["lli output #PLT", "lli", "output", "PLT"],
        ]
        expected = pd.DataFrame(data, columns=columns)
        assert expected.equals(actual)


def test_sort_by_full():
    file_content_mock = """git status
git stash"""
    with patch("builtins.open", mock_open(read_data=file_content_mock)):
        e = Export(file, False, "zsh")
        e.sort_by("Full Command")
        actual = e.df
        columns = ["Command", "Main Command", "Arguments", "Tags"]
        data = [["git stash", "git", "stash", ""], ["git status", "git", "status", ""]]
        expected = pd.DataFrame(data, columns=columns)
        assert expected.equals(actual)


def test_sort_full_frequency():
    file_content_mock = """git status
git stash
git status"""
    with patch("builtins.open", mock_open(read_data=file_content_mock)):
        e = Export(file, False, "zsh")
        e.sort_by("Full Frequency")
        actual = e.df
        columns = ["Command", "Frequency"]
        data = [["git status", 2], ["git stash", 1]]
        expected = pd.DataFrame(data, columns=columns)
        assert expected.equals(actual)


def test_sort_start_frequency():
    file_content_mock = """lli output
git status
git stash"""
    with patch("builtins.open", mock_open(read_data=file_content_mock)):
        e = Export(file, False, "zsh")
        e.sort_by("Start Frequency")
        actual = e.df
        columns = ["Command", "Frequency"]
        data = [["git", 2], ["lli", 1]]
        expected = pd.DataFrame(data, columns=columns)
        assert expected.equals(actual)


def test_sort_collate_main():
    file_content_mock = """lli output
git status
git stash"""
    with patch("builtins.open", mock_open(read_data=file_content_mock)):
        e = Export(file, False, "zsh")
        e.sort_by("Collate Main")
        actual = e.df
        columns = ["Main Command", "Command"]
        data = [["git", {"git status", "git stash"}], ["lli", {"lli output"}]]
        expected = pd.DataFrame(data, columns=columns)
        assert expected.equals(actual)


def test_sort_exception():
    file_content_mock = """lli output
git status
git stash"""
    with patch("builtins.open", mock_open(read_data=file_content_mock)):
        e = Export(file, False, "zsh")
        incorrect_way = "abc"
        exception_info = "The " + incorrect_way + " value is not implemented"
        with pytest.raises(ValueError) as exception_info:
            e.sort_by(incorrect_way)


@patch('terminal_tracker.tag.Tags.search_df')
def test_pick_tag(mock_tag_search):
    file_content_mock = """lli output
git status
git stash"""
    with patch("builtins.open", mock_open(read_data=file_content_mock)):
        e = Export(file, False, "zsh")
        value = "abc"
        e.pick("tag", value)
        assert mock_tag_search.call_count == 1
        mock_tag_search.assert_called_with(value)


@patch('terminal_tracker.timeanalysis.TimeAnalysis.search_day')
def test_pick_time_exception(mock_tag_search):
    file_content_mock = """lli output
git status
git stash"""
    with patch("builtins.open", mock_open(read_data=file_content_mock)):
        e = Export(file, False, "zsh")
        value = "2022-02-18"
        exception_info = "The file doesnot contain time information"
        with pytest.raises(Exception) as exception_info:
            e.pick("time", value)


@patch('terminal_tracker.timeanalysis.TimeAnalysis.search_day')
def test_pick_time(mock_time_search):
    file_content_mock = """: 1676578148:0;lli output"""
    with patch("builtins.open", mock_open(read_data=file_content_mock)):
        e = Export(file, True, "zsh")
        value = "2022-02-18"
        e.pick("time", value)
        assert mock_time_search.call_count == 1
        mock_time_search.assert_called_with(value)


def test_pick_exception():
    file_content_mock = """: 1676578148:0;lli output"""
    with patch("builtins.open", mock_open(read_data=file_content_mock)):
        e = Export(file, True, "zsh")
        incorrect_category = "abc"
        random_value = "r"
        exception_info = "The " + incorrect_category + " value is not implemented"
        with pytest.raises(ValueError) as exception_info:
            e.pick(incorrect_category, random_value)
