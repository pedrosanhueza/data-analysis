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