import pandas as pd

from utils.string_ops import show_decoration


# load big data df from csv for big data with respondent column as index column
results_df = pd.read_csv("survey_results_public.csv", index_col="Respondent")
# let's load the schema as well, indexed at Column
schema_df = pd.read_csv("survey_results_schema.csv", index_col="Column")

# set max display values
pd.set_option('display.max_columns', 5)
pd.set_option('display.max_rows', 10)

# Lets's learn median(). check notes first if you don't know what's median.
# When ran on entire df, it will return full df with the
# median values across applicable columns. median() is applicable only for columns with
# numerical data so passing the numeric_only=True arg is a must else ValueError.

print(results_df.median(numeric_only=True))

show_decoration(1)

# Median is far better when ran on a series in terms of output. No extra args required.
print(results_df['Age'].median())

show_decoration(2)

# Let's learn describe(). This method will return quick stats about your df.
# like mean, median, 20th percentile etc. Also note median == 50th percentile.
print(results_df.describe()) # check notes

show_decoration(3)

# let's learn count() on a numerical series. This returns the count of all values
# in a column. Note that it excludes blanks and NaN types and only counts remaining
# values.
print(results_df["ConvertedComp"].count())

show_decoration(4)

# Now let's re-learn value_counts(). It returns a series of distinct values in a
# column. Learn more about it on the pandas_slicing_and_counting_basics.py.
# Let's do a Q&A format, so you know what question you are answering by doing this.
# let's start with how we are answering first.
print(results_df["SocialMedia"].value_counts())

# Now let's find out what are we answering by the above. Check Notes.
print(schema_df.loc["SocialMedia", "QuestionText"])

show_decoration(5)

# The value_counts() also has a normalize= params which takes a bool arg.
# When set to True it will convert the value_counts to a percentage which helps
# us inspect how much percentage of the total responses were for a specific
# SocialMedia. Check notes.
print(results_df["SocialMedia"].value_counts(normalize=True))

show_decoration(6)

# Now let's study how to group various SocialMedia users according to their
# country. Let's first get the "Country" column, this step is optional and is
# just shown here to see the column in output for reference. Skip to next block.
print(results_df["Country"])

show_decoration(7)

# Now let's learn groupby(). This takes a column_name as its arg. It creates
# and returns a GroupBy obj which splits the data into groups based on the values
# from the supplied column/series. Any function you apply later to this obj is
# applied per group and is returned.
# Let's create a group by obj for the Country Series. This creates a group by
# obj which splits our df based on distinct values from the Country column and
# stores them in the obj, so that it can be used later to create specific country groups.
print(results_df.groupby("Country"))

# Just saving the GroupBy obj so we can use it later
country_group = results_df.groupby("Country")

show_decoration(8)

# Once we have the group by obj then we can easily access the split up data in
# the df by specifying which group of data we want to access using the
# get_group("group_values_required") method. This returns a smaller df
# containing records filtered by that particular value in the group.
# Syntax: GroupByobj.get_group("group_values_required")
# Let's see the records for the United States group from our df.
print(country_group.get_group("United States")) # check notes

show_decoration(9)

# We can also now apply functions to our group and see it applied to every group
# in our Series that we picked for grouping. After the function is applied, The
# results are combined and displayed.
# The following returns a df of distinct values for the SocialMedia Series
# grouped by Country. In other terms, value_counts() is applied to the SocialMedia
# column per country in group. We are basically answering how many people use
# which social media site the most per country.
print(country_group["SocialMedia"].value_counts())

show_decoration(10)

# We can also further pull results for specific groups instead of pulling for
# every group using the .loc["row_label"] notation where row_label is the group
# you want to access.
# Let's see which SocialMedia, the prevert and unhygienic nation uses the most.
print(country_group["SocialMedia"].value_counts().loc["India"])

show_decoration(11)

# Let's now see that in percentages
print(country_group["SocialMedia"].value_counts(normalize=True).loc["India"] * 100)

show_decoration(12)

# Let's just do the same exercise with a different column and a different
# function instead of value_counts now. This will give the median age of
# respondents per country and display the first 50 results.
print(country_group["Age"].median())

show_decoration(13)

# Let's pull the median age of respondents for Lithuania
print(country_group["Age"].median().loc["Lithuania"])

show_decoration(14)



# Notes:
# 1. A median value is simply the middle value of any numerical series. It is
#    simply the middle number of the series after it is sorted ascending. If
#    the series has odd no. of elements then it is the middle value after sorting
#    and if the series has even no. of elements it is just the average of the
#    middle two elements (m+n / 2).
# 2. A median is better than mean (average) in statistics because it is not
#    affect by outliers or sudden extreme values in the series which will otherwise
#    skew the mean of the series.
# 3. The e+04 in your data in the describe() df is equivalent to exponential of 4.
#    Meaning *10^4 mathematically.
# 4. The question we are trying to answer basically using the schema_df in this
#    module is how many respondents use which SocialMedia most. In simple terms
#    Group social media by no.of or count of respondents and give me the output.
# 5. The noramlize=True doesn't actually show a true percentage it just shows a
#    per-unit value i.e, count/100. You need to multiply it by 100 to get the
#    percentage value like so:
#    results_df["SocialMedia"].value_counts(normalize=True) * 100
# 6. The groupby() and get_group() work similar to filters that we learnt
#    previously. But the advantage of using groupby objects instead of filters
#    is that you don't have to write a filter every time for different values
#    across a series  for a particular value
#    to display your filtered data. You simply change the country name
#    on your conutry_group.value_count().loc["India"] line to access.
# 7. To do the above with filters. you have to do so:
#    filt = (results_df[Country] == "United States")
#    results_df.loc[filt, "SocialMedia"].value_counts()
# 8. The groupby() uses a split, apply and combine pattern. When we apply any
#    function like .count() or mean() to the group by obj then it is applied
#    per group and the results are combined and provided in a final df.