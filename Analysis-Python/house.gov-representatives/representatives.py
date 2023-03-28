# import libraries

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px

st.markdown('''
<head>
	<title>US House of Representatives</title>
	<link rel="stylesheet" type="text/css" href="style.css">
    <style>
		img {
			width: 100%;
			height: 5%;
			object-fit: cover;
		}
	</style>
</head>
<body>
    <center>
	<h1><strong>US House of Representatives</strong></h1>
	<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Flag_of_the_United_States_House_of_Representatives.svg/2560px-Flag_of_the_United_States_House_of_Representatives.svg.png" alt="Flag of the United States House of Representatives">
	</center><br>
    <p>The <span class="key"><strong style="color: blue;">U.S. House of Representatives</strong></span>, alongside the U.S. Senate, concoct federal laws that govern the land.\nThe code, a fine tool of extraction, fetches Congressmen's data from <a href="https://www.house.gov/representatives" target="_blank"><span class="key"><strong style="color: blue;">house.gov/representatives</strong></span></a> to form a handy table. It's got their name, district, party, and committee assignment. The data, ripe for the plucking, can be used for a spot of exploratory analysis.</p></body>
''',unsafe_allow_html=True)

script_scrape = '''
# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define URL and user-agent headers
url = "https://www.house.gov/representatives"
headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}

# Send a request to the website and get the HTML response
response = requests.get(url, headers=headers)

# Parse the HTML response using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Extract all tables from the HTML page
tables = soup.select('table')

# Loop through each table and extract relevant information
rows = []
for table in tables[:56]:
    # Extract information from table and store it in a dictionary
    row = {}
    row['District'] = [x.text.strip() for x in table.select('td')][0::6]
    row['Name'] = [x.text.strip() for x in table.select('td')][1::6]
    row['Party'] = [x.text.strip() for x in table.select('td')][2::6]
    row['Office Room'] = [x.text.strip() for x in table.select('td')][3::6]
    row['Phone'] = [x.text.strip() for x in table.select('td')][4::6]
    row['Committee Assignment'] = [x.text.strip() for x in table.select('td')][5::6]
    row['State'] = table.select_one('caption').text.strip()

    # Convert the dictionary to a DataFrame and append to a list
    df_state = pd.DataFrame(row)
    rows.append(df_state)

# Concatenate all DataFrames into one
df = pd.concat(rows)
'''

st.markdown('''
<h2>Code Explanation: Web Scrape</h2>
<p>This code extracts US House of Representatives' district representatives' information from the government website using BeautifulSoup and stores it in a table format using pandas.</p>
''',unsafe_allow_html=True)

# with st.expander("Python Data Extraction Code 🐍"):
st.code(script_scrape,language="python")

url = "https://www.house.gov/representatives"
headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.select('table')
rows = []
for table in tables[:56]:
    row = {}
    row['District']             = [x.text.strip() for x in table.select('td')][0::6]
    row['Name']                 = [x.text.strip() for x in table.select('td')][1::6]
    row['Party']                = [x.text.strip() for x in table.select('td')][2::6]
    row['Office Room']          = [x.text.strip() for x in table.select('td')][3::6]
    row['Phone']                = [x.text.strip() for x in table.select('td')][4::6]
    row['Committee Assignment'] = [x.text.strip() for x in table.select('td')][5::6]
    row['State']                = table.select_one('caption').text.strip()
    df_state = pd.DataFrame(row)
    rows.append(df_state)
df = pd.concat(rows)

st.markdown('''
<h2>Data Overview</h2>
<p>Now that we have we've got some awesome data to work with! Let's dive in and uncover some cool insights!</p>
''',unsafe_allow_html=True)

# ---------------------------------------- KPI 1 ----------------------------------------

# Calculate the value counts of each party
party_counts = df['Party'].value_counts()

# Calculate the percentage of each party
party_percentages = round(party_counts / len(df['Party']) * 100,0)

R = int(party_percentages['R'])
D = int(party_percentages['D'])

col1, col2, col3 = st.beta_columns(3)

with col1:
    st.metric("Republicans",f"{R}%")
with col2:
    st.metric("Democrats",f"{D}%")
with col3:
    st.metric("Difference",f"{abs(R-D)}%")

# ---------------------------------------- PLOT 1 ----------------------------------------

script_plot1 = '''
PARTY_NAMES = {'R': 'Republicans', 'D': 'Democrats'}

# Replace party abbreviations with full party names
df['Party'] = df['Party'].replace(PARTY_NAMES)

# Create pie chart
fig = px.pie(df, names='Party', color='Party', color_discrete_sequence=['#d62728', '#0096FF'])

# Customize chart
fig.update_traces(textfont_size=22, textinfo='percent+value')
fig.update_layout(
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=0.67))

# Display chart
st.plotly_chart(fig, use_container_width=True)
'''

