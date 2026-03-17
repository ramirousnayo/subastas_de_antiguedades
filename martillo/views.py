from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max, Q
from django.utils import timezone
from .models import Subasta, Oferta, Categoria
from .forms import UserRegistrationForm, SubastaForm, OfertaForm


def home(request):
    # Lazy closing centralizado
    Subasta.objects.cerrar_expiradas()
    
    # Parámetros de filtrado
    q = request.GET.get('q')
    cat_id = request.GET.get('cat')
    sort = request.GET.get('sort', 'novedad')

    # QuerySet base optimizado con select_related
    subastas = Subasta.objects.select_related('categoria').all()
    
    # Aplicar filtros usando el QuerySet personalizado
    subastas = subastas.buscar(q).por_categoria(cat_id)
        
    # Aplicar ordenamiento
    if sort == 'urgente':
        subastas = subastas.urgentes()
    elif sort == 'popular':
        subastas = subastas.populares()
    else: # novedad
        subastas = subastas.novedades()

    return render(request, 'martillo/home.html', {
        'subastas': subastas,
        'q': q,
        'current_cat': cat_id,
        'current_sort': sort
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
    
    # Lazy closing
    if subasta.estado == 'ACTIVA' and subasta.fecha_cierre <= timezone.now():
        subasta.cerrar_subasta()
        # Refrescamos la instancia por si cambió a CERRADA/DESIERTA
        subasta.refresh_from_db()
        
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

@login_required
def perfil(request):
    # Optimizamos con select_related y annotations
    subastas_ganadas = Subasta.objects.filter(ganador=request.user).select_related('categoria')
    
    # Subastas publicadas por el usuario, con la puja más alta actual
    subastas_publicadas = Subasta.objects.filter(vendedor=request.user)\
        .select_related('categoria')\
        .annotate(puja_actual=Max('oferta__monto'))
        
    # HU-05: Subastas en las que participó, con su puja más alta personal
    subastas_participadas = Subasta.objects.filter(oferta__usuario=request.user)\
        .select_related('categoria')\
        .annotate(mi_puja_max=Max('oferta__monto', filter=Q(oferta__usuario=request.user)))\
        .distinct()
    
    # HU-07: Estadísticas
    total_publicadas = subastas_publicadas.count()
    exitosas = subastas_publicadas.filter(estado='CERRADA').count()
    tasa_exito = (exitosas / total_publicadas * 100) if total_publicadas > 0 else 0
    
    return render(request, 'martillo/perfil.html', {
        'subastas_ganadas': subastas_ganadas,
        'subastas_publicadas': subastas_publicadas,
        'subastas_participadas': subastas_participadas,
        'stats': {
            'total': total_publicadas,
            'exitosas': exitosas,
            'tasa': round(tasa_exito, 1)
        }
    })
