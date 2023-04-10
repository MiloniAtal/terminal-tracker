from terminal_tracker import Tags
from unittest.mock import patch

file = "terminal_tracker/tests/zsh_test.txt"


@patch('terminal_tracker.preprocess.Preprocessing')
def test_convert(mock_prep):
    p = Tags(file, False, "zsh")
    mock_prep.assert_called_once()


file = "terminal_tracker/tests/zsh_test.txt"
timeframe = False
shell = "zsh"


def test_tags():
    t = Tags(file, timeframe, shell)
    result_expected = ['python trigram_model2.py #NLP']
    result = t.search("NLP")
    assert result == result_expected
