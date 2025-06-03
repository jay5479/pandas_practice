import pandas as pd
from utils.string_ops import show_decoration


people = {
    "Name":["Kanushi", "Adhi", "Jeeshma"],
    "Age":[6, 33, 28],
    "Email":["kanushi_g@gmail.com", "adhi_seshan@comcast.com", "jeeshma_john@comcast.com"],
    }

# Creating a df from a python dictionary
df = pd.DataFrame(people)
print(df.head())
show_decoration()

# Accessing a column aka series from your df
print(df['Email']) #This is not the same as accessing values of a key from dict, check output
show_decoration()
print(type(df['Email']))
show_decoration()

# Another way to access a series is with a dot notation
# This method is ill-advised because sometimes in your df a column might be named
# as same as an inbuilt df method like for eg: count. So prefer previous method.
print(df.Email)
show_decoration()

# Accessing multiple series from a df
print(df[['Name', 'Age']])
show_decoration()





# Notes:
# 1. A data frame is a two-dimensional array i.e, just rows & columns.
# 2. A series is a one-dimensional array i.e, rows in a column.