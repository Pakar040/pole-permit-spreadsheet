from typing import List
import pandas as pd
from pole import Pole
import openpyxl
from abc import ABC, abstractmethod


class ExcelManager(ABC):
    """Extracts data from excel and formats it"""
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    def __repr__(self):
        return f"{self.df.to_string(index=False)}"

    @abstractmethod
    def read_excel(self) -> None:
        pass

    @abstractmethod
    def format(self) -> None:
        pass

    @abstractmethod
    def rename_header(self, attachment_name: str) -> str:
        pass


class PSEManager(ExcelManager):
    """Extracts data from excel and formats it to PSE template"""
    def __init__(self, file_path: str):
        super().__init__(file_path)

    def read_excel(self) -> None:
        """Takes data from excel file to create a dataframe"""
        self.df = pd.read_excel(self.file_path, skiprows=8).astype(str)

    def create_output(self) -> None:
        """Combines template dataframe with make manipulated dataframe"""
        self.df.to_excel('temp/temp.xlsx', sheet_name='Sheet1', index=False)

        # Load the source workbook
        source_wb = openpyxl.load_workbook('temp/temp.xlsx')
        source_sheet = source_wb.active

        # Load the destination workbook
        destination_wb = openpyxl.load_workbook('user_input/JB0001175447-1_Appendix A Field Survey.xlsx')
        destination_sheet = destination_wb.active

        # Copy cells from source to destination
        for row in source_sheet.iter_rows(min_row=2, min_col=2):
            for cell in row:
                destination_sheet.cell(row=cell.row + 8, column=cell.column, value=cell.value)

        # Save the destination workbook
        destination_wb.save('output/output.xlsx')

    def format(self) -> None:
        """Changes DataFrame into a standard DataFrame that is usable in other classes"""
        standard_df = pd.DataFrame()
        for column in self.df:
            standard_df[self.rename_header(column)] = self.df[column]
        self.df = standard_df

    def rename_header(self, attachment_name: str) -> str:
        """Renames attachments to match standard convention or template convention"""
        attachment_map = {
            'Seq #': '_title',
            'PSE Pole #': 'tag_number',
            'Pole Type T/D': 'pole_type',
            'Pole Owner': 'jursidiction',
            'Latitude': '_latitude',
            'Longitude': '_longitude',
            'Neutral ': 'neutral_height',
            'Secondary ': 'secondary_spool',
            'Drip Loop': 'drip_loop',
            'Primary Riser': 'primary_riser',
            'Secondary Riser': 'secondary_riser',
            'Street Light': 'streetlight',
            'CATV': 'catv',
            'TelCo': 'telco',
            'Fiber': 'fiber',
            'Make Ready Notes': 'make_ready',
            'PSE Field Notes': 'additional_measurements'
        }

        # Create a reversed mapping
        reversed_map = {v: k for k, v in attachment_map.items()}

        try:
            # Try to get the value from the original map
            return attachment_map[attachment_name]
        except KeyError:
            try:
                # If not found in the original map, try the reversed map
                return reversed_map[attachment_name]
            except KeyError:
                # If the key is not found in either map, return the original attachment name
                return attachment_name

    def parse_notes(self) -> None:
        """Splits the notes up into attachment dictionaries"""
        for index, row in self.df.iterrows():
            note = row['PSE Field Notes']
            notes = note.split('\n')
            parsed_note = []
            for piece in notes:
                part = piece.split(': ')
                try:
                    if part[0] != 'nan':
                        pair = {
                            'name': part[0],
                            'value': part[1],
                        }
                        parsed_note.append(pair)
                except IndexError:
                    parsed_note = part
            self.df.at[index, 'PSE Field Notes'] = parsed_note

    def reverse_parse_notes(self) -> None:
        """Combines attachment dictionaries into a single notes field"""
        if 'additional_measurements' not in self.df.columns:
            print("Error: 'additional_measurements' column not found in DataFrame.")
            return

        for index, row in self.df.iterrows():
            parsed_note = row['additional_measurements']
            if isinstance(parsed_note, list):
                if len(parsed_note) == 0:
                    self.df.at[index, 'additional_measurements'] = 'nan'
                else:
                    note = ""
                    for item in parsed_note:
                        if isinstance(item, dict):
                            name = item.get('name', '')
                            value = item.get('value', '')
                            note += f"{name}: {value}\n"
                        elif isinstance(item, str):
                            note += item + "\n"
                    self.df.at[index, 'additional_measurements'] = note.strip()

    def update_make_ready(self, lst: List[Pole]) -> None:
        for index, row in self.df.iterrows():
            self.df.at[index, 'make_ready'] += "\n" + lst[index].make_ready


class TemplateB(ExcelManager):
    def read_excel(self):
        pass

    def format(self):
        pass

    def rename_header(self, attachment_name: str):
        pass
