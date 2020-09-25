from django.shortcuts import render
from django.http import JsonResponse

def login(request):
    return render(request, 'login.html')

def main(request):
    return render(request, 'main.html')

def page404(request):
    return JsonResponse({ 'error': 'Not exist' })
