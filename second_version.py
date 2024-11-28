# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    second_version.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: akuburas <akuburas@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/28 22:41:29 by akuburas          #+#    #+#              #
#    Updated: 2024/11/28 23:13:15 by akuburas         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend because I am using WSL lol
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load the CSV file into a pandas DataFrame
file_path = "survey_results_public.csv"
df = pd.read_csv(file_path)

# Function to clean the YearsCodePro column. Might not of been necessarily because there is no "More than 50 years" in the Finland data set.
def clean_years_code_pro(value):
    if pd.isna(value) or value == "NA":
        return None  # Exclude "NA" values
    elif value == "Less than 1 year":
        return 0.5  # Treat as half a year
    elif value == "More than 50 years":
        return 51  # Treat as 51 years
    else:
        try:
            return float(value)  # Convert numeric strings to float
        except ValueError:
            return None  # Exclude unexpected non-numeric values

# Apply the cleaning function
df["YearsCodeProCleaned"] = df["YearsCodePro"].apply(clean_years_code_pro)

# Step 1: Filter by country and minimum professional coding years
filtered_df = df[(df["Country"] == "Finland") & (df["YearsCodeProCleaned"] >= 1)]

# Generalized function to count items in a given column
def count_items(column):
    items = filtered_df[column].dropna().str.split(";").sum()  # Split and flatten
    return Counter(items)

# Function to create and save a bar chart from a column
def create_bar_chart_from_column(column, title, filename):
    data = count_items(column)
    plt.figure(figsize=(10, 6))
    data_series = pd.Series(data).sort_values(ascending=False)
    data_series.plot(kind="bar", color="skyblue")
    plt.title(title)
    plt.xlabel("Items")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Graph saved as {filename}")

# Step 2: Generate charts for programming languages, databases, etc.
columns_and_titles = [
    ("LanguageHaveWorkedWith", "Languages Professionals Have Worked With in Finland", "have_worked_with.png"),
    ("LanguageWantToWorkWith", "Languages Professionals Want to Work With in Finland", "want_to_work_with.png"),
    ("LanguageAdmired", "Languages Professionals Admire in Finland", "admired.png"),
    ("DatabaseHaveWorkedWith", "Databases Professionals Have Worked With in Finland", "db_have_worked_with.png"),
    ("DatabaseWantToWorkWith", "Databases Professionals Want to Work With in Finland", "db_want_to_work_with.png"),
    ("DatabaseAdmired", "Databases Professionals Admire in Finland", "db_admired.png"),
]

for column, title, filename in columns_and_titles:
    create_bar_chart_from_column(column, title, filename)

