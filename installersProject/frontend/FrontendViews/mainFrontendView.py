from django.shortcuts import render, redirect
import requests
from django.contrib import messages


def installationFrontView(request):
    return render(request=request, template_name='frontend/main/installation-form.html')


def mapPageFrontView(request):
    return render(request=request, template_name='frontend/main/map.html')