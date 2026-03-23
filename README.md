# 🔨 MartilloVirtualDjango

Plataforma premium de subastas de antigüedades desarrollada para **Don Roberto**, conectando la tradición de Barrio Italia con el mundo digital.

## ✨ Características Principales

- **Identidad Visual Premium**: Diseño elegante utilizando una paleta de colores Negro Ébano y Dorado Antiguo, con tipografía refinada (`Playfair Display` e `Inter`).
- **Arquitectura Optimizada**: Implementación de Managers y QuerySets personalizados para una lógica de negocio centralizada y eficiente.
- **Buscador y Filtrado Inteligente**: Motor de búsqueda avanzado integrado con filtros por categoría (vía Context Processors) y ordenamiento dinámico.
- **Dashboard de Usuario**: Panel con estadísticas de vendedor (tasa de éxito) e historial completo de participaciones y subastas ganadas.
- **Efectos WOW**: Tarjetas con rotación 3D, indicadores de actividad en tiempo real y manejo elegante de estados de subasta (Activa, Cerrada, Desierta).

## 🛠️ Stack Tecnológico

- **Backend**: Python 3.13 + Django 6.0
- **Base de Datos**: SQLite (Optimizado con `select_related` para evitar N+1 queries)
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript
- **Procesamiento de Imagen**: Pillow

## 🏗️ Mejoras Arquitectónicas (Clean Code)

- **Custom Managers**: Centralización de la lógica de "Lazy Closing" y filtrado complejo en el modelo `Subasta`.
- **Global Context**: Listado de categorías disponible en todos los templates mediante un `context_processor` personalizado, reduciendo redundancia en las vistas.
- **Optimización de Consultas**: Uso preventivo de `select_related` en vistas de alta concurrencia para minimizar accesos a disco.
- **Formato de Moneda Localizado**: Implementación de un filtro personalizado `|clp` para forzar separadores de miles con punto (`.`) y supresión de decimales, garantizando un formato profesional acorde al mercado chileno.
- **Configuración Regional Robusta**: Soporte para formatos personalizados mediante `FORMAT_MODULE_PATH` para la región `es-cl`.

## 🚀 Instalación y Ejecución

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/ramirousnayo/subastas_de_antiguedades.git
   cd subastas_de_antiguedades
   ```

2. **Configurar el entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Mac/Linux
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplicar migraciones**:
   ```bash
   python manage.py migrate
   ```

5. **Iniciar el servidor**:
   ```bash
   python manage.py runserver
   ```

Accede a `http://127.0.0.1:8000/` para ver la plataforma.

## 📁 Estructura del Proyecto

- `config/`: Configuración centralizada, middleware y ajustes de seguridad (CSRF Trust).
- `martillo/`: Core de la aplicación:
    - `models.py`: Modelos con Managers personalizados.
    - `views.py`: Controladores optimizados.
    - `context_processors.py`: Lógica inyectable globalmente.
    - `templatetags/`: Filtros personalizados (`clp`) para formato de moneda.
    - `formats/`: Overrides de configuración regional (CLP).
- `media/`: Almacenamiento local de piezas.
- `static/`: Identidad visual y scripts de interacción.

---
*Desarrollado para el Módulo 7 — Desarrollo Web con Django.*
