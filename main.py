
import pandas as pd

k = 4  # (default anonymization parameter)
ld = 3  # (default diversity parameter)
s1 = 0.5  # (default 1st similarity parameter or duplicate probability parameter)
s2 = 0.1  # (default 2nd similarity parameter or coefficient of variation parameter)

# taking input csv
names = ('NAME', 'AGE', 'GENDER', 'ZIP', 'SALARY')
df = pd.read_csv('sampledata.csv', names=names, index_col=False)
df = df.sort_values(by=['AGE'])

row_count = len(df.index)
new_index = list(range(0, row_count))
s = pd.Series(new_index)
df.set_index([s], inplace=True)
print(df)


# def make_kls_anonymize(df,k,ld,s1,s2):
