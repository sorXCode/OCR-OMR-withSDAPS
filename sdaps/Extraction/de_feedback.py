import get_name
import os
import pandas as pd


class Exploit:

    def __init__(self, file_):
        self.df = pd.read_csv(file_)
        self.df.index += 1
        self.df_orig = self.df.copy()
        pass

    def max_drop(self, x):
        frame = self.df.iloc[:, x]
        max_ = frame.idxmax(axis=1)
        self.df.drop(columns=frame, axis=1, inplace=True)
        if len(x) == 2:
            max_.replace(regex={r'.*1': 'Yes', r'.*2': 'No'}, inplace=True)
        if len(x) == 5:
            max_.replace(regex={
                r'.*1': 'Highly Satisfactory',
                r'.*2': 'Satisfactory',
                r'.*3': 'Neutral',
                r'.*4': 'Unsatisfactory',
                r'.*5': 'Highly Unsatisfactory'}, inplace=True)
        return max_

    def get_options(self):
        # self.df = self.df[self.df.valid == 1] #Sometimes you need to subset cos you can drop
        col1 = list(self.df.columns)
        col2 = list(filter(lambda x: x.endswith('_review'), col1))
        self.df.drop(col1[:7], axis=1, inplace=True)
        self.df.drop(col2, axis=1, inplace=True)
        # col = list((map(str, self.df.columns))
        categories = [
            'Training_useful',
            'Need_an_account',
            'Have_BVN',
            'Willing_to_get_BVN',
            'Overall Experience'
        ]
        for category in categories:
            if category != 'Overall Experience':
                # Defaulting to Highest if both are equal
                self.df[f'{category}'] = self.max_drop([0, 1])
            else:
                self.df[f'{category}'] = self.max_drop([0, 1, 2, 3, 4])

        for i in range(1, self.df.shape[0]+1):
            if self.df['Have_BVN'][i] == 'Yes':
                self.df['Willing_to_get_BVN'][i] = 'NA'
        print(self.df)


if __name__ == "__main__":
    file_ = "thesthing/handbook/feedback/data_1.csv"
    survey = Exploit(os.path.join(os.getcwd(), file_))
    survey.get_options()
