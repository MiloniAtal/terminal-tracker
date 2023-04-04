from . import preprocess


class TimeAnalysis:
    """This class helps to search commands with certain tags

    Attributes:
        prep (Preprocessing): Preprocessing the file using the Preprocessing class
        df (pandas.DataFrame):
            Preprocessed dataframe
            Columns:
                Command(str), Main Command (str), Arguments (str), Tags (str),
                Time (str), Pretty Time (datetime.datetime)

    Todo:
        * reject files with no timeframe
    """

    def __init__(self, file, shell):
        self.prep = preprocess.Preprocessing(file, True, shell)
        self._df_raw = self.prep.df
        self.df = self._remove_no_time_rows()

    def _remove_no_time_rows(self):
        return self._df_raw[self._df_raw["Pretty Time"] != "No"].reset_index(drop=True)

    def search_day(self, day):
        """Finds commands that were executed on the given day

        Args:
            day (str): Day in 2023-02-18 format

        Returns:
            pandas.DataFrame: Dataframe containing rows that were executed on the day

        """
        return self.df[self.df['Pretty Time'].astype(str).str.contains(day)].reset_index(drop=True)
