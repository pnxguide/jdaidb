# `jdaidb` - Educational Database Management System in Python

![sunbears, not your pandas alternative](thumbnail.png)

`jdaidb` is an educational database management system written in Python. This system is not ready for production. Please use it at your risk.

This system is based on the great Codd's Relational data model. It is enhanced with the fake LRU-based buffer pool for OLTP-based workloads. This system also supports a subset of SQL-92 with decent implementations of relational operators. This system does not support multiple users at the same time (i.e., concurrent access).

## Trying `jdaidb`
Before we begin, I would suggest you try using `jdaidb` first. To run it, you should go to the driver file (`src/run.py`) or simply type the following command in your terminal.

```
python3 src/run.py
```

You will get a shell interface that you can type anything there (but not everything will be valid). To exit, type `exit`.

The first version of `jdaidb` allows you to do three main things:
- Create a table using a `CREATE TABLE` statement. However, it is not based on the SQL-92 standard. Please check out the `src/test_jdaidb.py` for the precise syntax.
- Insert a row into a table using a `INSERT INTO` statement
- Drop a table using a `DROP TABLE` statement.

## Overview
There are multiple components in `jdaidb` as described below:
- `catalog`: The collection of code maintaining the system catalog for `jdaidb`
- `common`: The collection of utility code (e.g., files)
- `interface`: The collection of code making an interface (e.g., command-line interface)
- `parser`: The collection of code for parsing the SQL statement and executing it
- `query_engine`: The collection of code for executing the parsed SQL statement
- `storage_manager`: The collection of code for managing database storage and buffer pool
- **(NEW!) `structure`: The collection of code for database data structures (e.g., BST, hash table)**


## Assignment #1 - Database Storage (Due: January 13th, 2025 11:59 PM)
<details>
The first assignment will be on the `storage_manager` component. In short, you will need to implement the `buffer_pool` code and make the `core` code utilizes it.

In order to do so, you will need to understand the code in the `storage_manager` component and other relevant components.

### Part A - Understanding Storage Manager
Firstly, to understand the storage manager, you will need to understand the role of typical storage managers first. We did it in the class, by the way.

The storage manager of `jdaidb` has the following bits and pieces:
- `catalog`: The list of entries describing database objects. Fortunately, the only database object at the moment is a table.
- `page_filepath`: The mapping between a page identifier and its corresponding file path
- `page_directory`: Similarly to Lecture 3. The mapping between a database object identifer (i.e., table name) and its corresponding collection of pages. You should check the file `src/jdaidb/storage_manager/page_directory_entry.py` for more detail.

Other components/variables are more like a facilitator for making this storage manager work.

More importantly, you may see a lot of `flush`, `restore` functions/methods in many files. They are for saving the states of the objects on disk (instead of on memory). Whenever you stop using `jdaidb`, the data will still remain on your machine. You do not need to touch them (unless instructed).

