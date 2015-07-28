from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse

from .forms import PreferenceForm, InclusiveKeywordSet, ExclusiveKeywordSet
from .services import *


def index(request):
    if not request.user.is_authenticated():
        return redirect('/login/')
    else:
        return redirect('/welcome/')


def logout_view(request):
    logout(request)
    return redirect('/')


def loginPage(request):
    if request.method == 'POST':
        input_user_id = request.POST['user_id']
        if (validEtsyUsername(input_user_id) and
             authenticateUserAndLogin(request, updateUser(input_user_id))):
                updateUser(input_user_id)
                return redirect('/welcome/')
        else:
            return render(request,
                          'tys_webapp/login.html',
                          {'message':
                           'Invalid username/password entered. Try again?'})
    return render(request, 'tys_webapp/login.html')


def welcomePage(request):
    if not request.user.is_authenticated():
        return redirect('/login/')

    current_user = EtsyUser.objects.get(user=request.user)
    current_pref = getEtsyUserPreferences(current_user)

    if request.method == 'POST':
        form = PreferenceForm(request.POST, instance=current_pref)
        if form.is_valid():
            updated_pref = form.save(commit=False)
            inclusive_key_set = InclusiveKeywordSet(request.POST,
                                                    instance=current_user)
            exclusive_key_set = ExclusiveKeywordSet(request.POST,
                                                    instance=current_user)
            if inclusive_key_set.is_valid() and exclusive_key_set.is_valid():
                updated_pref.save()
                inclusive_key_set.save()
                exclusive_key_set.save()
                return HttpResponse('Successful update')
    else:
        form = PreferenceForm(instance=current_pref)
        inclusive_key_set = InclusiveKeywordSet(instance=current_user)
        exclusive_key_set = ExclusiveKeywordSet(instance=current_user)

    return render(request,
                  'tys_webapp/welcome.html',
                  {'form': form,
                   'inclusive_key_set': inclusive_key_set,
                   'exclusive_key_set': exclusive_key_set,
                   'username': request.user.username})
