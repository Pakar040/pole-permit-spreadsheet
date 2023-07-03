import logging
from dataclasses import dataclass, field
from typing import List
import attachment as at
import pandas as pd
import os


# ----- Static Methods ----- #
# def identify_comment_attachment(comment, sequence_number):
#     comment = comment.lower()   # convert the comment to lowercase
#
#     # Get a list of all files in the directory
#     files = os.listdir('identify_attachments/attachments')
#
#     # Filter to only .txt files
#     txt_files = [f for f in files if f.endswith('.txt')]
#
#     for file in txt_files:
#         with open('identify_attachments/attachments/' + file, 'r') as f:
#             for line in f:
#                 items = line.split()  # split line into items
#
#                 # Convert all items to lowercase
#                 items = [item.lower() for item in items]
#
#                 # If item contains '!', it must not be in comment
#                 # If item does not contain '!', it must be in comment
#                 if all(item.replace('!', '') not in comment if '!' in item else item in comment for item in items):
#                     return file[:-4]   # return the file name without '.txt'
#
#     # If no matching file found, return None
#     logging.warning(f"Pole {sequence_number}: \"{comment}\" not recognized")
#     return comment


@dataclass
class Pole:
    row: pd.DataFrame

    def __post_init__(self):
        self.factory = at.AttachmentFactory()
        self.make_ready = None
        self.sequence_number = self.row['_title']
        self.attachment_list = self.extract_attachments()

    def set_to_proposed_attachments(self):
        """Call class like a method"""
        Pole.SetToProposedAttachments(self.attachment_list, self.row, self.sequence_number)

    class SetToProposedAttachments:
        def __init__(self, attachment_list: List[at.Attachment], row: pd.DataFrame, sequence_number: str) -> None:
            """Loops through each comment in column and replaces attachment list heights to match proposed pole"""

            # Set variables
            self.sequence_number = sequence_number
            self.attachment_list = attachment_list
            self.row = row
            self.factory = at.AttachmentFactory()

            # Handle each comment
            for comment in self.row['make_ready']:
                # Ex: comment = {'name': 'Move CATV to', 'value': '21' 06"'}
                if isinstance(comment, dict):
                    self.update_attachment_height(comment)
                elif comment == 'Dress Drip Loop':
                    self.dress_drip_loop()
                elif comment == 'Ground Streetlight':
                    self.ground_streetlight()
                elif comment == 'Mold Streetlight':
                    self.mold_streetlight()
                else:
                    logging.warning(f"Pole {self.sequence_number}: \"{comment}\" comment was not recognized")

        def update_attachment_height(self, comment):
            """Handles comments that move an attachment to a new height"""
            name = self.factory.identify_comment_attachment(comment['name'], self.sequence_number)
            proposed_height = comment['value']
            match_found = False
            for attachment in self.attachment_list:
                if attachment.name in name:
                    attachment.height = proposed_height
                    match_found = True
            if not match_found:
                logging.warning(f"Pole {self.sequence_number}: \"{comment['name']}\" attachment not on pole")

        def dress_drip_loop(self):
            """Updates drip loop height"""
            self.attachment_list.sort(reverse=True)
            drip_loop_obj = next((item for item in self.attachment_list if item.name == 'drip_loop'), None)
            for attachment in reversed(self.attachment_list):
                if attachment.name == 'secondary_spool.txt' or attachment.name == 'secondary_riser':
                    drip_loop_obj.height = at.feet_and_inches(attachment.get_height_in_inches() - 6)

        def ground_streetlight(self):
            """Updates streetlight to be grounded"""
            streetlight_obj = next((item for item in self.attachment_list if item.name == 'streetlight'), None)
            if streetlight_obj is not None:
                streetlight_obj.grounded = True

        def mold_streetlight(self):
            """Updates streetlight to be grounded molded"""
            streetlight_obj = next((item for item in self.attachment_list if item.name == 'streetlight'), None)
            if streetlight_obj is not None:
                streetlight_obj.molded = True

    def extract_attachments(self) -> List[at.Attachment]:
        """Combines attachments from columns and notes"""
        lst1 = self._extract_column_attachments()
        lst2 = self._extract_note_attachments()
        return lst1 + lst2

    def _extract_column_attachments(self) -> List[at.Attachment]:
        """Loops through each column and creates attachment list"""
        lst = []
        for column, value in self.row.items():
            attachment_obj = self.factory.create_attachment(column, value, self.row)
            if attachment_obj is not None and pd.notna(value):
                lst.append(attachment_obj)
        return lst

    def _extract_note_attachments(self) -> List[at.Attachment]:
        """Loops through each attachment in notes and creates attachment list"""
        lst = []
        for attachment in self.row['additional_measurements']:
            if isinstance(attachment, dict):
                name = attachment['name'].lower()
                height = attachment['value'].lower()
                attachment_obj = self.factory.create_attachment(name, height, self.row)
                if attachment_obj is not None:
                    lst.append(attachment_obj)
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

    def get_attachment(self, attachment_name: str) -> at.Attachment:
        """Finds the attachment instance using its name"""
        for attachment in self.attachment_list:
            if attachment.name == attachment_name:
                return attachment
        return "No attachment with this name was found"
