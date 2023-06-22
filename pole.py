from dataclasses import dataclass, field
from typing import List
import attachment as at
import pandas as pd


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
        self.make_ready = None
        self.row = dataframe_row
        self.sequence_number = self.row['_title']
        self.attachment_list = self.extract_attachments()

    def extract_attachments(self) -> List[at.Attachment]:
        """Combines attachments from columns and notes"""
        lst1 = self.extract_column_attachments()
        lst2 = self.extract_note_attachments()
        return lst1 + lst2

    def extract_column_attachments(self) -> List[at.Attachment]:
        """Loops through each column and creates attachment list"""
        lst = []
        for column, value in self.row.items():
            if at.create_attachment(column, value) is not None and pd.notna(value):
                lst.append(at.create_attachment(column, value))
        return lst

    def extract_note_attachments(self) -> List[at.Attachment]:
        """Loops through each attachment in notes and creates attachment list"""
        lst = []
        for attachment in self.row['additional_measurements']:
            if type(attachment) == dict:
                attach_obj = at.create_attachment(attachment['name'].lower(), attachment['value'].lower())
                if attach_obj is not None:
                    lst.append(attach_obj)
        return lst

    def find_violations(self) -> str:
        """Finds all the violations"""
        # Store violations in a string
        violations = ""
        # Sort by highest to the lowest attachment heights
        self.attachment_list.sort(reverse=True)
        # Compare to only attachments lower on the pole
        for i, attachment1 in enumerate(self.attachment_list):
            for attachment2 in self.attachment_list[i + 1:]:
                if attachment1.check_for_violation(attachment2) is not None:
                    violations += attachment1.check_for_violation(attachment2) + "\n"
        return violations.rstrip()

    def add_violations(self):
        """Updates make ready data in dataframe"""
        self.row['make_ready']

    def get_attachment(self, attachment_name: str) -> at.Attachment:
        """Finds the attachment instance using its name"""
        for attachment in self.attachment_list:
            if attachment.name == attachment_name:
                return attachment
        return "No attachment with this name was found"
