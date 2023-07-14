from model.pole import Pole
from typing import List


class PoleManager:
    """
    Stores poles and gets violations for make ready

    Example of how its used:
    # Get make ready violations from poles
    poles = PoleManager()
    poles.extract_poles(fulcrum_excel.make_ready_df)
    poles.get_all_violations()

    # Add violations to excel and format template
    fulcrum_excel.update_make_ready(poles.pole_list)
    """
    pole_list: List[Pole] = []

    def __repr__(self) -> str:
        poles_str = ""
        for pole in self.pole_list:
            poles_str += str(pole) + "\n"
        return poles_str

    def extract_poles(self, dataframe) -> None:
        """Gets all the poles from the dataframe and stores it in a list"""
        # Make sure pole list is empty
        self.pole_list = []
        # Add poles
        for index, row in dataframe.iterrows():
            pole = Pole(row)
            self.pole_list.append(pole)

    def set_to_proposed(self):
        for index, pole in enumerate(self.pole_list):
            pole.set_to_proposed_heights()

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
