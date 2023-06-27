from typing import List
import numpy as np
import pandas as pd
from excel_manager import ExcelManager
from pole import Pole


# ----- Static Methods ----- #
def convert_unconvertible_to_na(val):
    """This is used to convert a DataFrame to only contain int values"""
    try:
        val = int(val)
    except ValueError:
        return np.nan
    return val


class CableComAppManager:
    """Handles directly downloaded data from fulcrum CableComApp"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
        self.attachment_df = None
        self.make_ready_df = None
        self.excel_manager: ExcelManager() = None

    def __repr__(self):
        return f"{self.df.to_string(index=False)}"

    def set_excel_manager(self, manager: ExcelManager) -> None:
        self.excel_manager = manager

    def update_make_ready(self, lst: List[Pole]) -> None:
        """Receives a list of poles and adds the make ready data to DataFrame"""
        self.df['make_ready'] = np.nan
        for index, row in self.df.iterrows():
            if pd.isna(self.df.at[index, 'make_ready']):
                self.df.at[index, 'make_ready'] = lst[index].make_ready
            else:
                self.df.at[index, 'make_ready'] += "\n" + lst[index].make_ready

    def read_excel(self) -> None:
        """Takes data from excel file to create a regular DataFrame and make_ready only DataFrame"""
        dataframe = pd.read_excel(self.file_path, skiprows=0)  # .astype(str)
        self.df = dataframe.astype(str)
        self.attachment_df = dataframe.iloc[:, 48:83].apply(pd.to_numeric, errors='coerce').astype('Int64')
        self.make_ready_df = dataframe.applymap(convert_unconvertible_to_na).astype('Int64')
        self.df[self.df.columns[48:83]] = self.df[self.df.columns[48:83]].apply(pd.to_numeric,
                                                                                errors='coerce').astype('Int64')

        self.make_ready_df = self.make_ready_df.rename(columns={'streetlight_grounded': 'grounded',
                                                                'streetlight_molded': 'molded'})
        self.make_ready_df['grounded'] = dataframe['streetlight_grounded'].astype('object')
        self.make_ready_df['molded'] = dataframe['streetlight_molded'].astype('object')
        self.make_ready_df['additional_measurements'] = dataframe['additional_measurements'].astype(str)
        self.make_ready_df['_title'] = dataframe['_title'].astype(str)

    def format_to_template(self):
        """Formats DataFrame to fit in template"""
        self._add_missing_columns(self.excel_manager.standard_headers)
        self.df = self.df.loc[:, self.excel_manager.standard_headers]
        self._add_additional_attachments()
        formatted_df = pd.DataFrame()
        for column in self.df:
            formatted_df[self.excel_manager.rename_header(column)] = self.df[column]
        self.df = formatted_df

        # Add grounded and molded to the end
        self.df['grounded'] = self.make_ready_df['grounded']
        self.df['molded'] = self.make_ready_df['molded']

    def _add_missing_columns(self, column_headers: List[str]):
        """Adds columns to DataFrame that are in template"""
        for col in column_headers:
            if col not in self.df.columns:
                self.df[col] = None
        return self.df

    def _add_additional_attachments(self):
        """Takes any attachments that don't have a column and put it in additional notes"""
        # Remove columns with the specified header names
        self.attachment_df = self.attachment_df.drop(columns=self.excel_manager.standard_headers, errors='ignore')
        # Loop through rows
        for i in self.attachment_df.index:
            # Loop through columns
            for j in self.attachment_df.columns:
                # Check if value is not NaN
                if pd.notna(self.attachment_df.at[i, j]):
                    # Create the string
                    note = f"{j}: {self.attachment_df.at[i, j]}"
                    # Check if 'additional_notes' is NaN
                    if self.df.at[i, 'additional_measurements'] == 'nan':
                        # If it is, set the value as the new string
                        self.df.at[i, 'additional_measurements'] = note
                    else:
                        # If it's not, append the new string
                        self.df.at[i, 'additional_measurements'] += '\n' + note
