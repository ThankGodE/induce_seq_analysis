"""
A collection of classes or functions that performs breaks processing operations
"""

import os.path
import sys

from package.enumsoperations.delimiter_enums import Delimiters
from package.enumsoperations.numerical_enums import Positions
from package.fileoperations.filehandlers import read_csv


class BreaksOperator:
    """Performs breaks processing operations"""

    breaks_bed_file = None
    asisi_file = None
    output_directory = None
    score_threshold = None

    def __init__(self, breaks_file: list, asisi_file: str, output_directory: str, score_threshold: int) -> None:
        """
        Constructor

        Parameters
        ----------
        breaks_file :list
           Path to breaks file
        asisi_file:str
           Path to asisi file
        output_directory:str
           Path to output directory
        """

        self.breaks_file = breaks_file
        self.asisi_file = asisi_file
        self.output_directory = output_directory
        self.score_threshold = score_threshold

    def process_breaks(self) -> None:
        """ process breaks bed file """

        a = BreaksOperator.__filter_reads_from_breaks_file(self)

    def __filter_reads_from_breaks_file(self) -> str:
        """ filter reads from a breaks bed file """

        a = [row for row in
             read_csv(self.breaks_file, Delimiters.TAB_SEPERATOR) if BreaksOperator.__filter_read_from_breaks_row(
                row, self.score_threshold)
             ]

        print(a)

    @classmethod
    def __filter_read_from_breaks_row(cls, line: str, threshold: int) -> bool:
        """ filter reads from a breaks bed line """

        return int(line[Positions.FIFTH]) >= threshold
