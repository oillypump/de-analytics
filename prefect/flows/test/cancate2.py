import pandas as pd

# create two sample dataframes
df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df1.reset_index(drop=True)
df1.set_index=('A')

df2 = pd.DataFrame({'A': [1, 2, 4], 'B': [4, 5, 7]} )
df2.set_index=('A')

print(f"\n{df1}")
# print(f"\n{df2}")

# use lambda function to check if each row is not in both dataframes
# not_in_both = df1[~df1.apply(lambda row: (
#     row['A'], row['B']) in zip(df2['A'], df2['B']), axis=1)]

# print(f"\n{not_in_both}")
