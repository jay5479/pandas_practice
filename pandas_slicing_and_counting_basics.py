import pandas as pd
from utils.string_ops import show_decoration


# creating a data frame from a CSV
df = pd.read_csv('survey_results_schema.csv')

# Counting distinct values in a series
# similar to GROUP BY in SQL, counts no. of occurrences of unique values in the series and
# returns a series of unique values and their corresponding occurrence counts
print(df['force_resp'].value_counts())

show_decoration(1)

# Data frame slicing
# Unlike python slicing, df slicing in pandas is inclusive of end value.
# need to use df.loc[start:end] syntax for slicing
print(df.loc[0:5])

show_decoration(2)

# To slice columns using labels use loc
# this will return empty df since we are only telling to slice columns but not pull any values
print(df.loc['qid':'question'])

show_decoration(3)

# To also pull values from columns qid to question (inclusive),
# pull some rows/records as well, below will fetch all rows from 0th to 5th index
print(df.loc[0:5, 'qid':'question'])

show_decoration(4)

# To slice using indexes, use .iloc[start_row:end_row, start_column:end_column]
# CAUTION: Integer based slicing is always end value exclusive, same as python slicing
print(df.iloc[0:3, 0:2])

show_decoration(5)