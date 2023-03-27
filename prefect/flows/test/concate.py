import pandas as pd

df = pd.DataFrame({'Courses': ["Spark","PySpark","Python","pandas"]})

df1 = pd.DataFrame({'Courses': ["Spark","PySpark","Python","pandas","Java"],
                    'Fee' : [20000,25000,22000,24000,23000]})

# df1 = pd.DataFrame({'Courses': ["Pandas","Hadoop","Hyperion","Java"],
#                     'Fee': [25000,25200,24500,24900]})
# Using pandas.concat() to concat two DataFrames

# print(df)
# print(df1)

data = [df, df1]
df = pd.concat(data)
# print(df)
df = df.drop_duplicates(subset="Courses", keep="last")

print(df)