import streamlit as st
# import requests
# from bs4 import BeautifulSoup
import pandas as pd
# import matplotlib.pyplot as plt
# import altair as alt
# import plotly.express as px

st.markdown('''
<head>
	<title>Santiago Airport</title>
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
	<h1><strong>SANTIAGO DE CHILE AIRPORT (SCL)</strong></h1>
	<img src="https://www.swissasiatrading.com/wp-content/uploads/2018/04/72-min-1.jpg" alt="Arturo Merino Benítez International Airport (SCL) is the busiest airport in Chile.">
	</center>
    <br>
        <a href="https://www.santiago-airport.com" target="_blank"><span class="key"><strong style="color: blue;">Santiago-Airport.com</strong></span></a>
        has live data about flights in the Santiago Airport. We are analyzing particularly the 
        <a href="https://www.santiago-airport.com/scl-departures" target="_blank"><span class="key"><strong style="color: blue;">departure</strong></span></a>
        and
        <a href="https://www.santiago-airport.com/scl-arrivals" target="_blank"><span class="key"><strong style="color: blue;">arrival</strong></span></a>
        data. It has information about the status of the flights, the terminal location, the departure/arrival time, the destination/origin, and more.
</body>
''',unsafe_allow_html=True)

st.markdown('''
<h2>Data Extraction Code</h2>
	<ol>
	<li> Loops over all pages from santiago-airport extracting its data. </li>
    <li> Structures the data into a dataframe. </li>
	</ol>
''',unsafe_allow_html=True)

script_scrape = '''
import requests
from bs4 import BeautifulSoup
import pandas as pd

filterDay = ['yesterday', 'today', 'tomorrow']

filterHour = [str(i) for i in range(0, 24, 6)]

df_departures = pd.DataFrame(columns=['Destination', 'Destination Code', 'Departure', 'Flight', 'Airline', 'Terminal', 'Status', 'Date', 'Reference Day', 'url'])
for day in filterDay:
    for hour in filterHour:
        url = f'https://www.santiago-airport.com/scl-departures?day={day}&tp={hour}'
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')
        reference_day = url.split('=')[1][:-3]
        date = soup.find('option', {'selected': 'selected'}).text.split(' ')[0] if reference_day != 'Tomorrow' else soup.find('option', {'value': '?day=tomorrow'}).text.split(' ')[0]
        rows = []
        for flight in soup.find_all('div', class_='flight-row')[1:]:
            if flight.find('div', {'class', 'adsense'}): # advertisement row
                continue
            destination = flight.find('div', {'class', 'flight-col flight-col__dest-term'}).find('b').text
            destination_code = flight.find('div', {'class', 'flight-col flight-col__dest-term'}).find('span').text
            departure = flight.find('div', {'class', 'flight-col flight-col__hour'}).text.strip()
            flight_number = flight.find('div', {'class', 'flight-col flight-col__flight'}).text.strip().split('\n')
            airline = flight.find('div', {'class', 'flight-col flight-col__airline'}).text.strip().split('\n')
            terminal = flight.find('div', {'class', 'flight-col flight-col__terminal'}).text.strip()
            status = flight.find_all('a')[-1].text
            for i in range(max(len(flight_number), len(airline))):
                rows.append({
                    'Destination': destination,
                    'Destination Code': destination_code,
                    'Departure': departure,
                    'Flight': flight_number[i] if i < len(flight_number) else '',
                    'Airline': airline[i] if i < len(airline) else '',
                    'Terminal': terminal,
                    'Status': status,
                    'Date': date,
                    'Reference Day': reference_day,
                    'url': url
                })
        df_departures = pd.concat([df_departures, pd.DataFrame(rows)], ignore_index=True)

df_arrivals = pd.DataFrame(columns=['Origin', 'Origin Code', 'Departure', 'Flight', 'Airline', 'Terminal', 'Status', 'Date', 'Reference Day', 'url'])

for day in filterDay:
    for hour in filterHour:
        url = f'https://www.santiago-airport.com/scl-arrivals?day={day}&tp={hour}'
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')
        reference_day = url.split('=')[1][:-3]
        date = soup.find('option', {'selected': 'selected'}).text.split(' ')[0] if reference_day != 'Tomorrow' else soup.find('option', {'value': '?day=tomorrow'}).text.split(' ')[0]
        rows = []
        for flight in soup.find_all('div', class_='flight-row')[1:]:
            if flight.find('div', {'class', 'adsense'}): # advertisement row
                continue
            origin = flight.find('div', {'class', 'flight-col flight-col__dest-term'}).find('b').text
            origin_code = flight.find('div', {'class', 'flight-col flight-col__dest-term'}).find('span').text
            departure = flight.find('div', {'class', 'flight-col flight-col__hour'}).text.strip()
            flight_number = flight.find('div', {'class', 'flight-col flight-col__flight'}).text.strip().split('\n')
            airline = flight.find('div', {'class', 'flight-col flight-col__airline'}).text.strip().split('\n')
            terminal = flight.find('div', {'class', 'flight-col flight-col__terminal'}).text.strip()
            status = flight.find_all('a')[-1].text
            for i in range(max(len(flight_number), len(airline))):
                rows.append({
                    'Origin': origin,
                    'Origin Code': origin_code,
                    'Departure': departure,
                    'Flight': flight_number[i] if i < len(flight_number) else '',
                    'Airline': airline[i] if i < len(airline) else '',
                    'Terminal': terminal,
                    'Status': status,
                    'Date': date,
                    'Reference Day': reference_day,
                    'url': url
                })
        df_arrivals = pd.concat([df_arrivals, pd.DataFrame(rows)], ignore_index=True)
'''


