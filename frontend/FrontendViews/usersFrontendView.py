from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.apps import apps


def homePageFrontView(request):
    if not request.session.session_key:
        return redirect('/login/')
    return render(request, 'frontend/index.html')


def dashboardFrontView(request):
    if not request.session.session_key:
        return redirect('/login/')
    return render(request, 'frontend/users/dashboard.html')


def editProfileFrontView(request):
    if not request.session.session_key:
        return redirect('/login/')
    return render(request, 'frontend/users/edit-profile.html')


def loginUserFrontView(request):

    if request.session.session_key:
        return redirect('/dashboard/')

    return render(request, 'frontend/users/login.html')


def userProfileFrontView(request):
    if not request.session.session_key:
        return redirect('/login/')
    return render(request, 'frontend/users/profile.html')


def usersListFrontView(request):
    if not request.session.session_key:
        return redirect('/login/')
    return render(request, 'frontend/users/users-list.html')


def createUserFrontView(request):
    if not request.session.session_key:
        return redirect('/login/')
    return render(request, 'frontend/users/create-user.html')


def userDetailsFrontView(request, pk):
    if not request.session.session_key:
        return redirect('/login/')
    context = {'user_id': pk}
    return render(request, 'frontend/users/user-details.html', context)


def updateUserFrontView(request, pk):
    if not request.session.session_key:
        return redirect('/login/')
    context = {'user_id': pk}
    return render(request, 'frontend/users/update-user.html', context)


def deleteUserFrontView(request, pk):
    if not request.session.session_key:
        return redirect('/login/')
    context = {'user_id': pk}
    return render(request, 'frontend/users/delete-user.html', context)


def resetPasswordFrontView(request, pk):
    if not request.session.session_key:
        return redirect('/login/')
    context = {'user_id': pk}
    return render(request, 'frontend/users/reset_password.html', context)
