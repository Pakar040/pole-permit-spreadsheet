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


def check_string(list_of_lists: List[List[str]], string: str):
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

    @abstractmethod
    def find_violations(self, attachment_array: List['Attachment']):
        pass


class Power(Attachment):
    TYPE: str = "Power"

    def find_violations(self, attachment_array: List['Attachment']):
        pass


class Comm(Attachment):
    TYPE: str = 'Comm'

    def find_violations(self, attachment_array: List['Attachment']):
        pass


class Streetlight(Attachment):
    TYPE: str = 'Streetlight'

    def find_violations(self, attachment_array: List['Attachment']):
        pass
