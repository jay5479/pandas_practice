import pandas as pd

from utils.string_ops import show_decoration


# load a demo df for studies
people = {
    "First":["Kanushi", "Adhi", "Jeeshma", "Raavan"],
    "Last":["Gopi", "Seshan", "Seshan", "Krishnan"],
    "Email":["kanushi_g@gmail.com", "adhi_seshan@comcast.com", "jeeshma_john@comcast.com", "raavan@gmail.com"],
    }

people_df = pd.DataFrame(people)

# This is called a conditional, returns a series object with Bool values
# For whichever values in the column satisfy the conditional, the value is returned
# as true
print(people_df["Last"] == "Seshan")

show_decoration(1)

# We can use conditionals to create filters and then apply it to our df to view
# our data. This is called a mask.
filter_conditional = (people_df["Last"] == "Seshan")

# This will return all records that match the filter's condition
print(people_df[filter_conditional])

show_decoration(2)

# We can also use conditionals to fetch specific column values alone that match
# our filter like below.
print(people_df.loc[filter_conditional, "Email"])

show_decoration(3)

# We can also do the same for fetching multiple values across different columns
# that match our filter like below. Note that you columns has to be passed as a list.

print(people_df.loc[filter_conditional, ["Email", "Last"]])

show_decoration(4)

# We can also negate the conditional and fetch all remaining values that do not
# satisfy our filter like below. Notice the "~" (tilde) before filter, it is syntax.

print(people_df.loc[~filter_conditional, ["Email", "Last"]])

show_decoration(5)

# We can also combine multiple conditionals and create a filter using the
# & (and) and | (or) operators
combine_filter = ((people_df["Last"] == "Seshan") & (people_df["Email"] == "jeeshma_john@comcast.com"))

# below will list the first name's alone for records whose last name value is Seshan
# and email is jeeshma_john@comcast.com
print(people_df.loc[combine_filter, "First"])

show_decoration(6)

# example using or
combine_filter = ((people_df["Last"] == "Gopi") | (people_df["Last"] == "Krishnan"))


# list First and last names of all whose last name is either Gopi OR Krishnan
print(people_df.loc[combine_filter, ["First", "Last"]])

show_decoration(7)

# let's load a df to work with big data and also use what we learnt above.
results_df = pd.read_csv("survey_results_public.csv")

# set max display values
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 50)

# Let us create a filter to view all languages that are paid more than 70000 USD
# as their compensation and also get their country.
# The ConvertedComp column holds their USD converted annual salary.

creamy_filter = (results_df["ConvertedComp"] > 70000)

print(results_df.loc[creamy_filter, ["Respondent", "Country", "LanguageWorkedWith"]])

show_decoration(8)

# Now let's filter the respondents whose salary is above 70000 and also is only
# from specific countries while keeping the output to same columns as above.

countries_we_require = ["United States", "India", "United Kingdom", "Germany", "Canada"]

# filter-ception
extra_creamy_filter = (
        (results_df["ConvertedComp"] > 70000)
        &
        # this is syntax for pulling countries matching our list
        (results_df["Country"].isin(countries_we_require))
)

print(results_df.loc[extra_creamy_filter, ["Respondent", "Country", "LanguageWorkedWith"]])


show_decoration(9)

# Now let's filter all respondents who know python. This info can be found in
# the values of the LanguageWorkedWith column but at the same time the data in
# it is a string of languages separated by a ";" semicolon.
# Below is the syntax for creating a mask to grab values based on an expected
# string that is contained within the value. check notes for na=False arg
language_filter = (results_df["LanguageWorkedWith"].str.contains("Python", na=False))

print(results_df.loc[language_filter, ["Respondent", "LanguageWorkedWith"]])

show_decoration(10)




# Notes:
# 1. The filter var in line 24 is not a tuple, a tuple must have more than one
#    element separated by a "," within the parantheses. This is a python concept.
# 2. The parentheses in line 24 is also totally optional and is added only for
#    better readability.
# 3. Note: Python already has a filter keyword in built, so to avoid confusion,
#    we use filter_conditional as the variable to store filters. In general
#    people also call the filters a mask.
# 4. The str.contains() method takes the na= arg mandatorily if the column you're
#    filtering contains NaN (Not a Number) data type. you must explicitly tell
#    the str.contains() method what you want to do with such data types. Here
#    we simply set it to False, meaning we don't wanna do anything with it.
# 5. Remove the na=False arg to see the error you get if are not handling NaN types.