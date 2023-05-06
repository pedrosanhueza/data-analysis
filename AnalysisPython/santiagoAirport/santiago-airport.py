import streamlit as st
# import requests
# from bs4 import BeautifulSoup
import pandas as pd
import time
import matplotlib.pyplot as plt
import altair as alt
# import plotly.express as px
from scipy.stats import chi2_contingency


st.set_page_config(
	page_title='Santiago Airport',
	page_icon=':airplane:',
	layout='wide',
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
			header {visibility: hidden;}
			"""

st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown('''
<head>
	<title>Santiago Airport</title>
	<link rel="stylesheet" type="text/css" href="style.css">
    <style>
		img {
			width: 50%;
			height: 5%;
			object-fit: cover;
		}
		h1 {
			font-size: 60px;
		}
	</style>
</head>
<body>
    <center>
	<h1><strong>SANTIAGO AIRPORT</strong></h1>
	<br>
	<img src="https://www.swissasiatrading.com/wp-content/uploads/2018/04/72-min-1.jpg" alt="Arturo Merino Benítez International Airport (SCL) is the busiest airport in Chile.">
    <br><br>
	The website 
    <a href="https://www.santiago-airport.com" target="_blank"><span class="key">
		Santiago-Airport.com
	</span></a>
    provides real-time data on flight departures and arrivals from Santiago International Airport.
	</center>
</body>
<br><br>
''',unsafe_allow_html=True)

if st.button('Refresh Data'):
    st.info('Takes about 10 seconds to refresh', icon='⏰')
    from slcAirportFlights import df_arrivals, df_departures
    today_date = df_arrivals[df_arrivals['Reference Day'] == 'today'].Date.iloc[0]
    st.success(f'Data refreshed ({today_date})', icon='✅')

else:
	df_arrivals = pd.read_csv('AnalysisPython/santiagoAirport/arrivals.csv')
	df_departures = pd.read_csv('AnalysisPython/santiagoAirport/departures.csv')

	df_arrivals['Date_Time'] = pd.to_datetime(df_arrivals['Date_Time'])
	df_departures['Date_Time'] = pd.to_datetime(df_departures['Date_Time'])

# # ---------------------------------------- Tabs ----------------------------------------

tab1_Extraction_Code, tab2_Descriptive_Statistics, tab3_Time_Series_Analysis, tab4_Hypothesis_Testing, tab5_Conclusion = st.tabs([
    "Data", 
    "Descriptive",
    "Time Series Analysis",
    "Hypothesis Testing",
    "Conclusion"])

with tab1_Extraction_Code:

	st.markdown('''
	<h2>Data Extraction Code</h2>
		<ol>
		<li> Loops over all pages from
		    <a href="https://www.santiago-airport.com" target="_blank">
			santiago-airport
			</a>
			extracting its data.</li>
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

	st.markdown('''
	<h2>Code Output</h2>
	<p>
	Display output table
	</p>
	<br>
	''',unsafe_allow_html=True)
    
	st.code("st.dataframe(df_departures)",language="python")
    
	st.dataframe(df_departures)
    
	st.code("st.dataframe(df_arrivals)",language="python")

	st.dataframe(df_arrivals)
        
	st.markdown('''<br><br>''',unsafe_allow_html=True)

# # ---------------------------------------- Descriptive Statistics ----------------------------------------


with tab2_Descriptive_Statistics:
	st.markdown(f'''<h2>Descriptive Analysis</h2>''',unsafe_allow_html=True)

	st.markdown(f'''<br><br><br>''',unsafe_allow_html=True)

	airlines_amount = df_departures.Airline.nunique()
	top_airlines_amount = 6
	top_airlines_percentage_from_total = round(top_airlines_amount / airlines_amount * 100)
	airlines_flights_sum = df_departures.groupby('Airline')['Flight'].count().sum()
	top_airlines_flights_sum = df_departures.groupby('Airline')['Flight'].count().nlargest(top_airlines_amount).sum()
	top_airlines_flights_percentage_from_total = round(top_airlines_flights_sum/airlines_flights_sum*100)

	col1, col2, col3 = st.columns([1,2,1])

	with col1:
		st.write("")

	with col2:
		
		font_size = 24

		st.markdown(f'''
		<div style="text-align: center;">
		<p style="font-family: Arial, sans-serif; font-size: 16px;">
			Santiago Airport hosts
				<span style="color: gray; font-weight: bold; font-size: {font_size}px;">
			   {airlines_amount}
				</span>
				airlines, managing
				<span style="color: gray; font-weight: bold; font-size: {font_size}px;">
				{airlines_flights_sum}
				</span>
				flights, from which the 
		</p>
		</div>
		<div style="text-align: center;">
			<p>
				top
				<span style="color: orange; font-weight: bold; font-size: {font_size}px;">
					{top_airlines_amount} Airlines
				</span>
				<!-- ({top_airlines_percentage_from_total}%) -->
				account for the
				<span style="color: orange; font-weight: bold; font-size: {font_size}px;">
					{top_airlines_flights_percentage_from_total}%
				</span>
				<!-- ({top_airlines_flights_sum}) -->
				 of all flights.
			</p>
		</div>
		<br>
		''',unsafe_allow_html=True)

	with col3:
		st.write("")

	df_counts = df_departures.groupby('Airline').agg({'Flight': 'count'}).reset_index()
	df_counts = df_counts.rename(columns={'Flight': 'FlightCount'})
	df_counts = df_counts.sort_values('FlightCount', ascending=False)
	df_counts['Rank'] = range(1, len(df_counts) + 1)
	chart = alt.Chart(df_counts).mark_bar().encode(
		y=alt.Y('Airline:N', sort='-x', title=''),
		x=alt.X('FlightCount:Q', title='Flights Amount'),
		color=alt.condition(
			alt.datum.Rank <= top_airlines_amount,
			alt.value('orange'),
			alt.value('gray')
		)
	).properties(
	title=alt.TitleParams(text='Flights by Airline',align='center',subtitle='Number of flights per airline',subtitleColor='gray'),
	).configure_axis(
    grid=False
	)
	st.altair_chart(chart, use_container_width=True)

	st.markdown(f'''<br><br><br>''',unsafe_allow_html=True)

	# ------- Destination Cities by Flights -------

	df_international_flights = df_departures[df_departures['Destination Country'] != 'Chile']
	international_percentage = len(df_international_flights) / len(df_departures) * 100

	st.markdown(f'''
		<div style="text-align: center;">
			<p style="font-family: Arial, sans-serif; font-size: 16px;">
				<span style="color: orange; font-weight: bold; font-size: {font_size}px;">
					International
				</span>
				destinations account for the
				<span style="color: orange; font-weight: bold; font-size: {font_size}px;">
					{international_percentage:.1f}%
				</span>
				of all flights.
			</p>
		</div>
		<br>
	''',unsafe_allow_html=True)

	df_departures_grouped = df_departures.groupby(['Destination City','Destination Country']).size().reset_index(name='Count')
	chart = alt.Chart(df_departures_grouped).mark_bar().encode(
		y=alt.Y('Destination City:N', sort='-x', title=''),
		x='Count:Q',
		tooltip=['Destination City', 'Count'],
		text=alt.Text('Count:Q', format=',d'),
		color=alt.condition(
			alt.datum['Destination Country'] == 'Chile',
			alt.value('gray'),  # set color to orange if Destination Country is Chile
			alt.value('orange')     # set color to gray otherwise
		)
	).properties(
	title=alt.TitleParams(text='Flights by Destination',align='center',subtitle='Number of flights per destination city',subtitleColor='gray'),
	).configure_axis(
    grid=False
	)

	st.altair_chart(chart, theme="streamlit", use_container_width=True)

	# st.markdown(f'''
	# <center>
	# 	<img src="https://images.cdn.centreforaviation.com/stories/ctc/2018/07/SCL001.png" style="width: 30%; height: 5%; object-fit: cover;">
	# </center><br><br>
	# ''',unsafe_allow_html=True)

with tab3_Time_Series_Analysis:
	st.markdown('''
	<h2>Time Series Analysis</h2>
	''',unsafe_allow_html=True)

	col1, col2, col3 = st.columns([1,2,1])
	with col1:
		st.write("")
	with col2:
		font_size = 24
		st.markdown(f'''
		<br><br>
		<div style="text-align: center;">
			<p>
				<span style="color: gray; font-weight: bold; font-size: {font_size}px;">
					Most departures
				</span>
					occure
				<span style="color: orange; font-weight: bold; font-size: {font_size}px;">
					before noon.
			</p>
			<p>
				<span style="color: gray; font-weight: bold; font-size: {font_size}px;">
					Most arrivals
				</span>
					occure
				<span style="color: orange; font-weight: bold; font-size: {font_size}px;">
					after noon.
				</span>
			</p>
		</div>
		<br><br><br>
		''',unsafe_allow_html=True)
	with col3:
		st.write("")

	# ---------------------------------------- Hourly Flights ----------------------------------------

	col_departures, col_empty2, col_arrivals = st.columns([1,0.1,1]) 

	with col_departures:
		df_departures['Hour'] = df_departures['Date_Time'].dt.hour

		skewness = round(df_departures['Hour'].skew(),2)
		skewness_kpi = (
		"right-skewed" if skewness > 0.01 else
		"left-skewed" if skewness < -0.01 else
		"zero-skewed")
		skewness_description= (
		"highly skewed" if skewness > 0.1 else
		"moderately skewed" if skewness < -0.1 else
		"approximately symmetric")
		
		kurtosis = round(df_departures['Hour'].kurtosis(),2)
		if kurtosis < -0.3:
			kurtosis_descriptive = "infrequent outliers"
		elif kurtosis > 0.3:
			kurtosis_descriptive = "defined outliers"
		else:
			kurtosis_descriptive = "normal dispersation"

		st.markdown(f'''<h3>Flights amount per hour</h3><h6>Departure Flights</h6><br><br>''',unsafe_allow_html=True)

		kpi1, kpi2 = st.columns(2)

		kpi1.metric(label='Skewness', value=skewness, delta=skewness_kpi)
		kpi2.metric(label='Kurtosis', value=kurtosis, delta=kurtosis_descriptive)

		st.markdown(f'''
		<p>
			The distribution of flights over time is
			<span style="color: orange; font-weight: bold; font-size: {font_size}px;"> {skewness_description} 
			</span>
			with statistically {kurtosis_descriptive}
		<br>
		''',unsafe_allow_html=True)

		hourly_flights = df_departures.groupby('Hour').count()['Flight'].reset_index(name='Count')
		chart = alt.Chart(hourly_flights).transform_calculate(HourLabel="datum.Hour + ':00'").mark_bar().encode(
			x=alt.X('HourLabel:N',sort=alt.SortField('Hour'), title='Hours of the Day',axis=alt.Axis(labelAngle=0)),
			y=alt.Y('Count:Q', title='',axis=alt.Axis(labels=False),scale=alt.Scale(domain=[0, 100])),color=alt.condition(
			alt.datum.Count >= hourly_flights.nlargest(2, 'Count')['Count'].min(),
			alt.value('orange'),alt.value('gray'))
		).properties(height=700,title=alt.TitleParams(text='',align='left',subtitle='',subtitleColor='gray'),
		).configure_axis(grid=False
		).configure_title(fontSize=20,fontWeight='bold')
		st.altair_chart(chart, use_container_width=True)

	with col_empty2:
		st.write('')

	with col_arrivals:
		df_arrivals['Hour'] = df_arrivals['Date_Time'].dt.hour

		skewness = round(df_arrivals['Hour'].skew(),2)
		skewness_kpi = (
		"right-skewed" if skewness > 0.01 else
		"left-skewed" if skewness < -0.01 else
		"zero-skewed")
		skewness_description= (
		"highly skewed" if skewness > 0.1 else
		"moderately skewed" if skewness < -0.1 else
		"approximately symmetric")
		
		kurtosis = round(df_arrivals['Hour'].kurtosis(),2)
		if kurtosis < -0.3:
			kurtosis_descriptive = "infrequent outliers"
		elif kurtosis > 0.3:
			kurtosis_descriptive = "defined outliers"
		else:
			kurtosis_descriptive = "normal dispersation"

		st.markdown(f'''<h3>Flights amount per hour</h3><h6>Arrival Flights</h6><br><br>''',unsafe_allow_html=True)

		kpi1, kpi2 = st.columns(2)

		kpi1.metric(label='Skewness', value=skewness, delta=skewness_kpi)
		kpi2.metric(label='Kurtosis', value=kurtosis, delta=kurtosis_descriptive)

		st.markdown(f'''
		<p>
			The distribution of flights over time is
			<span style="color: orange; font-weight: bold; font-size: {font_size}px;"> {skewness_description} 
			</span>
			with statistically {kurtosis_descriptive}
		<br>
		''',unsafe_allow_html=True)

		hourly_flights = df_arrivals.groupby('Hour').count()['Flight'].reset_index(name='Count')
		chart = alt.Chart(hourly_flights).transform_calculate(HourLabel="datum.Hour + ':00'").mark_bar().encode(
			x=alt.X('HourLabel:N',sort=alt.SortField('Hour'),title='Hours of the Day',axis=alt.Axis(labelAngle=0)),
			y=alt.Y('Count:Q', title='',axis=alt.Axis(labels=False),scale=alt.Scale(domain=[0, 100])),color=alt.condition(
			alt.datum.Count >= hourly_flights.nlargest(2, 'Count')['Count'].min(),alt.value('orange'),alt.value('gray'))
		).properties(height=700,title=alt.TitleParams(text='Flights per Hour', align='left', subtitle='Arrivals',subtitleColor='gray'),
		).configure_axis(grid=False
		).configure_title(fontSize=20,fontWeight='bold')
		st.altair_chart(chart, use_container_width=True)
		
	st.markdown(f'''
	<div style="text-align: center;">
		<p>
			The drop of flights from the hours: 1:00 am to 3:00am for departures is
		<span style="color: orange; font-weight: bold;">
			not
		</span>
			statistically significant across the day based on the skewness and kurtosis of the distribution.
		<br>
			Although there is a difference between departure and arrival flights over time, it is
		<span style="color: orange; font-weight: bold;">
			not
		</span>
			statistically significant across the day based on the skewness and kurtosis of the distribution.
		</p>
	</div>
	<br><br>
	''',unsafe_allow_html=True)

with tab4_Hypothesis_Testing:
	st.markdown('''<h2>Hypothesis Testing</h2>''',unsafe_allow_html=True)

	st.markdown(f'''
	<br><br>
	<div style="text-align: center;">
	<h3>
		Relationship Between the Terminal and Flight
	</h3>
	''',unsafe_allow_html=True)

	st.latex(r'''H_0: \text{There is no significant difference between the number of flights arriving at each terminal}''')
	st.latex(r'''H_a: \text{There is a significant difference between the number of flights arriving at each terminal}''')	
	
	df_arrivals.Terminal = df_arrivals.Terminal.astype('float')
	df_arrivals_terminal = df_arrivals[(df_arrivals['Terminal']==1) | (df_arrivals['Terminal'] == 2)]

	chart = alt.Chart(df_arrivals_terminal).transform_calculate(Terminal="'Terminal '+datum.Terminal"
	).mark_bar(
		size=120
	).encode(
		x=alt.X('Terminal:O', title='', axis=alt.Axis(labelAngle=0)),
		y=alt.Y('count()', title='')
	).properties(height=500,width=100
	).configure_axis(grid=False
	)

	col1, col2, col3 = st.columns([1,1,1])
	with col1:
		st.write('')
	with col2:
		st.altair_chart(chart, use_container_width=True)
	with  col3:
		st.write('')

	st.markdown(f'''
	<div style="text-align: center;">
	<h6>
		Chi-Square Test of Independence
	</h6>
	''',unsafe_allow_html=True)

	st.latex(r'''\tilde{\chi}^2=\frac{1}{d}\sum_{k=1}^{n} \frac{(O_k - E_k)^2}{E_k}''')
	
	st.code('''
	contingency_table = pd.crosstab(df_arrivals_terminal['Terminal'], df_arrivals_terminal['Flight'])
	stat, p, dof, expected = chi2_contingency(contingency_table)
	print(f'The chi-square test of independence is performed with a p-value of {p}')
	''',language='python')

	contingency_table = pd.crosstab(df_arrivals_terminal['Terminal'], df_arrivals_terminal['Flight'])
	stat, p, dof, expected = chi2_contingency(contingency_table)
	
	st.latex(r'''\text{The chi-square test of independence is performed with a p-value of } %s \approx 0.00''' %p)

	col1,col2,col3 = st.columns([0.7,1,0.7])
	with col1:
		st.write('')
	with col2:
		st.markdown(f'''
		<div style="text-align: center;">
		<p>
		The p-value extremely close to zero indicates that the probability of frequencies of flights arriving at each terminal under the assumption of independence between the Terminal and Flight variables is extremely low.
		<br><br>
		In other words, <b> there is a statistically significant association</b> between the Terminal and Flight variables.
		</p>
		</div>
		''',unsafe_allow_html=True)
	with col3:
		st.write('')

# ---

	st.markdown(f'''
	<br><br>
	<div style="text-align: center;">
	<h3>
		Relationship Between the Arrival Time and City of Origin
	</h3>
	''',unsafe_allow_html=True)

	st.latex(r'''H_0: \text{There is no significant difference between the arriving time and city of origin}''')
	st.latex(r'''H_a: \text{There is a significant difference between the arriving time and city of origin}''')	
	
	city_list = tuple(df_arrivals['Origin City'].unique())
	
	col1,col2 = st.columns([1,1])

	with col1:
		country_option_1 = st.selectbox("City A",city_list)
	with col2:
		country_option_2 = st.selectbox("City B",city_list)

	col1, col2, col3 = st.columns([1,1,1])
	with col1:
		st.write('')
	with col2:
		st.altair_chart(chart, use_container_width=True)
	with  col3:
		st.write('')

	st.markdown(f'''
	<div style="text-align: center;">
	<h6>
		Chi-Square Test of Independence
	</h6>
	''',unsafe_allow_html=True)

	st.latex(r'''\tilde{\chi}^2=\frac{1}{d}\sum_{k=1}^{n} \frac{(O_k - E_k)^2}{E_k}''')
	
	st.code('''
	contingency_table = pd.crosstab(df_arrivals_terminal['Terminal'], df_arrivals_terminal['Flight'])
	stat, p, dof, expected = chi2_contingency(contingency_table)
	print(f'The chi-square test of independence is performed with a p-value of {p}')
	''',language='python')

	contingency_table = pd.crosstab(df_arrivals_terminal['Terminal'], df_arrivals_terminal['Flight'])
	stat, p, dof, expected = chi2_contingency(contingency_table)
	
	st.latex(r'''\text{The chi-square test of independence is performed with a p-value of } %s \approx 0.00''' %p)

	col1,col2,col3 = st.columns([0.7,1,0.7])
	with col1:
		st.write('')
	with col2:
		st.markdown(f'''
		<div style="text-align: center;">
		<p>
		The p-value extremely close to zero indicates that the probability of frequencies of flights arriving at each terminal under the assumption of independence between the Terminal and Flight variables is extremely low.
		<br><br>
		In other words, <b> there is a statistically significant association</b> between the Terminal and Flight variables.
		</p>
		</div>
		''',unsafe_allow_html=True)
	with col3:
		st.write('')

with tab5_Conclusion:
	st.write('''
	<br><br>
	''',unsafe_allow_html=True)