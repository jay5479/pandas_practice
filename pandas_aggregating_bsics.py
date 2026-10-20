import pandas as pd

from utils.string_ops import show_decoration


# load big data df from csv for big data with respondent column as index column
results_df = pd.read_csv("survey_results_public.csv", index_col="Respondent")

# set max display values
pd.set_option('display.max_columns', 5)
pd.set_option('display.max_rows', 10)


# Let's first create a Country group. Check notes #1.
country_group = results_df.groupby("Country")

# Let us now get the median ConvertedComp values by each group
print(country_group["ConvertedComp"].median())

show_decoration(1)


show_decoration(2)
show_decoration(3)
show_decoration(4)
show_decoration(5)


# Notes:
# 1. You must know grouping and filtering basics before you start to study this
#    module.