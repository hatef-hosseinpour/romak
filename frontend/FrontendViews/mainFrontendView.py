from django.shortcuts import render, redirect
import requests
from django.contrib import messages


def installationFrontView(request, pk):
    if not request.session.session_key:
        return redirect('/login/')
    context = {'id': pk}
    return render(request,'frontend/main/installation-form.html', context)


def mapPageFrontView(request):
    if not request.session.session_key:
        return redirect('/login/')
    return render(request=request , template_name='frontend/main/map.html')



def enginroomListFrontView(request):
    if not request.session.session_key:
        return redirect('/login/')
    return render(request, 'frontend/main/enginroom-list.html')

def createEnginroomFrontView(request):
    if not request.session.session_key:
        return redirect('/login/')
    return render(request, 'frontend/main/enginroom.html')

def updateEnginroomFrontView(request, pk):
    if not request.session.session_key:
        return redirect('/login/')
    page = 'update_device'

    context = {'device_id': pk, 'page': page}
    return render(request, 'frontend/main/enginroom.html', context)


def enginroomDetailsFrontView(request, pk):
    if not request.session.session_key:
        return redirect('/login/')
    context = {'enginroom_id': pk}
    return render(request, 'frontend/main/enginroom-details.html', context)


def eventHistoryFrontView(request):
    if not request.session.session_key:
        return redirect('/login/')
    return render(request , 'frontend/main/event-history.html')

def editEventHistoryFrontView(request, pk):
    if not request.session.session_key:
        return redirect('/login/')
    
    page = 'update_event'

    context = {'event_id': pk, 'page': page}

    return render(request , 'frontend/main/event-history.html', context)


def eventHistoryListFrontView(request):
    if not request.session.session_key:
        return redirect('/login/')
    return render(request , 'frontend/main/event-history-list.html')



def organizationListFrontView(request):
    if not request.session.session_key:
        return redirect('/login/')
    return render(request, 'frontend/main/organization.html')


def locationListFrontView(request):
    if not request.session.session_key:
        return redirect('/login/')
    return render(request, 'frontend/main/location.html')

def engineroomFeatureListFrontView(request):
    if not request.session.session_key:
        return redirect('/login/')
    return render(request, 'frontend/main/engineroom_feature.html')
