import pandas as pd
from . import preprocess


class Export:
    def __init__(self, file, timeframe, shell):
        self.prep = preprocess.Preprocessing(file, timeframe, shell)
        self.df = self.prep.df

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

    def csv(self, filename):
        self.df.to_csv(filename)

    def excel(self, filename):
        self.df.to_excel(filename)

    def html(self, filename):
        if ".html" not in filename:
            filename = filename + ".html"
        self.df.to_html(filename)
