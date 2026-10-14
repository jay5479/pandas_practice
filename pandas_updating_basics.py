import pandas as pd

from utils.string_ops import show_decoration


# load a demo df for studies
people = {
    "First":["Kanushi", "Adhi", "Jeeshma", "Raavan"],
    "Last":["Gopi", "Seshan", "Seshan", "Krishnan"],
    "Email":["kanushi_g@gmail.com", "adhi_seshan@comcast.com", "jeeshma_john@comcast.com", "raavan@gmail.com"],
    }

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 5)

people_df = pd.DataFrame(people)


# to update all column names
people_df.columns = ["first name", "last name", "email"]

print(people_df)

# revert column name update but don't do it for all columns
# This will return an error as entering all column names is a must
# people_df.columns = ["First", "Last"] # uncomment and run to check error
# print(people_df) # uncomment and run to check error


show_decoration(1)

# you can also use list comprehension to create a list and then assign to series
# objects for column name manipulations.
# the x.upper() will run for every value present in your series object.
people_df.columns = [x.upper() for x in people_df.columns]
print(people_df)

show_decoration(2)

# If column names contain spaces then it will be difficult to work with them
# when using . notations, eg: people_df.FIRST NAME.
# To avoid this replace all whitespaces in your column names using the str.replace()
people_df.columns = people_df.columns.str.replace(" ", "_")
print(people_df)

show_decoration(3)

# Another way to rename columns, inplace args is required here to make the change permanent
# supply a dict of old_value:new_value pairs as a dict to columns arg. For this
# method you don't have to supply every column name as well, you can safely omit
# key-value pairs of any column names that you don't wanna change, eg: Email column is
# omitted below.
people_df.rename(columns={"FIRST_NAME": "First", "LAST_NAME": "Last"}, inplace=True)
print(people_df)

show_decoration(4)

# Let's see how to update row values. Rows can be identified using their labels.
people_df.loc[1] = ["Niranjanadevi", "Senthilkumar", "niranjj@gmail.com"]
print(people_df)

show_decoration(5)

# We can also change specific column values alone on a row like so.
people_df.loc[1, ["Last", "EMAIL"]] = ["Chezhiyan", "niranj20@gmail.com"]
print(people_df.loc[1])

show_decoration(6)

# We can also use df.at[] instead of df.loc[] to fetch rows for manipulations.
# let's change the last name value of second row. No idea why this .at exists when
# .loc can also do the same. But good to know and we will stick to .loc for this project.
people_df.at[1, "Last"] = "Seshan"
print(people_df.loc[1])

show_decoration(7)

# Let's study Limitations of not using df.loc[filter, [columns]] and using df[filter][columns]
# let's create a filter to fetch rows with specific email
filt = (people_df["EMAIL"] == "niranj20@gmail.com")

# let's assign the last name value of this record to something else.
# This will error out. Uncomment to read the warning and follow the documentation.
# people_df[filt]["Last"] = "kniranj@amazon.com"
print(people_df[filt]["Last"]) # check notes

# Let's properly manipulate this time using .loc[]
people_df.loc[filt, "Last"] = "kniranj@amazon.com"
print(people_df[filt]["Last"])

show_decoration(8)




# Notes:
# 1. df.columns will return a series object. Any assignments you do it should
#    also be a list of equal length.
# 2. Note accessing columns using dot notation like people_df.FIRST NAME is generally
#    ill-advised especially when column names contain spaces as it will lead to error
#    and also your column name might also be a python inbuilt keyword. So stick to
#    accessing columns like this: people_df["FIRST NAME"].
# 3. Using df[filter][column_name] is a legit syntax to access column values, that's
#    why the print() statement in line 85 gives a neat output. But it runs into errors
#    when we uncomment line 84. Because this line is trying to assign a value instead
#    of just accessing. This is not supported since df[filter][column_name] returns a
#    copy of a slice. This is why we prefer using the df.loc[filter, column_name]
#    notation instead to manipulate values