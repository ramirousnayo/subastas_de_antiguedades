from django.test import TestCase
from django.utils import timezone
from .forms import SubastaForm
from .models import Categoria
import datetime

class SubastaFormTest(TestCase):

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Test Categoria")

    def test_subasta_con_fecha_pasada_invalida(self):
        # Crear fecha en el pasado
        fecha_pasada = timezone.now() - datetime.timedelta(days=1)
        
        form_data = {
            'titulo': 'Test Item',
            'descripcion': 'A test description',
            'precio_base': 100.00,
            'fecha_cierre': fecha_pasada,
            'categoria': self.categoria.id
        }
        
        form = SubastaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('fecha_cierre', form.errors)
        self.assertEqual(form.errors['fecha_cierre'][0], "La fecha de cierre no puede estar en el pasado.")

    def test_subasta_con_fecha_futura_valida(self):
        # Crear fecha en el futuro
        fecha_futura = timezone.now() + datetime.timedelta(days=1)
        
        form_data = {
            'titulo': 'Test Item Valid',
            'descripcion': 'Another test description',
            'precio_base': 250.00,
            'fecha_cierre': fecha_futura,
            'categoria': self.categoria.id
        }
        
        form = SubastaForm(data=form_data)
        # Form should be valid (imagen is not required based on the model if blank=True/null=True)
        self.assertTrue(form.is_valid(), form.errors)