For Part A, you will be tasked to write comments on each function/method. You need to write it in [docstring](https://peps.python.org/pep-0257/) or like

```python
def add(a: int, b: int) -> int:
    """
    Add two integers together and return the sum
    """
    return a + b
```

### Part B - Implementing Buffer Pool
This is probably the hardest part of this assignment. You will need to complete the `src/jdaidb/storage_manager/buffer_pool.py` file by implementing the `BufferPool` class as annotated with `TODO(A1):`. This requires knowledge from Lecture 4.

The buffer pool in `jdaidb` required in this assignment is the buffer pool that can store pages in memory and must be able to evict a page using the [LRU (least-recently used)](https://redis.io/glossary/lru-cache/) policy. Implementing the LRU policy may require additional research (but it is not that hard). However, if you just copy and paste it from external sources, be prepared for the interview.

(Hint: do not use `OrderedDict` as many people on the internet suggested if you do not understand how it works. We do not evaluate you in terms of performance. You only need to use several Python lists to deal with this.)

### Part C - Linking Storage Manager with Buffer Pool
If you look at the `src/jdaidb/storage_manager/core.py` carefully, you will see that there are many `TODO(A1):`. Those positions are where you need to link the original storage manager with the buffer pool. Unless you understand the storage manager and buffer pool code, you will not be able to complete this. To help you, several hints are provided pretty straightforwardly. You can consult with those in order to get this part done.
</details>

## Assignment #2 - Database Tree and Hash Table (Due: February 10th, 2025 11:59 PM)
<details>

You will be implementing two database data structures, Binary Search Tree (BST), and Hash Table. Even though BST is uncommon in typical database management systems, it is better to start from BST rather than implementing the popular B+Tree.

### Part A - Binary Search Tree
For the binary search tree, look at the `src/jdaidb/structure/binary_search_tree.py`. The file will contain classes `BinarySearchTree` and `Node` (which is used along the `BinarySearchTree`). You will implement the methods in the `BinarySearchTree`, including, `insert`, `read`, `delete`, and `update`. The hard part would be the `delete` that requires *tree re-structuring*.

#### Implementing `insert`
To implement `insert`, you need to understand the mandatory condition of the `BinarySearchTree`, which is as follows:

```
The key of the left child is always less than the key of the node. Also, the key of the right child is always greater than the key of the node.
```
 
You may want to traverse the tree by checking the inserted key against the current node's key until you are able to insert the new key. For example, given the following BST.

```
               [5]
              /   \
            [3]   [7]
           /   
         [1]   
```

If I would like to insert `4`, firstly, I will need to start traversing from the root node, node whose key is `5`.

```
               [5] <- current
              /   \
            [3]   [7]
           /   
         [1]   
```

Since `4 < 5`, we will move to the left child, node whose key is `3`.

```
               [5]
              /   \
 current -> [3]   [7]
           /
         [1]
```

Again, since `4 > 3`, we will traverse to the right child. However, there is no right child. This is our chance. We will insert node `4` (along with its value) as the right child of node `3`.

```
               [5]
              /   \
            [3]   [7]
           /   \
         [1]   [4]
```

And this should conclude the `insert` method.

**You may assume that there will be no duplicate values inserted into the same BST.**

#### Implementing `read`
`read` should be pretty straightforward after you implement `insert`. `read` is essentially the traversing part of `insert`; you only need to read the value based on the given key. If there is no associated key, you should report an error.

#### Implementing `delete`
`delete` should be the hardest method in this assignment. Let us assume that we will delete node `3` from the following BST.

```
               [5]
              /   \
            [3]   [7]
           /   \
         [1]   [4]
           \
            [2]
```

You cannot just remove the left child of node `5` since it will also discard nodes `1`, `2`, and `4` too.

```
               [5]
                  \
            [*]   [7]
           /   \
         [1]   [4]
           \
            [2]
```

The naive approach on keeping the disconnected nodes in touch with the tree is to reinsert all of them. Therefore, you need to re-read all the nodes that are children of node `3` (nodes `1`, `2`, and `4`) and reinsert them.

#### Implementing `update`
You will need to locate the node based on the given key. After that, you just need to change its value with the given new value.

### Part B - Hash Table
For the hash table, look at the `src/jdaidb/structure/hash_table.py`. The file will contain classes `HashTable` and `HashTableEntry` (which is used along the `HashTableEntry`). You will implement the methods in the `HashTable` similary to the `BinarySearchTree`, including, `insert`, `read`, `delete`, and `update`.

The hash function we will use for the hash table is:

```
h(key) = key % table_size
```

#### Implementing `insert`
To implement `insert`, you will need to use the provided hash function to locate the hash table entry you want to put the value in. However, a *collision* may occur. If you encounter *collision*, for this assignment, we require you to do *separate chaining* (Please check out Lecture 5 if you do not remember). We will use a simple list as a chain.

#### Implementing `read`
`read` should be simple by accessing the hash table entry based on the hash function. Since we are using *separate chaining*, you will need to iterate through all the elements in the list and match the key.

#### Implementing `delete`
`delete` should be similar to read. Except, you will need to locate the key and remove the key and the associated value from the entry.

#### Implementing `update`
Similar to BST, you will need to locate the hash table entry based on the given key and change its value with the given new value.

### Part C - Testing Code
You are required to write a code to test both of the data structures you implemented. Honestly, along the way, you should write the testing code to see whether your implementation is correct or not.

We will not give you a specification of how the testing code should look like. You need to think and create your own testing code by yourself. We do not expect you to get 100% coverage for the testing but, at least for the major functionalities, you should be able to cover them.

### Check-Out
The regular schedule for the check-out should be released 1 week before the due date. However, if you want an early check-out, please feel free to contact me via Discord.

</details>

## Assignment #3 - Query Operator Implementation (Due: March 2nd, 2025 11:59 PM)
In the last assignment, you will implement key query operators, including, `DISTINCT`, `GROUP BY` along with `COUNT(*)`, and `INNER JOIN`. Since you have done an implementation of in-memory tables (e.g., `sunbears`) in Assignment 0, we will leverage that implementation so that you do not need to deal with the table again.

In case that you do not have a proper implementation of `sunbears`, you do not need to use `project`, `filter`, `count`, and methods you implemented in Assignment 0. Actually, you can use `src/jdaidb/sunbears/dataframe.py` we give you in this repository.

Also, as you have learned from the lectures, all of those query operators can utilize hash tables to implement them. Luckily, you have an implementation of an integer-based `HashTable` from Assignment 2, you will have a chance to use it. However, you need to make sure that your implementation is valid.

There will be 5 parts. We try to arrange it from easy to hard. Please see them for yourself.

### Part A - Distinct
**Target File: `src/jdaidb/query_engine/op/op_distinct.py`**

`DISTINCT` in this assignment is close to the following SQL statement:

```sql
SELECT DISTINCT integer_column
FROM dataframe;
```

For `DISTINCT`, we will simplify it that you only need to deal with a single-column integer dataframe. Thus, you need to do `if` check to see whether the input dataframe has only a single column and it is integer or not.

To implement `DISTINCT`, you should be able to do it by iterating through all the rows (i.e., integers). For each row, you will read whether the integer is already an existing key in the hash table or not (Hint: Use `read`). If it is, you do not need to do anything. Otherwise, you `write` the integer into the hash table as a key (for the value, it can be anything (e.g., `1`); we do not use it anyway).

Note that you may want to modify the `read` method of the `HashTable` so that it throws an error when the key does not exist.

```py3
def read(self, key):
  # Code for doing read

  if not_found:
    raise Exception("key does not exist")
```

The code inside of the loop should be similar to this:

```py3
try:
  value = hash_table.read(key)
  # TODO: Push the value into the new dataframe
  #       ...
except:
  pass
```

Finally, you can read through the hash table to extract all the existing keys and create a new dataframe based on them.

### Part B - Group Count Star
**Target File: `src/jdaidb/query_engine/op/op_aggregate_count.py`**

As a reference, this part is close to the following SQL statement:

```sql
SELECT COUNT(*)
FROM dataframe
GROUP BY group_column;
```

Again, we will simplify that you only need to support a single `group_column` whose type must be integer. Be sure to verify this through `if` before going further.

To implement this, it is similar to `DISTINCT`. However, if the key does not exist, you then now need to `write` the key with the value `1`. If the key does exist, you need to increment the value of the key by `1`. You may want to use the following code to increment:

```py3
old_value = hash_table.read(key)
new_value = old_value + 1
hash_table.write(key, new_value)
```

### Part C - Nested Loop Join
**Target File: `src/jdaidb/query_engine/op/op_nested_loop_join.py`**

Now, we are working on joining two dataframes, which should be similar to the following SQL statement:

```sql
SELECT *
FROM outer, inner
WHERE outer.outer_join_column = inner.inner_join_column;
```

Again, to simplify, the join columns need to be integers (i.e., this is for Part E, which is Hash Join).

Firstly, you should check whether the join columns exist in the dataframes or not. Also, do not forget to check whether they are integers. Then, you need to find the indexes of the join columns. This should be similar to when you did `project` in Assignment 0.

```py3
outer_join_column_index = -1
for i in range(0, len(column_names), 1):
  if column_names[i] == outer_join_column:
    outer_join_column_index = i
    break

if outer_join_column_index == -1:
  raise Exception("no join column in outer")
```

After that, you need to do the join. In this part, you will be doing [Nested-Loop Join](https://en.wikipedia.org/wiki/Nested_loop_join). While doing the join, you should create the new dataframe along the way.

### Part D - Sort-Merge Join
**Target File: `src/jdaidb/query_engine/op/op_sort_merge_join.py`**

Similar to Part C, instead, you need to do [Sort-Merge Join](https://en.wikipedia.org/wiki/Sort-merge_join).

The algorithm in the link is quite complicated. You may want to go through the following guideline:
1. Sort both dataframes based on the join keys. You may want to use [`sorted()`](https://learnpython.com/blog/sort-tuples-in-python/).
2. Do the merge scan. The merge scan should be similar to the followign code:

```py3
outer_index = 0
inner_index = 0

while outer_index < len(outer) and inner_index < len(inner):
  outer_tuple = outer[outer_index]
  inner_tuple = inner[inner_index]
  if outer_tuple == inner_tuple:
    # TODO: Combine outer_tuple and inner_tuple into one and append it into the new dataframe

    outer_index += 1
    inner_index += 1
  elif outer_tuple < inner_tuple:
    outer_index += 1
  else:
    inner_index += 1
```

Even though we give you the code for merge scan, you will still need to understand it in order to pass the check-out.

### Part E - Hash Join
**Target File: `src/jdaidb/query_engine/op/op_hash_join.py`**

Similar to Part C, instead, you need to do [Hash Join](https://en.wikipedia.org/wiki/Hash_join).

The hash join consists of two main phases:
1. **Hash Table Creation**: You need to create a hash table based on the join column of the outer table. The value must be a list of tuples. When the key collides, you need to append the tuple to the list of that key.
2. **Hash Table Probing**: You need to loop through each tuple in the inner table and check whether the value of the join column exists in the hash table or not. If it is, then this tuple and the tuple(s) in the hash table whose key matches must be combined and appended to the result.

The idea should be pretty similar to the following code:

```py3
hash_table = create_hash_table(outer)

for inner_tuple in inner:
  try:
    outer_tuples = hash_table.read(inner_tuple[inner_join_index])
    for outer_tuple in outer_tuples:
      # TODO: Combine outer_tuple and inner_tuple into one and append it into the new dataframe

  except:
    pass
```

### Check-Out
You should check-out during March 8th to March 9th. If you want an early check-out, please contact me in advance. In order to pass the check-out, you will encounter the questions in the following topics:

- Distinct or Group Count Star
- Sort-Merge Join (especially, the **merge scan** part)
- Hash Join

For this check-out, you only have one attempt. However, you can get consulted with TAs before the time. Please be well-prepared.
