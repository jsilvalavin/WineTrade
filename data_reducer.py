# imports 
import pandas as pd

# run
if __name__ == "__main__":
    # read data
    df = pd.read_csv('data_v2.csv')
    # only consider year - reduce size
    df.loc[df['Period'] == 'Total annuel', cols].to_csv('data.csv')