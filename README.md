# 🧠 Desarrollo de Aplicaciones Python para Extracción de Datos Web con Interfaz Gráfica

Proyecto académico desarrollado por Leandro Marquez

Este repositorio contiene dos aplicaciones en Python que realizan scraping de datos desde sitios web públicos, presentando los resultados en interfaces gráficas modernas, con posibilidad de exportación a CSV. Ambos ejercicios están diseñados para simular escenarios reales en contextos de análisis de mercado y monitoreo de contenido.

---

## 📦 Estructura del Proyecto

├── ejercicio1.py # Módulo 1: Extracción de títulos de blogs
├── ejercicio2.py # Módulo 2: Scraping de libros en books.toscrape.com
├── screenshots/ # Carpeta para las capturas de pantalla
│ ├── blog_scraper.png
│ └── book_scraper.png
├── README.md # Este archivo


---

## ✅ Ejercicio 1: Extractor de Títulos de Blog

Este módulo permite ingresar la URL de cualquier blog y extraer los títulos de los primeros 5 artículos publicados en su página principal.

### Características:

- Interfaz gráfica con tkinter
- Validación de URL
- Extracción robusta con múltiples selectores CSS
- Resultados mostrados en consola y GUI (ScrolledText)
- Manejo de errores y mensajes amigables

### Captura de pantalla:

📸  
<img width="916" height="739" alt="image" src="https://github.com/user-attachments/assets/77484ddf-b960-4610-84cb-12af5a428731" />



---

## 📚 Ejercicio 2: Scraper de Libros en books.toscrape.com

Este módulo simula la extracción de datos desde una tienda virtual de libros para tareas de análisis de mercado. Extrae información clave de las tres primeras páginas del catálogo.

### Datos extraídos:

- Título
- Precio (£)
- Rating (número de estrellas)
- Enlace a la página del libro

### Funcionalidades destacadas:

- Interfaz gráfica avanzada
- Control de cantidad de páginas a scrapear
- Visualización en tabla (Treeview)
- Exportación directa a archivo CSV
- Simulación de guardado en base de datos

### Captura de pantalla:

📸  
<img width="1116" height="839" alt="image" src="https://github.com/user-attachments/assets/7620f3f4-4a1d-41fd-a3af-1af412dd664c" />

---

## 🔧 Requisitos

- Python 3.9 o superior
- Librerías externas:

#Instalación por consola:

pip install requests beautifulsoup4 pillow
🚀 Cómo Ejecutar
Desde la terminal o entorno de desarrollo:
```bash

python ejercicio1.py

python ejercicio2.py
```
📁 Exportación de Datos
El módulo 2 permite exportar todos los libros encontrados a un archivo .CSV con las siguientes columnas:

Número

Título

Precio

Rating (formato visual y numérico)

Enlace

El archivo se guarda donde lo indique el usuario mediante un diálogo gráfico.

📚 Recursos Utilizados
```bash
GitHub – Oxylabs. (2023). Python Web Scraping Tutorial
https://github.com/oxylabs/Python-Web-Scraping-Tutorial

YouTube – KeepCoding España. (2023). Web Scraping con Python desde cero paso a paso
https://www.youtube.com/watch?v=bK3EwIMHm94

BeautifulSoup. (s.f.). Documentación oficial
https://beautiful-soup-4.readthedocs.io/es/latest/

Tkinter (Python Docs)
https://docs.python.org/es/3/library/tk.html

Requests
https://requests.readthedocs.io/es/latest/

```