# # with st.expander("Python Data Extraction Code 🐍"):
st.code(script_scrape,language="python")

df_arrivals = pd.read_csv('Analysis-Python/santiago-airport.com-flights/arrivals.csv')
df_departures = pd.read_csv('departures.csv')

st.markdown('''
<h2>Descriptive statistics</h2>
<p>Calculate the mean, median, mode, variance, standard deviation, and other measures of central tendency and dispersion to gain insights into the distribution of different variables.</p>
''',unsafe_allow_html=True)

col1, col2, col3 = st.beta_columns(3)

n_airlines_yesterday = df_arrivals[df_arrivals.Reference_Day == 'yesterday'].Airline.nunique()
n_airlines_today = df_arrivals[df_arrivals.Reference_Day == 'today'].Airline.nunique()
n_airlines_tomorrow = df_arrivals[df_arrivals.Reference_Day == 'tomorrow'].Airline.nunique()

date_yesterday = df_arrivals[df_arrivals.Reference_Day == 'yesterday'].Date.unique()[0]
date_today = df_arrivals[df_arrivals.Reference_Day == 'today'].Date.unique()[0]
date_tomorrow = df_arrivals[df_arrivals.Reference_Day == 'tomorrow'].Date.unique()[0]

with col1:
    st.metric(f"Airlines on {date_yesterday}",f"{n_airlines_today}")
with col2:
    st.metric(f"Airlines on {date_today}",f"{n_airlines_today}")
with col3:
    st.metric(f"Airlines on {date_tomorrow}",f"{n_airlines_today}")

st.markdown('''
<h2>Time Series Analysis</h2>
<p>Plot the number of flights over time and identify seasonal variations, trends, and anomalies.</p>
''',unsafe_allow_html=True)

st.markdown('''
<h2>Hypothesis Testing</h2>
<p>Test whether the average delay time of different airlines is statistically significant or not.</p>
''',unsafe_allow_html=True)

st.markdown('''
<h2>Regression analysis</h2>
<p>Explore the relationship between the departure time and the delay time or the relationship between the airline and the status of the flight.</p>
''',unsafe_allow_html=True)

# # ---------------------------------------- KPI 1 ----------------------------------------



# # Calculate the value counts of each party
# party_counts = df['Party'].value_counts()

# # Calculate the percentage of each party
# party_percentages = round(party_counts / len(df['Party']) * 100,0)

# R = int(party_percentages['R'])
# D = int(party_percentages['D'])

# col1, col2, col3 = st.beta_columns(3)

# with col1:
#     st.metric("Republicans",f"{R}%")
# with col2:
#     st.metric("Democrats",f"{D}%")
# with col3:
#     st.metric("Difference",f"{abs(R-D)}%")

# # ---------------------------------------- PLOT 1 ----------------------------------------

# script_plot1 = '''
# PARTY_NAMES = {'R': 'Republicans', 'D': 'Democrats'}

# # Replace party abbreviations with full party names
# df['Party'] = df['Party'].replace(PARTY_NAMES)

# # Create pie chart
# fig = px.pie(df, names='Party', color='Party', color_discrete_sequence=['#d62728', '#0096FF'])

# # Customize chart
# fig.update_traces(textfont_size=22, textinfo='percent+value')
# fig.update_layout(
#     legend=dict(
#         orientation='h',
#         yanchor='bottom',
#         y=1.02,
#         xanchor='right',
#         x=0.67))

# # Display chart
# st.plotly_chart(fig, use_container_width=True)
# '''

# st.code(script_plot1,language="python")


# PARTY_NAMES = {'R': 'Republicans', 'D': 'Democrats'}

# # Replace party abbreviations with full party names
# df['Party'] = df['Party'].replace(PARTY_NAMES)

# # Create pie chart
# fig = px.pie(df, names='Party', color='Party', color_discrete_sequence=['#d62728', '#0096FF'])

