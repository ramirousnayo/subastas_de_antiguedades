# 🔨 MartilloVirtualDjango

Plataforma premium de subastas de antigüedades desarrollada para **Don Roberto**, conectando la tradición de Barrio Italia con el mundo digital.

## ✨ Características Principales

- **Identidad Visual Premium**: Diseño elegante utilizando una paleta de colores Negro Ébano y Dorado Antiguo, con tipografía refinada (`Playfair Display` e `Inter`).
- **Buscador y Filtrado Avanzado**: Motor de búsqueda por texto integrado con filtros por categoría (chips interactivos) y ordenamiento por urgencia o popularidad.
- **Dashboard de Usuario**: Panel con estadísticas de vendedor (tasa de éxito) e historial completo de participaciones y subastas ganadas.
- **Efectos WOW**: Tarjetas con rotación 3D en perspectiva, indicadores de actividad en tiempo real, animaciones de entrada y manejo elegante de errores (404/500).
- **Sistema de Subastas**: Gestión completa de piezas, categorías y ofertas automáticas con cierre inteligente.

## 🛠️ Stack Tecnológico

- **Backend**: Python 3.13 + Django 6.0
- **Base de Datos**: SQLite (Listo para migración a PostgreSQL)
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript
- **Procesamiento de Imagen**: Pillow

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
   pip install django Pillow
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

- `config/`: Configuración central del proyecto Django.
- `martillo/`: Aplicación principal que contiene la lógica de negocio, modelos y vistas.
- `media/`: Almacenamiento de imágenes de las subastas.
- `static/`: Archivos CSS y JavaScript para la identidad visual.

---
*Desarrollado para el Módulo 7 — Desarrollo Web con Django.*
