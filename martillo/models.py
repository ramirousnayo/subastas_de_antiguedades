from django.db import models
from django.contrib.auth.models import User


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

    def __str__(self):
        return self.titulo


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
