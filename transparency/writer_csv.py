import csv
from transparency.writer import Writer

class WriterCSV(Writer):
    def write(self, pandasDataFrame, outputFile):
        pandasDataFrame.to_csv(outputFile, quoting=csv.QUOTE_ALL, encoding="UTF-8", index=False)
