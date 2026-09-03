from django.shortcuts import render, redirect
from . import services as svs
from django.http import JsonResponse

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