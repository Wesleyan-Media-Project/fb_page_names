from pandasgui import show
import pandas as pd

#This script may take a while (>10 min) to run depending on the size of the data.

# Read csv.gz file
df = pd.read_csv('FB_page_names_date_spans.csv')

# Launch GUI
show(df)
