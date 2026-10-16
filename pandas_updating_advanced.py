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

# Let's learn about the apply() method. apply() works on both a df or a series.
# The apply() takes any python function as its arg. Note that we just have to
# pass the function as arg not call it. Here we use python's inbuilt len() function
# on a series. This applies the length function to all values in the series and
# returns the series.
print(people_df["Email"].apply(len))

show_decoration(1)

# The same can be applied to the entire df as well. But when applied to a dataframe
# it will apply the method only across rows and display the values by each column by
# default and return you the df with the length of each column (i.e, count of values in each column).
print(people_df.apply(len)) # check notes

show_decoration(2)

# if you want the method to be applied across columns and display values by each row
# instead use the axis="columns" arg.
# len will be applied column wise to all your rows and will return you the df
# with length of each row (i.e, count of all values in each row).
print(people_df.apply(len, axis="columns"))

show_decoration(3)

# We can also use the apply() with any custom functions as well
def update_email(email):
    return email.upper()

# applying to a series
print(people_df["Email"].apply(update_email)) # pass, don't call

show_decoration(4)

# The above operation is not applied to our df yet. It's just showing it.
# To apply, overwrite your series.
people_df["Email"] = people_df["Email"].apply(update_email)
print(people_df["Email"])

show_decoration(5)

# We can also use lambda functions for quick manipulations
people_df["Email"] = people_df["Email"].apply(lambda email: email.lower())
print(people_df["Email"])

show_decoration(6)

# let's learn about the pandas.series.min() method. This method will be applied
# on entire dataframe and will return a df with the minimum values from each series.
# check notes
print(people_df.apply(pd.Series.min)) # pass don't call, also pandas is imported as pd

show_decoration(7)

# now let's learn how to apply a function to each and every value of our df.
# this method is now deprecated, uncomment to see the error. We use map() instead.
# print(people_df.applymap(len))

# This is the latest method to do the above. This applies len() to each and
# every value present in our df and return the df.
print(people_df.map(len))

show_decoration(8)

# Let's learn the limitations of map() by applying a str method
# this works only because our df has all its value as str. if we have a different
# data type anywhere this will error out.
print(people_df.map(str.lower))

# let's create a sample df to demonstrate the above, uncomment below code block
# and run to see error. We need to create custom functions to handle different
# datatypes in such cases.

# sample_data = {
#     "First": ["Adhi", "Jeeshma"],
#     "Age":[34, 30]
# }
#
# sample_df = pd.DataFrame(sample_data)
#
# print(sample_df.map(str.lower))

show_decoration(9)

# map() can also be used to substitute values within a Series, syntax is as follows
# df[column_name].map({old_val_1: new_val_1, old_val_2: new_val_2, ...old_val_n: new_val_n})
# The below output will have Nan types, ignore and move to next block.
print(people_df["First"].map({"Kanushi": "Indu", "Adhi": "Jeeshma"}))


show_decoration(10)

# Notice that in the previous output we have any value from our series that we
# didn't substitute in the "First" series is converted to a NaN type. This is
# not helpful as sometimes we want to retain values unchanged. That's when we
# use the replace() instead of map. It has similar substitution syntax.
print(people_df["First"].replace({"Kanushi": "Indu", "Adhi": "Jeeshma"}))

show_decoration(11)

# doing the same as above but also saving changes to original series, check notes
people_df["First"] = people_df["First"].replace({"Kanushi": "Indu", "Adhi": "Jeeshma"})

print(people_df)

show_decoration(12)

# let's demonstrate few examples we learnt in this module and updating_basics on
# big data.
results_df = pd.read_csv("survey_results_public.csv")

# set max display values
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 8)

# let's rename a column
results_df.rename(columns={"ConvertedComp": "SalaryInUSD"}, inplace=True)

# let's change yes or no :str responses to True or False :bool values in the
# Hobbyist column
# You will see the output but will also get a warning as pandas is planning to
# stop downcasting (replacing str with bool) behaviour in replace(). So we
# have to use the .infer_object(copy=False) also additionally as per their documentation.
results_df["Hobbyist"] = results_df["Hobbyist"].replace({"Yes": True, "No": False}).infer_objects(copy=False)

print(results_df)

show_decoration(13)



# Notes:
# 1. The code in line 30 is same as len(people_df). Just another way to do it.
# 2. Note that the apply() method, when we're applying it over a df, always
#    applies our function either on rows or columns depending on how we want it.
#    The len() is not applied to each and every value from our df because if it
#    did then it will give us the length of each str value in our df. This is
#    why we use map() instead.
# 3. Note that in line 67, our df only contain str values. When using min() on
#    a series of strings, it will always sort the series alphabetically first
#    and return the first value in the series. This is not equivalent to the
#    behaviour of the min() method that we learn in maths. So use the
#    pd.Series.min cautiously and restrict to running it on numerical data types
#    like int or float etc. instead so that this method behaves as it should
#    like in maths. This is python's in built min() method's behaviour and has
#    nothing to do with pandas as pandas simply leverages it.
# 4. Do note that some lines of code (like line 67, 77, 84 etc) in this module
#    are not permanently updating our original df. To do that assign the
#    operation back to your df or series (like in line 53) with which you're
#    doing that specific operation to see the changes reflected in your
#    original df. We are purposefully avoiding doing it so that we can maintain
#    the original df to demo other methods we are learning down the line like
#    map, replace etc.