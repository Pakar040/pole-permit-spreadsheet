from pole import Pole
from typing import List


class PoleManager:
    pole_list: List[Pole] = []

    def get_poles(self, dataframe):
        for index, row in dataframe.iterrows():
            pole = Pole(row)
            self.pole_list.append(pole)
