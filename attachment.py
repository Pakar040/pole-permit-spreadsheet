import os
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List


# ----- Static Functions ----- #
def get_identifiers(identifier_file: str) -> List[List]:
    """Returns a list to identify attachment type"""
    file_path = os.path.join('identify_attachments', identifier_file)
    file_lines = open(file_path, 'r').readlines()
    return [line.strip().lower().split(' ') for line in file_lines]


def check_string(list_of_lists: List[List[str]], string: str) -> bool:
    """Allows for 'primary riser' to match with 'primary_riser'"""
    for lst in list_of_lists:
        if all(item in string for item in lst):
            return True
    return False


def create_attachment(name: str, height: str):
    """Creates an attachment object of any type"""
    comm = get_identifiers('comm.txt')
    power = get_identifiers('power.txt')
    streetlight = get_identifiers('streetlight.txt')
    if check_string(streetlight, name):
        return Streetlight(
            name=name,
            height=height
        )
    elif check_string(power, name):
        return Power(
            name=name,
            height=height
        )
    elif check_string(comm, name):
        return Comm(
            name=name,
            height=height
        )


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
        self_inches = self.get_height_in_inches()
        other_inches = other.get_height_in_inches()
        if abs(self_inches - other_inches) < 40 and isinstance(other, Comm):
            return f"VIOLATION-{other.name} is within 40 inches of {self.name}"


class Comm(Attachment):

    def check_for_violation(self, other: 'Attachment') -> str:
        self_inches = self.get_height_in_inches()
        other_inches = other.get_height_in_inches()
        if abs(self_inches - other_inches) < 12 and isinstance(other, Comm):
            return f"VIOLATION-{other.name} is within 12 inches of {self.name}"


class Streetlight(Attachment):

    def check_for_violation(self, other: 'Attachment') -> str:
        self_inches = self.get_height_in_inches()
        other_inches = other.get_height_in_inches()
        if abs(self_inches - other_inches) < 40 and isinstance(other, Comm):
            return f"VIOLATION-{other.name} is within 40 inches of {self.name}"
