"""
Data Extraction of Social Lender Financial Literacy Feedback
"""

import os
import pandas as pd
import regex as rgx


class Exploit:
    """
    Data Exploitation of survey csv data

    """

    def __init__(self, file_):
        self.data_frame = pd.read_csv(file_)
        self.data_frame.index += 1
        self.data_frame_orig = self.data_frame.copy()

    def max_drop(self, pos):
        """
        Reverse one hot encoding

        """
        frame = self.data_frame.iloc[:, pos]
        max_ = frame.idxmax(axis=1)
        self.data_frame.drop(columns=frame, axis=1, inplace=True)
        if len(pos) == 2:
            max_.replace(regex={r'.*1': 'Yes', r'.*2': 'No'}, inplace=True)
        if len(pos) == 5:
            max_.replace(regex={
                r'.*1': 'Highly Satisfactory',
                r'.*2': 'Satisfactory',
                r'.*3': 'Neutral',
                r'.*4': 'Unsatisfactory',
                r'.*5': 'Highly Unsatisfactory'}, inplace=True)
        return max_

    def get_options(self):
        '''
        Feedback Data mungling

        '''
        col1 = list(self.data_frame.columns)
        col2 = list(filter(lambda x: x.endswith('_review'), col1))
        self.data_frame.drop(col1[:7], axis=1, inplace=True)
        self.data_frame.drop(col2, axis=1, inplace=True)
        categories = [
            'Training_useful',
            'Need_an_account',
            'Have_BVN',
            'Willing_to_get_BVN',
            'Overall Experience',
        ]
        for category in categories:
            if category != 'Overall Experience':
                # Defaulting to Highest if both are equal
                self.data_frame[f'{category}'] = self.max_drop([0, 1])
            else:
                self.data_frame[f'{category}'] = self.max_drop([0, 1, 2, 3, 4])

        for i in range(1, self.data_frame.shape[0]+1):
            if self.data_frame['Have_BVN'][i] == 'Yes':
                self.data_frame['Willing_to_get_BVN'][i] = 'NA'
        self.export()
        return self.data_frame

    def export(self, out_='Exports/Feedback1'):
        """
        Export dataframe to csv

        """
        while os.path.exists(f"{out_}.csv"):
            pattern = rgx.compile(r'([0-9]+)')
            span = pattern.search(out_).span()
            end = int(out_[span[0]:span[1]]) + 1
            out_ = out_[:span[0]] + str(end)
        self.data_frame.to_csv(f'{out_}.csv', index_label="Respondent")
        print(f'FILE SAVED AS {os.path.abspath(out_)}.csv')


if __name__ == "__main__":
    FILE = "../thesthing/handbook/feedback/data_1.csv"
    SURVEY = Exploit(FILE)
    SURVEY.get_options()
