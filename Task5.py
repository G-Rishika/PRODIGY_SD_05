import requests
from bs4 import BeautifulSoup
import csv

# URL of the website to scrape
URL = "http://books.toscrape.com/"
response = requests.get(URL)

# Parse HTML
soup = BeautifulSoup(response.text, 'html.parser')
books = soup.find_all('article', class_='product_pod')

# CSV File setup
with open('books.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Price', 'Rating'])

    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        rating = book.p['class'][1]  # e.g., 'Three', 'Five'

        writer.writerow([title, price, rating])

print("Data saved to books.csv")

