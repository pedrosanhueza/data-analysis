# import libraries

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

st.markdown('''
<ol>
<li>What is the distribution of net worth among billionaires?</li>
<li>What is the distribution of age among billionaires?</li>
<li>Is there a correlation between age and net worth?</li>
<li>What are the most common industries among billionaires?</li>
<li>What is the gender distribution among billionaires?</li>
<li>What is the self-made status distribution among billionaires?</li>
<li>What is the country distribution among billionaires?</li>
<li>What is the position distribution among billionaires?</li>
<li>What is the average net worth of billionaires by industry?</li>
<li>What is the average age of billionaires by industry?</li>
<li>What is the average net worth of billionaires by gender?</li>
<li>What is the average age of billionaires by gender?</li>
<li>What is the average net worth of self-made billionaires compared to non-self-made billionaires?</li>
<li>What is the average age of self-made billionaires compared to non-self-made billionaires?</li>
<li>What is the average net worth of billionaires in each country?</li>
<li>What is the average age of billionaires in each country?</li>
<li>Who are the top 10 billionaires by net worth?</li>
<li>Who are the youngest and oldest billionaires?</li>
<li>What are the top industries for self-made billionaires?</li>
</ol>
''',unsafe_allow_html=True)







url = "https://www.forbes.com/billionaires/page-data/index/page-data.json"

response = requests.get(url)

json_data = response.json()

rows = json_data['result']['pageContext']['tableData']

ls_=[]

for row in rows:
    tableData = {
        k: v
        for (k, v) in row.items()
        if
        (k != 'person') & # dict
        (k != 'employment') & # dict
        (k != 'qas') & # two dicts
        (k != 'bios') & # list
        (k != 'abouts') & #list
        (k != 'csfDisplayFields') #list
        }
    ls_.append(tableData)

data = pd.DataFrame(ls_)

cols_to_drop = [
    'parentListUri',
    'organization',
    'title',
    'selfMadeRank',
    'residenceStateRegion',
    'embargo',
    'residenceMsa',
    'impactInvestor',
    'numberOfSiblings',
    'numberOfSiblingsEst',
    'bio',
    'thumbnail',
    'notableDeal',
    'valueCreated',
    'primaryIndustry',
    'portraitImage',
    'landscapeImage',
    'clients']

data.drop(cols_to_drop, axis=1, inplace=True)

data['squareImage'].fillna('https://i.forbesimg.com/media/assets/forbes_1200x1200.jpg', inplace=True)

data['country'].fillna('Not Specified', inplace=True)

data['state'].fillna('Not Specified', inplace=True)

data['city'].fillna('Not Specified', inplace=True)

data['gender'].fillna('Not Specified', inplace=True)

data['birthDate'].fillna('Not Specified', inplace=True)

data['firstName'].fillna('Not Specified', inplace=True)

df = data[[
    'rank',
    'finalWorth',
    'category',
    'personName',
    'age',
    'country',
    'state',
    'city',
    'source',
    'industries',
    'countryOfCitizenship',
    'position',
    'selfMade',
    'status',
    'gender',
    'lastName',
    'firstName',
    'netWorth'
]]

def convert_networth(value):
    abbreviations = {"B": 1000000000, "M": 1000000, "K": 1000}
    value = value.replace("$", "")
    for abbr, factor in abbreviations.items():
        if abbr in value:
            return float(value.replace(abbr, "")) * factor
    return float(value)

df['netWorth'] = df['netWorth'].apply(convert_networth)

st.markdown('''
<p><strong>Distribution of net worth:</strong> The histogram can help us understand how the net worth of billionaires is distributed. For example, we can see whether the distribution is normal, skewed, or bimodal.</p>
''',unsafe_allow_html=True)

st.dataframe(df)

# ---------------------------------------- PLOT 1 ----------------------------------------

# Set the theme for the chart
alt.themes.enable('fivethirtyeight')

# Define the chart
chart = alt.Chart(df).mark_bar(
    opacity=0.8,
    color='#008FD5'
).encode(
    x=alt.X('netWorth:Q', bin=alt.Bin(step=500000000), title='Net Worth (in billions)'),
    y=alt.Y('count()', title='Number of Billionaires'))