# # Customize chart
# fig.update_traces(textfont_size=22, textinfo='percent+value')
# fig.update_layout(
#     legend=dict(
#         orientation='h',
#         yanchor='bottom',
#         y=1.02,
#         xanchor='right',
#         x=0.67),
#     width=500,
#     height=400
# )

# # Display chart
# st.plotly_chart(fig, use_container_width=True)

# # ---------------------------------------- KPI 2 ----------------------------------------

# # Get the two highest state counts
# top_states = df['State'].value_counts().nlargest(2)

# # Get the names of the top two states
# state_names = top_states.index.tolist()

# # Store the counts in separate variables
# state1_count = top_states[0]
# state2_count = top_states[1]

# # Store the state names in separate variables
# state1_name = state_names[0]
# state2_name = state_names[1]

# total_count = df['State'].count()

# col1, col2, col3 = st.beta_columns(3)

# with col1:
#     st.metric(f"{state1_name}",f"{state1_count} seats","Highest Amount")
# with col2:
#     st.metric(f"{state2_name}",f"{state2_count} seats","2nd Highest Amount")
# with col3:
#     st.metric("All States",f"{total_count} seats")

# committee_counts = df['Committee Assignment'].str.split('|', expand=True).stack().value_counts()

# highest_committee_name = committee_counts.index[0]
# highest_committee_count = committee_counts[0]

# # st.markdown(f'''<ul><li><p>The <strong>{highest_committee_name}</strong> committee assignment has the highest count of <strong>{highest_committee_count}</strong>.</p></li></ul>''',unsafe_allow_html=True)

# # ---------------------------------------- PLOT 2 ----------------------------------------

# script_plot2 = '''
# # Group the data by Party and State, and count the number of representatives
# data = df.groupby(['Party', 'State']).size().reset_index(name='Count')

# # Create a bar chart using Altair
# chart = alt.Chart(data).mark_bar().encode(
#     y=alt.Y('State:N', sort='-x'),   # Specify the y-axis as State, and sort the values in descending order
#     x='Count:Q',                     # Specify the x-axis as Count
#     color=alt.Color('Party:N', scale=alt.Scale(range=['#0096FF', '#d62728']))   # Use blue and red colors for Democrats and Republicans, respectively
# ).properties(
#     width=800,
#     height=500,
#     title='Number of Representatives by State and Party Affiliation'   # Set the chart title
# )

# # Display the chart using Streamlit
# st.altair_chart(chart, theme="streamlit", use_container_width=True)

# '''

# st.code(script_plot2,language="python")

# data = df.groupby(['Party', 'State']).size().reset_index(name='Count')
# chart = alt.Chart(data).mark_bar().encode(
#     y=alt.Y('State:N', sort='-x'),
#     x='Count:Q',
#     color=alt.Color('Party:N', scale=alt.Scale(range=['#0096FF', '#d62728']))
# ).properties(
#     width=800,
#     height=500,
#     title='Number of Representatives by State and Party Affiliation')
# st.altair_chart(chart, theme="streamlit", use_container_width=True)

# # ---

# # Get the two highest party counts
# top_parties = df['Party'].value_counts().nlargest(2)

# # Get the names of the top two parties
# party_names = top_parties.index.tolist()

# # Store the counts in separate variables
# party1_count = top_parties[0]
# party2_count = top_parties[1]

# # Store the party names in separate variables
# party1_name = party_names[0].lower()
# party2_name = party_names[1].lower()

# st.markdown(f'''
# <h2>Data Insight</h2>
# <ul>
#     <li><p>There are more {party1_name} representatives overall than {party2_name} representatives ({party1_count} vs. {party2_count}).</p></li>
#     <li><p>The Democratic Party won more delegates overall, with a total of 104 delegates compared to the Republican Party's 70 delegates.</p></li>
#     <li><p>California has the highest number of delegates, with 40 for the Democratic Party and 12 for the Republican Party.</p></li>
#     <li><p>Texas is the second most significant state, with 13 delegates for the Democratic Party and 25 delegates for the Republican Party.</p></li>
#     <li><p>Several states, including Alaska, Kansas, Kentucky, Louisiana, Mississippi, Northern Mariana Islands, South Carolina, Tennessee, Virgin Islands, and Wyoming, only had one delegate for either the Democratic or Republican Party.</p></li>
#     <li><p>There are some states, such as Arizona, Colorado, Georgia, Michigan, Minnesota, Nevada, New Hampshire, and Pennsylvania, where both parties won significant numbers of delegates.</p></li>
#     <li><p>It's worth noting that some US territories are included in this dataset, such as American Samoa, Guam, Northern Mariana Islands, and Puerto Rico, which collectively won three delegates for the Republican Party.</p></li>
# </ul>
# ''',unsafe_allow_html=True)
