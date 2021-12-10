# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 13:25:08 2021

@author: wes_c, for Juno College of Technology
"""

import numpy.random as random

#Make medical log information based loosely on UCI heart disease dataset

MED_PREFIX = 'bid'
MEDS = ['apixaban', 'dabigatran', 'clopidogrel', 'dipyridamole', 'benazepril']
SEPS = [',', 'BREAK', '\t']
PAIN_TYPE = ['typical angina', 'atypical angina',\
             'non-anginal pain', 'asymptomatic'] #unused
SYSTOLIC_RANGE = [100, 160]
DIASTOLIC_RANGE = [60, 110]
CHOLESTEROL_RANGE = [150, 300] #mg/dL
RESTECG_VALUES = ['0', 'ST-T wave abnormality', 'left ventricular hypertrophy']
HEART_RATE_MAX = [100, 200]
EX_IND = ['0', '1', 'yes', 'no', 'symptomatic', 'asymptomatic']

def biased_coin(p):
    return random.uniform(0, 1) < p

def str_round(range_, method=random.uniform):
    return str(round(method(*range_)))

def create_med_line():
    num_meds = random.randint(low=1, high=len(MEDS)+1)
    meds = random.choice(MEDS, size=num_meds, replace=False)
    if meds.shape[0] > 0:
        med_str = MED_PREFIX + '||'.join(meds)
    else:
        med_str = ''
    return med_str #insert randomly in row

def create_blood_pressure():
    sys = str_round(SYSTOLIC_RANGE)
    dia = str_round(DIASTOLIC_RANGE)
    return ''.join([sys, '/', dia])

def calculate_diagnosis(age, bps, chol, restecg, max_hr, ex_ind, med_line):
    #bias outcome based on presence/non-presence of abnormality then
    #add arbitrary variance
    age_outcome = min(1, int(age)/95)
    bps = bps.split('/')
    sys, dia = bps[0], bps[1]
    sys = int(int(sys) > 140)
    dia = int(int(dia) > 100)
    chol = int(int(chol) > 240)
    restecg = int(restecg == '0')
    max_hr = min(1, int(max_hr)/(220 - int(age)))
    ex_ind = int(ex_ind in ['0', 'no', 'asymptomatic'])
    med_line = len(med_line.split('||'))/5
    probability = sum([age_outcome, sys, dia, chol, restecg,\
                       max_hr, ex_ind, med_line])/8
    probability = random.normal(probability, 0.10)
    probability = max(0, min(probability, 1)) #[0, 1]
    return str(int(biased_coin(probability)))

def generate_row():
    #row is always formatted the same EXCEPT random placement
    #of medications line, and random separators
    row = ''
    age = str_round([65, 12], method=random.normal)
    bps = create_blood_pressure()
    chol = str_round(CHOLESTEROL_RANGE)
    restecg = random.choice(RESTECG_VALUES)
    max_hr = str_round(HEART_RATE_MAX)
    ex_ind = random.choice(EX_IND)
    med_line = create_med_line()
    diagnosis = calculate_diagnosis(age, bps, chol, restecg,
                                    max_hr, ex_ind, med_line)
    normal_fields = [age, bps, chol, restecg, max_hr, ex_ind, diagnosis]
    med_insert = 0
    for idx, field in enumerate(normal_fields):
        if biased_coin(0.2) and not med_insert:
            if idx == 0:
                row += med_line + random.choice(SEPS)
            else:
                row += random.choice(SEPS) + med_line
            med_insert = 1
        if idx == 0:
            row += field
        else:
            row += random.choice(SEPS) + field
    if not med_insert:
        row += random.choice(SEPS) + med_line
    return row

def make_dataset(n_rows=50000, savename='heart_disease.log'):
    rows = []
    for _ in range(n_rows):
        rows.append(generate_row())
    with open(savename, 'w') as f:
        for row in rows:
            f.write(row + '\n')
    return

if __name__ == '__main__':
    make_dataset()