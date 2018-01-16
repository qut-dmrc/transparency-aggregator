import csv


class WriterCSV:
    def write(self, pandasDataFrame, outputFile):
        pandasDataFrame.to_csv(outputFile, quoting=csv.QUOTE_ALL, encoding="UTF-8")
