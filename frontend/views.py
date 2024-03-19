from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def search(request):
    query = request.POST.get('query')
    # Example data (replace this with actual data fetched from backend)
    data = {'example_key': 'example_value'}
    return render(request, 'results.html', {'data': data})
