import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

"""
"""

# Significant Constants
DATA_SET = "Postsecondary_School_Locations_-_Current.csv"
NEW_ENGLAND = ('Maine', 'Vermont', 'New Hampshire', 'Massachusetts', 'Connecticut', 'Rhode Island')
STATES = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
          'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
          'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois',
          'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
          'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan',
          'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana',
          'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
          'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota',
          'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island',
          'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
          'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virgina', 'WA': 'Washington', 'WV': 'West Virgina',
          'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'Washington DC', 'PR': 'Puerto Rico'}
REGIONS = {'Northeast': ('CT', 'DC', 'DE', 'ME', 'MA', 'NH', 'NJ', 'NY', 'RI', 'VT', 'PA'),
           'West': ('AK', 'AZ', 'CA', 'CO', 'HI', 'ID', 'MT', 'NV', 'NM', 'OR', 'UT', 'WA', 'WY'),
           'Midwest': ('IL', 'IN', 'IA', 'KS', 'MI', 'MN', 'MO', 'NE', 'ND', 'OH', 'SD', 'WI'),
           'South': ('AL', 'AR', 'DE', 'FL', 'GA', 'KY', 'LA', 'MD', 'MS', 'NC', 'OK', 'SC', 'TN', 'TX', 'VA', 'WV'),
           'Other': ('PR', 'NULL')}

df = pd.read_csv(DATA_SET)


def find_key(val):
    for key, value in REGIONS.items():
        if val == value:
            return key

    return "State doesn't exist."


region = []
for i in range(len(df)):
    state = df['STATE'].loc[i]
    for val in REGIONS.values():
        if state in val:
            region.append(find_key(val))
            continue

remove = len(region) - len(df)
region = region[:len(region) - remove]

df['REGION'] = region


        if state_input in STATES.values():
            key = find_key(state_input)
            print(key)
            state = STATES.get(key)

            st.write("Schools found in ", state)
            st.table(sort_by_state(df, state))

# print(df.loc[:, ['NAME', 'CITY', 'STATE', 'ZIP', 'NMCNTY']][df['REGION'] == region])
print(region)
print(len(region))
print(len(df))


