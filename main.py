import requests
import csv
from bs4 import BeautifulSoup

def clean(text: str) -> str:
	return text.replace('\t', '').replace('\n', '').strip()

def get_data(url: str) -> dict:
	request = requests.get(url)
	soup = BeautifulSoup(request.text, 'html.parser')
	table = soup.find('table', {'id': 'offers_table'})
	rows = table.find_all('tr', {'class': 'wrap'})
	data = []

	for row in rows:
		name = clean(row.find('h3').text)
		url = row.find('h3').find('a').get('href')
		price = clean(row.find('p', {'class': 'price'}).text)

		data.append({
			'name': clean(row.find('h3').text),
			'url': row.find('h3').find('a').get('href'),
			'price': clean(row.find('p', {'class': 'price'}).text)
		})

	return data

def main(urls: list) -> None:
	with open('data.csv', 'w', newline='') as file:
		writer = csv.writer(file)

		for url in urls:
			data = get_data(url)
			for item in data:
				writer.writerow( (
					item['name'],
					item['price'],
					item['url']
				))

if __name__ == '__main__':
	main([f'https://www.olx.ua/uk/transport/legkovye-avtomobili/audi/?page={i}' for i in range(1, 5)])