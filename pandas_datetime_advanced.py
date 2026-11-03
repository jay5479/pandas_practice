import pandas as pd

# mandatory import to generate plots and charts
import matplotlib.pyplot as plt

from utils.string_ops import show_decoration


# load big data containing date-time series from csv with all date values
# converted to date-time objects and index set to date column
eth_df = pd.read_csv("ETH_1h.csv", parse_dates=["Date"],
                     date_format="%Y-%m-%d %I-%p", index_col="Date")

# Let's sort the index column for easy lookup & filtering. Also, a wise practice.
eth_df.sort_index(inplace=True)

# set max display values
pd.set_option('display.max_columns', 7)
pd.set_option('display.max_rows', 10)

# our df contains hourly OHLCV values of Ethereum crypto coin.
print(eth_df)

show_decoration(1)


# This module builds upon the datetime basics chapter.
# Let's say we want to get the average volume traded per week, then we would
# do something like so, note that we have to repeat this step for every date
# that we require and then once more repeat for every week.
print(eth_df.loc["2020-02-29", "Volume"].mean())

# And let's say we want to view the highs of each day, then first we would need
# to get all the 24-hour records for a specific day and run a max() on it and
# repeat the same process for every day that we require
print(eth_df.loc["2020-02-29", "High"].max())

show_decoration(2)

# The above process is tedious, so our initial plan would be to group our data
# by dates so that we can then run aggregation functions such as mean, max etc.
# But instead of that, Especially, when working with a timeseries data, we can
# use resample() method instead.
# Resampling is a technique in which any timeseries data can be zoomed in or
# zoomed out based on a DateOffset object.
# The resample method works on both df or series and takes a DateOffset
# frequency string: "D" in our case, as its arg. Check notes.
# Now we have resampled (grouped) our hourly "High" column data into daily data,
# this returns a DateTimeIndexResampler obj
print(eth_df["High"].resample("D"))

show_decoration(3)

# Now on our resampled data, we can simply run max() to view highs of each day.
print(eth_df["High"].resample("D").max())

show_decoration(4)

# Now we can simply save this resampler obj and then pull highs for specific dates
highs = eth_df["High"].resample("D").max()
print(highs["2018-03-31"])

show_decoration(5)

# We can also resample entire df like so and apply funcs.
# Here we apply min() to pull day wise minimum across all columns present in df.
# Note that min() method only works on numeric values other types are ignored.
print(eth_df.resample("D").min())

show_decoration(6)

# We can now also resample our Volume data week wise by using "W": Dateoffset
# frequency string as our arg and run mean() to fetch average volume traded per
# week data
print(eth_df["Volume"].resample("W").mean())

# let's also store this for future chart
avg_v = eth_df["Volume"].resample("W").mean()

show_decoration(7)

# Now averaging volume did not yield useful/sensible info. Because most
# traders or analysts will be looking for sum of volume traded in a week with
# minimum lows hit and maximum highs hit in that week along with average close
# values in a week. So let's try to give them all this using multiple aggregation
# and extract useful/sensible data.
# Check aggregation basics if you do not know multi-aggregation.
print(eth_df.resample("W").agg({"Close":"mean", "Low":"min", "High":"max", "Volume":"sum"}))


show_decoration(8)


# We can now also plot simple plots/chart using pandas' plot() on the resampler
# obj. You can see the output chart directly in this step if you're working on
# data science platforms like Jupyter Notebook, Spyder or Pycharm rich people's edition.
highs.plot()

# Once pandas plot is generated, we can now see it using the plt.show() from
# matplotlib. This will also open a pyplot display backend window to render
# your plot.
# You will see the output chart only here you're using regular IDEs like pycharm
# poor people edition or other similar IDE's like Sublime.
plt.show()

show_decoration(9)

# let's plot the average volumes too even though its nonsensical data.
avg_v.plot()
plt.show() # check notes.

show_decoration(10)




# Notes:
# 1. For geniuses familiar with audio codec, Think of resampling as analogous
#    to downsampling a 96Khz flac to a 44.1Khz mp3 or upsampling vice versa.
#    We are just upsampling or downsampling audio data from lower to higher
#    frequencies or vice versa respectively i.e, we are just sampling either
#    more bits per second if upsampling or fewer bits per second if downsampling.
# 2. Similarly, using resample(), we are either zooming in on more granular
#    levels of data like hourly basis from a larger set of data or zooming
#    out to see larger set of data like day-wise or month-wise data from a
#    more granular level of data.
# 3. A DateOffset object is a pandas inbuilt object that can be used when
#    working with timeseries data. Every DateOffset object defined in pandas has
#    an associated offset alias aka DateOffset frequency string which can be
#    used to access it.
# 4. You can read more about it here:
#    https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects
# 5. The frequency string tells pandas to which level we want to group or
#    zoom in/out of our timeseries data. you can find teh associated frequency
#    strings for each level of timeseries data in the table provided in the doc.
# 6. For our case, We want to zoom out from our hourly data to day wise data
#    to view highs of each day. So, we use the associated offset alias "D" as
#    our arg to the resample() method which is equivalent to grouping our data
#    by one calendar day"
# 7. Note that plt.show() pauses your python execution, you have to close the
#    pyplot GUI manually from UI so the execution can resume and move to next
#    block for seeing the next chart or execution completion.