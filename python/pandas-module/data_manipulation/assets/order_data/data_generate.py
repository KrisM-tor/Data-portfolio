# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 08:26:38 2021

@author: wes_c for Juno College of Technology
"""

import numpy as np
import pandas as pd
import numpy.random as random

from uuid import uuid4

CONTS = ['North America', 'South America', 'Europe',\
         'Asia', 'Africa', 'Australia']
PRICE_RANGE = [49.99, 499.99]
AGE_RANGE = [18, 85]

def biased_coin(p):
    return random.uniform(0, 1) < p

def row_generate(raw_chance, cont_bias, bias_chance):
    id_ = uuid4().hex
    order_id = uuid4().hex
    age = random.randint(*AGE_RANGE)
    price = round(random.uniform(*PRICE_RANGE), 2)
    if biased_coin(raw_chance):
        price = np.nan
    continent = random.choice(CONTS)
    if continent == cont_bias:
        if biased_coin(bias_chance):
            price = np.nan
    return [id_, age, continent, price, order_id]

def generate_df(n, raw_chance=0.07,
                cont_bias='North America', bias_chance=0.3):
    rows = []
    for _ in range(n):
        rows.append(row_generate(raw_chance, cont_bias, bias_chance))
    return pd.DataFrame(rows, columns=['customer_id', 'age', 'continent',\
                                       'price', 'order_id'])

def duplicate(df, chance=0.2, raw_chance=0.07, bias_chance=0.3,
              cont_bias='North America'):
    new_rows = []
    for user in pd.unique(df['customer_id']):
        if biased_coin(chance):
            user_frame = df[df['customer_id'] == user].iloc[0, :]
            continent = random.choice(CONTS)
            price = round(random.uniform(*PRICE_RANGE), 2)
            if continent == cont_bias:
                if biased_coin(bias_chance):
                    price = np.nan
            elif biased_coin(raw_chance):
                price = np.nan
            row = [user, user_frame.age, user_frame.continent,\
                   price, uuid4().hex]
            new_rows.append(row)
    new_df = pd.DataFrame(new_rows, columns=df.columns)
    final = pd.concat([df, new_df], axis=0)
    final.reset_index(drop=True, inplace=True)
    return final

if __name__ == '__main__':
    df = generate_df(25000)
    df = duplicate(duplicate(duplicate(df)))
    df.to_csv('customer_order_data.csv', index=False)
