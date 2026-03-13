from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Subasta
from .forms import UserRegistrationForm


def home(request):
    subastas = Subasta.objects.all()
    return render(request, 'martillo/home.html', {
        'subastas': subastas
    })


def registro(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'martillo/register.html', {'form': form})
