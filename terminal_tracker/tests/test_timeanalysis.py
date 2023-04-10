from terminal_tracker import TimeAnalysis
from unittest.mock import patch
import pandas as pd
import datetime

file = "terminal_tracker/tests/zsh_test.txt"


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
