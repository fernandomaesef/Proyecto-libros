from django.shortcuts import render, redirect
from . import services as svs
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Book, UserBook

# Create your views here.
def index(request):

    context = {}
    
    return render(request,'books/index.html',context)

def suggestions(request):

    search = request.GET.get('query')

    if len(search)<3:
        return JsonResponse({'books':[]})

    books = svs.search_books(search)

    return JsonResponse({'books': books})

def book_detail(request):

    book_id = request.GET.get('book_id')

    if not book_id:
        return redirect('index')

    book = svs.search_book(book_id)

    context = {
        'book' : book
    }


    return render(request,'books/book_detail.html',context)

def book_search(request):

    query = request.GET.get('query')
    books = svs.get_books(query)

    if not query:
        return redirect('index')

    context = {
        'books' : books,
        'query' : query
    }
    return render(request,'books/searched_books.html',context)

@login_required
def add_to_library(request):

    if request.method == 'POST':

        book_id = request.POST.get('book_id')
        book_status = request.POST.get('book_status')

        book = svs.search_book(book_id)

        book_obj, created = Book.objects.get_or_create(
            api_id = book['id'],
            defaults={
                'title' : book['title'],
                'author' : ', '.join(book['authors']),
                'published_date' : book['published_date'],
                'cover_url' : book['thumbnail'],
                'isbn' : book['isbn']
            }
        )

        UserBook.objects.get_or_create(
            user = request.user,
            book = book_obj,
            defaults={
                'status' : book_status
            }
            
        )

        return JsonResponse({
            'message' : 'Libro añadido a tu biblioteca'
        })

