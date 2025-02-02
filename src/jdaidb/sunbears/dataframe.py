class DataFrame:
    def __init__(self, column_names: list[str], column_types: list[type], rows: list[object]):
        self.column_names = column_names
        self.column_types = column_types
        self.rows = rows

    def __str__(self):
        dataframe_string = ""

        # Print column names
        for i in range(len(self.column_names)):
            dataframe_string += f"{self.column_names[i]}:{str(self.column_types[i])}"
            if i < len(self.column_names) - 1:
                dataframe_string += "|"
        dataframe_string += "\n"

        # Print data
        for row in self.rows:
            for i in range(len(row)):
                dataframe_string += f"{row[i]}"
                if i < len(row) - 1:
                    dataframe_string += "|"
            dataframe_string += "\n"
        
        return dataframe_string
