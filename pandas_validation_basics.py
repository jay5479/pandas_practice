import pandas as pd

from utils.string_ops import show_decoration

# Let's create a small df with no index
orders_df = pd.DataFrame({
    'order_id': [101, 102],
    'user_id': ['id1', 'id1']
})

# Let's create another small df with index which contains duplicate index values.
users_df = pd.DataFrame({
    'name': ['Alice', 'Alice_Updated', 'Bob']
}, index=['id1', 'id1', 'id2'])


print(orders_df, f"\n\n", users_df)

show_decoration(1)

# Let's learn validate= params. This params can be supplied to both join() and
# merge() that we studied in the previous modules, and it uses the underlying
# pd.errors.MergeError() class to raise exceptions.
# Let's learn what it does,
# Without validate= params, the following join silently duplicates order 101
# into two rows
result_df = orders_df.join(users_df, on='user_id')
print(result_df)

show_decoration(2)


# With validate='m:1', it catches the dirty data immediately,
# uncomment below line and study as this raises exceptions.
# The arg m:1 means that the left df can have many (m) duplicate keys (if you don't
# know what are keys check notes #1) but the right df can only have unique (1)
# keys. This relationship is called a many-to-one relationship.
# I am putting this in try block so that this module doesn't stop because
# of the exception raised during validation as our right df does not have unique keys.

try:
    orders_df.join(users_df, on='user_id', validate='m:1')
except Exception as e:
    print(e) # read the error word by word it tells which table is conflicting

show_decoration(3)


# Similarly one-to-many relationship can also be tested by supplying 1:m,
# where your left df can only have unique keys but right can have many
try:
    orders_df.join(users_df, on='user_id', validate='1:m')
except Exception as e:
    print(e)


show_decoration(4)


# Similarly let's test 1:1 relationship where keys must be unique across
# both columns.
# Just using merge() instead of join(), since it will still work.
# And since key column names on both dfs are not same we supply left_on= params
# and for supplying the index column of the right df, since it as no column name,
# we use the right_index= params which takes a bool arg,
# similarly we can also use left_index= as a params also for merge() or join().

try:
    orders_df.merge(users_df, left_on='user_id', right_index=True, validate='1:1')
except Exception as e:
    print(e)


show_decoration(5)


# similarly, we can also test m:m relationship. But this is ill-advised as it
# does no checks / validation for unique keys and raises no exception.
# Generally many duplicate keys in your df actually means your df is not clean.
# This is just used as a development notation to suggest that there are no
# unique keys in any df. Also, just using pd.merge() to flex.

error_df = pd.merge(orders_df, users_df, left_on='user_id', right_index=True, validate='m:m')
print(error_df)

show_decoration(6) # check notes




# Notes:
# 1. The values in whatever column name(s) that we supply to the on= params, are
#    called as keys when it is a regular column on which another df is to be
#    joined, and is called as index when it is an index column on which the
#    other df is to be joined. This is just standard SQL convention.
# 2. Just like on, lsuffix, and rsuffix, validate only works when other (right df)
#    is a single DataFrame or Series. Passing a list of DataFrames alongside
#    validate like how we learned in multiple join will raise a ValueError.