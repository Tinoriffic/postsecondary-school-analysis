import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

"""
Name: Faustino Andrade
CS230: Section 002
Data:  Postsecondary School Locations

This program displays and analyzes some of the information in the Post Secondary Schools dataset.
   - It provides a user interface on a streamlit sidebar that:
       - Filters the data by a new column: "REGION"
       - Filters the data by state
       - Creates a pie chart of the 'market share' of schools by region
       - Opens up a map with a scatter layer of all the locations of each school
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


def filter_region(data, user_input):
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

    return data.loc[:, ['NAME', 'CITY', 'STATE', 'ZIP', 'NMCNTY', 'REGION']][data['REGION'] == user_input]


def sort_by_state(data, state):
    return data.loc[:, ['NAME', 'CITY', 'STATE', 'ZIP', 'NMCNTY']][data['STATE'] == state]


# Checks dictionary to see if state's key exists
def find_key(val):
    for key, value in REGIONS.items():
        if val == value:
            return key

    for key, value in STATES.items():
        if val == value:
            return key

    return "State doesn't exist."


# Compiles the location for each school
def find_coordinates():
    coordinates = []
    df_length = len(df)
    for i in range(df_length):
        coordinates.append((df['NAME'].loc[i],
                            df['LAT'].loc[i],
                            df['LON'].loc[i]))

    return coordinates


# Create a pie chart of states with most schools
def get_pie_chart():
    fig, ax = plt.subplots()
    ax.axis('equal')
    regions = ['Northeast', 'West', 'Midwest', 'South', 'Other']
    schools = [0, 0, 0, 0, 0]

    # Iterates through each row (school) in the dataframe
    for i in range(len(df)):
        state = df['STATE'].loc[i]
        # Takes the state of the school and finds its region
        for val in REGIONS.values():
            if state in val:
                # Keeps tally of the amount of schools per region

                if find_key(val) == 'Northeast':
                    schools[0] += 1
                elif find_key(val) == 'West':
                    schools[1] += 1
                elif find_key(val) == 'Midwest':
                    schools[2] += 1
                elif find_key(val) == 'South':
                    schools[3] += 1
                else:
                    schools[4] += 1

    ax.set_title("Percentage of schools by region")
    ax.pie(schools, labels=regions, autopct='%.1f%%', explode=(0, 0, 0, 0.08, 0),
           shadow=False, startangle=90)

    return plt


# Create a map and scatter layer that plots all school's coordinates
def get_map():
    locations = find_coordinates()

    map_df = pd.DataFrame(locations, columns=["Name", "lat", "lon"])

    st.write("Colleges across the United States")

    # Determine where map will open, and zoom
    view_state = pdk.ViewState(
        latitude=map_df["lat"].mean(),
        longitude=map_df["lon"].mean(),
        zoom=3,
        pitch=0)

    # Scatter plot layer that inserts each location
    layer = pdk.Layer('ScatterplotLayer',
                      data=map_df,
                      get_position='[lon, lat]',
                      get_radius=450,
                      get_color=[0, 51, 102],
                      pickable=True)

    tool_tip = {"html": "School:<br/> <b>{Name}</b> ",
                "style": {"backgroundColor": "spacegray",
                          "color": "white"}}

    colleges = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[layer],
        tooltip=tool_tip
    )

    return colleges


# Builds the application
def run_streamlit():
    st.title("Post Secondary Institutions in the USA")
    st.sidebar.header("Interface")
    st.sidebar.write("")

    region_input = st.sidebar.selectbox('Sort by Region: ', ('Northeast', 'West', 'Midwest', 'South', 'Other'))
    sort_by_state_button = st.sidebar.button("Filter")

    if sort_by_state_button:
        st.write("\n\n\n\n")
        st.write("Schools in ", region_input)
        st.table(filter_region(df, region_input))

    state_input = st.sidebar.text_input('Sort by State: ', "")
    state_input_button = st.sidebar.button("Sort")

    if state_input_button:
        if state_input in STATES.values():
            key = find_key(state_input)
            state = STATES.get(key)

            st.write("Schools found in ", state)
            st.table(sort_by_state(df, key))
        else:
            st.write("State:", state_input, "not found")

    st.sidebar.write("Percentage of Schools by Region")
    pie_button = st.sidebar.button("Calculate")

    if pie_button:
        st.write("\n\n\n\n")
        st.write("")
        st.pyplot(get_pie_chart())

    st.sidebar.write("Nationwide Map of Schools")
    build_map = st.sidebar.button("Open")
    if build_map:
        st.write("\n\n\n\n\n")
        st.pydeck_chart(get_map())


run_streamlit()

