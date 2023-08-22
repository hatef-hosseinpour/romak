from django.shortcuts import render, redirect
import requests
from django.contrib import messages


def locationPublicInfoListFrontView(request):

    return render(request, 'frontend/locationPublicInfo/location-public-info-list.html')


def createLocationPublicInfoFrontView(request):

    return render(request, 'frontend/locationPublicInfo/location-public-info-form.html')
