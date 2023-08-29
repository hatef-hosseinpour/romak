from django.shortcuts import render, redirect


def homePageFrontView(request):

    return render(request, 'frontend/index.html')

def dashboardFrontView(request):
    return render(request, 'frontend/users/dashboard.html')

def loginUserFrontView(request):
    if request.session.session_key:
        return redirect('front-profile')

    return render(request, 'frontend/users/login.html')


def userProfileFrontView(request):
    return render(request, 'frontend/users/profile.html')


def usersListFrontView(request):
    return render(request, 'frontend/users/users-list.html')


def createUserFrontView(request):

    return render(request, 'frontend/users/create-user.html')


def userDetailsFrontView(request, pk):
    context = {'user_id': pk}
    return render(request, 'frontend/users/user-details.html', context)


def updateUserFrontView(request, pk):
    context = {'user_id': pk}
    return render(request, 'frontend/users/update-user.html', context)


def deleteUserFrontView(request, pk):
    context = {'user_id': pk}
    return render(request, 'frontend/users/delete-user.html', context)
