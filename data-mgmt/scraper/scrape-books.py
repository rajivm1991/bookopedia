import requests
from bs4 import BeautifulSoup
from models import *
from slugify import slugify
ALLOWED_URL_PREFIX = 'http://books.toscrape.com/catalogue/category/books/'


def scrape(url):
    resp = requests.get(url)
    assert resp.status_code == 200
    return resp.content


def parse_books(html):
    html_soup = BeautifulSoup(html)

    category = html_soup.find('ul', class_='nav').find('strong').text

    for li_soup in html_soup.find('section').find_all('li'):
        # Title
        title = li_soup.find('h3').find('a').attrs['title']

        # Thumbnail
        img_src = li_soup.find('img').attrs['src']
        img_src = '/'.join(['http://books.toscrape.com/media'] + img_src.split('/')[5:])

        # Rating
        class_ = li_soup.find('p', class_='star-rating')['class']
        stars = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}.get(class_[1], 0)

        # Availability
        availability = li_soup.find('p', class_='availability')['class'][0]

        # Price
        price = li_soup.find('div', class_='product_price').find('p', class_='price_color').text
        currency, amount = price[:1], float(price[1:])

        book = {
            'title': title,
            'category': category,
            'thumbnail': img_src,
            'rating': stars,
            'availability': availability,
            'price': amount,
            'currency': currency
        }
        yield book


if __name__ == '__main__':
    urls = [
        'http://books.toscrape.com/catalogue/category/books/travel_2/index.html',
        'http://books.toscrape.com/catalogue/category/books/classics_6/index.html',
        'http://books.toscrape.com/catalogue/category/books/music_14/index.html',
    ]
    for url in urls:
        try:
            assert url.startswith(ALLOWED_URL_PREFIX)
            html = scrape(url)
            for book in parse_books(html):
                category = book.pop('category')
                category_slug = slugify(category)

                category_obj, _ = get_or_create(session=session, model=Category, defaults={'title': category}, slug=category_slug)
                session.commit()

                book['category'] = category_obj.id
                print('BOOK', book)
                book_obj = get_or_create(session=session,
                                         model=Book,
                                         defaults=book,
                                         title=book['title'])
                session.commit()
        except AssertionError:
            print(f'InvalidURL: {url}')
    session.close()