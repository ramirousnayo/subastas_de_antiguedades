from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Subasta, Oferta
from .forms import UserRegistrationForm, SubastaForm, OfertaForm


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

def detalle_subasta(request, subasta_id):
    subasta = get_object_or_404(Subasta, id=subasta_id)
    ofertas = subasta.oferta_set.all().order_by('-fecha')
    oferta_maxima = subasta.obtener_oferta_mas_alta()
    
    form = OfertaForm()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para ofertar.")
            return redirect('login')
            
        if request.user == subasta.vendedor:
            messages.error(request, "No puedes ofertar en tu propia subasta.")
            return redirect('detalle_subasta', subasta_id=subasta.id)
            
        form = OfertaForm(request.POST, subasta=subasta)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.usuario = request.user
            oferta.subasta = subasta
            oferta.save()
            messages.success(request, "¡Tu oferta ha sido aceptada!")
            return redirect('detalle_subasta', subasta_id=subasta.id)
        else:
            messages.error(request, "Hubo un error con tu oferta.")
            
    return render(request, 'martillo/detalle_subasta.html', {
        'subasta': subasta,
        'ofertas': ofertas,
        'oferta_maxima': oferta_maxima,
        'form': form
    })
