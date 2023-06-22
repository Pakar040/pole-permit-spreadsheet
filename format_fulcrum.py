from typing import List
import pandas as pd
import excel_manager as em


class CableComAppManager:
    """Handles directly downloaded data from fulcrum CableComApp"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
        self.extra_attachment_df = None
        self.excel_manager: em.ExcelManager() = None

    def __repr__(self):
        return f"{self.df.to_string(index=False)}"

    def read_excel(self):
        """Takes data from excel file to create a dataframe"""
        self.df = pd.read_excel(self.file_path, skiprows=0).astype(str)
        self.extra_attachment_df = self.df.iloc[:, 48:83].apply(pd.to_numeric, errors='coerce').astype('Int64')

    def select_jurisdiction(self, jurisdiction):
        """Creates a manager instance of chosen jurisdiction"""
        if jurisdiction == 'PSE':
            self.excel_manager = em.PSEManager()

    def format(self):
        """Formats data frame to fit in template"""
        standard_headers = [self.excel_manager.rename_header(header) for header in self.excel_manager.template_headers]
        self.remove_columns_with_header(standard_headers)  # <-- for attachment.df
        self.add_missing_columns(standard_headers)
        self.df = self.df.loc[:, standard_headers]
        self.add_additional_attachments()

    def add_missing_columns(self, column_headers: List[str]):
        """Adds columns to data frame that are in template"""
        for col in column_headers:
            if col not in self.df.columns:
                self.df[col] = None
        return self.df

    def transfer_to_spreadsheet(self):
        self.format()
        self.excel_manager.df = self.df
        self.excel_manager.format()
        self.excel_manager.format_measurements()

    def create_output(self):
        self.excel_manager.create_output()

    def remove_columns_with_header(self, header_names: List[str]) -> None:
        """Reduces data frame to only contain attachments that don't have a column in template"""
        # Remove columns with the specified header names
        self.extra_attachment_df = self.extra_attachment_df.drop(columns=header_names, errors='ignore')

    def add_additional_attachments(self):
        """Takes any attachments that don't have a column and put it in additional notes"""
        # Loop through rows
        for i in self.extra_attachment_df.index:
            # Loop through columns
            for j in self.extra_attachment_df.columns:
                # Check if value is not NaN
                if pd.notna(self.extra_attachment_df.at[i, j]):
                    # Create the string
                    note = f"{j}: {self.extra_attachment_df.at[i, j]}"
                    # Check if 'additional_notes' is NaN
                    if self.df.at[i, 'additional_measurements'] == 'nan':
                        # If it is, set the value as the new string
                        self.df.at[i, 'additional_measurements'] = note
                    else:
                        # If it's not, append the new string
                        self.df.at[i, 'additional_measurements'] += '\n' + note

