import pandas as pd
import numpy as np 
from collections import Counter
import os


dir_path = os.path.dirname(os.path.realpath(__file__))
df = pd.read_csv("email_info.csv")

df['To'] = df['To'].str.replace(r'\\n','') 
df['To'] = df['To'].str.replace(r'\\t','') 
df['To'] = df['To'].str.replace(r'\\n\\t','') 
df['To'] = df['To'].str.replace(r'\\t\\n','') 
df['To'] = df['To'].str.replace(" ", "")

#sample = df.sample(n=1000)

email_from_list = []
email_to_list = []
email_count_list = []

print("STARTING:")

from_list = list(set(df['From']))
email_count_matrix = pd.DataFrame(columns=['To','From','Count'])
for person in from_list:
    to_email_list = []
    temp_df = df.loc[df['From'] == person]
    email_to = temp_df['To'].dropna()
    to_email_list = [name.strip() for email in email_to for name in email.split(",")]
    count_list = Counter(to_email_list)
    for k in count_list:
        email_from_list.append(person)
        email_to_list.append(k)
        email_count_list.append(count_list[k])

email_count_matrix['To'] = email_to_list
email_count_matrix['From'] = email_from_list
email_count_matrix['Count'] = email_count_list



print(len(from_list))
print(len(email_from_list))