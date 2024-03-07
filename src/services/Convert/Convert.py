from json import loads, dumps
import pandas as pd

class Convert():
    
    @classmethod
    def convert_file_to_format(self, file):
        data = pd.read_excel(file)
        jsonData = data.to_json(orient="records") # records, split, index, columns, values, table
        parsed = loads(jsonData)
        return parsed
    
    @classmethod
    def convert_format_to_file(self, data):
        return "ok"