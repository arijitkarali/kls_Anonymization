
import pandas as pd

global sensitive_col, QID, fully_suppressedID, partly_suppressedID
k = 4  # (default anonymization parameter)
ld = 3  # (default diversity parameter)
s1 = 0.5  # (default 1st similarity parameter or duplicate probability parameter)
s2 = 0.1  # (default 2nd similarity parameter or coefficient of variation parameter)


sensitive_col = 'SALARY'        # this is the column based on which kls anonymization is carried out
QID = 'AGE'                     # a numerical quasi identifier that will be generalized
fully_suppressedID = 'NAME'     # the columns to be suppressed fully
partly_suppressedID = 'ZIP'     # the columns to be suppressed partially

# taking input csv
names = ('NAME', 'AGE', 'GENDER', 'ZIP', 'SALARY')
df = pd.read_csv('sampledata.csv', names=names, index_col=False)
df = df.sort_values(by=[QID])

row_count = len(df.index)
new_index = list(range(0, row_count))
s = pd.Series(new_index)
df.set_index([s], inplace=True)
# print(type(s[0]))
print(df)


def is_l_diverse(mydf, ld):
    if len(mydf[sensitive_col].unique()) >= ld:
        return True
    else:
        return False


def is_s_similar(mydf, s1, s2):
    s1prob = (len(mydf)-len(mydf[sensitive_col].unique()))/len(mydf)   # calculating duplicate prob
    s2prob = mydf[sensitive_col].std()/mydf[sensitive_col].mean()  # calculating coefficient of variation
    if (s1prob < s1) and (s2prob > s2):
        return True
    else:
        return False


def make_kls_anonymize(mydf, k, ld, s1, s2, dfsize):
    partitions = []
    i = 0
    j = 0
    while i < dfsize:
        partition_beg = i
        partition_end = partition_beg + j + k
        # partition size should be greater than equals k , as it is k anonymization
        if k > (dfsize - partition_end):
            break
        df_part = mydf[partition_beg:partition_end]
        if (is_l_diverse(df_part, ld) is True) and (is_s_similar(df_part, s1, s2) is True):
            partitions.append(partition_end)
            i = partition_end
            j = 0
        else:
            j += 1
    partitions.append(dfsize)
    return partitions


for i in df[fully_suppressedID]:                                        # suppressing 'NAME'
    df = df.replace([i], '***')

df_class_partitions = make_kls_anonymize(df, k, ld, s1, s2, row_count)  # finding equivalence classes

print("\npartitions based on k=4, l=3 are\n")
print(df_class_partitions)                                              # partitioning done
print("\n")

df[QID] = df[QID].astype('string')

begin_index = 0
for x in df_class_partitions:                                           # generalizing QID 'age'
    min_val = df[QID].iloc[begin_index]
    max_val = df[QID].iloc[x-1]
    df[QID].iloc[begin_index:x] = min_val + '-' + max_val
    begin_index = x

print(df)
