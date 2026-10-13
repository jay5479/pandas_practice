import pandas as pd

from utils.string_ops import show_decoration


# load a demo df for studies
people = {
    "First":["Kanushi", "Adhi", "Jeeshma", "Raavan"],
    "Last":["Gopi", "Seshan", "Seshan", "Krishnan"],
    "Email":["kanushi_g@gmail.com", "adhi_seshan@comcast.com", "jeeshma_john@comcast.com", "raavan@gmail.com"],
    }

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 5)

people_df = pd.DataFrame(people)
print(people_df)

show_decoration(1)