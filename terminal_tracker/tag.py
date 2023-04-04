from . import preprocess


class Tags:
    """This class helps to search commands with certain tags

    Attributes:
        prep (Preprocessing): Preprocessing the file using the Preprocessing class
        df (pandas.DataFrame):
            Preprocessed dataframe
            Columns:
                Command(str), Main Command (str), Arguments (str), Tags (str)
            Optional Columns:
                Time (str), Pretty Time (datetime.datetime)
    """

    def __init__(self, file, timeframe, shell):
        self.prep = preprocess.Preprocessing(file, timeframe, shell)
        self.df = self.prep.df

    def search_df(self, a):
        """
        Searches for commands with tag "a" in history file and get the entire information

        Args:
            a (str): Tag

        Returns:
            pandas.Dataframe: Dataframe with only rows with commands containing the tag
        """
        return self.df[self.df["Tags"].str.contains(a, case=False, na=False)]

    def search(self, a):
        """
        Searches for commands with tag "a" in history file and get only the commands

        Args:
            a (str): Tag

        Returns:
            list: Commands containing the tag "a"
        """
        df = self.search_df(a)
        return df["Command"].values.tolist()
