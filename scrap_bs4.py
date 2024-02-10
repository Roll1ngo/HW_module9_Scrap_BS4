import json
import requests
from bs4 import BeautifulSoup


def scrape_page(url, quotes_data_list: list, authors_data_list: list):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for quote in soup.find_all('div', class_='quote'):
        quote_text = quote.find('span', class_='text').text
        author_name = quote.find('small', class_='author').text
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]

        quotes_data_list.append({
            "tags": tags,
            "author": author_name,
            "quote": quote_text
        })

        if author_name not in [name['fullname'] for name in authors_data_list]:
            author_url = quote.find('a')['href']
            author_data = scrape_author(f"http://quotes.toscrape.com{author_url}", author_name)
            authors_data_list.append(author_data)

    next_page = soup.find('li', class_='next')
    if next_page:
        next_page_url = next_page.find('a')['href']
        scrape_page(f"http://quotes.toscrape.com{next_page_url}", quotes_data_list, authors_data_list)


def scrape_author(url, author_name: str) -> dict:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    author_data = {
        "fullname": author_name,
        "born_date": soup.find('span', class_='author-born-date').text,
        "born_location": soup.find('span', class_='author-born-location').text,
        "description": soup.find('div', class_='author-description').text.strip()
    }
    return author_data


if __name__ == '__main__':
    quotes_data_list = []
    authors_data_list = []

    scrape_page('http://quotes.toscrape.com', quotes_data_list, authors_data_list)

    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(quotes_data_list, f, ensure_ascii=False, indent=4)

    with open('authors.json', 'w', encoding='utf-8') as f:
        json.dump(authors_data_list, f, ensure_ascii=False, indent=4)
