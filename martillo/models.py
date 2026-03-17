from django.db import models
from django.db.models import Count, Q
from django.contrib.auth.models import User
from django.utils import timezone


class SubastaQuerySet(models.QuerySet):
    def activas(self):
        return self.filter(estado='ACTIVA')

    def buscar(self, query):
        if not query:
            return self
        return self.filter(Q(titulo__icontains=query) | Q(descripcion__icontains=query))

    def por_categoria(self, categoria_id):
        if not categoria_id:
            return self
        return self.filter(categoria_id=categoria_id)

    def populares(self):
        return self.annotate(num_ofertas=Count('oferta')).order_by('-num_ofertas')

    def urgentes(self):
        return self.activas().order_by('fecha_cierre')

    def novedades(self):
        return self.order_by('-id')


class SubastaManager(models.Manager):
    def get_queryset(self):
        return SubastaQuerySet(self.model, using=self._db)

    def cerrar_expiradas(self):
        now = timezone.now()
        expiradas = self.get_queryset().activas().filter(fecha_cierre__lte=now)
        for subasta in expiradas:
            subasta.cerrar_subasta()


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Subasta(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVA', 'Activa'),
        ('CERRADA', 'Cerrada'),
        ('DESIERTA', 'Desierta'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_cierre = models.DateTimeField()
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='subastas/', null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVA')
    ganador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='subastas_ganadas')

    objects = SubastaManager()

    def __str__(self):
        return self.titulo

    def obtener_oferta_mas_alta(self):
        return self.oferta_set.order_by('-monto').first()

    def cerrar_subasta(self):
        if self.estado != 'ACTIVA':
            return

        oferta_maxima = self.obtener_oferta_mas_alta()
        if oferta_maxima:
            self.estado = 'CERRADA'
            self.ganador = oferta_maxima.usuario
        else:
            self.estado = 'DESIERTA'
        
        self.save()


class Oferta(models.Model):
    subasta = models.ForeignKey(Subasta, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    reputacion_ventas = models.PositiveIntegerField(default=0)
    reputacion_compras = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
