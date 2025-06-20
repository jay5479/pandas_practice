import pandas as pd
from utils.string_ops import show_decoration


# creating a data frame from a CSV
df = pd.read_csv('survey_results_public.csv')

# Attribute that displays total rows & columns in a tuple
print(df.shape)
show_decoration(1)

# Method to display properties of your data frame
print(df.info())
show_decoration(2)

# Methods to display 'n' number of columns/rows while printing your data frame
pd.set_option('display.max_columns', 5)
pd.set_option('display.max_rows', 10)
print(df)
show_decoration(3)

# Method to show the first 'n' rows from your df
# if no args provided it will always show first 5 rows
print(df.head(10))
show_decoration(4)

# Method to show the last 'n' rows from your df
# if no args provided it will always show last 5 rows
print(df.tail())
show_decoration(5)

