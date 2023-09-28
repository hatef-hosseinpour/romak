from django.shortcuts import render, redirect
import requests
from django.contrib import messages


def installationFrontView(request, pk):
    context = {'id': pk}
    return render(request,'frontend/main/installation-form.html', context)


def mapPageFrontView(request):
    return render(request=request , template_name='frontend/main/map.html')



def enginroomListFrontView(request):
    return render(request, 'frontend/main/enginroom-list.html')

def createEnginroomFrontView(request):
    return render(request, 'frontend/main/enginroom.html')

def updateEnginroomFrontView(request, pk):
    page = 'updateOrgan'

    context = {'organ_id': pk, 'page': page}
    return render(request, 'frontend/main/enginroom.html', context)


def enginroomDetailsFrontView(request, pk):
    context = {'enginroom_id': pk}
    return render(request, 'frontend/main/enginroom-details.html', context)
