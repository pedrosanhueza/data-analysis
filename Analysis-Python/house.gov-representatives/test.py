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