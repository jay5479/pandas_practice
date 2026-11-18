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

# Let's learn flattening a multi-index. Flattening converts a MultiIndex into
# regular columns or a single-level index. Flattening removes the nested
# hierarchy so downstream operations (like .join(), .merge(), plotting, or CSV
# exports) are easier to work with.
# Now let's flatten Row MultiIndex to Regular Columns using reset_index(). It
# takes inplace=True arg to permanently reset. But here we are not doing that
# as we want to use the revenue_df later.

new_revenue_df = revenue_df.reset_index() # Flattens ALL levels into columns
print(new_revenue_df)

show_decoration(5)

# Now let's learn how to flatten one level alone by using the level= params.
# This params also takes a list of str level names as arg if you want to reset
# multiple levels but not all levels.
# syntax: df.reset_index(level=["level_0_name", "level_1_name", ...], inplace=True)
new_revenue_df = revenue_df.reset_index(level="year")
print(new_revenue_df)

show_decoration(6)

# Now let's learn Flattening Row MultiIndex to a Single Joined Index using
# .to_flat_index()
# If you want to keep a single index rather than moving keys into columns,
# convert the tuples into flat strings.
# To do that that let's make a copy of our revenue_df first
df_flat_idx = revenue_df.copy()

# Now let's simply use list comprehension to join level names
df_flat_idx.index = ['_'.join(col) for col in revenue_df.index.to_flat_index()]

print(df_flat_idx)

show_decoration(7)

# Now let's learn Flattening Column MultiIndex (Very Common After .groupby())
# When you run .groupby(...).agg(['sum', 'mean']), you get 2-tier column headers
# like ('revenue', 'sum'). Flatten them with a list comprehension over df.columns.
# let's first join our tax and revenue dfs and flatten it.
combined_df = revenue_df.join(tax_df).reset_index()

# and create a group_by df to demonstrate this.
grouped_df = combined_df.groupby('country').agg({'revenue': ['sum', 'mean']})

# See how column names are tiered (2-tier)
print(grouped_df)

show_decoration(8)

# Now to avoid this, let's use this trick using list comprehension and
# .to_flat_index()
grouped_df.columns = ['_'.join(col).strip() for col in grouped_df.columns.to_flat_index()]
print(grouped_df)

# Tip: If one level is empty—such as ('id', '') after reset_index(), use
# '_'.join(filter(None, col)) to avoid trailing underscores like 'id_'.


show_decoration(9)

# Now let's learn swapping MultiIndex Levels using the swaplevel().
# Sometimes you want to keep the MultiIndex, but change which level is on the
# outside (level 0) versus the inside (level 1).
# syntax: df.swaplevel(i, j, axis=0) exchanges the positions of two levels.
# With a 2-level MultiIndex, calling .swaplevel() with no arguments swaps
# levels 0 and 1.
# Before: outer='country', inner='year'
# After:  outer='year', inner='country'
swapped_df = revenue_df.swaplevel('country', 'year')
print(swapped_df)

show_decoration(10)

# Always follow swaplevel() with sort_index() so outer keys group together
# cleanly.
# Why .sort_index() matters: swaplevel() only flips the labels in place—it does
# not re-group identical outer labels together, which can break slicing (eg: df.loc['2025'])
# or hurt lookup performance until sorted.
swapped_df = revenue_df.swaplevel().sort_index()
print(swapped_df)

show_decoration(11)

# Now let's learn reordering Multi-index levels by reordering 3+ Levels using
# reorder_levels().
# For that first let's create a 3 level MultiIndex and a df with it
idx_3df = pd.MultiIndex.from_tuples(
    [('US', 'North', '2025'), ('US', 'South', '2026'), ('IN', 'East', '2025')],
    names=['country', 'region', 'year'])

revenue_3df = pd.DataFrame({'revenue': [100, 120, 80]}, index=idx_3df)
print(revenue_3df)

show_decoration(12)

# When you have three or more index levels, reorder_levels() lets you specify
# the exact order in one step instead of chaining multiple swaplevel() calls:
# Works on both row index (axis=0) and column MultiIndex (axis=1)
print(revenue_3df.reorder_levels(['year', 'region', 'country'], axis=0).sort_index())

show_decoration(13)

# Let's create a df with both row and column MultiIndex to demonstrate
# swaplevel() on a column MultiIndex.
# Let's create a column MultiIndex obj first
col_idx = pd.MultiIndex.from_tuples(
    [('Financials', 'Revenue'), ('Operations', 'TaxRate')],
    names=['category', 'metric'])

# Let's create a df with both Row and Column MultiIndex now using the
# idx_3f created previously for our regular row index and col_idx for our
# column index using the columns= params
multi_df = pd.DataFrame([[100, 0.21], [120, 0.21], [80, 0.25]], index=idx_3df, columns=col_idx)

print(multi_df)

show_decoration(14)

# Now let's do a swaplevel() on column MultiIndex using the axis=1 arg
# This Reorders column levels from ['category', 'metric'] to ['metric', 'category']
cols_reordered_df = multi_df.reorder_levels(['metric', 'category'], axis=1)
print(cols_reordered_df)

show_decoration(15)

# Let's learn how to Drop a Single Unused Level using droplevel()
# If one level of a MultiIndex becomes redundant (for example, after filtering
# to a single country df.loc['US'] or aggregating), droplevel() removes that
# tier cleanly without resetting the remaining index levels.
# let's demonstrate this using the 3 tier revenue_3df created previously
print(revenue_3df.droplevel('country'))  # Leaves 'year' as a clean single index

show_decoration(16)

# We can also Drop multiple levels using droplevel() by passing a list of level
# names or level integer locations like 0, 1 etc. to the arg. Here we use the names,
print(revenue_3df.droplevel(['country', 'year']))

show_decoration(17)



# Notes:
# 1. You have successfully completed all basics required for working with pandas!
# 2. This module is a heavy and lengthy module, practice this module more if you
#    don't understand multi indexing.
