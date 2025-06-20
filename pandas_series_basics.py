import pandas as pd
from utils.string_ops import show_decoration


people = {
    "Name":["Kanushi", "Adhi", "Jeeshma", "Raavan"],
    "Age":[6, 33, 28, 2],
    "Email":["kanushi_g@gmail.com", "adhi_seshan@comcast.com", "jeeshma_john@comcast.com", "raavan@gmail.com"],
    }

# Creating a df from a python dictionary
df = pd.DataFrame(people)
print(df.head())

show_decoration(1)

# Accessing a column aka series from your df
print(df['Email']) #This is not the same as accessing values of a key from dict, check output

show_decoration(2)

print(type(df['Email'])) #Returns a Series obj

show_decoration(3)

# Another way to access a series is with a dot notation
# This method is ill-advised because sometimes in your df a column might be named
# as same as an inbuilt df method like for eg: count. So prefer previous method.
print(df.Email)

show_decoration(4)

# Accessing multiple series from a df, takes a list of keys as arg
print(df[['Name', 'Age']])
print(type(df[['Name', 'Age']])) # returns a smaller data frame obj

show_decoration(5)

# Show all columns in our df
print(df.columns)

show_decoration(6)

# Grab a row using its index in df
print(df.iloc[0]) # returns the first row of our df, iloc stads for integer location
print(type(df.iloc[0])) # returns a series obj

show_decoration(7)

# Grab multiple rows using their index, takes list of indices as arg
print(df.iloc[[0, 1]]) # grabs 1st and 2nd row
print(type(df.iloc[[0, 1]])) # returns a df obj

show_decoration(8)

# Grab multiple rows by index but only with specific column value
# Grabs 1st and 3rd row but with values only from 3rd column, returns df obj
print(df.iloc[[0, 2], 2])

show_decoration(9)

# Grab multiple rows by index but only with specific columns values
print(df.iloc[[0, 2, 3], [0, 1]]) # Grabs 1st, 3rd & 4th row but with values only from 1st & 2nd column

show_decoration(10)

# Grab multiple rows by labels
# loc stands for location, by default rows have their indices as label, check notes
print(df.loc[0]) # returns a series obj

show_decoration(11)

print(df.loc[0, 'Name']) # returns 1st row with values only from column with label 'name'

show_decoration(12)

# Returns 1st and second rows by its default label with values only from columns labelled
# 'Email', 'Name' and displays output df in that exact order of columns even if original df
# column order is different
print(df.loc[[0, 1], ['Email', 'Name']])

show_decoration(13)


# Notes:
# 1. A data frame is a two-dimensional array i.e, just rows & columns.
# 2. A series is a one-dimensional array i.e, rows/values in a column.
# 3. The loc() method unlike iloc() method treats int args as labels because df rows unless
#    labelled explicitly, will take their indices as default labels.