# Pandas Assignment: Data Manipulation & Validation

import pandas as pd
from functools import partial


# Createing a sample CSV data file

data = """name,age,city,join_date,salary
Katana,25,Lala-land,2022-05-12,5000
Jhin,30,Green-land,2020-08-20,7000
Yone,22,Ice-land,2023-01-10,4500
Samira,30,Water-land,2020-08-20,7000
Zack,,Lunaris,2021-03-15,
"""

# Save the data to a CSV file
with open("users.csv", "w") as f:
    f.write(data)

#Load data into Pandas DataFrame

df = pd.read_csv("users.csv")
print(" Initial DataFrame:\n", df)


# Define a Pandas Series with a custom index

ages = pd.Series([25, 30, 22, 30, None],
                 index=["Katana", "Jhin", "Yone", "Samira", "Zack"])
print("\n Pandas Series with custom index:\n", ages)


# Inspect the DataFrame

print("\n Data types:\n", df.dtypes)
print("\n First 3 rows:\n", df.head(3))
print("\n Last 2 rows:\n", df.tail(2))
print("\n Data description:\n", df.describe())


#  Data slicing
# row position
print("\n Slice by position (first 3 rows):\n", df.iloc[0:3])

#  column name
print("\n Column 'name':\n", df["name"])
print("\n Columns 'name' and 'city':\n", df[["name", "city"]])

# filtering
print("\n Users older than 25:\n", df[df["age"] > 25])

# Range filtering
print("\n Users aged between 22 and 30:\n",
      df[(df["age"] >= 22) & (df["age"] <= 30)])


# Data cleaning: duplicates & unique values


print("\n Duplicated rows:\n", df.duplicated())
print("\n Unique cities count:", df["city"].nunique())

# Remove duplicate rows

df = df.drop_duplicates()
print("\n After removing duplicates:\n", df)


# Type conversion using pd.to_numeric & pd.to_datetime

df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
df["join_date"] = pd.to_datetime(df["join_date"], errors="coerce")

print("\n After type conversions:\n", df.dtypes)


# Fill missing data using .apply()

def fill_missing_salary(s):
    """Fill missing salary values with a default amount (4000)."""
    if pd.isna(s):
        return 4000
    return s

df["salary"] = df["salary"].apply(fill_missing_salary)
print("\n After filling missing salary values:\n", df)

# Cleaning step in a pipeline using .pipe()

def convert_types(data):
    """Convert numeric and datetime columns safely."""
    data["age"] = pd.to_numeric(data["age"], errors="coerce")
    data["join_date"] = pd.to_datetime(data["join_date"], errors="coerce")
    return data

df = df.pipe(convert_types)
print("\n After .pipe() conversion:\n", df.dtypes)


# Using .pipe() with a threshold parameter via partial

def filter_by_salary(data, threshold):
    """Return only rows with salary above a given threshold."""
    return data[data["salary"] > threshold]

# Fix threshold = 5000 using partial
df = df.pipe(partial(filter_by_salary, threshold=5000))
print("\n After filtering salaries > 5000:\n", df)


#  Final output

print("\n Final cleaned DataFrame:\n", df)

