import requests
from bs4 import BeautifulSoup
import pandas as pd

filterDay = ['yesterday', 'today', 'tomorrow']

filterHour = [str(i) for i in range(0, 24, 6)]

df_departures = pd.DataFrame(columns=['Destination City', 'Destination Code', 'Departure', 'Flight', 'Airline', 'Terminal', 'Status', 'Date', 'Reference Day', 'url'])
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
                    'Destination City': destination,
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

df_arrivals = pd.DataFrame(columns=['Origin City', 'Origin Code', 'Arrival', 'Flight', 'Airline', 'Terminal', 'Status', 'Date', 'Reference Day', 'url'])

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
            arrival = flight.find('div', {'class', 'flight-col flight-col__hour'}).text.strip()
            flight_number = flight.find('div', {'class', 'flight-col flight-col__flight'}).text.strip().split('\n')
            airline = flight.find('div', {'class', 'flight-col flight-col__airline'}).text.strip().split('\n')
            terminal = flight.find('div', {'class', 'flight-col flight-col__terminal'}).text.strip()
            status = flight.find_all('a')[-1].text
            for i in range(max(len(flight_number), len(airline))):
                rows.append({
                    'Origin City': origin,
                    'Origin Code': origin_code,
                    'Arrival': arrival,
                    'Flight': flight_number[i] if i < len(flight_number) else '',
                    'Airline': airline[i] if i < len(airline) else '',
                    'Terminal': terminal,
                    'Status': status,
                    'Date': date,
                    'Reference Day': reference_day,
                    'url': url
                })
        df_arrivals = pd.concat([df_arrivals, pd.DataFrame(rows)], ignore_index=True)

df_departures['Date_Time'] = pd.to_datetime(df_departures.Date + "-" + df_departures.Departure, format='%Y-%m-%d-%H:%M')
df_arrivals['Date_Time'] = pd.to_datetime(df_arrivals.Date + "-" + df_arrivals.Arrival, format='%Y-%m-%d-%H:%M')

city_country = {
    'Antofagasta': 'Chile',
    'Lima': 'Peru',
    'Buenos Aires': 'Argentina',
    'Sao Paulo': 'Brazil',
    'Calama': 'Chile',
    'Concepcion': 'Chile',
    'Iquique': 'Chile',
    'Puerto Montt': 'Chile',
    'Bogota': 'Colombia',
    'Temuco': 'Chile',
    'La Serena': 'Chile',
    'Madrid': 'Spain',
    'Copiapo': 'Chile',
    'Miami': 'United States',
    'Punta Arenas': 'Chile',
    'Panama City': 'Panama',
    'Rio De Janeiro': 'Brazil',
    'Arica': 'Chile',
    'Auckland': 'New Zealand',
    'New York': 'United States',
    'Montevideo': 'Uruguay',
    'Mendoza': 'Argentina',
    'Atlanta': 'United States',
    'Valdivia': 'Chile',
    'Osorno': 'Chile',
    'Paris': 'France',
    'Cordoba': 'Argentina',
    'Houston': 'United States',
    'Los Angeles': 'United States',
    'Balmaceda': 'Chile',
    'Porto Alegre': 'Brazil',
    'Castro': 'Chile',
    'London': 'United Kingdom',
    'Asuncion': 'Paraguay',
    'Mexico City': 'Mexico',
    'Guayaquil': 'Ecuador',
    'Curitiba': 'Brazil',
    'Easter Island': 'Chile',
    'Florianopolis': 'Brazil',
    'Sydney': 'Australia',
    'Cali': 'Colombia',
    'San Juan': 'Argentina',
    'Toronto': 'Canada',
    'Santa Cruz': 'Bolivia',
    'Iguassu Falls': 'Brazil',
    'Dallas': 'United States',
    'Quito': 'Ecuador',
    'Trujillo': 'Peru'
}

df_departures['Destination Country'] = df_departures['Destination City'].map(city_country)
df_arrivals['Origin Country'] = df_arrivals['Origin City'].map(city_country)

Airline_Parent_Company = {
    'Copa Airlines': 'Copa Holdings',
    'LATAM Airlines': 'LATAM Airlines Group',
    'Delta Air Lines': 'Delta Air Lines Inc.',
    'Qantas': 'Qantas Airways Limited',
    'Cathay Pacific': 'Swire Pacific Limited',
    'Malaysia Airlines': 'Malaysia Aviation Group',
    'Avianca': 'Avianca Holdings S.A.',
    'Air Canada': 'Air Canada',
    'Atlas Air': 'Atlas Air Worldwide Holdings',
    'Sky Airline': 'Sky Airline S.A.',
    'JetSMART': 'Indigo Partners',
    'British Airways': 'International Airlines Group',
    'LATAM Cargo Chile': 'LATAM Airlines Group',
    'DHL Aero Expreso': 'DHL Aviation (Panama) S.A.',
    'Aerolineas Argentinas': 'Argentine government',
    'Iberia': 'International Airlines Group',
    'KLM Royal Dutch Airlines': 'Air France-KLM',
    'El Al Israel Airlines': 'Kanaf Arkia Holdings Ltd',
    'Qatar Airways': 'Qatar Airways Group',
    'Turkish Airlines': 'Turkish Airlines',
    'Air France': 'Air France-KLM',
    'Aeromexico': 'Delta Air Lines Inc.',
    'ITA Airways': 'Italian government',
    'United Airlines': 'United Airlines Holdings',
    'ANA All Nippon Airways': 'ANA Holdings Inc.',
    'American Airlines': 'American Airlines Group',
    'Air Europa': 'Globalia',
    'Korean Air': 'Hanjin Group',
    'JAL Japan Airlines': 'Japan Airlines Co. Ltd.',
    'LATAM Cargo Brasil': 'LATAM Airlines Group',
    'JetSMART Airlines Peru': 'Indigo Partners',
    'Jetsmart Airlines': 'Indigo Partners',
    'Ethiopian Airlines': 'Ethiopian government',
    'Martinair': 'Air France-KLM'
}

df_departures['Parent Company'] = df_departures['Airline'].map(Airline_Parent_Company)
df_arrivals['Parent Company'] = df_arrivals['Airline'].map(Airline_Parent_Company)