import streamlit as st

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