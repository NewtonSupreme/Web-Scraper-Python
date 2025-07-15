"""
Programa que extrae datos de libros de books.toscrape.com con interfaz gráfica.
Extrae título, precio, rating y enlace de las primeras 3 páginas.
Por: Leandro Marquez
Para: Programación V - UBA
"""

import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.font import Font
from PIL import Image, ImageTk
import csv
import io
import os
from urllib.parse import urljoin

class BookScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scraper de Libros - Books.toscrape.com")
        self.root.geometry("1100x800")
        self.root.resizable(True, True)
        self.root.configure(bg='#f5f5f5')
        
        # Configuración de estilo
        self.setup_styles()
        self.create_widgets()
        self.setup_db_connection()
    
    def setup_styles(self):
        """Configura los estilos visuales de la aplicación"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colores principales
        self.primary_color = '#3498db'
        self.secondary_color = '#2980b9'
        self.success_color = '#27ae60'
        self.danger_color = '#e74c3c'
        self.warning_color = '#f39c12'
        self.light_color = '#ecf0f1'
        self.dark_color = '#2c3e50'
        
        # Configurar estilos
        self.style.configure('TFrame', background=self.light_color)
        self.style.configure('TLabel', background=self.light_color, font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=6)
        self.style.configure('Header.TLabel', font=('Segoe UI', 18, 'bold'), foreground=self.dark_color)
        self.style.configure('Secondary.TLabel', font=('Segoe UI', 12), foreground=self.dark_color)
        self.style.configure('Success.TLabel', foreground=self.success_color)
        self.style.configure('Error.TLabel', foreground=self.danger_color)
        self.style.configure('Treeview', font=('Segoe UI', 10), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
        self.style.map('TButton', 
                      foreground=[('active', 'white'), ('!active', 'white')],
                      background=[('active', self.secondary_color), ('!active', self.primary_color)])
    
    def setup_db_connection(self):
        """Configura la conexión a la base de datos (simulada)"""
        self.db_connected = False
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Encabezado
        self.create_header(main_frame)
        
        # Panel de control
        self.create_control_panel(main_frame)
        
        # Área de resultados
        self.create_results_area(main_frame)
        
        # Barra de estado
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Crea el encabezado de la aplicación"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Logo
        try:
            logo_img = Image.open(io.BytesIO(requests.get(
                "https://cdn-icons-png.flaticon.com/512/2232/2232688.png").content))
            logo_img = logo_img.resize((60, 60), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(header_frame, image=self.logo)
            logo_label.pack(side=tk.LEFT, padx=(0, 15))
        except Exception as e:
            print(f"Error cargando logo: {e}")
        
        # Título
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        main_title = ttk.Label(title_frame, text="Scraper de Libros", style='Header.TLabel')
        main_title.pack(anchor=tk.W)
        
        sub_title = ttk.Label(title_frame, 
                             text="Extrae datos de libros de books.toscrape.com", 
                             style='Secondary.TLabel')
        sub_title.pack(anchor=tk.W)
    
    def create_control_panel(self, parent):
        """Crea el panel de control con botones y opciones"""
        control_frame = ttk.Frame(parent, relief=tk.GROOVE, borderwidth=2)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Botones de acción
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        scrape_btn = ttk.Button(btn_frame, text="Iniciar Scraping", 
                              command=self.start_scraping, width=15)
        scrape_btn.pack(side=tk.LEFT, padx=5)
        
        export_btn = ttk.Button(btn_frame, text="Exportar CSV", 
                              command=self.export_to_csv, width=15)
        export_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(btn_frame, text="Limpiar", 
                             command=self.clear_results, width=15)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Opciones de scraping
        options_frame = ttk.Frame(control_frame)
        options_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        pages_label = ttk.Label(options_frame, text="Páginas a scrapear:")
        pages_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.pages_var = tk.IntVar(value=3)
        pages_spin = ttk.Spinbox(options_frame, from_=1, to=10, 
                                textvariable=self.pages_var, width=3)
        pages_spin.pack(side=tk.LEFT)
        
        # Checkbox para conexión a BD
        self.db_var = tk.BooleanVar()
        db_check = ttk.Checkbutton(options_frame, text="Guardar en BD", 
                                  variable=self.db_var)
        db_check.pack(side=tk.LEFT, padx=(15, 0))
    
    def create_results_area(self, parent):
        """Crea el área donde se mostrarán los resultados"""
        results_frame = ttk.Frame(parent)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview para mostrar los libros
        self.tree = ttk.Treeview(results_frame, columns=('Título', 'Precio', 'Rating', 'Enlace'), 
                                selectmode='extended')
        
        # Configurar columnas
        self.tree.heading('#0', text='#')
        self.tree.column('#0', width=40, stretch=tk.NO)
        
        self.tree.heading('Título', text='Título')
        self.tree.column('Título', width=300)
        
        self.tree.heading('Precio', text='Precio')
        self.tree.column('Precio', width=80, anchor=tk.CENTER)
        
        self.tree.heading('Rating', text='Rating')
        self.tree.column('Rating', width=80, anchor=tk.CENTER)
        
        self.tree.heading('Enlace', text='Enlace')
        self.tree.column('Enlace', width=250)
        
        # Scrollbars
        y_scroll = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        x_scroll = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        # Layout
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        y_scroll.grid(row=0, column=1, sticky=tk.NS)
        x_scroll.grid(row=1, column=0, sticky=tk.EW)
        
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        # Contador de resultados
        self.results_count = ttk.Label(parent, text="Libros encontrados: 0", style='Secondary.TLabel')
        self.results_count.pack(anchor=tk.E, pady=(5, 0))
    
    def create_status_bar(self, parent):
        """Crea la barra de estado en la parte inferior"""
        self.status_var = tk.StringVar()
        self.status_var.set("Listo para comenzar")
        
        status_bar = ttk.Label(parent, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def extract_book_data(self, book_element, base_url):
        """Extrae los datos de un libro individual"""
        title = book_element.h3.a['title']
        
        # Extraer y limpiar el precio (eliminar caracteres no deseados)
        price_text = book_element.select_one('p.price_color').text
        price = ''.join(c for c in price_text if c.isdigit() or c in '£.')
        
        rating = self.convert_rating(book_element.select_one('p.star-rating')['class'][1])
        link = urljoin(base_url, book_element.h3.a['href'])
        
        return {
            'title': title,
            'price': price,
            'rating': rating,
            'link': link
        }
    
    def convert_rating(self, rating_text):
        """Convierte el rating de texto a número"""
        rating_map = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }
        return rating_map.get(rating_text, 0)
    
    def add_book_to_tree(self, book_data, index):
        """Añade un libro al Treeview"""
        self.tree.insert('', tk.END, iid=index, text=str(index),
                       values=(book_data['title'], book_data['price'], 
                              f"{'★' * book_data['rating']} ({book_data['rating']})",
                              book_data['link']))
    
    def start_scraping(self):
        """Inicia el proceso de scraping"""
        self.clear_results()
        self.status_var.set("Iniciando scraping...")
        self.root.update()
        
        try:
            base_url = "https://books.toscrape.com/"
            catalogue_url = "https://books.toscrape.com/catalogue/"
            pages_to_scrape = self.pages_var.get()
            
            books = []
            
            for page in range(1, pages_to_scrape + 1):
                # Construir URL correcta para cada página
                if page == 1:
                    url = base_url
                else:
                    url = f"{catalogue_url}page-{page}.html"
                    
                self.status_var.set(f"Scrapeando página {page} de {pages_to_scrape}...")
                self.root.update()
                
                try:
                    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    book_elements = soup.select('article.product_pod')
                    
                    for book in book_elements:
                        book_data = self.extract_book_data(book, catalogue_url)
                        books.append(book_data)
                        self.add_book_to_tree(book_data, len(books))
                        
                except requests.exceptions.RequestException as e:
                    messagebox.showwarning("Advertencia", 
                                        f"No se pudo acceder a la página {page}: {str(e)}")
                    continue
            
            self.status_var.set(f"Scraping completado. {len(books)} libros encontrados.")
            self.results_count.config(text=f"Libros encontrados: {len(books)}")
            
            if self.db_var.get():
                self.save_to_database(books)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el scraping: {str(e)}")
            self.status_var.set("Error en el scraping")
    
    def save_to_database(self, books):
        """Simula el guardado en base de datos"""
        self.status_var.set(f"Datos guardados en la base de datos ({len(books)} registros)")
    
    def export_to_csv(self):
        """Exporta los datos a un archivo CSV"""
        if not self.tree.get_children():
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Guardar archivo CSV"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['#', 'Título', 'Precio', 'Rating', 'Enlace'])
                
                for item in self.tree.get_children():
                    values = self.tree.item(item, 'values')
                    writer.writerow([self.tree.item(item, 'text')] + list(values))
            
            messagebox.showinfo("Éxito", f"Datos exportados correctamente a:\n{file_path}")
            self.status_var.set(f"Archivo exportado: {os.path.basename(file_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el archivo:\n{str(e)}")
            self.status_var.set("Error al exportar")
    
    def clear_results(self):
        """Limpia los resultados actuales"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.results_count.config(text="Libros encontrados: 0")
        self.status_var.set("Resultados limpiados")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookScraperApp(root)
    root.mainloop()