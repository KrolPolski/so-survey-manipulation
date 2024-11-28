# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    second_version.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: akuburas <akuburas@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/28 22:41:29 by akuburas          #+#    #+#              #
#    Updated: 2024/11/28 23:40:28 by akuburas         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend because I am using WSL lol
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os

# Load the CSV file into a pandas DataFrame
file_path = "survey_results_public.csv"
df = pd.read_csv(file_path)

# Create the pictures folder if it does not exist
output_folder = "pictures"
os.makedirs(output_folder, exist_ok=True)

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
    full_path = os.path.join(output_folder, filename)
    plt.savefig(full_path)
    plt.close()
    print(f"Graph saved as {full_path}")

# Step 2: Generate charts for programming languages, databases, etc.
columns_and_titles = [
    ("LanguageHaveWorkedWith", "Languages Professionals Have Worked With in Finland", "languages_have_worked_with.png"),
    ("LanguageWantToWorkWith", "Languages Professionals Want to Work With in Finland", "languages_want_to_work_with.png"),
    ("LanguageAdmired", "Languages Professionals Admire in Finland", "languages_admired.png"),
    ("DatabaseHaveWorkedWith", "Databases Professionals Have Worked With in Finland", "db_have_worked_with.png"),
    ("DatabaseWantToWorkWith", "Databases Professionals Want to Work With in Finland", "db_want_to_work_with.png"),
    ("DatabaseAdmired", "Databases Professionals Admire in Finland", "db_admired.png"),
    ("PlatformHaveWorkedWith", "Platforms Professionals Have Worked With in Finland", "platform_have_worked_with.png"),
    ("PlatformWantToWorkWith", "Platforms Professionals Want to Work With in Finland", "platform_want_to_work_with.png"),
    ("PlatformAdmired", "Platforms Professionals Admire in Finland", "platform_admired.png"),
    ("WebframeHaveWorkedWith", "Web Frameworks Professionals Have Worked With in Finland", "webframe_have_worked_with.png"),
    ("WebframeWantToWorkWith", "Web Frameworks Professionals Want to Work With in Finland", "webframe_want_to_work_with.png"),
    ("WebframeAdmired", "Web Frameworks Professionals Admire in Finland", "webframe_admired.png"),
    ("EmbeddedHaveWorkedWith", "Embedded Platforms Professionals Have Worked With in Finland", "embedded_have_worked_with.png"),
    ("EmbeddedWantToWorkWith", "Embedded Platforms Professionals Want to Work With in Finland", "embedded_want_to_work_with.png"),
    ("EmbeddedAdmired", "Embedded Platforms Professionals Admire in Finland", "embedded_admired.png"),
    ("MiscTechHaveWorkedWith", "Miscellaneous Tech Professionals Have Worked With in Finland", "misc_tech_have_worked_with.png"),
    ("MiscTechWantToWorkWith", "Miscellaneous Tech Professionals Want to Work With in Finland", "misc_tech_want_to_work_with.png"),
    ("MiscTechAdmired", "Miscellaneous Tech Professionals Admire in Finland", "misc_tech_admired.png"),
	("ToolsTechHaveWorkedWith", "Tools Professionals Have Worked With in Finland", "tools_have_worked_with.png"),
    ("ToolsTechWantToWorkWith", "Tools Professionals Want to Work With in Finland", "tools_want_to_work_with.png"),
	("ToolsTechAdmired", "Tools Professionals Admire in Finland", "tools_admired.png"),
    ("NEWCollabToolsHaveWorkedWith", "Collaboration Tools Professionals Have Worked With in Finland", "collab_tools_have_worked_with.png"),
    ("NEWCollabToolsWantToWorkWith", "Collaboration Tools Professionals Want to Work With in Finland", "collab_tools_want_to_work_with.png"),
    ("NEWCollabToolsAdmired", "Collaboration Tools Professionals Admire in Finland", "collab_tools_admired.png"),
]

for column, title, filename in columns_and_titles:
    create_bar_chart_from_column(column, title, filename)

