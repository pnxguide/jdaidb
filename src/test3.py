import sys

from jdaidb.query_engine.op import op_distinct, op_aggregate_count, op_nested_loop_join, op_sort_merge_join, op_hash_join

from jdaidb.sunbears.parser import Parser
from jdaidb.sunbears.dataframe import DataFrame

"""
Simple Unit Test
"""

p = Parser()

def test_distinct():
    df = p.read_csv("./test_data/distinct.csv")

    try:
        df = op_distinct.op_distinct(df)
    except:
        return False

    return len(df.rows) == 10

def test_aggregate_count():
    df = p.read_csv("./test_data/aggregate_count.csv")

    try:
        df = op_aggregate_count.op_aggregate_count(df)
        dict = {}
        for row in df.rows:
            dict[str(row[0])] = int(row[1])
    except:
        return False

    return (len(df.rows) == 3) and (dict["Thailand"] == 8) and (dict["China"] == 5) and (dict["US"] == 3)

def test_nested_loop_join():
    emp_df = p.read_csv("./test_data/employees.csv")
    dept_df = p.read_csv("./test_data/departments.csv")
    
    try:
        df = op_nested_loop_join.op_nested_loop_join(emp_df, dept_df, "department", "department_id")
    except:
        return False

    return (len(df.rows) == 6) and (len(df.rows[0]) == 4)

def test_sort_merge_join():
    emp_df = p.read_csv("./test_data/employees.csv")
    dept_df = p.read_csv("./test_data/departments.csv")

    try:
        df = op_sort_merge_join.op_sort_merge_join(emp_df, dept_df, "department", "department_id")
    except:
        return False

    return (len(df.rows) == 6) and (len(df.rows[0]) == 4)

def test_hash_join():
    emp_df = p.read_csv("./test_data/employees.csv")
    dept_df = p.read_csv("./test_data/departments.csv")

    try:
        df = op_hash_join.op_hash_join(emp_df, dept_df, "department", "department_id")
    except:
        return False

    return (len(df.rows) == 6) and (len(df.rows[0]) == 4)

tests = [test_distinct, test_aggregate_count, test_nested_loop_join, test_sort_merge_join, test_hash_join]
for test in tests:
    original_stdout = sys.stdout
    sys.stdout = None
    test_result = test()
    sys.stdout = original_stdout

    if test_result:
        print(f"test {test} OK")
    else:
        print(f"test {test} Not OK")
        sys.exit()
