from . import preprocess
from . import tag
from . import timeanalysis


class Export:
    def __init__(self, file, timeframe, shell):
        self.prep = preprocess.Preprocessing(file, timeframe, shell)
        self.df = self.prep.df
        self.tag = tag.Tags(file, timeframe, shell)
        self.timeframe = timeframe
        if self.timeframe:
            self.time = timeanalysis.TimeAnalysis(file, shell)

    def sort_by(self, way):
        if way == "Start Command":
            self.df = self.df.sort_values(by='Main Command', ascending=True).reset_index(drop=True)
        elif way == "Full Command":
            self.df = self.df.sort_values(by='Command', ascending=True).reset_index(drop=True)
        elif way == "Frequency":
            freq = self.df['Command'].value_counts().reset_index()
            freq.columns = ['Command', 'Frequency']
            self.df = freq
        elif way == "Main Frequency":
            freq = self.df['Main Command'].value_counts().reset_index()
            freq.columns = ['Command', 'Frequency']
            self.df = freq
        elif way == "Collate Main":
            collated_df = self.df.groupby('Main Command')['Command'].apply(set).reset_index()
            self.df = collated_df
        else:
            raise ("Cannot sort in the requested manner")

    def pick(self, category, value):
        if category == "tag":
            self.df = self.tag.search_df(value)

        elif category == "time" and self.timeframe:
            self.df = self.time.search_day(value)

        else:
            raise ("Cannot pick in the requested manner")

    def csv(self, filename):
        self.df.to_csv(filename)

    def excel(self, filename):
        self.df.to_excel(filename)

    def html(self, filename):
        if ".html" not in filename:
            filename = filename + ".html"
        self.df.to_html(filename)
