# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 07:58:43 2021

@author: wes_c
"""

import string
import numpy.random as random
import pandas as pd

MARITAL = {'single':'0', 'married':'1', 'divorced':'2'}
EDUCATION = {'unknown':'99', 'primary':'1', 'secondary':'2', 'tertiary':'3'}
LETTERS = list(string.ascii_lowercase)
RAND_RANGE = [2, 4]
HOURS_PER_WEEK = [20, 51]

def yes_no_randomizer(bool_):
    start = random.randint(*RAND_RANGE)
    end = random.randint(*RAND_RANGE)
    start = ''.join(random.choice(LETTERS, size=start))
    end = ''.join(random.choice(LETTERS, size=end))
    if bool_:
        str_ = start + 'yes' + end
        if 'no' in str_:
            return yes_no_randomizer(bool_)
        else:
            return str_
    else:
        str_ = start + 'no' + end
        if 'yes' in str_:
            return yes_no_randomizer(bool_)
        else:
            return str_

def make_messy(lines, savename='bank_info.log', educ_frame='earnings.csv'):
    lines = [line.split(';') for line in lines]
    cols = lines[0]
    cols[5] = '"hours_per_week"'
    rows = lines[1:]
    age = [row[0] for row in rows]
    job = [row[1] for row in rows]
    marital = [MARITAL[row[2][1:-1]] if random.randint(2) else row[2]\
               for row in rows]
    education = [EDUCATION[row[3][1:-1]] if random.randint(2) else row[3]\
                 for row in rows]
    default = [yes_no_randomizer(True) if 'yes' in row[4] else\
               yes_no_randomizer(False) for row in rows]
    hpw = [str(random.randint(*HOURS_PER_WEEK)) for _ in rows]
    newlines = list(zip(age, job, marital, education, default, hpw))
    newlines.insert(0, cols[:6])
    newlines = [';'.join(line) if random.randint(2) else ','.join(line)\
                for line in newlines]
    with open(savename, 'w') as f:
        for line in newlines:
            f.write(line + '\n')
    educ_earnings = [['unknown', 25.42], ['primary', 29.86],\
                     ['secondary', 30.17], ['tertiary', 33.91]]
    df = pd.DataFrame(educ_earnings,
                      columns=['education_level', 'mean_hourly_wage'])
    df.to_csv(educ_frame, index=False)
    return

if __name__ == '__main__':
    with open('./bank-full.csv', 'r') as f:
        lines = f.readlines()
    make_messy(lines)
