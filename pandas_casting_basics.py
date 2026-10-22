import pandas as pd
import numpy as np

from utils.string_ops import show_decoration

# load a demo df for studies, Note that it contains numpy NaN types, None: bool
# values, NA as str, Missing as str and also age values as str instead of int.
# We will be studying how to clean up all such types.
people = {
    "First":["Kanushi", "Adhi", "Jeeshma", "Raavan", np.nan, None, "NA"],
    "Last":["Gopi", "Seshan", "Seshan", "Krishnan", np.nan, np.nan, "Missing"],
    "Email":[
        "kanushi_g@gmail.com", "adhi_seshan@comcast.com",
        "jeeshma_john@comcast.com", None, np.nan, "Anonymous@email.com", "NA" ],
    "Age":["6", "34", "30", "4", None, np.nan, "Missing"]
    }

people_df = pd.DataFrame(people)

# This line is a required line to suppress downcasting related warning when doing
# replace() in this module. Comment out this line and run to see the warning.
# Read the pandas docs to understand more about it. We just handle this warning
# differently in the pandas_updating_advanced.py module.
# This is just yet another way to handle it.
pd.set_option("future.no_silent_downcasting", True)


# check this output to understand what's np.nan and how it is represented in df
print(people_df)

show_decoration(1)

# To check what data types (dtypes) our df is holding, We can access the .dytpes
# attribute of our df. Note the output says our Age series holds the dtype: objects.
# This is because by default, str type is treated as an obj.
# Only literals like int or bool or None are not objects in python.
# Also, our Age series not only contains str but also bool types. If multiple
# dtypes are mixed in a series then our output will report the dtype as obj.
print(people_df.dtypes)

show_decoration(2)

# However, if our series contains all its values as a single literal dtype then
# the output will report it as that particular dtype.
# The dtype of our entire df will always be an obj. The series dtypes can
# however vary depending on its contents.
# You can see both of it in the output of below code block.
some_data = {"randos":[1, 2, 3, 10, 12]}
some_df = pd.DataFrame(some_data)
print(some_df.dtypes)

show_decoration(3)

# Let's learn how to cast datatypes (aka dtypes) into other dtypes.
# Our people_df has age values as str when ideally it'd be more useful as
# an int type instead for computational purposes. Eg: to run the mean() method
# on it since this method will only work on numerical dtypes else TypeError.
# To do this we will use the astype() method. Note that this method will work
# on entire df as well if all the values in your df are homogeneous.

# Uncomment and run this code to see the error
# people_df["Age"].astype(int)

show_decoration(4)

# We get a TypeError in the previous code block because our age series is trying
# to convert NaNs and None's and "Missing" strings to int.
# To avoid this let's clean up our data first and replace Nones and str to NaNs.
people_df["Age"] = people_df["Age"].replace({None: np.nan, "Missing": np.nan})


# Now instead of casting the Age values to int. We will simply cast them into
# float type instead and save it to our series. Why? Because NaN under the hood
# is just float and it can't be cast to int else TypeError.
# Check the notes on cleaning_basics.py, if you don't understand why NaN is a float.
# Now while casting, all the NaNs will be retained as it is since they're already
# floats and all the str age values in the column is cast to float type.
# Now our age series is computation ready since we don't always need only int
# to do calculations.
people_df["Age"] = people_df["Age"].astype(float)
print(people_df["Age"])

show_decoration(5)

# And finally
print(people_df["Age"].mean())

show_decoration(6)