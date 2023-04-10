from terminal_tracker import SearchFile
from unittest.mock import patch, mock_open
import pytest

file = "terminal_tracker/tests/zsh_test.txt"


def test_searchfile_find():
    file_content_mock = """lli output
lli output
git status
git stash
git stash"""
    with patch("builtins.open", mock_open(read_data=file_content_mock)):
        sf = SearchFile(file)
        actual = sf.find("status")
        expected = ["git status"]
        assert actual == expected


def test_searchfile_latest():
    file_content_mock = """lli output
lli output
git status
git stash
git stash"""
    with patch("builtins.open", mock_open(read_data=file_content_mock)):
        sf = SearchFile(file)
        actual = sf.latest("git")
        expected = "git stash"
        assert actual == expected
        actual = sf.latest("lli")
        expected = "lli output"
        assert actual == expected


def test_searchfile_latest_iterator():
    file_content_mock = """lli output
git status
lli output
git stash"""
    with patch("builtins.open", mock_open(read_data=file_content_mock)):
        sf = SearchFile(file)
        iterator = sf.latest_iterator("git")
        actual = next(iterator)
        expected = "git stash"
        assert actual == expected
        actual = next(iterator)
        expected = "git status"
        assert actual == expected
        with pytest.raises(StopIteration):
            next(iterator)


@patch('builtins.print')
@patch('terminal_tracker.searching.SearchFile.latest_iterator')
def test_print_top(mock_iterator, mock_print):
    mock_iterator.return_value = ["lli output"]
    file_content_mock = """lli output"""
    with patch("builtins.open", mock_open(read_data=file_content_mock)):
        sf = SearchFile(file)
        sf.using_latest_iterator("lli")
        assert mock_print.call_args.args == ("lli output",)
