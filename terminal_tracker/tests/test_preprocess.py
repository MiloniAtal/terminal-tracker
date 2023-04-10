from terminal_tracker import Preprocessing
from unittest.mock import patch, mock_open
import pandas as pd
import datetime
import pytz

file = "terminal_tracker/tests/zsh_test.txt"


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
    with patch("builtins.open", mock_open(read_data=file_content_mock)) as mock_file:
        prep = Preprocessing(file, False, "bash")
        actual = prep._convert_timeframe_bash()
        expected = [
            ["ls", "No", "No", "ls", "", ""],
            ["history -u #HIST", "No", "No", "history", "-u", "HIST"],
            ["ls", "1676578148", datetime.datetime(2023, 2, 16, 20, 9, 8, tzinfo=pytz.utc), "ls", "", ""],
        ]
        assert actual == expected
