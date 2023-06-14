import pandas as pd
from abc import ABC, abstractmethod
import openpyxl


class ExcelManager(ABC):
    """Extracts data from excel and formats it"""
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
        self.dict = None
        self.column_headers = None

    def __repr__(self):
        return f"{self.df}"

    def read_excel(self):
        self.df = pd.read_excel(self.file_path)
        self.dict = self.df.to_dict()
        self.column_headers = self.df.columns

    def write_excel(self, data, sheet_name='Sheet1'):
        data.to_excel(self.file_path, sheet_name=sheet_name, index=False)

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
        self.df = pd.read_excel(self.file_path, skiprows=8)
        self.dict = self.df.to_dict()
        self.column_headers = self.df.columns

    def format_to_standard(self):
        """Changes dict into a standard dict that is usable in other classes"""
        standard_dict = {}
        for header in self.df:
            standard_dict[self.rename_header_to_standard(header)] = self.df[header].tolist()
        self.dict = standard_dict

    def rename_header_to_standard(self, attachment_name: str):
        """Renames attachments to match standard convention"""
        attachment_map = {
            'Seq #': '_title',
            'PSE Pole #': 'pse_tag_number',
            'Pole Type T/D': 'pse_pole_type',
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


class TemplateB(ExcelManager):
    def process_data(self):
        # Implement the specific processing for Template B
        pass

    def rename_header_to_standard(self):
        pass
