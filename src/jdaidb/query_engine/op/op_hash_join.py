from jdaidb.sunbears.dataframe import DataFrame
from jdaidb.structure.hash_table import HashTable

def op_hash_join(outer: DataFrame, inner: DataFrame, outer_join_column: str, inner_join_column: str) -> DataFrame:
    # TODO(A3): Verify whether the outer and inner tables are appropriate
    #           (e.g., they have a valid join column, the join columns are integers)

    # TODO(A3): Create a new DataFrame based on columns in the join result
    new_dataframe = DataFrame()
    # Add more code...

    # TODO(A3): Create a hash table from outer

    # TODO(A3): Probe the hash table to create

    # Return new_dataframe
    return new_dataframe
