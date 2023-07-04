import logging
from dataclasses import dataclass
from typing import List
import attachment as at
import pandas as pd
import constants


@dataclass
class Pole:
    row: pd.DataFrame

    def __post_init__(self):
        self.factory = at.AttachmentFactory()
        self.make_ready = None
        self.sequence_number = self.row['_title']
        self.attachment_list = self.extract_attachments()

    def set_to_proposed_heights(self):
        """Call class like a method"""
        Pole.SetToProposedHeights(self.attachment_list, self.row, self.sequence_number)

    class SetToProposedHeights:
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
                    self.dress_drip_loop(comment)
                elif comment == 'Ground Streetlight':
                    self.ground_streetlight(comment)
                elif comment == 'Mold Streetlight':
                    self.mold_streetlight(comment)
                else:
                    logging.warning(f"Pole {self.sequence_number}: \"{comment}\" comment was not recognized")

        def update_attachment_height(self, comment):
            """Handles comments that move an attachment to a new height"""
            # Get proposed name and height
            proposed_attachment_name = self.factory.identify_comment_attachment(comment['name'], self.sequence_number)
            proposed_attachment_height = comment['value']
            is_attachment_existing = False
            # Finds attachment
            for existing_attachment in self.attachment_list:
                if existing_attachment.name in proposed_attachment_name:
                    # Sets attachment height to proposed height
                    existing_attachment.height = proposed_attachment_height
                    is_attachment_existing = True
            # If attachment cant be found log a warning
            if not is_attachment_existing:
                logging.warning(f"Pole {self.sequence_number}: \"{comment['name']}\" attachment not on pole")

        def dress_drip_loop(self, comment):
            """Updates drip loop height"""
            # Sorts attachments from highest to lowest
            self.attachment_list.sort(reverse=True)
            # Set reference variable to drip loop
            drip_loop_obj = next((item for item in self.attachment_list if item.name == 'drip_loop'), None)
            if drip_loop_obj is not None:
                # Finds which ever is lower 'spool' or 'riser;
                for attachment in reversed(self.attachment_list):
                    if attachment.name == 'secondary_spool' or attachment.name == 'secondary_riser':
                        # Set drip loop INCHES_OF_DRIP below power
                        inches_of_drip = constants.INCHES_OF_DRIP
                        drip_loop_obj.height = at.feet_and_inches(attachment.get_height_in_inches() - inches_of_drip)
            else:
                logging.warning(f"{self.sequence_number}: \"{comment}\" no drip loop found")

        def ground_streetlight(self, comment):
            """Updates streetlight to be grounded"""
            streetlight_obj = next((item for item in self.attachment_list if item.name == 'streetlight'), None)
            if streetlight_obj is not None:
                streetlight_obj.grounded = True
            else:
                logging.warning(f"{self.sequence_number}: \"{comment}\" no streetlight found")

        def mold_streetlight(self, comment):
            """Updates streetlight to be grounded molded"""
            streetlight_obj = next((item for item in self.attachment_list if item.name == 'streetlight'), None)
            if streetlight_obj is not None:
                streetlight_obj.molded = True
            else:
                logging.warning(f"{self.sequence_number}: \"{comment}\" no streetlight found")

    def extract_attachments(self) -> List[at.Attachment]:
        """Combines attachments from columns and notes"""
        return Pole.ExtractAttachments(self.row).extract_attachments()

    class ExtractAttachments:

        def __init__(self, row: pd.DataFrame):
            self.factory = at.AttachmentFactory()
            self.row = row

        def extract_attachments(self):
            """Combine column and not attachments"""
            lst1 = self.extract_column_attachments()
            lst2 = self.extract_note_attachments()
            return lst1 + lst2

        def extract_column_attachments(self) -> List[at.Attachment]:
            """Extract attachments out of columns"""
            lst = []
            for column, value in self.row.items():
                name = column
                height = value
                attachment_obj = self.factory.create_attachment(name, height, self.row)
                if self.is_valid_attachment(attachment_obj):
                    lst.append(attachment_obj)
            return lst

        def extract_note_attachments(self) -> List[at.Attachment]:
            """Loops through each attachment in notes and creates attachment list"""
            lst = []
            for attachment in self.row['additional_measurements']:
                if isinstance(attachment, dict):
                    name = attachment['name'].lower()
                    height = attachment['value']
                    attachment_obj = self.factory.create_attachment(name, height, self.row)
                    if self.is_valid_attachment(attachment_obj):
                        lst.append(attachment_obj)
            return lst

        @staticmethod
        def is_valid_attachment(attachment_obj):
            return attachment_obj is not None and pd.notna(attachment_obj.height)

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
        raise ValueError("No attachment with this name was found")
