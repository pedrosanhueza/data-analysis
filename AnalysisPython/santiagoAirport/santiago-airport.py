import streamlit as st
# import requests
# from bs4 import BeautifulSoup
import pandas as pd
import time
import matplotlib.pyplot as plt
import altair as alt
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
    <br><br>
        <a href="https://www.santiago-airport.com" target="_blank"><span class="key"><strong style="color: blue;">Santiago-Airport.com</strong></span></a>
        has live data about flights in the Santiago Airport. We are analyzing particularly the 
        <a href="https://www.santiago-airport.com/scl-departures" target="_blank"><span class="key"><strong style="color: blue;">departure</strong></span></a>
        and
        <a href="https://www.santiago-airport.com/scl-arrivals" target="_blank"><span class="key"><strong style="color: blue;">arrival</strong></span></a>
        data. It has information about the status of the flights, the terminal location, the departure/arrival time, the destination/origin, and more.
</body>
<br><br>
''',unsafe_allow_html=True)

if st.button('Refresh Data'):
    from slcAirportFlights import df_arrivals, df_departures

else:
	df_arrivals = pd.read_csv('AnalysisPython/santiagoAirport/arrivals.csv')
	df_departures = pd.read_csv('AnalysisPython/santiagoAirport/departures.csv')

# # ---------------------------------------- Tabs ----------------------------------------

tab1_Extraction_Code, tab2_Descriptive_Statistics, tab3_Time_Series_Analysis, tab4_Hypothesis_Testing, tab5_Regression_Analysis, tab6_Conclusion = st.tabs([
    "Data Extraction Code", 
    "Descriptive statistics",
    "Time Series Analysis",
    "Hypothesis Testing",
    "Regression analysis",
    "Conclusion"])

with tab1_Extraction_Code:

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
				flight_number = flight.find('div',{'class','flight-col flight-col__flight'}).text.strip().split('\\n')
				airline = flight.find('div',{'class','flight-col flight-col__airline'}).text.strip().split('\\n')
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
				flight_number = flight.find('div',{'class','flight-col flight-col__flight'}).text.strip().split('\\n')
				airline = flight.find('div',{'class','flight-col flight-col__airline'}).text.strip().split('\\n')
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

	st.markdown('''<h2>Code Output</h2>''',unsafe_allow_html=True)
    
	st.code("st.dataframe(df_departures)",language="python")
    
	st.dataframe(df_departures)
    
	st.code("st.dataframe(df_arrivals)",language="python")

	st.dataframe(df_arrivals)
        
	st.markdown('''<br><br>''',unsafe_allow_html=True)

# # ---------------------------------------- Descriptive statistics ----------------------------------------

with tab2_Descriptive_Statistics:
	st.markdown('''
	<h2>Descriptive statistics</h2>
	<p>Calculate the mean, median, mode, variance, standard deviation, and other measures of central tendency and dispersion to gain insights into the distribution of different variables.</p>
	<o>
		<li>

	''',unsafe_allow_html=True)



	df_grouped_arrivals = df_arrivals.groupby(['Origin']).size().reset_index(name='Count')

	# create the bar chart using Altair
	chart = alt.Chart(df_grouped_arrivals).mark_bar().encode(
		y=alt.Y('Origin:N', sort='-x'),   # specify the y-axis as Origin, and sort the values in descending order
		x='Count:Q',                     # specify the x-axis as Count
		tooltip=['Origin', 'Count'],   # add a tooltip that shows the Origin and Count
		text=alt.Text('Count:Q', format=',d')  # add text to each bar to display the Count with comma separators
	).properties(
		width=800,
		height=500,
		title='Number of Flights by Origin Frequency'   # set the chart title
	)

	# remove the x-axis
	chart.configure_axisX(
		tickOpacity=0,
		labelOpacity=0
	)

	# display the chart using Streamlit
	st.altair_chart(chart, theme="streamlit", use_container_width=True)

	col1, col2, col3 = st.beta_columns(3)

	n_airlines_yesterday = df_arrivals[df_arrivals['Reference Day'] == 'yesterday'].Airline.nunique()
	n_airlines_today = df_arrivals[df_arrivals['Reference Day'] == 'today'].Airline.nunique()
	n_airlines_tomorrow = df_arrivals[df_arrivals['Reference Day'] == 'tomorrow'].Airline.nunique()

	date_yesterday = df_arrivals[df_arrivals['Reference Day'] == 'yesterday'].Date.unique()[0]
	date_today = df_arrivals[df_arrivals['Reference Day'] == 'today'].Date.unique()[0]
	date_tomorrow = df_arrivals[df_arrivals['Reference Day'] == 'tomorrow'].Date.unique()[0]

	with col1:
		st.metric(f"Airlines on {date_yesterday}",f"{n_airlines_today}")
	with col2:
		st.metric(f"Airlines on {date_today}",f"{n_airlines_today}")
	with col3:
		st.metric(f"Airlines on {date_tomorrow}",f"{n_airlines_today}")

with tab3_Time_Series_Analysis:
	st.markdown('''
	<h2>Time Series Analysis</h2>
	<p>Plot the number of flights over time and identify seasonal variations, trends, and anomalies.</p>
	''',unsafe_allow_html=True)

with tab4_Hypothesis_Testing:
	st.markdown('''
	<h2>Hypothesis Testing</h2>
	<p>Test whether the average delay time of different airlines is statistically significant or not.</p>
	''',unsafe_allow_html=True)

with tab5_Regression_Analysis:
	st.markdown('''
	<h2>Regression analysis</h2>
	<p>Explore the relationship between the departure time and the delay time or the relationship between the airline and the status of the flight.</p>
	''',unsafe_allow_html=True)

# # ---------------------------------------- KPI 1 ----------------------------------------