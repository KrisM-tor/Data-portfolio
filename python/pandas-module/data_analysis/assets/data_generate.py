# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 08:37:46 2021

@author: wes_c
"""

import numpy.random as random
import pandas as pd
from uuid import uuid4

LOCATION = ['AMERICAS', 'EUROPE', 'ASIA', 'AFRICA']
JOIN_RANGE = [1, 51]
JOINED_SALE = [0, 1]
EMAIL_LIST = [0, 1]
MEMBERSHIP_LEVELS = [0, 4]
SATISFACTION_SCORE = [1, 101]
COLOURS = ['BLUE', 'GREEN', 'RED', 'PINK', 'WHITE', 'BLACK']
ARTICLES = ['pants', 'shirt', 'jacket', 'skirt', 'bag']

def generate_customer_table(n_customers=1250):
    customer_list = []
    for _ in range(n_customers):
        id = uuid4().hex
        location = random.choice(LOCATION)
        joined_since = random.randint(*JOIN_RANGE)
        joined_sale = random.choice(JOINED_SALE)
        email_list = random.choice(EMAIL_LIST)
        membership = random.randint(*MEMBERSHIP_LEVELS)
        satisfaction = random.randint(*SATISFACTION_SCORE)
        customer_list.append([id, location, joined_since, joined_sale,
                          email_list, membership, satisfaction])
    df = pd.DataFrame(customer_list, columns=['customer_id', 'location',
                                          'days_since_joined',
                                          'joined_on_sale',
                                          'email_subscription',
                                          'membership_level',
                                          'satisfaction_score'])
    return df

def generate_items_table(n_items=150):
    items = []
    pants_num = 0
    shirts_num = 0
    jacket_num = 0
    skirt_num = 0
    bag_num = 0
    for sku_num in range(n_items):
        article = random.choice(ARTICLES)
        if 'pa' in article:
            num = pants_num
            title = 'pants' + str(num)
            pants_num += 1
        elif 'sh' in article:
            num = shirts_num
            title = 'shirt' + str(num)
            shirts_num += 1
        elif 'ja' in article:
            num = jacket_num
            title = 'jacket' + str(num)
            jacket_num += 1
        elif 'sk' in article:
            num = skirt_num
            title = 'skirt' + str(num)
            skirt_num += 1
        else:
            num = bag_num
            title = 'bag' + str(num)
            bag_num += 1
        colour = random.choice(COLOURS)
        items.append([title, sku_num, colour])
    items = pd.DataFrame(items, columns=['item_id', 'sku', 'colour'])
    return items

def generate_sales_table(customers, items, max_purchases=15):
    location_effect = {'AMERICAS':75, 'EUROPE':50, 'ASIA':100, 'AFRICA':25}
    purchases = []
    items = items['item_id'].values
    for _, row in customers.iterrows():
        factor = 0.008*row['days_since_joined'] +\
                 0.004*row['satisfaction_score'] +\
                 0.05*row['membership_level'] +\
                 0.05*row['email_subscription'] +\
                 0.0005*location_effect[row['location']] + random.normal(0, 0.1)
        factor = min(1, max(0, factor))
        num_purchases = max(1, round(factor*max_purchases))
        for _ in range(num_purchases):
            day_range = [JOIN_RANGE[1] - row['days_since_joined'],
                         JOIN_RANGE[1]]
            purchase_day = random.randint(*day_range)
            item = random.choice(items)
            purchases.append([row['customer_id'], purchase_day, item])
    purchases = pd.DataFrame(purchases, columns=['customer_id', 'day', 'item'])
    return purchases

if __name__ == '__main__':
    customers = generate_customer_table()
    items = generate_items_table()
    purchases = generate_sales_table(customers, items)
    customers.to_csv('customer_data.csv', index=False)
    items.to_csv('item_data.csv', index=False)
    purchases.to_csv('purchase_data.csv', index=False)
