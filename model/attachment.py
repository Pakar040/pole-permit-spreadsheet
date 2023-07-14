import model.constants as constants
import logging
import os
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List
import pandas as pd


# ----- Static Methods ----- #
def feet_and_inches(inches: int) -> str:
    feet = inches // 12
    remaining_inches = inches % 12
    return f'{feet}{remaining_inches:02d}'


class AttachmentFactory:

    def __init__(self):
        self.identifier_directory = 'model/identify_attachments'
        self.attachment_identifier_directory = os.path.join(self.identifier_directory, 'attachments')
        self.comm_identifiers = self.get_identifiers('comm.txt')
        self.power_identifiers = self.get_identifiers('power.txt')
        self.streetlight_identifiers = self.get_identifiers('streetlight.txt')

    def get_identifiers(self, identifier_file: str) -> List[List]:
        """Returns a list to identify attachment type"""
        file_path = os.path.join(self.identifier_directory, identifier_file)
        file_lines = open(file_path, 'r').readlines()
        return [line.strip().lower().split(' ') for line in file_lines]

    @staticmethod
    def is_attachment_type(identifiers: List[List[str]], attachment_name: str) -> bool:
        """Allows for 'primary riser' to match with 'primary_riser'"""
        for lst in identifiers:
            if all(item in attachment_name for item in lst):
                return True
        return False

    def is_streetlight(self, attachment_name: str) -> bool:
        return self.is_attachment_type(self.streetlight_identifiers, attachment_name)

    def is_power(self, attachment_name: str) -> bool:
        return self.is_attachment_type(self.power_identifiers, attachment_name)

    def is_comm(self, attachment_name: str) -> bool:
        return self.is_attachment_type(self.comm_identifiers, attachment_name)

    def create_attachment(self, name: str, height: str, dataframe_row) -> 'Attachment':
        """Creates an attachment of its type"""
        if self.is_streetlight(name):
            return self.create_streetlight_attachment(name, height, dataframe_row)
        elif self.is_power(name):
            return self.create_power_attachment(name, height)
        elif self.is_comm(name):
            return self.create_comm_attachment(name, height)

    @staticmethod
    def create_streetlight_attachment(name: str, height: str, dataframe_row: pd.DataFrame) -> 'Streetlight':

        # Gets grounded and molded
        grounded = pd.notna(dataframe_row['grounded']) and dataframe_row['grounded'].lower() == 'yes'  # True or False
        molded = pd.notna(dataframe_row['molded']) and dataframe_row['molded'].lower() == 'yes'  # True or False

        # Creates instance
        return Streetlight(
            name=name,
            height=height,
            grounded=grounded,
            molded=molded
        )

    @staticmethod
    def create_power_attachment(name: str, height: str) -> 'Power':
        # Creates instance
        return Power(
            name=name,
            height=height
        )

    @staticmethod
    def create_comm_attachment(name: str, height: str) -> 'Comm':
        # Creates instance
        return Comm(
            name=name,
            height=height
        )

    def identify_comment_attachment(self, comment, sequence_number):
        comment = comment.lower()  # convert the comment to lowercase

        # Filter to only .txt files
        txt_files = [f for f in os.listdir(self.attachment_identifier_directory) if f.endswith('.txt')]

        for file in txt_files:
            with open(os.path.join(self.attachment_identifier_directory, file), 'r') as f:
                for line in f:
                    items = line.split()  # split line into items

                    # Convert all items to lowercase
                    items = [item.lower() for item in items]

                    # If item contains '!', it must not be in comment
                    # If item does not contain '!', it must be in comment
                    if all(item.replace('!', '') not in comment if '!' in item else item in comment for item in items):
                        return file[:-4]  # return the file name without '.txt'

        # If no matching file found, return None
        logging.warning(f"Pole {sequence_number}: \"{comment}\" attachment was not recognized")
        return comment


