import pandas as pd

from utils.string_ops import show_decoration


# load a demo df for studies
people = {
    "First":["Kanushi", "Adhi", "Niranjanadevi", "Raavan"],
    "Last":["Gopi", "Seshan", "Chezhiyan", "Krishnan"],
    "Email":["kanushi_g@gmail.com", "adhi_seshan@comcast.com", "jeeshma_john@comcast.com", "raavan@gmail.com"],
    }

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 5)

people_df = pd.DataFrame(people)

# To add a new column to your df, do this
# Note that the values to add to this column must always be equal to the total
# no. of records/rows present in your df. Else it will throw a ValueError.
people_df["Age"] = [6, 34, 32, 4] # check notes
print(people_df)

show_decoration(1)

# similarly to add a new row to you df do this with the same rules
people_df.loc[4] = ["Tanu", "Kunihal", "tanu_kunihal@gmail.com", 32]
print(people_df)

show_decoration(2)

# if you want to create a new column by combining data from different columns,
# you can use string concatenation if your columns contain str values.
people_df["Full_Name"] = people_df["First"] + " " + people_df["Last"] # check notes
print(people_df)

show_decoration(3)

# To drop columns from our df
people_df.drop(columns=["First", "Last"], inplace=True) # check notes
print(people_df)

show_decoration(4)

# We can also use a str.split() on Full Name Column to split the Full name
# column back into First and Last name columns. Note this only works on Series
# with str values.
# The below operation creates a new First and Last series in our df and assigns
# the split Full Name values to the new columns. The split() even though without
# any arg will split strings based on whitespace and return a list of strings,
# We still just pass " " as an arg anyways to enforce whitespace split.
# The expand=True arg ensures that the split up values in the list returned by the
# split() method are correctly unpacked and mapped to the columns. check notes.
people_df[["First", "Last"]] = people_df["Full_Name"].str.split(" ", expand=True)
print(people_df)

show_decoration(5)

# Another way to add a new row to our df is to use the _append(). This method
# will not error out even if you omit certain column values unlike the method
# studied previously to add new rows. The omitted column values will be filled
# with the NaN type. The method takes a dict of column_name:new_value as its
# args. check notes.
people_df = people_df._append({"Full_Name": "Jeeshma John", "Email": "kniranj@amazon.com"}, ignore_index=True)
print(people_df)

show_decoration(6)

# We can also append entire dataframes to existing frames as long as the no.of
# columns and its key (i.e, column_names) match. Else ValueError.
# Your new df that is to be appended can have the column names in any order as
# long as the keys match.
# Let's create another sample df that has the same columns as people_df but in
# different order than people_df, to demonstrate this first.
extra_folks = {
    "Last":["Rawat", "Rakesh"],
    "First":["Rajnee", "Gia"],
    "Email":["rajnee@gmail.com", "gia@gmail.com"],
    "Age":[35, 6],
    "Full_Name":["Rajnee Rawat", "Gia Rakesh"]
}

df_2 = pd.DataFrame(extra_folks)

# append your new df to existing df and save it to existing df
people_df = people_df._append(df_2)

# note that the new df gets appended and starts with index/row label at 0 again.
# don't know what to do about it, might learn later.
print(people_df)

show_decoration(7)

# to drop rows from our df,
# follow this syntax: .drop(index= row_index :int | row_indices :list, inplace= True :bool)
# We can drop a single row if we pass an int arg to index params or multiple rows
# if we pass a list of int as arg.
# Note that this operation removes all rows with 0 & 1 as their indices/row labels.
# our df has 4 such rows.
people_df.drop(index=[0, 1], inplace=True)
print(people_df)

# reverting the above change to demonstrate next concept


show_decoration(8)

# We can also drop rows based on masks that we learnt from filtering module.
# This way of dropping is only applicable to rows and not columns.
# let's create a conditional / mask to remove all rows where Age is 32.
filt = (people_df["Age"] == 32) # check notes

# The .index attribute returns the indices/row_labels of all records that has
# matched our conditional for the Age column.
people_df.drop(index=people_df[filt].index, inplace=True)
print(people_df)

show_decoration(9)





# Notes:
# 1. In line 21, ensure you are always adding a column or row using df["column_name"]
#    or df["row_name"] notations and not the df.column_name or df.row_name notations
#    because while assigning our value list to the dot notation, python will think we
#    are actually assigning to the column/row object instead of the actual Series.
# 2. Line 34, deliberately concatenates a " " whitespace character so the full
#    name can be neat to read. else there will be no space between first and
#    last name
# 3. In line 40, we are using the inplace args as seen in previous modules to commit
#    the dropped series' to our df permanently. This will no longer be explained from
#    this chapter. inplace=True means permanent change to df inplace=False means give
#    me a temporary copy of the df with the applied operation.
# 4. In line 54, if our column to split contains values with multiple whitespaces
#    i.e, if any value in the column, when split gives us 3 or more words then
#    mapping the words to 2 columns is not possible, and you will get a ValueError.
# 5. The append() method to add rows is planned to be deprecated in future
#    hence as of today it has been converted to a protected method which is accessed
#    by the _ notation. The ignore_index=True arg is a must, if not then pandas
#    will throw a TypeError and say we can't append a dict unless we ignore
#    the index. Also note that the int age values in your df converts to float
#    the moment a NaN type enters your df. Read about it separately.
# 6. Brush up on your filtering basics if you aren't understanding what we are
#    doing in line 111 & 115.