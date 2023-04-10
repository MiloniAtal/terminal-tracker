from . import preprocess
from . import tag
from . import timeanalysis


class Export:
    """
    This class helps in exporting the history file in a better usable format

    Attributes:
        timeframe (bool): whether time values are present in the history file
        shell (str): "zsh" or "bash"
        df (pandas.DataFrame):
            Columns:
                Command(str), Main Command (str), Arguments (str), Tags (str)
            Optional Columns:
                Time (str), Pretty Time (datetime.datetime)
        tag (Tags): processed for efficient searching of tags
        time (TimeAnalysis): processed for efficient searching of day
    """

    def __init__(self, file, timeframe, shell):
        self.prep = preprocess.Preprocessing(file, timeframe, shell)
        self.df = self.prep.df
        self.tag = tag.Tags(file, timeframe, shell)
        self.timeframe = timeframe
        if self.timeframe:
            self.time = timeanalysis.TimeAnalysis(file, shell)

    def sort_by(self, way):
        """
        Sorts the commands in the dataframe using various methods and stores
        the sorted commands in the same "df" attribute.
        This method should be used before exporting the dataframe.

        Args:
            way (str): The method to use for sorting. Must be one of the following:,
                        "Start Command": Sort by the start command of each command.
                        "Full Command": Sort by the full command.
                        "Start Frequency": Keep only unique full commands with their frequency.
                        "Full Frequency": Keep only unique start commands with their frequency.
                        "Collate Main": Group the commands by their start command.

        Raises:
            ValueError: If way is not one of "Start Command", "Full Command",
                        "Start Frequency", "Full Frequency", or "Collate Main".

        """
        if way == "Start Command":
            self.df = self.df.sort_values(by='Main Command', ascending=True).reset_index(drop=True)
        elif way == "Full Command":
            self.df = self.df.sort_values(by='Command', ascending=True).reset_index(drop=True)
        elif way == "Full Frequency":
            freq = self.df['Command'].value_counts().reset_index()
            freq.columns = ['Command', 'Frequency']
            self.df = freq
        elif way == "Start Frequency":
            freq = self.df['Main Command'].value_counts().reset_index()
            freq.columns = ['Command', 'Frequency']
            self.df = freq
        elif way == "Collate Main":
            collated_df = self.df.groupby('Main Command')['Command'].apply(set).reset_index()
            self.df = collated_df.sort_values(by='Main Command', ascending=True).reset_index(drop=True)
        else:
            raise ValueError("The " + way + " value is not implemented")

    def pick(self, category, value):
        """
        Sorts the commands in the dataframe by a specified category and value,
        and stores the sorted dataframe in the same "df" attribute.
        This method should be used before exporting the dataframe.

        Args:
            category (str): The category to sort by. Must be one of "tag" or "time".
            value (str): The value to filter by. If category is "tag",
                        this should be a tag name. If category is "time",
                        this should be a date string in the format "YYYY-MM-DD".

        Raises:
            ValueError: If category is not one of "tag" or "time".
            Exception: If category is "time", but the file doesnot have time
                        values
        """
        if category == "tag":
            self.df = self.tag.search_df(value)

        elif category == "time":
            if self.timeframe:
                self.df = self.time.search_day(value)
            else:
                raise Exception("The file doesnot contain time information")

        else:
            raise ValueError("The " + category + " value is not implemented")

    def csv(self, filename):
        """
        Converts dataframe to csv file of given name
        """
        self.df.to_csv(filename)

    def excel(self, filename):
        """
        Converts dataframe to excel file of given name
        """
        self.df.to_excel(filename)

    def html(self, filename):
        """
        Converts dataframe to html file of given name, adds the extension
        ".html" if not present in the filename
        """
        if ".html" not in filename:
            filename = filename + ".html"
        self.df.to_html(filename)