# Set the axis labels and font size
axis_label_font_size = 12
chart = chart.properties(
    title='Histogram of Net Worth Among Billionaires',
    width=700,
    height=400
).configure_axis(
    labelFontSize=axis_label_font_size,
    titleFontSize=axis_label_font_size,
    labelColor='gray'
).configure_title(
    fontSize=16,
    font='Helvetica Neue Light',
    fontWeight='bold')
st.altair_chart(chart, theme="streamlit", use_container_width=True)

st.markdown('''
<p><strong>Impact of outliers:</strong> By removing outliers, we can see the distribution of net worth among the majority of billionaires more clearly. This can help us better understand how wealth is distributed among the majority of billionaires.</p>
''',unsafe_allow_html=True)

# ---------------------------------------- PLOT 1.1 ----------------------------------------

Q1 = df['netWorth'].quantile(0.25)
Q3 = df['netWorth'].quantile(0.75)
IQR = Q3 - Q1

lower_fence = Q1 - 1.5 * IQR
upper_fence = Q3 + 1.5 * IQR

df_outliers_removed = df[(df['netWorth'] >= lower_fence) & (df['netWorth'] <= upper_fence)]

# Define the chart
chart = alt.Chart(df_outliers_removed).mark_bar(
    opacity=0.8,
    color='#008FD5'
).encode(
    x=alt.X('netWorth:Q', bin=alt.Bin(step=500000000), title='Net Worth (in billions)'),
    y=alt.Y('count()', title='Number of Billionaires'))

# Set the axis labels and font size
axis_label_font_size = 12
chart = chart.properties(
    title='Histogram of Net Worth Among Billionaires (Excluding Outliers)',
    width=700,
    height=400
).configure_axis(
    labelFontSize=axis_label_font_size,
    titleFontSize=axis_label_font_size,
    labelColor='gray'
).configure_title(
    fontSize=16,
    font='Helvetica Neue Light',
    fontWeight='bold')

st.altair_chart(chart, theme="streamlit", use_container_width=True)

st.markdown('''
<p><strong>Number of billionaires:</strong> The histogram shows us how many billionaires fall into each bin of net worth. This can help us understand how many billionaires are in each wealth bracket and how many billionaires are outliers.</p>
''',unsafe_allow_html=True)

# ---------------------------------------- PLOT 2 ----------------------------------------

df_outliers_removed = df[
    (df['netWorth'] < df['netWorth'].quantile(0.99)) &
    (df['age'] < df['age'].quantile(0.99)) &
    (df['age'] != 0)
]


# Define the base chart with data
base_chart = alt.Chart(df_outliers_removed).encode(
    x=alt.X('age:Q', title='Age'),
    y=alt.Y('netWorth:Q', title='Net Worth (in billions)'),
    tooltip=['personName', 'age', 'netWorth']
)

# Add the scatter plot layer
scatter = base_chart.mark_circle(
    size=60,
    opacity=0.8,
    stroke='black',
    strokeWidth=0.5,
).properties(
    title='Scatterplot of Age and Net Worth'
)

# Add the linear regression line layer
regression = base_chart.transform_regression(
    'age', 'netWorth', method='linear'
).mark_line(
    color='red',
    strokeDash=[5, 5]
)

# Combine the layers and customize the chart
chart = (scatter + regression).configure_title(
    fontSize=20,
    font='Helvetica',
    anchor='start',
    color='gray'
).configure_axis(
    grid=False,
    titleFont='Helvetica',
    labelFont='Helvetica',
    labelFontSize=14,
    labelPadding=10,
    titleFontSize=16,
    titlePadding=15,
    domainWidth=0.5,
    tickWidth=0.5,
    tickColor='gray'
).configure_view(
    strokeWidth=0
).properties(
    width=800,
    height=500
)

st.altair_chart(chart, theme="streamlit", use_container_width=True)

# Calculate correlation coefficient between age and netWorth
correlation = df[['age', 'netWorth']].corr().loc['age', 'netWorth']

# Print the correlation coefficient
st.write(f"Correlation coefficient between age and netWorth: {correlation:.2f}")

st.write(f'''
Based on the correlation coefficient of {correlation:.2f}, there appears to be a very weak positive correlation between age and net worth. However, it is important to note that correlation does not imply causation and there may be other factors that influence the relationship between age and net worth.
''')
