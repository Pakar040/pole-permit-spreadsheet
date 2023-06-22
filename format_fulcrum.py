from typing import List
import pandas as pd
from excel_manager import ExcelManager


class CableComAppManager:
    """Handles directly downloaded data from fulcrum CableComApp"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
        self.attachment_df = None
        self.excel_manager: ExcelManager() = None

    def __repr__(self):
        return f"{self.df.to_string(index=False)}"

    def set_excel_manager(self, manager: ExcelManager) -> None:
        self.excel_manager = manager

    def read_excel(self) -> None:
        """Takes data from excel file to create a DataFrame and attachment only DataFrame"""
        self.df = pd.read_excel(self.file_path, skiprows=0).astype(str)
        self.attachment_df = self.df.iloc[:, 48:83].apply(pd.to_numeric, errors='coerce').astype('Int64')

    def format_to_template(self):
        """Formats DataFrame to fit in template"""
        self._add_missing_columns(self.excel_manager.standard_headers)
        self.df = self.df.loc[:, self.excel_manager.standard_headers]
        self._add_additional_attachments()
        formatted_df = pd.DataFrame()
        for column in self.df:
            formatted_df[self.excel_manager.rename_header(column)] = self.df[column]
        self.df = formatted_df

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

