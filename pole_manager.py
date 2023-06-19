from pole import Pole
from typing import List


class PoleManager:
    pole_list: List[Pole] = []

    def __repr__(self) -> str:
        poles_str = ""
        for pole in self.pole_list:
            poles_str += str(pole) + "\n"
        return poles_str

    def extract_poles(self, dataframe) -> None:
        """Gets all the poles from the dataframe and stores it in a list"""
        for index, row in dataframe.iterrows():
            pole = Pole(row)
            self.pole_list.append(pole)

    def get_all_violations(self) -> None:
        """Adds all violations for all poles to dict"""
        for pole in self.pole_list:
            pole.make_ready = pole.find_violations()

    def get_pole(self, sequence_number: str) -> Pole:
        """Finds a pole instance using its sequence number"""
        for pole in self.pole_list:
            if pole.sequence_number == sequence_number:
                return pole
        return "No poles have this sequence number"
