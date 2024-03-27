from django.shortcuts import render, redirect
import requests
from django.contrib import messages


def locationPublicInfoListFrontView(request):
    if not request.session.session_key:
        return redirect('/login/')
    return render(request, 'frontend/locationPublicInfo/location-public-info-list.html')


def createLocationPublicInfoFrontView(request):
    if not request.session.session_key:
        return redirect('/login/')
    return render(request, 'frontend/locationPublicInfo/location-public-info-form.html')
