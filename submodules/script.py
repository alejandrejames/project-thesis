import pandas as pd

data = pd.read_csv(csvname, 
error_bad_lines=False)
# We only need the Headlines text column from the data
data_text = data[['data']]
data_text = data_text.astype('str');
data = data_text.data.values.tolist()

print(data[1])
