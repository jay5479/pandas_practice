import pandas as pd

# To work with postgres db
import psycopg

# To work with ORMs, to connect to db
from sqlalchemy import create_engine

from utils.string_ops import show_decoration

# Let's load big data
results_df = pd.read_csv("survey_results_public.csv", index_col="Respondent")

# set max display values
pd.set_option('display.max_columns', 5)
pd.set_option('display.max_rows', 10)

# remove downcasting warnings
pd.set_option("future.no_silent_downcasting", True)

# Let's create a smaller df with small data to write to db
filt = (results_df["Country"]=="France")
france_df = results_df.loc[filt]

print(france_df)

show_decoration(1)

# Let's create a database connection obj using sql alchemy's create_engine()
# syntax: create_engine("postgresql://user:password@host:port/db_name")
# read the docs here to know more about the args it takes for different DB types:
# https://docs.sqlalchemy.org/en/21/core/engines.html#supported-databases
# For this to work you need to have the sample_db created already in your postgres
engine = create_engine('postgresql://postgres:admin@localhost:5432/sample_db')

# now let's write our df by creating a table in db using .to_sql()
# The pandas .to_sql() method takes a table name as its arg with a con= params
# which takes the DB's connection obj as its arg. If the table does not exist
# in DB it is created.
france_df.to_sql("france_survey", con=engine) # check notes

show_decoration(2)

# Let's create a new dataframe to write to our DB with the same schema as france_df
filt = (results_df["Country"]=="Azerbaijan")
new_df = results_df.loc[filt]

# If we run the to_sql() again with same table name, we get table "france_survey"
# already  exists error, comment out and run to see.
# new_df.to_sql("france_survey", con=engine) # check notes

show_decoration(3)

# To overwrite existing table, use the if_exists= params with "replace" as its arg
# This will actually drop the old table and replace it with the new table
new_df.to_sql("france_survey", con=engine, if_exists="replace")

show_decoration(4)

# To append to existing table instead of overwriting use the "append" arg to if_exists
# let's append back france data to our table
france_df.to_sql("france_survey", con=engine, if_exists="append")

show_decoration(5)

# let's create one more small df to append
filt = (results_df["Country"]=="Afghanistan")
temp_df = results_df.loc[filt]
print(temp_df.shape) # just checking how many rows we are adding

# If you want the row labels/indices alone to be dropped while writing to
# db, use the index=False arg. This actually drops all values here and replaces
# it with null on our respondent column because the respondent column already
# exists in our DB. We are just trying to drop the indices while appending
# to it. Check notes
temp_df.to_sql("france_survey", con=engine, if_exists="append", index=False)

show_decoration(6)

# But if we wanted to drop the index column itself entirely instead of just
# replacing values to null,then do this while first writing to db when the
# respondent column or any data doesn't exist in the table yet OR
# while overwriting the table since replacing drops the entire table and
# creates new like so
temp_df.to_sql("france_survey", con=engine, if_exists="replace", index=False)

show_decoration(7)

# To read from a DB table to a df simply use .read_sql(table_name, engine=conn_obj)
# Using Age as index_col since we dropped Respondent column from our table
# previously, do not do this as it is ill-advised, index columns should always
# have unique values. I am just doing it here for demonstrating.
# index_col is also optional here as without it pandas will assign default
# indices to our df anyways.
big_df = pd.read_sql("france_survey", con=engine, index_col="Age")
print(big_df)

show_decoration(8)

# To run queries on our DB and then export data to df,
# index_col is optional here again
sql_df = pd.read_sql("SELECT * FROM public.france_survey "
                     "WHERE \"Hobbyist\" = \'No\';", con=engine,
                     index_col="Age1stCode") # just using escape \ characters to escape " here

print(sql_df)

show_decoration(9)




# Notes:
# 1. For mysql dbs sqlite3 is part of std lib for python3, no need to install,
#    just import, read the doc and use.
# 2. For postgres db's:
#    $ pip install "psycopg[binary]"
# 3. To install SQL Alchemy:
#    $ pip install sqlalchemy
# 4. You need to have pgadmin4 installed to view your tables and data.
#    Install from the internet. You also need to have a sample_db created to
#    work with the code in this, run below query in your pgadmin query tool to
#    create it:
#    CREATE DATABASE sample_db;
# 5. Most code blocks will not have output for this module as we are working
#    with DB. Run each block of code one-by-one after another to see the output
#    reflected in your database table. Drop the table created after each step
#    before moving and running the next code block to avoid table already exists error.
# 6. Pandas' .to_sql() method's con= params doesn't take raw psycopg connection
#    objects like psycopg.conn() for postgres DBs and only supports and recommends
#    sql aclchemy or arrow DB or sqlite3's connection objects. So we use sql
#    alchemy connection obj for this module to work with postgres DB.
# 7. The if_exists= params for .to_sql() is an optional param and if not supplied,
#    is set to "fail" by default. This means that the to_sql() method will fail
#    if a table of similar name exists in the db. That's why line 50 fails.
# 8. Sometimes you might not see the appended records in the postgres' pgadmin
#    UI due to truncation. Use a SQL query to find them instead eg:
#    SELECT * FROM public.france_survey WHERE "Country" = 'Afghanistan';