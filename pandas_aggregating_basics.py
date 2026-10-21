import pandas as pd

from utils.string_ops import show_decoration


# load big data df from csv for big data.
results_df = pd.read_csv("survey_results_public.csv")

# set max display values
pd.set_option('display.max_columns', 5)
pd.set_option('display.max_rows', 10)


# Let's first create a Country group. Check notes #1.
country_group = results_df.groupby("Country")

# Let us now get the median ConvertedComp values by each group
print(country_group["ConvertedComp"].median())

show_decoration(1)

# Let us now learn aggregation by using the agg() method. Aggregation means
# applying multiple functions / methods on your groups and returning the
# combined/aggregated result.
# The agg() takes a list of functions that needs to be applied to your group
# as its args and returns the result by group.
# Let's apply the built-in mean and median methods on the ConvertedComp values
# grouped by Country. Note that list passed as arg contains the method names as
# str.
print(country_group["ConvertedComp"].agg(["mean", "median"]))

show_decoration(2)

# We can also fetch a record from a particular group after running agg()
print(country_group["ConvertedComp"].agg(["mean", "median"]).loc["Switzerland"])

show_decoration(3)

# Now let's try to answer how many people from each country know python.
# In doing so let's also learn how to apply custom functions on your group and
# aggregate results.
# But first let's learn how we can do this simply with filters that we studied previously
# Let's create a filter conditional / mask for one country first.
filt = (results_df["Country"] == "India")

# Let us now filter out by LanguageWorkedWith where Python is present. This will
# return a conditional/mask (Series obj with True/False values) again since
# we are asking it to check if the values in the filtered Series is containing
# a specific string i.e, "Python". Refresh filtering basics module if you don't
# understand this.
print(results_df.loc[filt, "LanguageWorkedWith"].str.contains("Python", na=False))

show_decoration(4)

# let's run the sum() method on the above. The sum method when ran on a conditional
# i.e, a series with bool types will consider all False values as 0 and True
# as 1 and will then sum it all up and give you the result.
# Now we know how many people from India know python.
print(results_df.loc[filt, "LanguageWorkedWith"].str.contains("Python", na=False).sum())

show_decoration(5)

# We can re-use the country filter conditional and by changing the Country value
# manually, we can answer the question for all remaining countries one by one.
# OR
# You can create a list of countries and run .isin(lst[countries]) on your
# filter conditional to display results by all countries.
# BUT
# we can do this far easily and with lesser code by simply running str.contains()
# on our country group's LanguageWorkedWith Series. Let's try it.
# comment out the code and run to see the error.
# print(country_group["LanguageWorkedWith"].str.contains("Python", na=False))

show_decoration(6)

# The code above this errored because str methods don't work on GroupBy obj.
# So instead, we will use the apply() method with a custom function that applies
# the str method directly on each value of our filtered series and then sum()
# up the values.
print(country_group["LanguageWorkedWith"].apply(lambda x: x.str.contains("Python", na=False).sum()))

show_decoration(7)

# Let us do another exercise. Let's now figure out how many percentage of people
# from each country who answered the Survey know python.

# let's figure out how many people responded to the survey from each country first.
# and store it to a variable.
country_resp = results_df["Country"].value_counts()

# let's now get how many people know python country wise and store it in a df.
country_uses_python = country_group["LanguageWorkedWith"].apply(lambda x: x.str.contains("Python", na=False).sum())

# now let's simply concatenate the group df with the Country value_counts series
custom_df = pd.concat([country_resp, country_uses_python], axis="columns")
print(custom_df)

show_decoration(8)

# now the custom_df shows all values needed for calculating percentages but the
# column headers are misleading. So let's rename it.
custom_df.rename(columns={"count": "Total Respondents", "LanguageWorkedWith":"Python Knowers"}, inplace=True)
print(custom_df)

show_decoration(9)

# now let's simply add a new column to our df that calculates percentages.
# pandas supports mathematical operations on numerical series, we leverage that.
# check notes
custom_df["prct of python knowers"] = (custom_df["Python Knowers"] / custom_df["Total Respondents"]) * 100
print(custom_df)

show_decoration(10)

# now we can pull this stat for any specific country easily by
print(custom_df.loc["Japan"])

show_decoration(11)


# Notes:
# 1. You must know grouping and filtering basics before you start to study this
#    module.
# 2. Aggregating results is a concept. That's what we learnt through the exercises
#    even if we didn't use the agg() method much in this module.
# 3. The grouping and aggregating modules teach how to explore and analyze datasets
#    using pandas.
# 4. In line 110, We just create a new series called prct of python knowers and
#    assign it to the resultant series values returned by the mathematical
#    operations. This results in a neat final result only because the groupby
#    obj returns data by no. of unique countries present in our survey and the
#    value_counts() method that ran on the Country series also returns data by
#    no. of unique countries present in our survey. Since it is a 1:1 mapping of
#    values across these objects, the multiplication of these values and
#    division by 100 to get the final percentages was accurate.
# 5. Keep caution of such operations and output when you're multiplying objects
#    that don't have such 1:1 mapping values.
# 6. You can also use the agg() method to run custom functions defined in your
#    module. Simply pass the name of the function to the list as str instead of
#    calling it. Read documentation or ask AI about the agg() method in pandas
#    to learn more nuances of its usage.