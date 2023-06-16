from dataclasses import dataclass, field
from typing import List
import attachment as at


@dataclass
class Pole:
    sequence_number: str
    tag_number: str
    type: str
    owner: str
    latitude: str
    longitude: str
    attachment_list: List[at.Attachment] = field(default_factory=list)

    def __init__(self, dataframe_row):
        self.row = dataframe_row
        self.sequence_number = self.row['_title']
        self.tag_number = self.row['tag_number']
        self.type = self.row['pole_type']
        self.owner = self.row['jursidiction']
        self.latitude = self.row['_latitude']
        self.longitude = self.row['_longitude']
        self.attachment_list = self.get_attachments()

    def get_attachments(self) -> List[at.Attachment]:
        """Combines attachments from columns and notes"""
        lst1 = self.get_column_attachments()
        lst2 = self.get_note_attachments()
        return lst1 + lst2

    def get_column_attachments(self) -> List[at.Attachment]:
        """Loops through each column and creates attachment list"""
        lst = []
        for column, value in self.row.items():
            if at.create_attachment(column, value) is not None and value != 'nan':
                lst.append(at.create_attachment(column, value))
        return lst

    def get_note_attachments(self) -> List[at.Attachment]:
        """Loops through each attachment in notes and creates attachment list"""
        lst = []
        for attachment in self.row['additional_measurements']:
            if type(attachment) == dict:
                attach_obj = at.create_attachment(attachment['name'].lower(), attachment['value'].lower())
                if attach_obj is not None:
                    lst.append(attach_obj)
        return lst