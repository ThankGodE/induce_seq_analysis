"""
A collection of functions that performs file writing operations.
"""

__name__ = "__main__"

import logging


class FileWriter:
    """ The FileWriter class handles the writing of the data to a file. """

    def __init__(self, file_path, mode):
        """
        Creates a new FileWriter object.

        :param file_path: Path to the file.
        :param mode: Mode of the file.
        """
        self.file_path = file_path
        self.mode = mode

    def write_str(self, data: str) -> None:
        """
        Writes data to a file. Data here is a string

        :param data: String data to write.
        """

        with open(self.file_path, self.mode) as file:
            file.write(data)

        logging.info("writing data to {}".format(self.file_path))