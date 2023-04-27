import requests
import json
from selectolax.parser import HTMLParser

base_url = "https://books.toscrape.com/catalogue/page-{}.html"
book_url = "https://books.toscrape.com/catalogue/{}"
page_number = 1

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

books = []  # list for storing books

while True:
    resp = requests.get(base_url.format(page_number))
    if resp.status_code != 200:
        break
    
    html = HTMLParser(resp.text)

    for item in html.css('article.product_pod'):
        rating_class = item.css_first('p.star-rating').attributes.get('class').split()[1]
        rating = rating_map.get(rating_class)
        book = {
            'title': item.css_first('h3 a').attributes['title'],
            'link': book_url.format(item.css_first('h3 a').attributes['href']),
            'price': item.css_first('p.price_color').text(),
            'stock': item.css_first('p.availability').text().strip(),
            'rating': rating,
        }
        books.append(book)  # add book to books list
        
    print("Scraped page {}".format(page_number))  # show progress
    page_number += 1

print("Completed scraping.")

# save books list to json file
with open('books.json', 'w') as f:
    json.dump(books, f, indent=4)
