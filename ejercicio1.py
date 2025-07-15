"""
Programa que extrae los títulos de los primeros 5 artículos de un blog mediante interfaz gráfica.
Por: Leandro Marquez
Para: Programación V - UBA
"""

# Importación de bibliotecas necesarias
import requests  # Para realizar solicitudes HTTP
from bs4 import BeautifulSoup  # Para analizar contenido HTML
import tkinter as tk  # Para la interfaz gráfica principal
from tkinter import ttk, messagebox, scrolledtext  # Componentes específicos de Tkinter
from tkinter.font import Font  # Para manejar fuentes de texto
from PIL import Image, ImageTk  # Para manejar imágenes en la interfaz
import io  # Para operaciones de entrada/salida
import re  # Para expresiones regulares (validación de URLs)
from urllib.parse import urljoin  # Para construir URLs absolutas a partir de relativas

class BlogScraperApp:
    """Clase principal que define la aplicación de extracción de artículos de blog."""
    
    def __init__(self, root):
        """Inicializa la aplicación con la ventana principal."""
        self.root = root
        # Configuración de la ventana principal
        self.root.title("Extractor de Artículos de Blog")  # Título de la ventana
        self.root.geometry("900x700")  # Tamaño inicial de la ventana
        self.root.resizable(True, True)  # Permite redimensionar la ventana
        self.root.configure(bg='#f0f2f5')  # Color de fondo
        
        # Configuración de estilos para los componentes de la interfaz
        self.style = ttk.Style()  # Crea un objeto de estilo
        self.style.theme_use('clam')  # Selecciona el tema 'clam' para los widgets ttk
        
        # Configuración de estilos específicos para diferentes componentes
        self.style.configure('TFrame', background='#f0f2f5')  # Fondo para frames
        self.style.configure('TLabel', background='#f0f2f5', font=('Helvetica', 10))  # Etiquetas
        self.style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=6)  # Botones
        # Estilo especial para encabezados
        self.style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'), foreground='#2c3e50')
        # Estilos para mensajes de éxito y error
        self.style.configure('Success.TLabel', foreground='#27ae60')
        self.style.configure('Error.TLabel', foreground='#e74c3c')
        
        # Crear todos los widgets de la interfaz
        self.create_widgets()
    
    def create_widgets(self):
        """Crea y organiza todos los componentes de la interfaz gráfica."""
        
        # Frame principal que contendrá todos los demás elementos
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ================== ENCABEZADO ==================
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))  # Se expande horizontalmente
        
        # Logo de la aplicación (intento de carga desde URL)
        try:
            # Descargar imagen del logo desde internet
            logo_img = Image.open(io.BytesIO(requests.get(
                "https://cdn-icons-png.flaticon.com/512/2721/2721620.png").content))
            # Redimensionar la imagen
            logo_img = logo_img.resize((60, 60), Image.Resampling.LANCZOS)
            # Convertir a formato compatible con Tkinter
            self.logo = ImageTk.PhotoImage(logo_img)
            # Crear etiqueta para mostrar el logo
            logo_label = ttk.Label(header_frame, image=self.logo)
            logo_label.pack(side=tk.LEFT, padx=(0, 10))
        except:
            # Manejo de errores si falla la descarga de la imagen
            pass
        
        # Título de la aplicación
        title_label = ttk.Label(header_frame, text="Extractor de Artículos de Blog", style='Header.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # ================== ÁREA DE ENTRADA ==================
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))  # Se expande horizontalmente
        
        # Etiqueta para el campo de URL
        url_label = ttk.Label(input_frame, text="URL del Blog:")
        url_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Campo de entrada para la URL del blog
        self.url_entry = ttk.Entry(input_frame, width=50, font=('Helvetica', 10))
        self.url_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        # Botón para iniciar la extracción de títulos
        extract_btn = ttk.Button(input_frame, text="Extraer Títulos", command=self.extract_titles)
        extract_btn.pack(side=tk.LEFT)
        
        # ================== ÁREA DE RESULTADOS ==================
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill=tk.BOTH, expand=True)  # Se expande en ambas direcciones
        
        # Título de la sección de resultados
        results_label = ttk.Label(results_frame, text="Resultados:", style='Header.TLabel')
        results_label.pack(anchor=tk.W, pady=(0, 10))  # Alineado a la izquierda
        
        # Área de texto con scroll para mostrar los resultados
        self.results_text = scrolledtext.ScrolledText(
            results_frame, 
            wrap=tk.WORD,  # Ajuste de palabras
            width=80,      # Ancho en caracteres
            height=15,     # Alto en líneas
            font=('Helvetica', 10),  # Fuente del texto
            padx=10,       # Relleno horizontal
            pady=10,       # Relleno vertical
            bg='white',    # Color de fondo
            bd=2,          # Grosor del borde
            relief=tk.GROOVE  # Estilo del borde
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)  # Llena todo el espacio disponible
        
        # ================== BARRA DE ESTADO ==================
        # Variable para mostrar mensajes de estado
        self.status_var = tk.StringVar()
        self.status_var.set("Listo")  # Mensaje inicial
        
        # Etiqueta que muestra el estado actual de la aplicación
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))  # Se expande horizontalmente en la parte inferior
    
    def validate_url(self, url):
        """
        Valida que una URL tenga el formato correcto usando expresiones regulares.
        
        Parámetros:
            url (str): La URL a validar
            
        Retorna:
            bool: True si la URL es válida, False en caso contrario
        """
        # Expresión regular para validar URLs
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # Protocolo (http, https, ftp, ftps)
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # Dominio
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # Dirección IP
            r'(?::\d+)?'  # Puerto opcional
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)  # Ruta y parámetros
        
        # Comprueba si la URL coincide con el patrón
        return re.match(regex, url) is not None
    
    def extract_titles(self):
        """Realiza el proceso de extracción de títulos de artículos de un blog."""
        # Obtener la URL ingresada por el usuario
        url = self.url_entry.get().strip()
        
        # Validar que se haya ingresado una URL
        if not url:
            messagebox.showerror("Error", "Por favor ingrese una URL del blog")
            return
        
        # Validar el formato de la URL
        if not self.validate_url(url):
            messagebox.showerror("Error", "La URL ingresada no es válida. Debe comenzar con http:// o https://")
            return
        
        # Actualizar estado de la aplicación
        self.status_var.set("Extrayendo títulos...")
        self.root.update()  # Actualizar la interfaz inmediatamente
        
        try:
            # Configurar encabezados HTTP para simular un navegador real
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'es-ES,es;q=0.9'  # Preferencia de idioma
            }
            
            # Realizar la solicitud HTTP al blog
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Lanzar excepción si hay error HTTP
            
            # Parsear el contenido HTML de la respuesta
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Lista para almacenar los títulos encontrados
            titulos = []
            
            # Lista de selectores CSS comunes para encontrar títulos de artículos
            selectores = [
                'h2 a',                # Selector genérico para títulos
                'h1 a',                 # Para blogs que usan h1 en artículos
                'article h2 a',         # Típico en WordPress y otros CMS
                '.post-title a',        # Clase común para títulos de posts
                '.entry-title a',       # Otra clase común en blogs
                '[itemprop="headline"] a', # Para sitios que usan schema.org
                'h3 a'                  # Algunos blogs usan h3 para títulos
            ]
            
            # Probar cada selector hasta obtener 5 títulos
            for selector in selectores:
                # Salir del bucle si ya tenemos 5 títulos
                if len(titulos) >= 5:
                    break
                
                # Buscar elementos que coincidan con el selector actual
                elementos = soup.select(selector)
                
                # Procesar cada elemento encontrado
                for elemento in elementos:
                    # Salir si ya tenemos 5 títulos
                    if len(titulos) >= 5:
                        break
                    
                    # Obtener el texto del título y eliminar espacios en blanco
                    texto = elemento.get_text().strip()
                    
                    # Solo agregar si el título tiene texto
                    if texto:
                        # Obtener el enlace del artículo
                        enlace = elemento.get('href', '#')
                        
                        # Convertir enlace relativo a absoluto si es necesario
                        if not enlace.startswith(('http://', 'https://')):
                            enlace = urljoin(url, enlace)
                        
                        # Agregar título y enlace a la lista
                        titulos.append((texto, enlace))
            
            # Comprobar si se encontraron títulos
            if not titulos:
                messagebox.showwarning("Advertencia", "No se encontraron artículos en la página")
                self.status_var.set("Listo")
                return
            
            # Limpiar el área de resultados
            self.results_text.delete(1.0, tk.END)
            
            # Mostrar encabezado con la URL analizada
            self.results_text.insert(tk.END, f"=== Títulos encontrados en: {url} ===\n\n", 'header')
            
            # Mostrar cada título encontrado (hasta 5)
            for i, (titulo, enlace) in enumerate(titulos[:5], 1):
                # Número de artículo
                self.results_text.insert(tk.END, f"{i}. ", 'number')
                # Título del artículo
                self.results_text.insert(tk.END, f"{titulo}\n", 'title')
                # Enlace al artículo
                self.results_text.insert(tk.END, f"   Enlace: {enlace}\n\n", 'link')
            
            # Actualizar estado con el número de títulos encontrados
            self.status_var.set(f"Éxito: {len(titulos[:5])} títulos encontrados")
            
        # Manejo de errores específicos de conexión
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo acceder al blog:\n{str(e)}")
            self.status_var.set("Error de conexión")
        # Manejo de cualquier otro error inesperado
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{str(e)}")
            self.status_var.set("Error")

# Punto de entrada principal del programa
if __name__ == "__main__":
    # Crear la ventana principal de Tkinter
    root = tk.Tk()
    
    # Definir estilos de texto para el área de resultados
    text_styles = {
        # Estilo para encabezados
        'header': {'foreground': '#2c3e50', 'font': ('Helvetica', 12, 'bold')},
        # Estilo para números de artículo
        'number': {'foreground': '#e74c3c', 'font': ('Helvetica', 10, 'bold')},
        # Estilo para títulos de artículos
        'title': {'foreground': '#2980b9', 'font': ('Helvetica', 10)},
        # Estilo para enlaces
        'link': {'foreground': '#7f8c8d', 'font': ('Helvetica', 9)}
    }
    
    # Crear la instancia de la aplicación
    app = BlogScraperApp(root)
    
    # Configurar los estilos de texto en el área de resultados
    for style, options in text_styles.items():
        app.results_text.tag_configure(style, **options)
    
    # Iniciar el bucle principal de la aplicación
    root.mainloop()
