import re
import numpy as np
import pandas as pd


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
    df_titanic = pd.read_csv(file)
    liters = df_titanic["liters_drunk"]
    mean_liters = round(liters[(0 <= liters) & (liters <= 5)].mean())
    for ind, row in df_titanic.iterrows():
        # sex
        rec = row['sex']
        rec_u = rec.upper()
        if rec_u == 'M' or rec_u == 'М':
            df_titanic = df_titanic.replace(rec, '1')
        elif rec_u == 'Ж':
            df_titanic = df_titanic.replace(rec, '0')
        else:
            df_titanic = df_titanic.drop(ind)
        # liters_drunk
        rec = row["liters_drunk"]
        if (rec < 0) | (rec > 5):
            df_titanic = df_titanic.replace(rec, mean_liters)

    # row_number
    df_titanic["row_number"] = df_titanic["row_number"].fillna(np.nanmax(df_titanic["row_number"]))
    return df_titanic


corrected_file = fix_csv("data/titanic_with_labels.csv")
stage1(corrected_file).to_csv('out.csv', index=False)
