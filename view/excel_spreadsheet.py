import os


class ExcelFile:
    """This represents the inputs and outputs"""
    def __init__(self):
        self.name = ''
        self.directory = ''
        self.template = ''

    def __repr__(self) -> str:
        return f"Name: {self.name}\nDirectory: {self.directory}\nPath: {self.path}\nTemplate: {self.template}"

    @property
    def path(self) -> str:
        return os.path.join(self.directory, self.name)

    @path.setter
    def path(self, path: str) -> None:
        self.directory = os.path.dirname(path)
        self.name = os.path.basename(path)


# Test
if __name__ == '__main__':
    file = ExcelFile()
    file.name = 'output.xlsx'
    file.directory = 'path/to/file'
    file.path = 'project\\test\\folder\\input.xlsx'
    print(file)
