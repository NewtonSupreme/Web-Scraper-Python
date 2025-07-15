"""
Programa que extrae datos de libros de books.toscrape.com con interfaz gráfica.
Extrae título, precio, rating y enlace de las primeras 3 páginas.
Por: Leandro Marquez
Para: Programación V - UBA
"""

# Importación de bibliotecas necesarias
import requests  # Para realizar solicitudes HTTP
from bs4 import BeautifulSoup  # Para analizar contenido HTML
import tkinter as tk  # Para la interfaz gráfica principal
from tkinter import ttk, messagebox, filedialog  # Componentes específicos de Tkinter
from tkinter.font import Font  # Para manejar fuentes de texto
from PIL import Image, ImageTk  # Para manejar imágenes en la interfaz
import csv  # Para trabajar con archivos CSV
import io  # Para operaciones de entrada/salida
import os  # Para operaciones del sistema de archivos
from urllib.parse import urljoin  # Para construir URLs absolutas a partir de relativas

class BookScraperApp:
    """Clase principal que define la aplicación de extracción de datos de libros."""
    
    def __init__(self, root):
        """Inicializa la aplicación con la ventana principal."""
        self.root = root
        # Configuración de la ventana principal
        self.root.title("Scraper de Libros - Books.toscrape.com")  # Título de la ventana
        self.root.geometry("1100x800")  # Tamaño inicial de la ventana
        self.root.resizable(True, True)  # Permite redimensionar la ventana
        self.root.configure(bg='#f5f5f5')  # Color de fondo
        
        # Configuración de estilos visuales
        self.setup_styles()
        # Creación de los componentes de la interfaz
        self.create_widgets()
        # Configuración inicial de la conexión a base de datos (simulada)
        self.setup_db_connection()
    
    def setup_styles(self):
        """Configura los estilos visuales para los componentes de la interfaz."""
        self.style = ttk.Style()  # Crea un objeto de estilo
        self.style.theme_use('clam')  # Selecciona el tema 'clam' para los widgets ttk
        
        # Definición de colores principales
        self.primary_color = '#3498db'  # Azul principal
        self.secondary_color = '#2980b9'  # Azul secundario
        self.success_color = '#27ae60'  # Verde para operaciones exitosas
        self.danger_color = '#e74c3c'  # Rojo para errores
        self.warning_color = '#f39c12'  # Amarillo para advertencias
        self.light_color = '#ecf0f1'  # Color claro de fondo
        self.dark_color = '#2c3e50'  # Color oscuro para texto
        
        # Configuración de estilos específicos
        self.style.configure('TFrame', background=self.light_color)  # Fondo para frames
        self.style.configure('TLabel', background=self.light_color, font=('Segoe UI', 10))  # Etiquetas
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=6)  # Botones
        # Estilos especializados
        self.style.configure('Header.TLabel', font=('Segoe UI', 18, 'bold'), foreground=self.dark_color)
        self.style.configure('Secondary.TLabel', font=('Segoe UI', 12), foreground=self.dark_color)
        self.style.configure('Success.TLabel', foreground=self.success_color)  # Éxito
        self.style.configure('Error.TLabel', foreground=self.danger_color)  # Errores
        # Estilos para el Treeview (tabla de resultados)
        self.style.configure('Treeview', font=('Segoe UI', 10), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))  # Encabezados de columnas
        # Mapeo de estados para botones
        self.style.map('TButton', 
                      foreground=[('active', 'white'), ('!active', 'white')],
                      background=[('active', self.secondary_color), ('!active', self.primary_color)])
    
    def setup_db_connection(self):
        """Configura la conexión a la base de datos (simulada en esta implementación)."""
        self.db_connected = False  # En una implementación real, aquí se establecería la conexión
    
    def create_widgets(self):
        """Crea y organiza todos los componentes de la interfaz gráfica."""
        
        # Frame principal que contendrá todos los demás elementos
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ================== ENCABEZADO ==================
        self.create_header(main_frame)
        
        # ================== PANEL DE CONTROL ==================
        self.create_control_panel(main_frame)
        
        # ================== ÁREA DE RESULTADOS ==================
        self.create_results_area(main_frame)
        
        # ================== BARRA DE ESTADO ==================
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Crea la sección de encabezado con logo y título."""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))  # Se expande horizontalmente
        
        # Logo de la aplicación (intento de carga desde URL)
        try:
            # Descargar imagen del logo desde internet
            logo_img = Image.open(io.BytesIO(requests.get(
                "https://cdn-icons-png.flaticon.com/512/2232/2232688.png").content))
            # Redimensionar la imagen
            logo_img = logo_img.resize((60, 60), Image.Resampling.LANCZOS)
            # Convertir a formato compatible con Tkinter
            self.logo = ImageTk.PhotoImage(logo_img)
            # Crear etiqueta para mostrar el logo
            logo_label = ttk.Label(header_frame, image=self.logo)
            logo_label.pack(side=tk.LEFT, padx=(0, 15))
        except Exception as e:
            # Manejo de errores si falla la descarga de la imagen
            print(f"Error cargando logo: {e}")
        
        # Contenedor para los títulos
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=tk.LEFT, fill=tk.Y)  # Alineado a la izquierda
        
        # Título principal de la aplicación
        main_title = ttk.Label(title_frame, text="Scraper de Libros", style='Header.TLabel')
        main_title.pack(anchor=tk.W)  # Alineado a la izquierda
        
        # Subtítulo descriptivo
        sub_title = ttk.Label(title_frame, 
                             text="Extrae datos de libros de books.toscrape.com", 
                             style='Secondary.TLabel')
        sub_title.pack(anchor=tk.W)  # Alineado a la izquierda
    
    def create_control_panel(self, parent):
        """Crea el panel de control con botones y opciones."""
        # Frame con borde para el panel de control
        control_frame = ttk.Frame(parent, relief=tk.GROOVE, borderwidth=2)
        control_frame.pack(fill=tk.X, pady=(0, 20))  # Se expande horizontalmente
        
        # Contenedor para botones de acción
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(side=tk.LEFT, padx=10, pady=10)  # Alineado a la izquierda
        
        # Botón para iniciar el scraping
        scrape_btn = ttk.Button(btn_frame, text="Iniciar Scraping", 
                              command=self.start_scraping, width=15)
        scrape_btn.pack(side=tk.LEFT, padx=5)
        
        # Botón para exportar a CSV
        export_btn = ttk.Button(btn_frame, text="Exportar CSV", 
                              command=self.export_to_csv, width=15)
        export_btn.pack(side=tk.LEFT, padx=5)
        
        # Botón para limpiar resultados
        clear_btn = ttk.Button(btn_frame, text="Limpiar", 
                             command=self.clear_results, width=15)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Contenedor para opciones adicionales
        options_frame = ttk.Frame(control_frame)
        options_frame.pack(side=tk.RIGHT, padx=10, pady=10)  # Alineado a la derecha
        
        # Etiqueta para el selector de páginas
        pages_label = ttk.Label(options_frame, text="Páginas a scrapear:")
        pages_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Selector numérico para cantidad de páginas
        self.pages_var = tk.IntVar(value=3)  # Valor por defecto: 3 páginas
        pages_spin = ttk.Spinbox(options_frame, from_=1, to=10, 
                                textvariable=self.pages_var, width=3)
        pages_spin.pack(side=tk.LEFT)
        
        # Checkbox para simular guardado en base de datos
        self.db_var = tk.BooleanVar()  # Variable para estado del checkbox
        db_check = ttk.Checkbutton(options_frame, text="Guardar en BD", 
                                  variable=self.db_var)
        db_check.pack(side=tk.LEFT, padx=(15, 0))
    
    def create_results_area(self, parent):
        """Crea el área donde se mostrarán los resultados en una tabla."""
        results_frame = ttk.Frame(parent)
        results_frame.pack(fill=tk.BOTH, expand=True)  # Se expande en ambas direcciones
        
        # Creación de Treeview (tabla) para mostrar los libros
        self.tree = ttk.Treeview(results_frame, columns=('Título', 'Precio', 'Rating', 'Enlace'), 
                                selectmode='extended')  # Permite selección múltiple
        
        # Configuración de columnas
        self.tree.heading('#0', text='#')  # Columna para número de registro
        self.tree.column('#0', width=40, stretch=tk.NO)  # Ancho fijo
        
        self.tree.heading('Título', text='Título')  # Columna para títulos
        self.tree.column('Título', width=300)  # Ancho inicial
        
        self.tree.heading('Precio', text='Precio')  # Columna para precios
        self.tree.column('Precio', width=80, anchor=tk.CENTER)  # Centrado
        
        self.tree.heading('Rating', text='Rating')  # Columna para calificaciones
        self.tree.column('Rating', width=80, anchor=tk.CENTER)  # Centrado
        
        self.tree.heading('Enlace', text='Enlace')  # Columna para enlaces
        self.tree.column('Enlace', width=250)  # Ancho inicial
        
        # Barras de desplazamiento
        y_scroll = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        x_scroll = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        # Configurar interacción con el Treeview
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        # Distribución en grid
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)  # Treeview ocupa la mayor parte
        y_scroll.grid(row=0, column=1, sticky=tk.NS)  # Barra vertical a la derecha
        x_scroll.grid(row=1, column=0, sticky=tk.EW)  # Barra horizontal en la parte inferior
        
        # Configuración de expansión del grid
        results_frame.grid_rowconfigure(0, weight=1)  # La fila 0 se expande
        results_frame.grid_columnconfigure(0, weight=1)  # La columna 0 se expande
        
        # Contador de resultados
        self.results_count = ttk.Label(parent, text="Libros encontrados: 0", style='Secondary.TLabel')
        self.results_count.pack(anchor=tk.E, pady=(5, 0))  # Alineado a la derecha
    
    def create_status_bar(self, parent):
        """Crea la barra de estado en la parte inferior de la ventana."""
        self.status_var = tk.StringVar()  # Variable para el texto de estado
        self.status_var.set("Listo para comenzar")  # Mensaje inicial
        
        # Etiqueta que muestra el estado actual
        status_bar = ttk.Label(parent, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W)  # Estilo hundido, texto alineado a la izquierda
        status_bar.pack(fill=tk.X, pady=(10, 0))  # Se expande horizontalmente
    
    def extract_book_data(self, book_element, base_url):
        """
        Extrae los datos de un libro a partir de un elemento HTML.
        
        Parámetros:
            book_element (bs4.element.Tag): Elemento HTML que contiene la información del libro
            base_url (str): URL base para construir enlaces absolutos
            
        Retorna:
            dict: Diccionario con los datos del libro (título, precio, rating, enlace)
        """
        # Extraer título del libro
        title = book_element.h3.a['title']
        
        # Extraer y limpiar el precio
        price_text = book_element.select_one('p.price_color').text
        # Mantener solo dígitos, símbolo de libra y punto decimal
        price = ''.join(c for c in price_text if c.isdigit() or c in '£.')
        
        # Convertir calificación de texto a número
        rating = self.convert_rating(book_element.select_one('p.star-rating')['class'][1])
        
        # Construir enlace absoluto
        link = urljoin(base_url, book_element.h3.a['href'])
        
        return {
            'title': title,
            'price': price,
            'rating': rating,
            'link': link
        }
    
    def convert_rating(self, rating_text):
        """
        Convierte una calificación en texto a su equivalente numérico.
        
        Parámetros:
            rating_text (str): Texto que representa la calificación (ej: 'One')
            
        Retorna:
            int: Número correspondiente a la calificación (1-5), o 0 si no se reconoce
        """
        # Mapeo de texto a números
        rating_map = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }
        return rating_map.get(rating_text, 0)  # Retorna 0 si el texto no está en el mapa
    
    def add_book_to_tree(self, book_data, index):
        """
        Añade un libro al Treeview (tabla de resultados).
        
        Parámetros:
            book_data (dict): Datos del libro a mostrar
            index (int): Número de índice para el libro
        """
        # Insertar nueva fila en el Treeview
        self.tree.insert('', tk.END, iid=index, text=str(index),
                       values=(book_data['title'], book_data['price'], 
                              f"{'★' * book_data['rating']} ({book_data['rating']})",  # Estrellas + número
                              book_data['link']))
    
    def start_scraping(self):
        """Inicia el proceso de scraping de libros."""
        # Limpiar resultados anteriores
        self.clear_results()
        # Actualizar estado
        self.status_var.set("Iniciando scraping...")
        self.root.update()  # Forzar actualización de la interfaz
        
        try:
            # URLs base para el scraping
            base_url = "https://books.toscrape.com/"
            catalogue_url = "https://books.toscrape.com/catalogue/"
            
            # Obtener número de páginas a scrapear
            pages_to_scrape = self.pages_var.get()
            
            # Lista para almacenar los libros encontrados
            books = []
            
            # Recorrer cada página
            for page in range(1, pages_to_scrape + 1):
                # Construir URL de la página actual
                if page == 1:
                    url = base_url  # La primera página tiene una URL diferente
                else:
                    url = f"{catalogue_url}page-{page}.html"
                    
                # Actualizar estado con progreso actual
                self.status_var.set(f"Scrapeando página {page} de {pages_to_scrape}...")
                self.root.update()  # Forzar actualización de la interfaz
                
                try:
                    # Realizar solicitud HTTP a la página
                    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                    response.raise_for_status()  # Verificar si hubo error HTTP
                    
                    # Parsear el contenido HTML
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Encontrar todos los elementos de libros en la página
                    book_elements = soup.select('article.product_pod')
                    
                    # Procesar cada libro encontrado
                    for book in book_elements:
                        # Extraer datos del libro
                        book_data = self.extract_book_data(book, catalogue_url)
                        # Añadir a la lista general
                        books.append(book_data)
                        # Añadir a la tabla de resultados
                        self.add_book_to_tree(book_data, len(books))
                        
                # Manejar errores de conexión específicos
                except requests.exceptions.RequestException as e:
                    messagebox.showwarning("Advertencia", 
                                        f"No se pudo acceder a la página {page}: {str(e)}")
                    continue  # Continuar con la siguiente página
            
            # Actualizar estado al finalizar
            self.status_var.set(f"Scraping completado. {len(books)} libros encontrados.")
            # Actualizar contador de resultados
            self.results_count.config(text=f"Libros encontrados: {len(books)}")
            
            # Simular guardado en base de datos si está seleccionada la opción
            if self.db_var.get():
                self.save_to_database(books)
            
        # Manejar errores generales durante el scraping
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el scraping: {str(e)}")
            self.status_var.set("Error en el scraping")
    
    def save_to_database(self, books):
        """
        Simula el guardado de datos en una base de datos.
        
        Parámetros:
            books (list): Lista de libros a guardar
        """
        # En una implementación real, aquí se conectaría a la BD y guardaría los datos
        self.status_var.set(f"Datos guardados en la base de datos ({len(books)} registros)")
    
    def export_to_csv(self):
        """Exporta los datos de la tabla a un archivo CSV."""
        # Verificar si hay datos para exportar
        if not self.tree.get_children():
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return
        
        # Diálogo para seleccionar ubicación del archivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",  # Extensión por defecto
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],  # Tipos de archivo
            title="Guardar archivo CSV"  # Título del diálogo
        )
        
        # Si el usuario cancela el diálogo
        if not file_path:
            return
        
        try:
            # Abrir archivo para escritura
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                # Escribir encabezados
                writer.writerow(['#', 'Título', 'Precio', 'Rating', 'Enlace'])
                
                # Recorrer todos los elementos del Treeview
                for item in self.tree.get_children():
                    # Obtener valores de la fila
                    values = self.tree.item(item, 'values')
                    # Escribir fila en el CSV
                    writer.writerow([self.tree.item(item, 'text')] + list(values))
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"Datos exportados correctamente a:\n{file_path}")
            # Actualizar barra de estado
            self.status_var.set(f"Archivo exportado: {os.path.basename(file_path)}")
            
        # Manejar errores durante la exportación
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el archivo:\n{str(e)}")
            self.status_var.set("Error al exportar")
    
    def clear_results(self):
        """Limpia todos los resultados actuales de la interfaz."""
        # Eliminar todos los elementos del Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Restablecer contador de resultados
        self.results_count.config(text="Libros encontrados: 0")
        # Actualizar barra de estado
        self.status_var.set("Resultados limpiados")

# Punto de entrada principal del programa
if __name__ == "__main__":
    # Crear la ventana principal de Tkinter
    root = tk.Tk()
    # Crear la instancia de la aplicación
    app = BookScraperApp(root)
    # Iniciar el bucle principal de la aplicación
    root.mainloop()
