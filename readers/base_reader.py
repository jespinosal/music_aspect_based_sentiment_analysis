import os
from abc import ABC, abstractmethod
import pandas as pd


class DataFrameManager(ABC):

    def __init__(self, artist_name, file_lastname):
        self.file_lastname = file_lastname
        self.data_path = 'data'
        self.file_format = '.csv'
        self.dataframe_sep = ';'
        self.filename_sep = '-'
        self.filename = artist_name + self.filename_sep + self.file_lastname + self.file_format
        self.file_path = os.path.join(self.data_path, self.filename)

    def load_dataframe(self):
        return pd.read_csv(self.file_path, sep=self.dataframe_sep)

    def save_dataframe(self, dataframe):
        return dataframe.to_csv(self.file_path, sep=self.dataframe_sep, index=False)

    def check_dataframe_files(self):
        files = os.listdir(self.data_path)
        if self.filename in files:
            return True
        else:
            return False

    @abstractmethod
    def build_dataframe(self):
        raise NotImplementedError("Should have implemented this")

    def get_data_frame(self):
        if self.check_dataframe_files():
            print(f'Loading {self.filename} from {self.file_path}')
            dataframe = self.load_dataframe()
            print(f'Dataframe {self.filename} has been load')

        else:
            print(f'Generating Dataframe {self.filename}')
            dataframe = self.build_dataframe()
            self.save_dataframe(dataframe=dataframe)
            print(f'Dataframe has been saved on {self.file_path}')
        return dataframe
