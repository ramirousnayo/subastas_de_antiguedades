from django.core.management.base import BaseCommand
from django.utils import timezone
from martillo.models import Subasta

class Command(BaseCommand):
    help = 'Cierra las subastas cuya fecha de cierre ya pasó'

    def handle(self, *args, **options):
        now = timezone.now()
        subastas_expiradas = Subasta.objects.filter(
            fecha_cierre__lte=now,
            estado='ACTIVA'
        )
        
        count = subastas_expiradas.count()
        for subasta in subastas_expiradas:
            subasta.cerrar_subasta()
            self.stdout.write(self.style.SUCCESS(f'Subasta "{subasta.titulo}" cerrada.'))
        
        if count == 0:
            self.stdout.write('No hay subastas pendientes por cerrar.')
        else:
            self.stdout.write(self.style.SUCCESS(f'Se cerraron {count} subastas.'))
