from django.shortcuts import render, redirect


def enginroomListFrontView(request):
    return render(request, 'frontend/enginroom/enginroom-list.html')


def createEnginroomFrontView(request):
    return render(request, 'frontend/enginroom/enginroom.html')


def updateEnginroomFrontView(request, pk):
    page = 'updateOrgan'

    context = {'organ_id': pk, 'page': page}
    return render(request, 'frontend/enginroom/enginroom.html', context)
