# 🔨 MartilloVirtualDjango

Plataforma premium de subastas de antigüedades desarrollada para **Don Roberto**, conectando la tradición de Barrio Italia con el mundo digital.

## ✨ Características Principales

- **Identidad Visual Premium**: Diseño elegante utilizando una paleta de colores Negro Ébano y Dorado Antiguo, con tipografía refinada (`Playfair Display` e `Inter`).
- **Sistema de Subastas**: Gestión completa de piezas, categorías y ofertas en tiempo real.
- **Perfiles de Usuario**: Registro de coleccionistas con sistema de reputación (compras y ventas).
- **Interfaz Animada**: Botones con efecto pulso y tarjetas con elevación visual para una experiencia de lujo.
- **Gestión de Multimedia**: Soporte para imágenes de alta calidad de las piezas de colección.

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
