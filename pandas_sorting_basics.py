import pandas as pd
from utils.string_ops import show_decoration


# load a demo df for studies
people = {
    "First":["Kanushi", "Adhi", "Jeeshma", "Janani"],
    "Last":["Gopi", "Seshan", "Seshan", "Seshan"],
    "Age": [6, 34, 30, 35],
    "Email":["kanushi_g@gmail.com", "adhi_seshan@comcast.com", "jeeshma_john@comcast.com", "kaminil@gmail.com"],
    }

people_df = pd.DataFrame(people)

# load one more df from csv for big data with respondent column as index column
results_df = pd.read_csv("survey_results_public.csv", index_col="Respondent")

# set max display values
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)

# let's sort our people_df by last name,
# syntax: df.sort_values(by="column_name"), inplace=True)
people_df.sort_values(by="Last", inplace=True)
print(people_df)

show_decoration(1)

# now let's sort our df by last name but in descending order
people_df.sort_values(by="Last", ascending=False, inplace=True)
print(people_df)

show_decoration(2)

# now to sort multiple columns, pass column_names as a list to by params.
# this will apply the sorting first to the left most column value in our list
# and will then move to columns in right until end of list.
people_df.sort_values(by=["Last", "First"], ascending=False, inplace=True)
print(people_df)

show_decoration(3)

# now to sort multiple columns but each column in a different order, just pass
# a list of bool values as args to the ascending= params. The sorting will be
# applied in a 1:1 mapping from left with your column values list passed to
# the by= params
people_df.sort_values(by=["Last", "First"], ascending=[False, True], inplace=True)
print(people_df)

show_decoration(3)

# If you want to undo all sorts, you can sort by index using sort_index() that
# we studied previously in the indexing module.
people_df.sort_index(inplace=True) # check notes
print(people_df)

show_decoration(4)

# you can also sort series objects and view them.
print(people_df["Age"].sort_values())

# But you cannot apply/insert the sorted series to your df.
# why is it so? Think about it.
# Uncomment the below lines and see to understand the logic error.
# people_df["Age"] = people_df["Age"].sort_values()
# print(people_df)

show_decoration(5)

# let's do some big data sorting, let's sort our df by Country
results_df.sort_values(by="Country", inplace=True)

# just fetching the Country column alone for the first 50 records to not clutter
# output with large data. Note that .head(n) works for Series objs as well and not
# just for dfs.
print(results_df["Country"].head(50))

show_decoration(6)

# let's fetch all salaries sorted by country in ascending and sorted by salary
# in descending, This will help us see the maximum salary offered per country
# easily as we are sorting the salary column in descending i.e, largest value first
results_df.sort_values(by=["Country", "ConvertedComp"], ascending=[True, False], inplace=True)
print(results_df[["Country", "ConvertedComp"]].head(50))

show_decoration(7)

# Instead of going through all this to see highest salaries, we can use the
# below method which gives us the first five largest salary in the series.
print(results_df["ConvertedComp"].nlargest())

show_decoration(8)

# We can also nlargest(n :int) to fetch n number of largest salaries in the
# series.
print(results_df["ConvertedComp"].nlargest(10))

show_decoration(9)

# We can also run nlargest() on entire df, but we have to tell the method to which
# column it should be applied. syntax: df.nlargest(n :int, column_name :str)
print(results_df.nlargest(10, "ConvertedComp")) # check notes

show_decoration(10)

# We can do all the above operations with same syntax for nsmallest(n) method
# as well, which will fetch us the smallest values for n records
print(results_df["ConvertedComp"].nsmallest(10))

show_decoration(11)

# load entire df sorted by smallest 10 salaries
print(results_df.nsmallest(10, "ConvertedComp"))

show_decoration(12)



# Notes:
# 1. If you want to undo all your sorts using the sort_index() then you need to
#    ensure that the default row labels (i.e, the int values) are intact for the
#    sorting to work.
# 2. If you have set a different column as index to your df then you need to use
#    the reset_index() learnt in indexing module on your df first and remove the
#    custom indexing so that you df reverts to default row labels and then you
#    run the sort_index() again to revert to your original df.
# 3. You cannot sort a series alone and try to expect it to be applied/inserted
#    to your df because, inserting a sorted series into your df will mess up original
#    order of your df. You can simply do sort_values(by='column_name') on your
#    df instead which does the same thing.
# 4. You cannot see the ConvertedComp values in your output because pycharm
#    truncates the columns because of large no. of columns and we have also set
#    max_columns=10 at the beginning of this module.
# 5. To verify if the output is only loading the records for nsmallest or
#    nlargest, crosscheck the index (Respondent) values against the series output
#    from previous output and verify.