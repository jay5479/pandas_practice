import pandas as pd
# mandatory import to work with numpy NaN types
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
    "Age":["6", "34", "30", "4", None, None, "Missing"]
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
# check output to understand how NaN even if it is Not a number is actually a
# float type. See notes for further details.
print(type(np.nan))

show_decoration(1)

# Now let's learn how to drop na types using dropna(). This method will drop all
# records that contain even a single NaN or None types. Note that it cannot however
# drop "NA" & "Missing" because they are actually str types and not true NoneType or NaN.

print(people_df.dropna()) # check notes

show_decoration(2)

# Let's learn more about the dropna(). It takes two args optionally viz,
# axis= and how= . If no arg is supplied then the values for these params
# are defaulted to "index" (meaning rows) and "any" (meaning any na values)
# respectively. The below line of code will do the same thing as a simple
# dropna() without any args as seen previously
print(people_df.dropna(axis="index", how="any"))

show_decoration(3)

# To drop records only if all values in it contain na types then pass the 'all'
# as arg to the how params. You can now see the 4th row label record alone is gone
# from people_df because it had all its values as na types but at the same time
# 5th and 6th row label records are retained in our df despite them having na types.
# This is because they did not match the 'all' criteria.
print(people_df.dropna(axis="index", how="all"))

show_decoration(4)

# We can also drop columns/series from our df by setting the axis arg to 'columns'
# Set how arg to 'any' if you want columns to be dropped when they have even a
# single na type value.
# Below will return empty df as pretty much every series in our people_df has
# at least one na type
print(people_df.dropna(axis="columns", how="any"))

show_decoration(5)

# Similarly set how arg to 'all' if you want your columns to be dropped
# only if it contains all its values as na types.
# Below will return people_df as it is since there are no series in our people_df
# that have all its values as na types.
print(people_df.dropna(axis="columns", how="all"))

show_decoration(6)

# Now let's drop records that have na types but only in specific columns.
# When we supply 'all' to the how params while doing this operation, then
# only those records will be dropped that have na types across all the columns
# that we supplied as a list to the subset params.
# Here only the 4th row label record is dropped as it is the only record in
# people_df that has na types for both Last and Email columns. Rest are retained.
print(people_df.dropna(axis="index", how="all", subset=["Last", "Email"]))

show_decoration(7)

# Similarly, When we supply 'any' to the how params while doing the same
# operation, then only those records will be dropped that which have at least
# a single na type value across even any one of the column from our columns list
# that we supplied to the subset params.
# Here pretty much records with 3, 4, 5 & 6 row labels are dropped since they have
# na type value at least in one of the Last or Email columns or both.
print(people_df.dropna(axis="index", how="any", subset=["Last", "Email"]))

show_decoration(8)

# Now let's handle the str NA and missing values. We can use the str replace()
# we learnt previously from updating_advanced.py.
# This method works on entire df as well.
people_df.replace({"NA": np.nan, "Missing": np.nan}, inplace=True)
print(people_df)

show_decoration(9)

# Sometimes we just want to know how much of our df or series has true na types.
# To do that we simply use the isna() conditional. This will return us a mask
# (bool obj) where True equates to values that are a na type in your df or series
# or False which mean that those values are not a true na type.
# The mask can later be used as filters to clean the na types.
# Learn filtering basics before this if you do not understand.
print(people_df.isna())

show_decoration(10)

# Now once we know which are all the na type values, we can replace/fill them
# in a single go by using the fillna() method. check notes
# Syntax: DataFrame | Series.fillna(value_to_be_replaced_with :obj, inplace= True | False :bool)
print(people_df.fillna("MISSING"))

show_decoration(11)

# Sometimes when working with numerical data such as "Age", it is better to
# replace the na types with 0 :int instead, since replacing it with a str or
# any other obj will bring in complications when we want to do mathematical
# computations.
# The previous .fillna() operation before this block is not saving any changes to
# original people_df because we did not supply the inplace=True arg. So you
# will not be seeing the "MISSING" values in the output of this code block as
# those values are all still na types as per our unchanged people_df which will
# now be replaced with 0.
print(people_df["Age"].fillna(0))

show_decoration(12)




# Notes:
# 1. In Python and NumPy, np.nan is a float because it follows the IEEE 754
#    Standard for Floating-Point Arithmetic.
# 2. Key Side Effects of NaN being a Float:
#    • It never equals itself: Following the IEEE standard, np.nan == np.nan
#      evaluates to False. You must use np.isnan() or math.isnan() to check for it.
#    • Contamination: Any mathematical operation involving a NaN results in NaN
#      (e.g., 5 + np.nan becomes np.nan).
# 3. To save the df after doing any dropna() or fillna() or replace() operations
#    in this module, supply the inplace=True arg. Most of the code shown in this
#    module will not be making a permanent change to people_df just for the sake
#    of convenience for demonstrating subsequent concepts without having to
#    modify the original people_df.
# 4. You would sometimes want to replace the na types on your data with "Missing"
#    or similar phrases on use cases such as when you are working with data of
#    customers who had paid their bill before due date vs yet to pay. It's wiser
#    to report such data as "Yet to be paid" or "Unsettled" instead of na as doing any
#    numerical operation on a na type later will skew your results for analysis.