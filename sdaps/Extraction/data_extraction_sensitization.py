import pandas as pd
import get_name
df = pd.read_csv("../thesthing/apply-suggested2/data_1.csv")
df_orig = df.copy()

df.dropna(axis=1, inplace=True)  # delete all review columns
df.drop(['questionnaire_id', 'global_id', 'empty'], axis=1, inplace=True)

#drop all invalid sheets
for x, y in enumerate(df['valid']):
    if y == 0:
        df.drop(index=x, axis=0, inplace=True)

#create header for dataframe
LOG = ['Valid', 'recognized', 'verified']
NAME = ['Name']
PHONE = [f'digit{i}' for i in range(1,12)]
SEX = ['Male', 'Female']
AGE = ['<18', '18-24', '25-34', '35-44', '45-54', '>=55']
USE_ACCT = ['Use_Acct_Yes', 'Use_Acct_No']
LOANHISTORY = ['Loan_History_Yes', 'Loan_History_No']
BVN = ['BVN_Yes', 'BVN_No']
ALL_CAT= [LOG, NAME, PHONE, SEX, AGE, USE_ACCT, LOANHISTORY, BVN]
HEADER =[_ for cat in ALL_CAT for _ in cat]

df.columns = HEADER #set header for dataframe

#Do some data mungling
for _ in ALL_CAT[3:]:
    df[f'{get_name(_)[0]}'] = df.loc[:,[*_]].idxmax(axis=1)
    df.drop([*_],axis=1,inplace=True)

df.replace(regex={r'.*Yes': 'Yes', r'.*No': 'No'}, inplace=True)
df.index += 1
df.to_csv('./survey.csv', header=True, index_label='respondent')

print('Operation completed!')