@dataclass
class Attachment(ABC):
    name: str
    height: str

    def __lt__(self, other):
        if isinstance(other, Attachment):
            return self.get_height_in_inches() < other.get_height_in_inches()

    def __le__(self, other):
        if isinstance(other, Attachment):
            return self.get_height_in_inches() <= other.get_height_in_inches()

    def __gt__(self, other):
        if isinstance(other, Attachment):
            return self.get_height_in_inches() > other.get_height_in_inches()

    def __ge__(self, other):
        if isinstance(other, Attachment):
            return self.get_height_in_inches() >= other.get_height_in_inches()

    def get_height_in_inches(self) -> int:
        """Takes '3400.0', '2802', or '33' 11"' and converts in to inches of type int"""
        # Check if height is in the format of feet and inches
        if "'" in str(self.height):
            feet, inches = self.height.split("'", 1)
            # Remove any additional single quotes from the inches
            inches = inches.replace('"', '').replace("'", '')
            total_inches = int(feet) * 12 + int(inches.strip())
        else:
            # Convert the height to an integer
            self.height = int(float(self.height))
            feet = self.height // 100
            inches = self.height % 100
            total_inches = feet * 12 + inches
        return total_inches

    @abstractmethod
    def check_for_violation(self, other: 'Attachment') -> str:
        pass


class Power(Attachment):

    def check_for_violation(self, other: 'Attachment') -> str:
        # Height of both attachments in inches
        self_inches = self.get_height_in_inches()
        other_inches = other.get_height_in_inches()
        # Set distance comm attachments should be from power attachments
        required_distance = constants.INCHES_POWER_TO_COMM
        # Set conditions for violation
        is_in_range = abs(self_inches - other_inches) < required_distance
        is_comm = isinstance(other, Comm)
        # Return violation string or none
        if is_in_range and is_comm:
            return f"VIOLATION-{other.name} is {abs(self_inches - other_inches)}\" from {self.name}"


class Comm(Attachment):

    def check_for_violation(self, other: 'Attachment') -> str:
        # Height of both attachments in inches
        self_inches = self.get_height_in_inches()
        other_inches = other.get_height_in_inches()
        # Set distance comm attachments should be apart
        required_distance = constants.INCHES_COMM_TO_COMM
        # Set conditions for violation
        is_in_range = abs(self_inches - other_inches) < required_distance
        is_also_comm = isinstance(other, Comm)
        is_the_same = self._is_the_same(other)
        # Return violation string or none
        if is_in_range and is_also_comm and not is_the_same:
            return f"VIOLATION-{other.name} is {abs(self_inches - other_inches)}\" from {self.name}"

    def _is_the_same(self, other: 'Attachment'):
        """'CATV' and 'CATV 2nd Attach' will return true"""
        # Check if the text starts with the keyword or the keyword starts with the text
        if other.name.startswith(self.name) or self.name.startswith(other.name):
            return True
        else:
            return False


class Streetlight(Attachment):
    grounded: bool
    molded: bool

    def __init__(self, name, height, grounded, molded):
        self.name = name
        self.height = height
        self.grounded = grounded
        self.molded = molded

    def __repr__(self):
        return f"Streetlight(name={self.name}, height={self.height}, grounded={self.grounded}, molded={self.molded})"

    def check_for_violation(self, other: 'Attachment') -> str:
        # Height of both attachments in inches
        self_inches = self.get_height_in_inches()
        other_inches = other.get_height_in_inches()
        # Set distance comm attachments should be apart
        required_distance = self._set_violation_range()
        is_in_range = abs(self_inches - other_inches) < required_distance
        is_comm = isinstance(other, Comm)
        # Return violation string or none
        if is_in_range and is_comm:
            return f"VIOLATION-{other.name} is {abs(self_inches - other_inches)}\" from {self.name}"

    def _set_violation_range(self):
        """Sets distance comm should be from streetlight"""
        if self.grounded and self.molded:
            return constants.INCHES_STREETLIGHT_GROUNDED_AND_MOLDED_TO_COMM
        elif self.grounded:
            return constants.INCHES_STREETLIGHT_GROUNDED_TO_COMM
        else:
            return constants.INCHES_STREETLIGHT_TO_COMM