st.code(script_plot1,language="python")


PARTY_NAMES = {'R': 'Republicans', 'D': 'Democrats'}

# Replace party abbreviations with full party names
df['Party'] = df['Party'].replace(PARTY_NAMES)

# Create pie chart
fig = px.pie(df, names='Party', color='Party', color_discrete_sequence=['#d62728', '#0096FF'])

# Customize chart
fig.update_traces(textfont_size=22, textinfo='percent+value')
fig.update_layout(
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=0.67),
    width=500,
    height=400
)

# Display chart
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------- KPI 2 ----------------------------------------

# Get the two highest state counts
top_states = df['State'].value_counts().nlargest(2)

# Get the names of the top two states
state_names = top_states.index.tolist()

# Store the counts in separate variables
state1_count = top_states[0]
state2_count = top_states[1]

# Store the state names in separate variables
state1_name = state_names[0]
state2_name = state_names[1]

total_count = df['State'].count()

col1, col2, col3 = st.beta_columns(3)

with col1:
    st.metric(f"{state1_name}",f"{state1_count} seats","Highest Amount")
with col2:
    st.metric(f"{state2_name}",f"{state2_count} seats","2nd Highest Amount")
with col3:
    st.metric("All States",f"{total_count} seats")

committee_counts = df['Committee Assignment'].str.split('|', expand=True).stack().value_counts()

highest_committee_name = committee_counts.index[0]
highest_committee_count = committee_counts[0]

# st.markdown(f'''<ul><li><p>The <strong>{highest_committee_name}</strong> committee assignment has the highest count of <strong>{highest_committee_count}</strong>.</p></li></ul>''',unsafe_allow_html=True)

# ---------------------------------------- PLOT 2 ----------------------------------------

script_plot2 = '''
# Group the data by Party and State, and count the number of representatives
data = df.groupby(['Party', 'State']).size().reset_index(name='Count')

# Create a bar chart using Altair
chart = alt.Chart(data).mark_bar().encode(
    y=alt.Y('State:N', sort='-x'),   # Specify the y-axis as State, and sort the values in descending order
    x='Count:Q',                     # Specify the x-axis as Count
    color=alt.Color('Party:N', scale=alt.Scale(range=['#0096FF', '#d62728']))   # Use blue and red colors for Democrats and Republicans, respectively
).properties(
    width=800,
    height=500,
    title='Number of Representatives by State and Party Affiliation'   # Set the chart title
)

# Display the chart using Streamlit
st.altair_chart(chart, theme="streamlit", use_container_width=True)

'''

st.code(script_plot2,language="python")

data = df.groupby(['Party', 'State']).size().reset_index(name='Count')
chart = alt.Chart(data).mark_bar().encode(
    y=alt.Y('State:N', sort='-x'),
    x='Count:Q',
    color=alt.Color('Party:N', scale=alt.Scale(range=['#0096FF', '#d62728']))
).properties(
    width=800,
    height=500,
    title='Number of Representatives by State and Party Affiliation')
st.altair_chart(chart, theme="streamlit", use_container_width=True)

# ---

# Get the two highest party counts
top_parties = df['Party'].value_counts().nlargest(2)

# Get the names of the top two parties
party_names = top_parties.index.tolist()

# Store the counts in separate variables
party1_count = top_parties[0]
party2_count = top_parties[1]

# Store the party names in separate variables
party1_name = party_names[0].lower()
party2_name = party_names[1].lower()

st.markdown(f'''
<h2>Data Insight</h2>
<ul>
    <li><p>There are more {party1_name} representatives overall than {party2_name} representatives ({party1_count} vs. {party2_count}).</p></li>
    <li><p>The Democratic Party won more delegates overall, with a total of 104 delegates compared to the Republican Party's 70 delegates.</p></li>
    <li><p>California has the highest number of delegates, with 40 for the Democratic Party and 12 for the Republican Party.</p></li>
    <li><p>Texas is the second most significant state, with 13 delegates for the Democratic Party and 25 delegates for the Republican Party.</p></li>
    <li><p>Several states, including Alaska, Kansas, Kentucky, Louisiana, Mississippi, Northern Mariana Islands, South Carolina, Tennessee, Virgin Islands, and Wyoming, only had one delegate for either the Democratic or Republican Party.</p></li>
    <li><p>There are some states, such as Arizona, Colorado, Georgia, Michigan, Minnesota, Nevada, New Hampshire, and Pennsylvania, where both parties won significant numbers of delegates.</p></li>
    <li><p>It's worth noting that some US territories are included in this dataset, such as American Samoa, Guam, Northern Mariana Islands, and Puerto Rico, which collectively won three delegates for the Republican Party.</p></li>
</ul>
''',unsafe_allow_html=True)
