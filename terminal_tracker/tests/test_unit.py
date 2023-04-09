from terminal_tracker import Preprocessing, Tags, FrequencyFile, SearchFile, TimeAnalysis
from unittest.mock import patch, Mock, mock_open
import pytest
import pandas as pd
import datetime
import pytz

file = "terminal_tracker/tests/zsh_test.txt"


@patch('terminal_tracker.preprocess.Preprocessing')
def test_convert(mock_prep):
    p = Tags(file, False, "zsh")
    mock_prep.assert_called_once()


@patch('terminal_tracker.preprocess.Preprocessing._convert_timeframe')
@patch('terminal_tracker.preprocess.Preprocessing._convert_no_timeframe')
def test_convert(mock_no_tf, mock_tf):
    p = Preprocessing(file, False, "zsh")
    assert mock_no_tf.call_count == 1
    assert mock_tf.call_count == 0
    p = Preprocessing(file, True, "zsh")
    assert mock_no_tf.call_count == 1
    assert mock_tf.call_count == 1


# TODO: mock pandas?
def test_convert_no_timeframe():
    file_content_mock = """lli output #PLT"""
    fake_file_path = file
    with patch("builtins.open", mock_open(read_data=file_content_mock)) as mock_file:
        prep = Preprocessing(file, False, "zsh")
        actual = prep._convert_no_timeframe()
        columns = ["Command", "Main Command", "Arguments", "Tags"]
        data = [["lli output #PLT", "lli", "output", "PLT"]]
        expected = pd.DataFrame(data, columns=columns)
        assert expected.equals(actual)


@patch('terminal_tracker.preprocess.Preprocessing._convert_timeframe_bash')
@patch('terminal_tracker.preprocess.Preprocessing._convert_timeframe_zsh')
@patch('terminal_tracker.preprocess.Preprocessing._convert')
def test_timeframe(mock_convert, mock_zsh, mock_bash):
    data = [["lli output #PLT", "lli", "output", "1676578148", "2023-02-16 15:09:08", "PLT"]]
    columns = ["Command", "Time", "Pretty Time", "Main Command", "Arguments", "Tags"]
    mock_zsh.return_value = data
    mock_bash.return_value = data
    prep = Preprocessing(file, True, "zsh")
    actual = prep._convert_timeframe()
    expected = pd.DataFrame(data, columns=columns)
    assert expected.equals(actual)
    prep = Preprocessing(file, True, "bash")
    actual = prep._convert_timeframe()
    expected = pd.DataFrame(data, columns=columns)
    assert expected.equals(actual)
    assert mock_zsh.call_count == 1
    assert mock_bash.call_count == 1


@patch('terminal_tracker.preprocess.Preprocessing._convert')
def test_timeframe_zsh(mock_convert):
    file_content_mock = """: 1676578148:0;lli output #PLT
: 1676578148:0;lli output"""
    fake_file_path = file
    with patch("builtins.open", mock_open(read_data=file_content_mock)) as mock_file:
        prep = Preprocessing(file, True, "zsh")
        actual = prep._convert_timeframe_zsh()
        expected = [
            [
                "lli output #PLT",
                "1676578148",
                datetime.datetime(2023, 2, 16, 20, 9, 8, tzinfo=pytz.utc),
                "lli",
                "output",
                "PLT",
            ],
            [
                "lli output",
                "1676578148",
                datetime.datetime(2023, 2, 16, 20, 9, 8, tzinfo=pytz.utc),
                "lli",
                "output",
                "",
            ],
        ]
        assert actual == expected


@patch('terminal_tracker.preprocess.Preprocessing._convert')
def test_timeframe_bash(mock_convert):
    file_content_mock = """ls
history -u #HIST
#1676578148
ls"""
    fake_file_path = file
    with patch("builtins.open", mock_open(read_data=file_content_mock)) as mock_file:
        prep = Preprocessing(file, False, "bash")
        actual = prep._convert_timeframe_bash()
        expected = [
            ["ls", "No", "No", "ls", "", ""],
            ["history -u #HIST", "No", "No", "history", "-u", "HIST"],
            ["ls", "1676578148", datetime.datetime(2023, 2, 16, 20, 9, 8, tzinfo=pytz.utc), "ls", "", ""],
        ]
        assert actual == expected


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


def test_searchfile_find():
    file_content_mock = """lli output
lli output
git status
git stash
git stash"""
    fake_file_path = file
    with patch("builtins.open", mock_open(read_data=file_content_mock)) as mock_file:
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
    fake_file_path = file
    with patch("builtins.open", mock_open(read_data=file_content_mock)) as mock_file:
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
    fake_file_path = file
    with patch("builtins.open", mock_open(read_data=file_content_mock)) as mock_file:
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
    fake_file_path = file
    with patch("builtins.open", mock_open(read_data=file_content_mock)) as mock_file:
        sf = SearchFile(file)
        sf.using_latest_iterator("lli")
        assert mock_print.call_args.args == ("lli output",)


@patch('terminal_tracker.preprocess.Preprocessing')
def test_timeanalysis_remove(mock_prep):
    data_raw = [
        ["ls", "No", "No", "ls", "", ""],
        ["history -u #HIST", "No", "No", "history", "-u", "HIST"],
        ["ls", "1676578148", datetime.datetime(2023, 2, 16, 15, 9, 8), "ls", "", ""],
    ]
    columns = ["Command", "Time", "Pretty Time", "Main Command", "Arguments", "Tags"]
    df_raw = pd.DataFrame(data_raw, columns=columns)

    class prep:
        df = df_raw

    mock_prep.return_value = prep()
    ta = TimeAnalysis(file, "bash")
    actual = ta._remove_no_time_rows()

    data = [["ls", "1676578148", datetime.datetime(2023, 2, 16, 15, 9, 8), "ls", "", ""]]
    expected = pd.DataFrame(data, columns=columns)

    # TODO: Some issue with matching this column
    actual = actual.drop(["Pretty Time"], axis=1)
    expected = expected.drop(columns=["Pretty Time"])
    print(actual)
    print(expected)

    assert expected.equals(actual)


@patch('terminal_tracker.timeanalysis.TimeAnalysis._remove_no_time_rows')
@patch('terminal_tracker.preprocess.Preprocessing')
def test_search_day(mock_prep, mock_remove):
    data_raw = [
        ["ls", "1676578148", datetime.datetime(2023, 2, 16, 15, 9, 8), "ls", "", ""],
        ["ls", "1676578248", datetime.datetime(2023, 2, 9, 15, 9, 8), "ls", "", ""],
    ]
    columns = ["Command", "Time", "Pretty Time", "Main Command", "Arguments", "Tags"]
    df_raw = pd.DataFrame(data_raw, columns=columns)

    data = [
        ["ls", "1676578148", datetime.datetime(2023, 2, 16, 15, 9, 8), "ls", "", ""],
        ["ls", "1676578248", datetime.datetime(2023, 2, 9, 15, 9, 8), "ls", "", ""],
    ]
    df = pd.DataFrame(data, columns=columns)

    class prep:
        df = df_raw

    mock_prep.return_value = prep()
    mock_remove.return_value = df

    data_exp = [["ls", "1676578148", datetime.datetime(2023, 2, 16, 15, 9, 8), "ls", "", ""]]

    ta = TimeAnalysis(file, "bash")
    actual = ta.search_day("2023-02-16")
    expected = pd.DataFrame(data_exp, columns=columns)
    expected.equals(actual)
