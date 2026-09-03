import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent/'.env')
url = "https://www.googleapis.com/books/v1/volumes"

def get_books(query):

    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')

    params = {
        'q': query,
        'key': api_key,
        'maxResults':5
    }

    response = requests.get(url,params)
    data = response.json()

    books = []

    for item in data.get('items',[]):

        volumeInfo = item.get('volumeInfo',{})
        industryIdentifiers = volumeInfo.get('industryIdentifiers',[])

        isbn = None

        for identifier in industryIdentifiers:
            if identifier.get('type') == 'ISBN_13':
                isbn = identifier.get('identifier')
                break

        books.append({
            'id' : item.get('id'),
            'title' : volumeInfo.get('title'),
            'authors' : volumeInfo.get('authors',[]),
            'published_date' : volumeInfo.get('publishedDate'),
            'ISBN' : isbn,
            'thumbnail' : volumeInfo.get('imageLinks',{}).get('thumbnail')

        })
    return books

def search_books(query):

    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')

    params = {
        'q': query,
        'key': api_key,
        'maxResults': 5
    }

    response = requests.get(url,params=params)
    response.raise_for_status()

    data = response.json()

    books = []

    for item in data.get('items',[]):

        volumeInfo = item.get('volumeInfo',{})

        books.append(
            {
                'id': item.get('id'),
                'title': volumeInfo.get('title'),
                'thumbnail': volumeInfo.get('imageLinks',{}).get('smallThumbnail')
                }
        )
    return books

def search_book(book_id):

    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
    url = f"https://www.googleapis.com/books/v1/volumes/{book_id}"

    params = {
        'key': api_key
    }

    response = requests.get(url,params=params)
    data = response.json()

    volumeInfo = data.get('volumeInfo',{})

    book = {
        'id' : data.get('id'),
        'title' : volumeInfo.get('title'),
        'authors' : volumeInfo.get('authors',[]),
        'published_date' : volumeInfo.get('publishedDate'),
        'description' : volumeInfo.get('description'),
        'pages' : volumeInfo.get('pageCount'),
        'categories' : volumeInfo.get('categories', []),
        'thumbnail' : volumeInfo.get('imageLinks',{}).get('thumbnail'),
        'preview_link' : volumeInfo.get('previewLink'),
    }

    return book