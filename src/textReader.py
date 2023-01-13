from IReader import IReader
from dumpObject import dobj
import os


class textReader(IReader):

    def __init__(self, _seperator: str):

        if _seperator is None:
            _seperator = " "

        self.seperator = _seperator

    def readData(self, path: str) -> dobj:

        if path is None or not os.path.exists(path):
            raise Exception("Please provide a valid path.")

        wordSet = dobj()
        wordSet.totalWords = 0
        wordSet.uniqueWordSet = {}
        # Open file
        with open(path, "r") as file1:

            # Read and extract into a set
            for line in file1:
                line = line.strip()
                word_list_from_line = line.split(self.seperator)
                wordSet.totalWords += len(word_list_from_line)
                wordSet.uniqueWordSet.update(word_list_from_line)
        
        # Return the set
        return wordSet
