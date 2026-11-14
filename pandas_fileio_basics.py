import pandas as pd

# import to read and write to Excel files in older pandas, no longer mandatory
import openpyxl

from utils.string_ops import show_decoration
# import for cleaning up files, ignore for studies
from utils.maintenance import cleanup


# To read data from csv
results_df = pd.read_csv("survey_results_public.csv", index_col="Respondent")

# set max display values
pd.set_option('display.max_columns', 5)
pd.set_option('display.max_rows', 10)

# remove downcasting warnings
pd.set_option("future.no_silent_downcasting", True)

print(results_df)

show_decoration(1)

# Let's learn how to write and save to different sources in pandas
# Let's make a new df of records from results_df where country is India
filt = (results_df["Country"] == "India")
india_df = results_df.loc[filt]
print(india_df)

# Now let's write this back to a csv file.
# This creates the csv file inside the data folder, with only India's records
india_df.to_csv("data/india.csv") # check notes #1

show_decoration(2)

# Similar to csv's, we also have tsv files which are nothing but tab separated
# value files.
# We can also simply save our df to tsv files like below, note that
# the method is still to_csv() just with a sep= arg that takes your separator
# which in our case is a \t (tab) character.
india_df.to_csv("data/modified_india.tsv", sep="\t")

# Open the tsv file in notepad++ if on Windows or Sublime Text editor on Linux
# to know and understand the difference of csv vs tsv instead of opening on IDE.
# To read back from a tsv file
modified_india_df = pd.read_csv("data/modified_india.tsv", sep="\t")
print(modified_india_df)

show_decoration(3)

# Now let's write to an Excel file.
india_df.to_excel("data/updated_india.xlsx")


# To read from an Excel file, use the built-in pandas.read_excel()
# pd.read_excel() uses the openpyxl library by default to parse .xlsx files.
# pd.read_excel() can also take the index_col arg similar to read_csv()
# The engine= arg is optional here, check notes #2 - #6
updated_india_df = pd.read_excel("data/updated_india.xlsx", engine="openpyxl", index_col="Respondent")
print(updated_india_df)

show_decoration(4)

# Let's learn how to write to JSON files by creating a new Zimbabwe only df from
# our survey results and writing it to a JSON
filt = (results_df["Country"] == "Zimbabwe")
z_df = results_df.loc[filt]

# let's write the new df to JSON.
# use sublime ot notepad++ to view the json file after creation and note that
# every series name from our z_df is a key that holds another nested dict as
# its value.
# The nested dict contains the index_column value of our z_df as its key's with
# the corresponding column's data as its value.
z_df.to_json("data/zimbabwe.json") # check notes #7

# now let's read back from the json to a df. Note that this json_df retains our
# respondent column values as index because the nested dicts key contain index.
json_df = pd.read_json("data/zimbabwe.json")
print(json_df)

show_decoration(5)

# the previous json was hard to read. Let's create neater json by orienting
# the data in our z_df row/record wise instead of column wise with line breaks
# separating each record to make it more human-readable.
# This is done using the orient params which takes "records" as its arg to orient
# our z_df row wise while writing and the lines params which takes a bool arg to
# add line breaks between each record.
# Note here that the resulting json file has a single dictionary per record/row
# in our z_df with the column names as keys and data as its values.
# Also note that the index column (respondent column) values are missing.
z_df.to_json("data/transposed_zimbabwe.json", orient="records", lines=True)


# let's read the oriented json back into a df.
# It is mandatory to specify the same orient and lines args while reading a json
# which is oriented row wise and has line breaks else ValueError.
# And since our neater json content destroyed index, new default row
# labels/indices are added. check notes #8
inverted_json_df = pd.read_json("data/transposed_zimbabwe.json", orient="records", lines=True)
print(inverted_json_df)

show_decoration(6)

# To avoid indexes from being dropped while re-orienting your json record wise,
# always reset your custom index before writing to a json.
# Because resetting custom index will bring back the indexed column (respondent
# column) back into our df as a regular series object and a default row label
# column will take its place as the index which can then be safely dropped
# while re-orienting.
# Or otherwise all this could have been simply avoided if we didn't use the
# index_col arg while creating the updated_india_df from excel in this module
# on which the z_df is built on
z_df.reset_index(inplace=True)
print(z_df)

# then write to json
z_df.to_json("data/clean_zimbabwe.json", orient="records", lines=True)

show_decoration(7)

# now read it back
clean_json_df = pd.read_json("data/clean_zimbabwe.json", orient="records", lines=True)
print(clean_json_df)
# check notes #9

show_decoration(8)

# You can also pass in raw urls containing json strings or json data to read
# to a df like so,
# You can navigate to the link below from a browser to see what it is.
post_df = pd.read_json("https://raw.githubusercontent.com/CoreyMSchafer/code_snippets/master/Python/Flask_Blog/snippets/posts.json")
print(post_df.head(3))

show_decoration(9)

# Comment out below line and run for cleaning up files created by this module
# cleanup("data")



# Notes:
# 1. Everytime you write to a file, if a filename with the same name and type
#    already exists in the location then that file gets overwritten.
#    If not, then a new file is created and saved with your changes/data in
#    that location. There is no opening a file to edit or appending to files
#    with the pandas write methods that you learn in this module. You have to
#    read from a file to a df, manipulate the df using pandas as you
#    want and write your modified df back on top of the original file, replacing
#    it. So be cautious of accidentally overwriting pre-existing files when
#    working on actual projects.
# 2. Run the below command to install openpyxl to read Excel files:
#    $ pip install openpyxl
# 3. By default, pd.read_excel() method uses an optional engine= params, sets
#    it to None and tries to use the following libraries/packages for reading
#    the following file types:

#    a. .xlsx (Modern Excel workbook) & .xlsm (Modern Excel macro-enabled workbooks) --> openpyxl library
#    b. legacy .xls (Excel binary files) --> xlrd library
#    c. legacy .xlr (Binary excel workbooks) --> pyxlsb library
#    d. .ods, .odf & .odt (OpenDocument Spreadsheets) --> odf library

#    This however will run into errors when trying to read from the above
#    filetypes if you haven't installed these packages already via your
#    package manager (pip in our case).

# 4. In this module we just explicitly set the engine= params to "openpyxl" to
#    force pandas to use the installed openpyxl lib when parsing the .xlsx
#    file. This is a best practice when you want to strictly enforce standards
#    according to the respective library while trying to read from a specific
#    filetype.
# 5. Reading and writing to Legacy excel or open spreadsheet filetypes
#    are not demonstrated in this module. Install those libraries and play with
#    those filetypes on your own using the same read_excel() method but with
#    the corresponding engine arg.
# 6. Also note while execution that reading from an excel takes some time and
#    is slow compared to reading from csv.
# 7. If the content in your json file looks too confusing, use any online json
#    formatter tool like: https://jsonformatter.org/json-viewer to view its
#    structure. Sometimes copy-pasting the entire json to the online tool will
#    lead to parsing error so copy one key-value pair at a time from your json
#    and paste it into the online tool to understand its structure.
# 8. When using to_json() and if no arg is supplied, then the optional orient
#    params is by default set to "columns" and lines params set to False. This
#    operation retains indexing. But if orient params is set to "records" then
#    the index is dropped by default, so our transposed_zimbabwe.json doesn't
#    contain the Respondent column and its data at all.
# 9. Pandas supports writing to lot other data and file types like html,
#    markdown, dict etc with their own .to() methods. Read the pandas
#    input/output documentation to learn more for your use case:
#    https://pandas.pydata.org/docs/reference/io.html
