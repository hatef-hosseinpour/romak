from django.shortcuts import render, redirect
import requests
from django.contrib import messages

base_url = 'http://127.0.0.1:8000/'


def enginroomPublicInfoListFrontView(request):
    if not request.session.session_key:
        return redirect('/login/')
    return render(request, 'frontend/enginroomPublicInfo/enginroomPublicInfo-list.html')


def enginroomPublicInfoDetialFrontView(request, pk):
    if not request.session.session_key:
        return redirect('/login/')
    # response = requests.get(
    #     f'{base_url}/api/enginroom-public-info/{pk}/', cookies=request.COOKIES)
    # data = response.json()
    # id = data.get('id')

    context = {'enginroom_id': pk}
    return render(request, 'frontend/enginroomPublicInfo/enginroomPublicInfo-detail.html', context)


def createEnginroomPublicInfoFrontView(request):
    if not request.session.session_key:
        return redirect('/login/')
    return render(request, 'frontend/enginroomPublicInfo/enginroomPublicInfo-form.html')


def updateEnginroomPublicInfoFrontView(request, pk):
    if not request.session.session_key:
        return redirect('/login/')
    context = {'id': pk}
    return render(request, 'frontend/enginroomPublicInfo/enginroomPublicInfo-update.html', context)
