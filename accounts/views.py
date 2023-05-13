from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, UserEditForm, ProfileEditForm, SfideForm, UserLoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from .models import Profile
from django.db.models import Q


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('accounts:profile')
    
    else:
        form = UserLoginForm()
    return render(request, "registration/login.html", {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profilo salvato correttamente!")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Dati inseriti non validi.")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'registration/edit.html', {'user_form': user_form, 'profile_form' : profile_form})



@login_required
def sceltaSfida(request):
    if request.method == 'POST':
        sfide_form = SfideForm(request.POST, instance=request.user.profile)
        if sfide_form.is_valid():
            sfide_form.save()
            messages.success(request, "Sfide scelte!")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Sfide non scelte.")
            return render(request, 'registration/scelta-sfide.html', {'sfide_form' : sfide_form})
    else:
        sfide_form = SfideForm(instance=request.user.profile)
    return render(request, 'registration/scelta-sfide.html', {'sfide_form' : sfide_form})


@login_required
def showallusers(request):
    data = Profile.objects.filter(Q(user__is_superuser=False), Q(user__is_staff=False)).order_by('-puntitotali')
    return render(request, "registration/classifica.html", {'data': data})


