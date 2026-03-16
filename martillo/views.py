from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Subasta
from .forms import UserRegistrationForm, SubastaForm


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

@login_required
def publicar_pieza(request):
    if request.method == 'POST':
        form = SubastaForm(request.POST, request.FILES)
        if form.is_valid():
            subasta = form.save(commit=False)
            subasta.vendedor = request.user
            # El estado 'ACTIVA' se asigna por defecto en el modelo
            subasta.save()
            return redirect('home')
    else:
        form = SubastaForm()
    
    return render(request, 'martillo/publicar_pieza.html', {'form': form})
