from django.shortcuts import render
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