import pandas as pd

from utils.string_ops import show_decoration

# Let's create two dfs to demonstrate
# Just another way to create a df by supplying the index column values
# directly, by using the index params which takes a list of values as arg.
names_df = pd.DataFrame({'name': ['Alice', 'Bob', 'Charlie']}, index=['id1', 'id2', 'id3'])

# Let's create another df similarly with slightly different index.
ages_df  = pd.DataFrame({'age': [25, 30, 35]}, index=['id1', 'id2', 'id4'])

# Let's learn join(). The join(), joins two dfs by index by default unlike
# merge() which allows us to join by any common column.
# Note that unlike merge() that we learnt previously, join() does not have an
# identical pd.join().
# When using join we have to strictly follow the df_1.join(df_2) syntax.
result_df = names_df.join(ages_df)

# Note that the default join is a LEFT JOIN where records are preserved from
# the left df with NaN types in place for missing/unmatached values.
print(result_df)

show_decoration(1)

# The .join() also takes a how= params which takes a str arg for controlling
# your joins similar to merge(). Now let's do an INNER JOIN.
inner_df = names_df.join(ages_df, how='inner')
print(inner_df)

show_decoration(2)

# Let's do a RIGHT JOIN
right_df = names_df.join(ages_df, how='right')
print(right_df)

show_decoration(3)

# Let's do an OUTER JOIN
outer_df = names_df.join(ages_df, how='outer')
print(outer_df)

show_decoration(4)

# Sometimes your left df has your values to be matched in a regular column
# while the right df has those values in an index. In such case you can supply
# the on= params with a str arg specifying which column you want to match the
# index on right df with. Let's first create two such dfs to demonstrate this

orders_df = pd.DataFrame({
    'order_id': [101, 102, 103],
    'user_id': ['id1', 'id2', 'id1']  # Key is in a regular column
})

users_df = pd.DataFrame({
    'name': ['Alice', 'Bob']
}, index=['id1', 'id2'])               # Key is in the index column

# Now let's demonstrate the join with the on= params. Note that if you wanted
# to do this without the on= params then you have to do a set_index() on your
# left df first and the join it which is tedious.
easy_join_df = orders_df.join(users_df, on='user_id')
print(easy_join_df)

show_decoration(5)

# Note that the on= params works only for matching a left df column to a right
# df index column. trying to do it in reverse leads to KeyError. Uncomment below
# code and run to see and understand the logic of why it errors out.
# error_df = users_df.join(orders_df, on='user_id')
# print(error_df)

show_decoration(6)

# The join() also takes a suffixes= arg similar to merge().
# But unlike merge() that will default to suffixing _x and _y to columns that
# have same names across both the dfs, join() will instead raise a ValueError.
# To avoid this use the lsuffix= and rsuffix= params instead to tell pandas how
# the left and right df column names need to be suffixed, where lsuffix stands
# for left df column name suffix and rsuffix for right df column name suffix.
# You can also either only use lsuffix= or rsuffix= params if you want only one
# df's column names to be suffixed rather than both.

scores_2025 = pd.DataFrame({'score': [80, 90]}, index=['Alice', 'Bob'])
scores_2026 = pd.DataFrame({'score': [85, 95]}, index=['Alice', 'Bob'])

all_years_scores_df = scores_2025.join(scores_2026, lsuffix='_2025', rsuffix='_2026')
print(all_years_scores_df)

show_decoration(7)

# You can also join a single named Series obj to your df using join().
# Let's create a Series object to join with our names_df from the start of
# this module. Note that your series explicitly needs to have a name,
# if not this join will raise ValueError.
# Also note names_df holds 3 records whereas our series has only 2 and
# Since join() defaults to a LEFT JOIN any unmatched values on the right series
# is dropped and missing values on right series is replaced with null.
s_city = pd.Series(['NYC', 'LA'], index=['id1', 'id2'], name='city')
print(names_df.join(s_city)) # Check notes

show_decoration(8)

# We can also join multiple dfs or Series objs to a df using join() if we
# supply them as a list. This is called a multi table join.
# The multi table join has three rules:
# 1. Only index based joins are strictly supported, you can no longer use the
#    on= params.
# 2. Also, all the dfs/Series objs you're joining must have unique column
#    names, so you can no longer use the l/rsuffix= params. Trying it will lead
#    to KeyError.
# 3. The how= params is still supported for all JOINs except RIGHT JOIN, since
#    there is no single right df while passing it is a list arg.
#    Trying to RIGHT JOIN will lead to ValueError.
multi_join_df = names_df.join([ages_df, s_city, orders_df], how='outer')
print(multi_join_df)

show_decoration(9)

# You can also use the sort= params and pass a Bool to order the output.
# This is an optional arg with a default value set to False. check notes.
# When set to true, the index of the resulting df will be sorted again after the join
# overriding the default sorting behaviour explained in notes.
# Let's create 2 dfs with misordered index values to demonstrate this.
new_name = pd.DataFrame({'name': ['Adhi', 'Jeeshma', 'Kanushi']}, index=['id6', 'id3', 'id4'])
new_age  = pd.DataFrame({'age': [35, 30, 6]}, index=['id5', 'id4', 'id6'])

# set sort=False or remove it from below line and play with different joins to
# understand behaviour explained in notes.
sorted_df = new_name.join(new_age, how='inner', sort=True)
print(sorted_df)

# check notes

show_decoration(10)




# Notes:
# 1. While joining a Series obj to a df is possible, joining a df to a Series
#    obj is not possible .i.e, s_city.join(names_df) as join() is strictly a
#    Dataframe method.
# 2. By default, sort= params is set to False and it handles joins and
#    resulting df's index as follows:
#    LEFT & INNER JOIN --> preserve index col order of left df
#    RIGHT JOIN --> preserve index col order of right df
#    OUTER JOIN --> sort final index column after joining left & right df
# 3. Only join() method supports multiple join where you can pass a list of
#    dfs or Series' to be joined. merge() does NOT support multiple join.
#    However, merges can be chained like so which helps us do multiple joins:
#    result_df = (
#     df1
#     .merge(df2, left_on='x_df1', right_on='y_df2')
#     .merge(df3, left_on='x_df1', right_on='z_df3')
# )