import pandas as pd
from abc import ABC, abstractmethod


class ExcelManager(ABC):
    """Extracts data from excel and formats it"""
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    def __repr__(self):
        return f"{self.df.to_string(index=False)}"

    @abstractmethod
    def read_excel(self):
        pass

    @abstractmethod
    def format_to_standard(self):
        pass

    @abstractmethod
    def rename_header_to_standard(self, attachment_name: str):
        pass


class PSEManager(ExcelManager):
    """Extracts data from excel and formats it to PSE template"""
    def __init__(self, file_path: str):
        super().__init__(file_path)

    def read_excel(self):
        self.df = pd.read_excel(self.file_path, skiprows=8).astype(str)

    def format_to_standard(self):
        """Changes DataFrame into a standard DataFrame that is usable in other classes"""
        standard_df = pd.DataFrame()
        for column in self.df:
            standard_df[self.rename_header_to_standard(column)] = self.df[column]
        self.df = standard_df

    def rename_header_to_standard(self, attachment_name: str) -> str:
        """Renames attachments to match standard convention"""
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
            'PSE Field Notes': 'additional_measurements'
        }

        try:
            return attachment_map[attachment_name]
        except KeyError:
            return attachment_name

    def parse_notes(self):
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


class TemplateB(ExcelManager):
    def read_excel(self):
        pass

    def format_to_standard(self):
        pass

    def rename_header_to_standard(self, attachment_name: str):
        pass
