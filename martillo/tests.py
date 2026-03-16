from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import SubastaForm, OfertaForm
from .models import Categoria, Subasta, Oferta
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


class OfertaFormTest(TestCase):

    def setUp(self):
        self.user_vendedor = User.objects.create_user(username='vendedor', password='password123')
        self.user_comprador = User.objects.create_user(username='comprador', password='password123')
        self.categoria = Categoria.objects.create(nombre="Test Categoria")
        self.subasta = Subasta.objects.create(
            titulo="Subasta Test",
            descripcion="Desc",
            precio_base=100.00,
            fecha_cierre=timezone.now() + datetime.timedelta(days=1),
            vendedor=self.user_vendedor,
            categoria=self.categoria,
            estado='ACTIVA'
        )

    def test_oferta_menor_que_precio_base_invalida(self):
        form_data = {'monto': 50.00}
        form = OfertaForm(data=form_data, subasta=self.subasta)
        self.assertFalse(form.is_valid())
        self.assertIn('monto', form.errors)
        self.assertIn("al menos igual al precio base", form.errors['monto'][0])

    def test_oferta_menor_que_oferta_maxima_invalida(self):
        # Crear una oferta previa de 150
        Oferta.objects.create(subasta=self.subasta, usuario=self.user_comprador, monto=150.00)
        
        form_data = {'monto': 140.00}
        form = OfertaForm(data=form_data, subasta=self.subasta)
        self.assertFalse(form.is_valid())
        self.assertIn('monto', form.errors)
        self.assertIn("mayor a la oferta actual", form.errors['monto'][0])

    def test_oferta_valida(self):
        form_data = {'monto': 110.00}
        form = OfertaForm(data=form_data, subasta=self.subasta)
        self.assertTrue(form.is_valid(), form.errors)


class CierreSubastaTest(TestCase):

    def setUp(self):
        self.user_vendedor = User.objects.create_user(username='vendedor_cierre', password='password123')
        self.user_comprador = User.objects.create_user(username='comprador_cierre', password='password123')
        self.categoria = Categoria.objects.create(nombre="Cierre Cat")
        
        # Subasta que expirará
        self.subasta = Subasta.objects.create(
            titulo="Subasta a Cerrar",
            descripcion="Desc",
            precio_base=100.00,
            fecha_cierre=timezone.now() - datetime.timedelta(hours=1), # Ya pasó
            vendedor=self.user_vendedor,
            categoria=self.categoria,
            estado='ACTIVA'
        )

    def test_cierre_con_oferta_determina_ganador(self):
        # Crear oferta de 150
        Oferta.objects.create(subasta=self.subasta, usuario=self.user_comprador, monto=150.00)
        
        self.subasta.cerrar_subasta()
        
        self.assertEqual(self.subasta.estado, 'CERRADA')
        self.assertEqual(self.subasta.ganador, self.user_comprador)

    def test_cierre_sin_oferta_queda_desierta(self):
        self.subasta.cerrar_subasta()
        
        self.assertEqual(self.subasta.estado, 'DESIERTA')
        self.assertIsNone(self.subasta.ganador)

    def test_comando_management_cierra_subastas(self):
        from django.core.management import call_command
        # Asegurarnos de que hay una oferta
        Oferta.objects.create(subasta=self.subasta, usuario=self.user_comprador, monto=200.00)
        
        # Llamar al comando
        call_command('cerrar_subastas')
        
        self.subasta.refresh_from_db()
        self.assertEqual(self.subasta.estado, 'CERRADA')
        self.assertEqual(self.subasta.ganador, self.user_comprador)
