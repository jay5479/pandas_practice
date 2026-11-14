import pandas as pd

from utils.string_ops import show_decoration

# Let's create two dfs to demonstrate

# DataFrame 1: Employees and their Department IDs
emp_df = pd.DataFrame({
    'emp_id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'dept_id': [10, 20, 10, 30],
    'location': ['Building A', 'Building B', 'Building A', 'Building C'],
})

# DataFrame 2: Departments and their Names
dept_df = pd.DataFrame({
    'dept_id': [10, 20, 40],
    'dept_name': ['Engineering', 'Marketing', 'HR'],
    'location': ['Building A', 'Building B', 'Building A']
})

print(emp_df)

show_decoration(1)

print(dept_df)

show_decoration(2)

# Let's learn pd.merge().
# pd.merge() helps us merge two dfs on any common Series across the two dfs
# syntax: pd.merge(df1, df2)
# In the below code emp_df is treated as the table on left and dept_df is
# treated as table on right.
# When no other args are specified to the merge(), pandas will look for matching
# columns across both dfs by default, find the first matching column, which in
# our case is the dept_id column and then merges the dfs by its values.
# This merge will keep only records where a dept_id value exists across both
# dfs and drops the remaining unmatched records (i.e., records where dept_id is 40).
# This is similar to SQL INNER JOIN statement.
result_df = pd.merge(emp_df, dept_df)

print(result_df)

show_decoration(3)

# The below syntax is also another way to do the same merge() studied above,
# useful when chaining methods.
# It will also take the on=, how= , left_on=, right_on= and suffixes= params
# which you will study further in this module.
# In this module we will stick to using pd.merge() as it is a bit cleaner to read.
result_df_2 = emp_df.merge(dept_df)

print(result_df_2)

show_decoration(4)

# If you want to join on a different column that is common on both df like
# location column in our case,
# supply the on= params with the column on which to be merged as arg.
result_df_3 = pd.merge(emp_df, dept_df, on="location")

# now you will see two new columns named dept_id_x and dept_id_y in your
# result_df_3. Where _x column is the dept_id column from the left table
# and _y is the dept_id column from the right table. This is to differentiate
# values between other common columns across our two dfs. Any unmatched
# location records ('Building C') are dropped as usual.
# You will also see Redundant records for Alice and Charlie as they're
# present in both Building A and B.
print(result_df_3)

show_decoration(5)

# While merging like above you can also supply a suffixes= params to customize
# your common column name suffixes instead of it displaying as _x or _y.
# The suffixes= params takes a tuple as its arg with your new suffixes from
# left to right.
result_df_3 = pd.merge(emp_df, dept_df, on="location", suffixes=("_emp", "_dep"))
print(result_df_3)

show_decoration(6)

# Sometimes you want to merge two dfs using two totally different uncommon
# columns where the values present in those columns however are similar.
# Let's first create such dfs.

# let's create a df to emulate an old database which stores dept_id as emp_id's
df_old_db = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'emp_id': [10, 20, 10]
})

# let's create another df to emulate a newer db which stores dept_id as
# department_id's
df_new_db = pd.DataFrame({
    'department_id': [10, 20, 30],
    'dept_name': ['Engineering', 'Marketing', 'HR']
})

# we now know both emp_id and department_id in these DBs actually refer to a
# dept_id value for an employee. So let's merge the df on these columns.
# To do that, you have to use the left_on= and right_on= params instead and
# supply them with their respective table's column names on which you want to
# join them on.
cleaned_df = pd.merge(df_old_db, df_new_db, left_on='emp_id', right_on='department_id')
print(cleaned_df)

show_decoration(7)

# By default, merge() does an inner join on your left and right dfs and drops
# any unmatched records if you do not supply any additional params.
# But sometimes you want to preserve data from one or both tables while still
# joining them similar to the LEFT, RIGHT and OUTER JOINS in SQL.
# To do so, supply the how= params with your join type as its str arg.
# Let's take our emp_df and dept_df to demonstrate a left join.
left_df = pd.merge(emp_df, dept_df, on="dept_id", how="left")

# The above line matches against dept_id values across both dfs but retains
# left df's records and fills it with NaN types where unmatched.
print(left_df)

show_decoration(8)

# Similarly for a right join where records from the right table is preserved.
# Note emp_id is converted to float as soon as NaN enters the column. Read
# casting basics if you do not understand this.
right_df = pd.merge(emp_df, dept_df, on="dept_id", how="right")
print(right_df)

show_decoration(9)

# Similarly for an outer join where every single record from both tables are
# retained with NaN types filling for unmatched values.
# Below line still works with the pd.merge() syntax as well but changing it
# here to the other syntax studied previously just to show all these operations
# can be done with the other syntax as well.
outer_df = emp_df.merge(dept_df, on="dept_id", how="outer", suffixes=("_emp", "_dep"))
print(outer_df)

# check notes

show_decoration(10)



# Notes:
# 1. You can also explicitly specify an inner join like so:
#    inner_df = pd.merge(emp_df, dept_df, on="dept_id", how="inner")
# 2. Mnemonic:
#    Inner join --> strictly keep only matching.
#    Outer join --> Full union. Keep everything.
#    Left join --> Match but Keep all from left alone and drop unmatched right.
#    Right join --> Match but Keep all from right alone and drop unmatched left.
# 3. The output is confusing as it is while studying this module for the first
#    time, so we are not gonna demonstrate the concepts learnt here with big data
#    since it will require multiple big dfs for the joins. Everything learnt
#    in this module will work for big data as well. Practice on your own.