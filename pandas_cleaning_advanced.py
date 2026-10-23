import pandas as pd
import numpy as np

from utils.string_ops import show_decoration


# load big data df from csv for big data.
# We can replace custom values like str NAs and str Missing with NaN type
# at the csv parsing stage itself using the na_values params which takes a list
# of values that you want to convert to NaN types.
na_vals_list = ["Na", "Missing", "Not sure"]

results_df = pd.read_csv("survey_results_public.csv", na_values=na_vals_list)

# set max display values
pd.set_option('display.max_columns', 5)
pd.set_option('display.max_rows', 10)

# remove downcasting warnings
pd.set_option("future.no_silent_downcasting", True)

print(results_df)

show_decoration(1)

# In this module we will be doing an exercise where we will apply all the
# concepts learnt so far from the cleaning and casting basics modules.
# Let's start with exploring the question for the YearsCode column.
schema_df = pd.read_csv("survey_results_schema.csv", index_col="Column")
print(schema_df.loc["YearsCode", "QuestionText"])

show_decoration(2)

# Let's say we want to look at our YearsCode series to get a hint about our data.
# We can see we already have missing data handled neatly with some NaN types but
# the years of coding value is str type and not an int or float.
print(results_df["YearsCode"].head(10))

# so let's go ahead and calculate the average years coded for all who responded.
# uncomment below code and run to see the error.
# print(results_df["YearsCode"].mean())

show_decoration(3)

# We can see from the previous error that there are few unexpected str types as
# well in our column like "Less than one year" etc. So let's first identify all
# distinct values in the column using either the value_counts() or unique() method.
# Both of the above methods will fetch distinct values from a series but here I
# prefer unique() for this use case as the output does not get truncated since
# value_counts() method prints the occurrences count as well.
print(results_df["YearsCode"].unique())

show_decoration(4)

# We can now see that we have two text/str type outliers in our data that cannot
# be safely cast to int or type i.e, "Less than 1 year" & "More than 50 years" values.
# Let's replace those to numeric types so we can cast it to float later.
# We will replace "Less than 1 year" to 0 as it wouldn't skew our average later.
results_df["YearsCode"] = results_df["YearsCode"].replace({"Less than 1 year": 0})

# We will also replace "More than 50 years" to NaN since nobody codes for that
# many years, and it could be very well be a lie that skews our metrics.
# We are just assuming this value as a lie for the sake of this exercise and
# is not actually a fact since these days there are polyglot coders who start
# very young.
results_df["YearsCode"] = results_df["YearsCode"].replace({"More than 50 years": np.nan})

# verify changes are present
print(results_df["YearsCode"].unique())

show_decoration(5)

# now let's cast the entire series as float and get our average
# Not casting as int so that NaN types remain handled. Go through casting basics
# if you don't understand this.
results_df["YearsCode"] = results_df["YearsCode"].astype(float)

print(results_df["YearsCode"].mean())

show_decoration(6)



# Notes:
# 1. Note that while casting to float or int any str types that are just numbers
#    get easily cast to float or int types unlike str that contain
#    character (alphabet and symbol) literals.
# 2. This is because in python, int("4") or int("56.75") will get converted to
#    integers because they're byte-code like data types but int("Four") or
#    int("lorem ipsum") can never be converted to integers as they're non byte-code
#    like data types.