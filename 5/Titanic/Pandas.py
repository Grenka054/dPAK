import re
import numpy as np
import pandas as pd
from datetime import time


# REWORKER FOR INITIAL FILES
def fix_csv(csv_name):
    csv = open(csv_name, 'r', encoding="UTF-8")
    # copy name but delete ".csv"
    new_name = csv_name[:-4] + "_fixed.csv"
    newcsv = open(new_name, 'w', encoding="UTF-8")

    # column names
    names = csv.readline().strip()
    newcsv.write(names.replace(' ', ',') + "\n")
    quoted = re.compile('"[^"]*"')
    # lines
    for line in csv.readlines():
        # find string in ""
        quoted_data = quoted.findall(line)
        # avoid split(' ')
        for match in quoted_data:
            line = re.sub(match, match.replace(' ', '_'), line)
        # line to list without id
        splited_list = line.split(' ')[1:]
        # empty to numpy.nan
        if '' in splited_list:
            splited_list[splited_list.index('')] = str(np.nan)
        for i in range(len(splited_list)):
            splited_list[i] = splited_list[i].replace('_', ' ')
        newcsv.write(','.join(splited_list))
    csv.close()
    newcsv.close()
    return new_name


def stage1(file):
    df = pd.read_csv(file)
    liters = df["liters_drunk"]
    mean_liters = round(liters[(0 <= liters) & (liters <= 5)].mean())
    for ind, row in df.iterrows():

        # sex
        rec = row['sex']
        rec_u = rec.upper()
        if rec_u == 'M' or rec_u == 'М':
            df = df.replace(rec, '1')
        elif rec_u == 'Ж':
            df = df.replace(rec, '0')
        else:
            df = df.drop(ind)

        # liters_drunk
        rec = row["liters_drunk"]
        if (rec < 0) | (rec > 5):
            df = df.replace(rec, mean_liters)

    # row_number
    df["row_number"] = df["row_number"].fillna(np.nanmax(df["row_number"]))
    return df


def stage2(file1, file2):
    df = pd.read_csv(file1)

    # age
    df['age_child'] = df.apply(lambda row: 1 if row.age < 18 else 0, axis=1)
    df['age_adult'] = df.apply(lambda row: 1 if 18 <= row.age <= 50 else 0, axis=1)
    df['age_old'] = df.apply(lambda row: 1 if row.age > 50 else 0, axis=1)

    # drink
    for ind, row in df.iterrows():
        if re.search(r'beer', row['drink']):
            df = df.replace(row['drink'], 1)
        else:
            df = df.replace(row['drink'], 0)

    # left join on check_number
    df_ses = pd.read_csv(file2)
    df = df.merge(df_ses, on='check_number', how='left')

    # get hour from session_start
    df['session_start'] = pd.to_datetime(df['session_start']).dt.hour

    df['start_morning'] = df.apply(lambda row: 1 if row.session_start < 12 else 0, axis=1)
    df['start_afternoon'] = df.apply(lambda row: 1 if 12 <= row.session_start < 18 else 0, axis=1)
    df['start_evening'] = df.apply(lambda row: 1 if row.session_start >= 18 else 0, axis=1)

    return df


corrected_titanic = fix_csv("data/titanic_with_labels.csv")
corrected_sessions = fix_csv("data/cinema_sessions.csv")
df_st1 = stage1(corrected_titanic)
df_st1.to_csv('stage1.csv', index=False)
stage2('stage1.csv', corrected_sessions).to_csv('stage2.csv', index=False)
