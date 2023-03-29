import pandas as pd

df1 = pd.DataFrame({'Courses': ["Spark", "PySpark", "Python", "pandas"],
                    'Fee': [20000, 25000, 22000, 24000]})

df2 = pd.DataFrame({'Courses': ["Spark", "PySpark", "Python", "pandas", "Java"],
                    'Fee': [20000, 25000, 22000, 24000, 23000]})

# df1 = pd.DataFrame({'Courses': ["Pandas","Hadoop","Hyperion","Java"],
#                     'Fee': [25000,25200,24500,24900]})
# Using pandas.concat() to concat two DataFrames

# print(df)
# print(df1)

data = [df1, df2]
# df = pd.concat(data)
# print(df)
# df = df.drop_duplicates(subset="Courses", keep="last")

# print(df)

# df = df.set_index('Courses').join(df1.set_index('Courses'), how='outer')

# df = df1[~df1.Courses.isin(df)]
# print(df)
# print(len(df))

not_in_both = df1[~df1.apply(lambda  row: (
    row['Courses']) in zip(df2['Courses']), axis=1)]

print(f"\n{not_in_both}")