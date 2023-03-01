from terminal_tracker import Preprocessing, Tags

file = "terminal_tracker/tests/zsh_test.txt"
timeframe = False
shell = "zsh"

def test_tags():
    t = Tags(file, timeframe, shell)
    result_expected = ['python trigram_model2.py #NLP']
    result = t.search("NLP")
    assert (result == result_expected)
