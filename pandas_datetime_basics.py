import pandas as pd

from utils.string_ops import show_decoration


# load big data containing date-time series from csv for big timeseries data.
eth_df = pd.read_csv("ETH_1h.csv")

# set max display values
pd.set_option('display.max_columns', 7)
pd.set_option('display.max_rows', 10)

# our df contains hourly OHLCV values of Ethereum crypto coin.
print(eth_df)

show_decoration(1)

# Now let's learn day_name() method which only works on datetime objects.
# The day_name() method will return the respective date's day name eg: Tuesday.
# But this doesn't work here because even though the date values in our
# dataframe appear to be neatly formatted as datetime obj, it is actually a str
# representation of it. That's why we get the AttributeError.
# Comment out and run the below line to see it.
# print(eth_df.loc[0, "Date"].day_name())

show_decoration(2)

# So let's check out the dtypes our Series is holding. It must be obj as str is
# considered by default as obj. Refer casting basics if you do not understand this.
print(eth_df["Date"].dtypes)

# Now let's convert the str value Date series to proper datetime objects.
# We do this by using pandas inbuilt to_datetime() method and supplying our
# series with date-times as its argument.
# This will lead to another error so comment out and run.
# eth_df["Date"] = pd.to_datetime(eth_df["Date"])

show_decoration(3)

# The error occurred because when we run the pd.to_datetime() without any
# formatting args, pandas will try to figure out the formatting of the date
# values automatically and try to convert. But this doesn't work for date
# values that are going to be in weird formats with -AM -PM etc. like in our
# dataset. So we supply the format args with a "date-time format string" which
# tells python/pandas how the date-time values are formatted in our dataframe
# so that it can convert the values accurately instead of guessing it. Check notes.
eth_df["Date"] = pd.to_datetime(eth_df["Date"], format="%Y-%m-%d %I-%p")

# Now that our Date values are converted to datetime objects, let's see
# how it looks now
print(eth_df["Date"])

# and let's also check its dtypes now.
# Now it holds datetime64[ns] objects. Where 64[ns] means 64-bit integer
# encoded date and time data and ns means nanosecond precision. Eg: 2262-04-11 23:47:16.854775807
# The nanoseconds part is ignored in output since that data is not originally
# available in our str representation before conversion.
print(eth_df["Date"].dtypes)

show_decoration(4)

# Now let's run the day_name() that we learnt.
print(eth_df.loc[0, "Date"].day_name())

show_decoration(5)

# We can handle all datetime values from multiple columns in our df at the csv 
# parsing stage itself by using:
# 1. A parse_dates params on the pd.read_csv() method which takes a list of 
#    Series' that you want to be converted into datetime objects as its arg 
#    
#    AND

# 2. A date_format params which will take a date-time format string that tells
#    pandas how date-time values in our dataset are structured/formatted as.

# We are re-reading our csv again to demonstrate the above and are creating a
# new eth_df_2 to distinguish from our previous eth_df.
eth_df_2 = pd.read_csv("ETH_1h.csv", parse_dates=["Date"], date_format="%Y-%m-%d %I-%p")

# Now you can see all the Date series values converted to datetime dtypes in this df
print(eth_df_2)

show_decoration(6)

# Note that day_name() only works for specific values in our df that are
# date-time objects and doesn't work on str objects as seen at the start of
# this module or on entire series since Series are series objects.
# If we want it applied to entire series we must follow this syntax after
# converting our date values in the series to date-time object (which is
# already handled at the parsing stage itself for eth_df_2):
# df["Series_Name"].dt.day_name()
# The .dt tells day_name() that it is actually working with already converted
# date-time objects and not str dtypes or Series objects
print(eth_df_2["Date"].dt.day_name())

show_decoration(7)

# Now let's add the day names as a new series to our df. This helps us quickly
# see trading details by day of the week if needed.
eth_df_2["DayOfWeek"] = eth_df_2["Date"].dt.day_name()
print(eth_df_2)

show_decoration(8)

# Once date values are converted to date-time obj, we can do a lot of exploratory
# analysis on our dataset like so.
print(eth_df_2["Date"].min()) # To find the date of earliest/oldest record in our df
print(eth_df_2["Date"].max()) # To find the date of last/most recent record in our df

show_decoration(9)

# This is called a time delta meaning time difference or duration or date range of our dataset
print(eth_df_2["Date"].max() - eth_df_2["Date"].min())

show_decoration(10)

# We can now also filter our data simply by using regular date strings like so
filt = (eth_df_2["Date"] >= "2020") # note we only supply year and it works
print(eth_df_2.loc[filt])

show_decoration(11)

# More filtering.
# Let's extract all records from 28 February 2019 (inclusive) upto 2020 (exclusive)
# note we supply full date here on one conditional and just the year on another
# conditional and this also still works!
filt = (eth_df_2["Date"] >= "28-02-2019") & (eth_df_2["Date"] < "2020")

print(eth_df_2.loc[filt])

show_decoration(12)

# Another way to filter directly using date-time obj instead of str dates
# Let's extract only 2017 July records
filt = (eth_df_2["Date"] >= pd.to_datetime("2017-07-01"))  & (eth_df_2["Date"] < pd.to_datetime("2017-08-01"))
print(eth_df_2.loc[filt])

show_decoration(13)

# The best part about date-time objects is we can use it as index for our df,
# This helps us filter records far easily than using complicated filter conditionals
eth_df_2.set_index("Date", inplace=True)

# let's also sort the index, so slicing works cleanly later
# This is also a best practice, check indexing basics notes
eth_df_2.sort_index(inplace=True)

# Now let's say we want only 2018 data, then we simply do
print(eth_df_2.loc["2018"])

show_decoration(14)

# And say we want data only for specific dates or months, we can simply do slicing
# Note slicing only works if your index is already sorted, else KeyError
print(eth_df_2.loc["01-2020":"02-2020"])

show_decoration(15)




# Notes:
# 1. OHLCV stands for open, high, low, close and volume data of a particular
#    stock or capital market instrument. Google or ask AI and learn about basics
#    of interpreting a candlestick trading chart if you do not know what this is.
# 2. We use this dataset for this module to learn datetime manipulations using
#    pandas. Our usual developer survey results doesn't have datetime data to
#    work with.
# 3. Formatting codes are used to tell python how our date time string is
#    formatted as, and you can find format codes for various date & time
#    parameters such as year, month etc. in the python documentation here:
#    https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
# 4. Parse the date time string in your dataframe yourself, understand which
#    format codes are needed for which element and then create your date-time
#    format string accordingly. -, _ or similar symbols and whitespaces should
#    be carried as it is as they do not have any format codes.
# 5. For the date values present in our ethereum dataset, the date-time format
#    string is built as: "%Y-%m-%d %I-%p". You can validate this with the
#    documentation link to understand how it is constructed.
# 6. Note that most of the methods and operations that we learn in this module
#    only work after you have converted your date values in your df to proper
#    date-time objects. That is the whole point of this chapter: Handle and
#    clean date-time values in your data to date-time objects so it can be
#    manipulated.