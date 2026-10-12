import pandas as pd
from utils.string_ops import show_decoration


# load a demo df for studies
people = {
    "Name":["Kanushi", "Adhi", "Jeeshma", "Raavan"],
    "Age":[6, 33, 28, 2],
    "Email":["kanushi_g@gmail.com", "adhi_seshan@comcast.com", "jeeshma_john@comcast.com", "raavan@gmail.com"],
    }

people_df = pd.DataFrame(people)

# load some more dfs from csv's
results_df = pd.read_csv("survey_results_public.csv")

# We are indexing the column named "Column" while parsing the csv itself
# come back to this line after studying indexing further down in this module
schema_df = pd.read_csv("survey_results_schema.csv", index_col="Column")

# set max display values
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)

print(people_df)
print(results_df)
print(schema_df)

show_decoration(1)

# In the people df we can use a column with unique values such as "Email" to act
# as index for the df.
people_df.set_index("Email")

# The index is set but won't be displayed below because the index set is not inplace.
print(people_df)

show_decoration(2)

# to make the indexing permanent to the df
people_df.set_index("Email", inplace=True)
print(people_df)

show_decoration(3)

# grab records now using row index, note that the email now gets output
# with a Name: as its label. This actually implies the row's name / label.
print(people_df.loc["kanushi_g@gmail.com"])

show_decoration(4)

# to reset index of your df
people_df.reset_index(inplace=True)
print(people_df)

show_decoration(5)

# Let's learn how to use indexes in actual data
# setting a column with unique values as index for survey results
results_df.set_index("Respondent", inplace=True)

# we can now use the Respondent label here to access the record with respondent
# value, this is not by row index
print(results_df.loc[1])

show_decoration(6)

# And now we can do all these
print(results_df.loc[1, "MainBranch"])

show_decoration(7)

print(results_df.loc[[1, 3], ["MainBranch", "Country"]])

show_decoration(8)

# we can also similarly use indexing to fetch data across dfs
# The schema_df is indexed in place at column: "Column" while parsing itself
# with the index_col arg , see line 19.
# We can use the column values as labels and grab the record
print(schema_df.loc["Hobbyist"])

show_decoration(9)

# same as above but explicitly fetching the "QuestionText" column value alone for
# the "MgrIdiot" row label record.
# This is helpful when you don't understand a column (say, "MgrIdiot") from survey
# results, so you want to look it up in the schema to determine which question was
# asked to fetch values for that particular column in survey results.
print(schema_df.loc["MgrIdiot", "QuestionText"])

show_decoration(10)

# sorting basics, to sort your index column alphabetically
schema_df.sort_index(inplace=True)
print(schema_df)

show_decoration(11)



# Notes:
# 1. Indexing helps search values or grab records/faster instead of using integer
#    indexes which are hard to keep track of. The indexed values from the column
#    selected for indexing will act as row labels. Hence, generally we always use any
#    columns containing unique values so every row can be identified with their own
#    identifier.
# 2. Indexing always creates a temp df. Use inplace=True arg to make the indexing
#    permanent for a df.
# 3. sort_index() also always a creates a temp df. Use inplace=True arg to make the sorting
#    permanent for a df.
# 4. To make lookups easy always keep indexes sorted where possible.