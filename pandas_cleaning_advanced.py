import pandas as pd
import numpy as np

from utils.string_ops import show_decoration


# load big data df from csv for big data.
results_df = pd.read_csv("survey_results_public.csv")

# set max display values
pd.set_option('display.max_columns', 5)
pd.set_option('display.max_rows', 10)

# remove downcasting warnings
pd.set_option("future.no_silent_downcasting", True)

print(results_df)

show_decoration(1)