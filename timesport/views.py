from django.shortcuts import render

def login(request):
    context = { 'name': 'Test' }
    return render(request, 'login.html', context)