import pandas as pd

from utils.string_ops import show_decoration

# Let's create a multi-index object from a list of tuples.
# The names 'country' and 'year' are called as index levels.
idx = pd.MultiIndex.from_tuples(
    [('US', '2025'), ('US', '2026'), ('IN', '2025')],
    names=['country', 'year']
)

print(type(idx))

show_decoration(1)

# Let's create two dataframes using our multi index
revenue_df = pd.DataFrame({'revenue': [100, 120, 80]}, index=idx)
tax_df = pd.DataFrame({'tax_rate': [0.21, 0.21, 0.25]}, index=idx)

# Let's do a simple left join.
# df.join() handles MultiIndex (hierarchical index) DataFrames natively,
# matching keys across levels automatically whenever index level names align.
# When both DataFrames share the exact same MultiIndex structure and level names,
# join() aligns rows by matching the full tuple of index keys.
# 1. This is called a multi-index to multi-index join (exact level match).
result_df = revenue_df.join(tax_df)
print(result_df)

show_decoration(2)

# Now let's see MultiIndex (Left) to Single-Index (Right) join.
# This is one of join()'s most convenient features:
# You do not need on= or .reset_index() when joining a single-index df onto a
# MultiIndex df, provided the single index has the same name as one of the
# MultiIndex levels.
# Pandas automatically detects the matching level name and broadcasts the
# right df's values across all matching rows in the MultiIndex.
# Let's create a new df with new index to demonstrate this. The pd.index() can
# be used to create index Series directly where values of index as passed as alist

currency_df = pd.DataFrame(
    {'currency': ['USD', 'INR']},
    index=pd.Index(['US', 'IN'], name='country')
)

# now let's join
result_2_df = revenue_df.join(currency_df)

# Important rule: The single index on the right df must be named either
# name='country' or name='year' so that it matches a index col name from the left df.
# If currency_df.index.name is None or doesn't match a level name in revenue_df,
# pandas will raise a ValueError: cannot join with no overlapping index names.
print(result_2_df)

show_decoration(3)

# Now let's see Single-Index (Left) to MultiIndex (Right) join
# When the left df has a single index (or regular columns) and the right df
# has a MultiIndex, pass a list of column names to on= in the exact order of
# the MultiIndex levels.
# let's create a new right df with multi index to demonstrate
flat_df = pd.DataFrame({
    'order_id': [1, 2],
    'country': ['US', 'IN'],
    'year': ['2026', '2025']
})

# Match flat_df[['country', 'year']] against revenue's MultiIndex
result_3_df = flat_df.join(revenue_df, on=['country', 'year'])


# Note: You cannot join a single-index left df onto only one level of a multi-level
# right MultiIndex using join(). The on list must supply values for every level
# of the right MultiIndex.
# To join on a partial MultiIndex on the right df, drop or reset the extra level
# first, or use pd.merge().
print(result_3_df)

show_decoration(4)

# Let's learn flattening a multi-index
