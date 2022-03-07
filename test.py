import pandas as pd

df = pd.DataFrame(columns=['Title','Date Added',"Watched?",'Time Watched','H','M'])
df.to_parquet('movie_df.parquet')
df.to_parquet('test.parquet')