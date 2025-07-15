"""
Programa que extrae los títulos de los primeros 5 artículos de un blog mediante interfaz gráfica.
Por: Leandro Marquez
Para: Programación V - UBA
"""

import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter.font import Font
from PIL import Image, ImageTk
import io
import re
from urllib.parse import urljoin

class BlogScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Extractor de Artículos de Blog")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f2f5')
        
        # Estilo moderno
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f0f2f5')
        self.style.configure('TLabel', background='#f0f2f5', font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=6)
        self.style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'), foreground='#2c3e50')
        self.style.configure('Success.TLabel', foreground='#27ae60')
        self.style.configure('Error.TLabel', foreground='#e74c3c')
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Encabezado
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Logo
        try:
            logo_img = Image.open(io.BytesIO(requests.get("https://cdn-icons-png.flaticon.com/512/2721/2721620.png").content))
            logo_img = logo_img.resize((60, 60), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(header_frame, image=self.logo)
            logo_label.pack(side=tk.LEFT, padx=(0, 10))
        except:
            pass
        
        title_label = ttk.Label(header_frame, text="Extractor de Artículos de Blog", style='Header.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Frame de entrada
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Campo de URL
        url_label = ttk.Label(input_frame, text="URL del Blog:")
        url_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.url_entry = ttk.Entry(input_frame, width=50, font=('Helvetica', 10))
        self.url_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        # Botón de extracción
        extract_btn = ttk.Button(input_frame, text="Extraer Títulos", command=self.extract_titles)
        extract_btn.pack(side=tk.LEFT)
        
        # Área de resultados
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        results_label = ttk.Label(results_frame, text="Resultados:", style='Header.TLabel')
        results_label.pack(anchor=tk.W, pady=(0, 10))
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame, 
            wrap=tk.WORD, 
            width=80, 
            height=15,
            font=('Helvetica', 10),
            padx=10,
            pady=10,
            bg='white',
            bd=2,
            relief=tk.GROOVE
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Barra de estado
        self.status_var = tk.StringVar()
        self.status_var.set("Listo")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def validate_url(self, url):
        """Valida que la URL tenga el formato correcto"""
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// o https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # dominio
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # o ip
            r'(?::\d+)?'  # puerto
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None
    
    def extract_titles(self):
        """Extrae los títulos de los artículos del blog"""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Por favor ingrese una URL del blog")
            return
        
        if not self.validate_url(url):
            messagebox.showerror("Error", "La URL ingresada no es válida. Debe comenzar con http:// o https://")
            return
        
        self.status_var.set("Extrayendo títulos...")
        self.root.update()
        
        try:
            # Hacer la solicitud HTTP
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'es-ES,es;q=0.9'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parsear el HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar títulos usando selectores comunes
            titulos = []
            
            # Intentar diferentes selectores comunes
            selectores = [
                'h2 a',                # Selector genérico
                'h1 a',                # Para algunos blogs
                'article h2 a',        # WordPress y otros CMS
                '.post-title a',       # Clase común para títulos
                '.entry-title a',      # Otra clase común
                '[itemprop="headline"] a', # Para schema.org
                'h3 a'                 # Algunos blogs usan h3
            ]
            
            for selector in selectores:
                if len(titulos) >= 5:
                    break
                elementos = soup.select(selector)
                for elemento in elementos:
                    if len(titulos) >= 5:
                        break
                    texto = elemento.get_text().strip()
                    if texto:  # Solo añadir si tiene texto
                        enlace = elemento.get('href', '#')
                        if not enlace.startswith(('http://', 'https://')):
                            enlace = urljoin(url, enlace)
                        titulos.append((texto, enlace))
            
            if not titulos:
                messagebox.showwarning("Advertencia", "No se encontraron artículos en la página")
                self.status_var.set("Listo")
                return
            
            # Mostrar resultados
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"=== Títulos encontrados en: {url} ===\n\n", 'header')
            
            for i, (titulo, enlace) in enumerate(titulos[:5], 1):
                self.results_text.insert(tk.END, f"{i}. ", 'number')
                self.results_text.insert(tk.END, f"{titulo}\n", 'title')
                self.results_text.insert(tk.END, f"   Enlace: {enlace}\n\n", 'link')
            
            self.status_var.set(f"Éxito: {len(titulos[:5])} títulos encontrados")
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo acceder al blog:\n{str(e)}")
            self.status_var.set("Error de conexión")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{str(e)}")
            self.status_var.set("Error")

if __name__ == "__main__":
    root = tk.Tk()
    
    # Configurar estilos de texto
    text_styles = {
        'header': {'foreground': '#2c3e50', 'font': ('Helvetica', 12, 'bold')},
        'number': {'foreground': '#e74c3c', 'font': ('Helvetica', 10, 'bold')},
        'title': {'foreground': '#2980b9', 'font': ('Helvetica', 10)},
        'link': {'foreground': '#7f8c8d', 'font': ('Helvetica', 9)}
    }
    
    app = BlogScraperApp(root)
    
    # Aplicar estilos al texto
    for style, options in text_styles.items():
        app.results_text.tag_configure(style, **options)
    
    root.mainloop()