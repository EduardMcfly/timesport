from django.shortcuts import render
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest


def login(request: WSGIRequest):
    return render(request, "login.html")


def main(request: WSGIRequest):
    return render(request, "main.html")


def page404(request: WSGIRequest):
    return JsonResponse({"error": "Not exist"})
