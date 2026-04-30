"""
TO-DO LIST PROFESIONAL
Aplicación completa con todas las funcionalidades excepto notificaciones
Autor: Christian Lera
Versión: 1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, filedialog
from datetime import datetime, timedelta
import json
import os
from typing import List, Dict, Any
import copy

class Tarea:
    """Clase que representa una tarea individual"""
    def __init__(self, texto: str, categoria: str = "General", prioridad: str = "Media", 
                 fecha_vencimiento: str = "", completada: bool = False, subtareas: List[Dict] = None):
        self.texto = texto
        self.categoria = categoria
        self.prioridad = prioridad
        self.fecha_vencimiento = fecha_vencimiento
        self.completada = completada
        self.subtareas = subtareas if subtareas else []
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        """Convierte la tarea a diccionario para JSON"""
        return {
            "texto": self.texto,
            "categoria": self.categoria,
            "prioridad": self.prioridad,
            "fecha_vencimiento": self.fecha_vencimiento,
            "completada": self.completada,
            "subtareas": self.subtareas,
            "fecha_creacion": self.fecha_creacion
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Crea una tarea desde un diccionario"""
        return cls(
            texto=data.get("texto", ""),
            categoria=data.get("categoria", "General"),
            prioridad=data.get("prioridad", "Media"),
            fecha_vencimiento=data.get("fecha_vencimiento", ""),
            completada=data.get("completada", False),
            subtareas=data.get("subtareas", [])
        )

class TodoListApp:
    """Aplicación principal de lista de tareas"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("📋 TO-DO LIST PROFESIONAL v1.0")
        self.root.geometry("1200x700")
        self.root.minsize(900, 500)
        
        # Configurar icono (opcional, si tienes archivo .ico)
        # self.root.iconbitmap("icon.ico")
        
        # Variables de estado
        self.tareas: List[Tarea] = []
        self.tema_oscuro = False
        self.archivo_json = "tareas.json"
        
        # Configurar estilos
        self.establecer_estilos()
        
        # Cargar tareas guardadas
        self.cargar_tareas()
        
        # Construir interfaz
        self.construir_interfaz()
        
        # Configurar atajos de teclado
        self.configurar_atajos()
        
        # Actualizar estadísticas
        self.actualizar_estadisticas()
        
        # Guardado automático cada 30 segundos
        self.programar_guardado_automatico()
        
    def establecer_estilos(self):
        """Configura los estilos visuales de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')  # Tema base moderno
        
        # Colores personalizados
        self.colores = {
            "fondo_claro": "#f5f5f5",
            "fondo_oscuro": "#2b2b2b",
            "texto_claro": "#000000",
            "texto_oscuro": "#ffffff",
            "btn_primary": "#4CAF50",
            "btn_danger": "#f44336",
            "btn_warning": "#ff9800",
            "btn_info": "#2196F3",
            "completado": "#888888"
        }
        
        self.aplicar_tema()
    
    def aplicar_tema(self):
        """Aplica tema claro u oscuro"""
        fondo = self.colores["fondo_oscuro"] if self.tema_oscuro else self.colores["fondo_claro"]
        texto = self.colores["texto_oscuro"] if self.tema_oscuro else self.colores["texto_claro"]
        
        self.root.configure(bg=fondo)
        
        # Actualizar estilos ttk
        style = ttk.Style()
        style.configure("TFrame", background=fondo)
        style.configure("TLabel", background=fondo, foreground=texto)
        style.configure("TLabelframe", background=fondo, foreground=texto)
        style.configure("TLabelframe.Label", background=fondo, foreground=texto)
        
        # Actualizar frames existentes
        if hasattr(self, 'frame_principal'):
            self.actualizar_colores_widgets(self.frame_principal, fondo, texto)
    
    def actualizar_colores_widgets(self, widget, fondo, texto):
        """Recursivamente actualiza colores de widgets"""
        try:
            if isinstance(widget, (tk.Frame, ttk.Frame, tk.LabelFrame)):
                widget.configure(bg=fondo)
            elif isinstance(widget, (tk.Label, ttk.Label)):
                widget.configure(bg=fondo, fg=texto)
            elif isinstance(widget, (tk.Button, ttk.Button)):
                pass  # Los botones tienen sus propios estilos
        except:
            pass
        
        for child in widget.winfo_children():
            self.actualizar_colores_widgets(child, fondo, texto)
    
    def construir_interfaz(self):
        """Construye toda la interfaz de usuario"""
        # Frame principal con paneles divididos
        self.frame_principal = ttk.Frame(self.root)
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Formulario de entrada
        self.construir_panel_entrada()
        
        # Panel central - Lista de tareas
        self.construir_panel_lista()
        
        # Panel derecho - Detalles y estadísticas
        self.construir_panel_derecho()
    
    def construir_panel_entrada(self):
        """Panel para añadir nuevas tareas"""
        frame_entrada = ttk.LabelFrame(self.frame_principal, text="➕ NUEVA TAREA", padding=10)
        frame_entrada.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Campo de texto
        ttk.Label(frame_entrada, text="Descripción:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.txt_tarea = tk.Text(frame_entrada, height=4, width=40, font=("Arial", 10))
        self.txt_tarea.grid(row=1, column=0, columnspan=2, pady=5, padx=5)
        
        # Categoría
        ttk.Label(frame_entrada, text="Categoría:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.categoria_var = tk.StringVar(value="General")
        categorias = ["General", "Trabajo", "Personal", "Estudios", "Hogar", "Salud", "Finanzas"]
        self.combo_categoria = ttk.Combobox(frame_entrada, textvariable=self.categoria_var, 
                                            values=categorias, width=30)
        self.combo_categoria.grid(row=3, column=0, columnspan=2, pady=5, padx=5)
        
        # Prioridad
        ttk.Label(frame_entrada, text="Prioridad:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.prioridad_var = tk.StringVar(value="Media")
        frame_prioridad = ttk.Frame(frame_entrada)
        frame_prioridad.grid(row=5, column=0, columnspan=2, pady=5, padx=5)
        
        ttk.Radiobutton(frame_prioridad, text="🔴 Alta", variable=self.prioridad_var, 
                       value="Alta").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(frame_prioridad, text="🟡 Media", variable=self.prioridad_var, 
                       value="Media").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(frame_prioridad, text="🟢 Baja", variable=self.prioridad_var, 
                       value="Baja").pack(side=tk.LEFT, padx=5)
        
        # Fecha de vencimiento
        ttk.Label(frame_entrada, text="Fecha vencimiento (YYYY-MM-DD):").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.fecha_var = tk.StringVar()
        self.entry_fecha = ttk.Entry(frame_entrada, textvariable=self.fecha_var, width=30)
        self.entry_fecha.grid(row=7, column=0, columnspan=2, pady=5, padx=5)
        
        # Botón añadir
        btn_agregar = tk.Button(frame_entrada, text="📌 AÑADIR TAREA", bg=self.colores["btn_primary"], 
                               fg="white", font=("Arial", 10, "bold"), command=self.agregar_tarea)
        btn_agregar.grid(row=8, column=0, columnspan=2, pady=15, padx=5, sticky=tk.W+tk.E)
        
        # Botón tema oscuro/claro
        self.btn_tema = tk.Button(frame_entrada, text="🌙 TEMA OSCURO", 
                                 command=self.cambiar_tema, bg="#555", fg="white")
        self.btn_tema.grid(row=9, column=0, columnspan=2, pady=5, sticky=tk.W+tk.E)
    
    def construir_panel_lista(self):
        """Panel central con la lista de tareas"""
        frame_lista = ttk.LabelFrame(self.frame_principal, text="📝 MIS TAREAS", padding=10)
        frame_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Frame de búsqueda
        frame_busqueda = ttk.Frame(frame_lista)
        frame_busqueda.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(frame_busqueda, text="🔍 Buscar:").pack(side=tk.LEFT, padx=5)
        self.busqueda_var = tk.StringVar()
        self.busqueda_var.trace('w', lambda *args: self.filtrar_tareas())
        self.entry_busqueda = ttk.Entry(frame_busqueda, textvariable=self.busqueda_var, width=30)
        self.entry_busqueda.pack(side=tk.LEFT, padx=5)
        
        # Filtros adicionales
        ttk.Label(frame_busqueda, text="Filtrar:").pack(side=tk.LEFT, padx=(20, 5))
        self.filtro_estado = ttk.Combobox(frame_busqueda, values=["Todas", "Pendientes", "Completadas"], 
                                         width=15, state="readonly")
        self.filtro_estado.set("Todas")
        self.filtro_estado.bind('<<ComboboxSelected>>', lambda e: self.filtrar_tareas())
        self.filtro_estado.pack(side=tk.LEFT, padx=5)
        
        # Treeview para mostrar tareas
        frame_tree = ttk.Frame(frame_lista)
        frame_tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(frame_tree)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x = ttk.Scrollbar(frame_tree, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview con columnas
        self.tree = ttk.Treeview(frame_tree, columns=("Estado", "Tarea", "Categoría", "Prioridad", "Vencimiento"), 
                                show="tree headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.tree.heading("#0", text="ID")
        self.tree.heading("Estado", text="✓")
        self.tree.heading("Tarea", text="Tarea")
        self.tree.heading("Categoría", text="Categoría")
        self.tree.heading("Prioridad", text="Prioridad")
        self.tree.heading("Vencimiento", text="Vence")
        
        self.tree.column("#0", width=50)
        self.tree.column("Estado", width=50)
        self.tree.column("Tarea", width=400)
        self.tree.column("Categoría", width=120)
        self.tree.column("Prioridad", width=100)
        self.tree.column("Vencimiento", width=120)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Bind eventos
        self.tree.bind('<Double-Button-1>', self.editar_tarea_dialog)
        self.tree.bind('<Button-3>', self.mostrar_menu_contextual)
        
        # Botones de acción
        frame_botones = ttk.Frame(frame_lista)
        frame_botones.pack(fill=tk.X, pady=(10, 0))
        
        btn_completar = tk.Button(frame_botones, text="✅ Marcar Completada", bg=self.colores["btn_info"], 
                                 fg="white", command=self.marcar_completada)
        btn_completar.pack(side=tk.LEFT, padx=5)
        
        btn_eliminar = tk.Button(frame_botones, text="🗑️ Eliminar", bg=self.colores["btn_danger"], 
                                fg="white", command=self.eliminar_tarea)
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        btn_editar = tk.Button(frame_botones, text="✏️ Editar", bg=self.colores["btn_warning"], 
                              fg="white", command=lambda: self.editar_tarea_dialog())
        btn_editar.pack(side=tk.LEFT, padx=5)
        
        btn_ordenar = tk.Button(frame_botones, text="🔄 Ordenar por prioridad", 
                               command=self.ordenar_por_prioridad)
        btn_ordenar.pack(side=tk.LEFT, padx=5)
        
        btn_exportar = tk.Button(frame_botones, text="📤 Exportar CSV", 
                                command=self.exportar_csv)
        btn_exportar.pack(side=tk.LEFT, padx=5)
    
    def construir_panel_derecho(self):
        """Panel derecho con detalles y estadísticas"""
        frame_derecho = ttk.Frame(self.frame_principal)
        frame_derecho.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Subtareas
        self.frame_subtareas = ttk.LabelFrame(frame_derecho, text="📋 SUBTAREAS", padding=10)
        self.frame_subtareas.pack(fill=tk.BOTH, pady=(0, 10))
        
        self.lista_subtareas = tk.Listbox(self.frame_subtareas, height=8, width=35)
        self.lista_subtareas.pack(fill=tk.BOTH, expand=True)
        
        frame_sub_btn = ttk.Frame(self.frame_subtareas)
        frame_sub_btn.pack(fill=tk.X, pady=(5, 0))
        
        self.txt_subtarea = ttk.Entry(frame_sub_btn, width=20)
        self.txt_subtarea.pack(side=tk.LEFT, padx=5)
        
        btn_add_sub = tk.Button(frame_sub_btn, text="+", width=3, command=self.agregar_subtarea)
        btn_add_sub.pack(side=tk.LEFT)
        
        btn_del_sub = tk.Button(frame_sub_btn, text="-", width=3, command=self.eliminar_subtarea)
        btn_del_sub.pack(side=tk.LEFT)
        
        # Estadísticas
        self.frame_estadisticas = ttk.LabelFrame(frame_derecho, text="📊 ESTADÍSTICAS", padding=10)
        self.frame_estadisticas.pack(fill=tk.BOTH)
        
        self.lbl_total = ttk.Label(self.frame_estadisticas, text="Total: 0")
        self.lbl_total.pack(anchor=tk.W, pady=2)
        
        self.lbl_pendientes = ttk.Label(self.frame_estadisticas, text="Pendientes: 0")
        self.lbl_pendientes.pack(anchor=tk.W, pady=2)
        
        self.lbl_completadas = ttk.Label(self.frame_estadisticas, text="Completadas: 0")
        self.lbl_completadas.pack(anchor=tk.W, pady=2)
        
        self.lbl_progreso = ttk.Label(self.frame_estadisticas, text="Progreso: 0%")
        self.lbl_progreso.pack(anchor=tk.W, pady=2)
        
        # Barra de progreso
        self.progreso = ttk.Progressbar(self.frame_estadisticas, length=200, mode='determinate')
        self.progreso.pack(pady=10)
    
    def agregar_tarea(self):
        """Añade una nueva tarea"""
        texto = self.txt_tarea.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Advertencia", "Por favor ingresa una descripción de la tarea")
            return
        
        tarea = Tarea(
            texto=texto,
            categoria=self.categoria_var.get(),
            prioridad=self.prioridad_var.get(),
            fecha_vencimiento=self.fecha_var.get()
        )
        
        self.tareas.append(tarea)
        self.actualizar_lista()
        self.limpiar_formulario()
        self.guardar_tareas()
        self.actualizar_estadisticas()
        
        messagebox.showinfo("Éxito", "Tarea agregada correctamente")
    
    def limpiar_formulario(self):
        """Limpia el formulario de entrada"""
        self.txt_tarea.delete("1.0", tk.END)
        self.categoria_var.set("General")
        self.prioridad_var.set("Media")
        self.fecha_var.set("")
    
    def actualizar_lista(self):
        """Actualiza el treeview con las tareas filtradas"""
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Aplicar filtros
        tareas_filtradas = self.filtrar_tareas_data()
        
        # Mostrar tareas
        for idx, tarea in enumerate(tareas_filtradas):
            estado = "✅" if tarea.completada else "⭕"
            
            # Color según prioridad (solo texto)
            prioridad_texto = tarea.prioridad
            if tarea.prioridad == "Alta":
                prioridad_texto = "🔴 Alta"
            elif tarea.prioridad == "Media":
                prioridad_texto = "🟡 Media"
            else:
                prioridad_texto = "🟢 Baja"
            
            # Verificar vencimiento
            vencimiento = tarea.fecha_vencimiento if tarea.fecha_vencimiento else "Sin fecha"
            if tarea.fecha_vencimiento and not tarea.completada:
                try:
                    fecha_vence = datetime.strptime(tarea.fecha_vencimiento, "%Y-%m-%d")
                    if fecha_vence < datetime.now():
                        vencimiento = "⚠️ VENCIDA"
                except:
                    pass
            
            # Insertar en treeview
            item_id = self.tree.insert("", tk.END, text=str(idx), 
                                      values=(estado, tarea.texto[:50], tarea.categoria, 
                                             prioridad_texto, vencimiento),
                                      tags=('completada' if tarea.completada else 'pendiente',))
            
            # Guardar referencia a la tarea
            self.tree.set(item_id, "Tarea", tarea.texto)  # Texto completo en tooltip
        
        # Configurar tags para colores
        self.tree.tag_configure('completada', foreground='#888888', font=('Arial', 9, 'overstrike'))
        self.tree.tag_configure('pendiente', foreground='#000000' if not self.tema_oscuro else '#ffffff')
    
    def filtrar_tareas_data(self) -> List[Tarea]:
        """Filtra las tareas según criterios de búsqueda"""
        texto_busqueda = self.busqueda_var.get().lower()
        filtro_estado = self.filtro_estado.get()
        
        tareas_filtradas = self.tareas.copy()
        
        # Filtrar por búsqueda
        if texto_busqueda:
            tareas_filtradas = [t for t in tareas_filtradas if texto_busqueda in t.texto.lower() or 
                               texto_busqueda in t.categoria.lower()]
        
        # Filtrar por estado
        if filtro_estado == "Pendientes":
            tareas_filtradas = [t for t in tareas_filtradas if not t.completada]
        elif filtro_estado == "Completadas":
            tareas_filtradas = [t for t in tareas_filtradas if t.completada]
        
        return tareas_filtradas
    
    def filtrar_tareas(self):
        """Refresca la lista aplicando filtros"""
        self.actualizar_lista()
    
    def marcar_completada(self):
        """Marca la tarea seleccionada como completada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una tarea")
            return
        
        # Obtener índice real considerando filtros
        idx_texto = self.tree.item(seleccion[0])['text']
        tareas_filtradas = self.filtrar_tareas_data()
        
        if int(idx_texto) < len(tareas_filtradas):
            tarea = tareas_filtradas[int(idx_texto)]
            # Encontrar la tarea original
            for t in self.tareas:
                if t.texto == tarea.texto and t.fecha_creacion == tarea.fecha_creacion:
                    t.completada = not t.completada
                    break
            
            self.actualizar_lista()
            self.guardar_tareas()
            self.actualizar_estadisticas()
    
    def eliminar_tarea(self):
        """Elimina la tarea seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una tarea")
            return
        
        if messagebox.askyesno("Confirmar", "¿Eliminar esta tarea?"):
            idx_texto = self.tree.item(seleccion[0])['text']
            tareas_filtradas = self.filtrar_tareas_data()
            
            if int(idx_texto) < len(tareas_filtradas):
                tarea = tareas_filtradas[int(idx_texto)]
                # Eliminar de la lista original
                self.tareas = [t for t in self.tareas if not (t.texto == tarea.texto and t.fecha_creacion == tarea.fecha_creacion)]
                
                self.actualizar_lista()
                self.guardar_tareas()
                self.actualizar_estadisticas()
                self.lista_subtareas.delete(0, tk.END)  # Limpiar subtareas
    
    def editar_tarea_dialog(self, event=None):
        """Abre diálogo para editar tarea"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una tarea")
            return
        
        idx_texto = self.tree.item(seleccion[0])['text']
        tareas_filtradas = self.filtrar_tareas_data()
        
        if int(idx_texto) < len(tareas_filtradas):
            tarea = tareas_filtradas[int(idx_texto)]
            
            # Diálogo de edición
            dialog = tk.Toplevel(self.root)
            dialog.title("Editar Tarea")
            dialog.geometry("400x400")
            dialog.transient(self.root)
            dialog.grab_set()
            
            ttk.Label(dialog, text="Descripción:").pack(pady=5)
            txt_edit = tk.Text(dialog, height=5, width=50)
            txt_edit.insert("1.0", tarea.texto)
            txt_edit.pack(pady=5)
            
            ttk.Label(dialog, text="Categoría:").pack(pady=5)
            categoria_edit = ttk.Combobox(dialog, values=["General", "Trabajo", "Personal", "Estudios", "Hogar", "Salud", "Finanzas"])
            categoria_edit.set(tarea.categoria)
            categoria_edit.pack(pady=5)
            
            ttk.Label(dialog, text="Prioridad:").pack(pady=5)
            prioridad_edit = ttk.Combobox(dialog, values=["Alta", "Media", "Baja"])
            prioridad_edit.set(tarea.prioridad)
            prioridad_edit.pack(pady=5)
            
            ttk.Label(dialog, text="Fecha vencimiento (YYYY-MM-DD):").pack(pady=5)
            fecha_edit = ttk.Entry(dialog)
            fecha_edit.insert(0, tarea.fecha_vencimiento)
            fecha_edit.pack(pady=5)
            
            def guardar_edicion():
                # Encontrar tarea original
                for t in self.tareas:
                    if t.texto == tarea.texto and t.fecha_creacion == tarea.fecha_creacion:
                        t.texto = txt_edit.get("1.0", tk.END).strip()
                        t.categoria = categoria_edit.get()
                        t.prioridad = prioridad_edit.get()
                        t.fecha_vencimiento = fecha_edit.get()
                        break
                
                self.actualizar_lista()
                self.guardar_tareas()
                dialog.destroy()
                messagebox.showinfo("Éxito", "Tarea actualizada")
            
            btn_guardar = tk.Button(dialog, text="Guardar", bg=self.colores["btn_primary"], 
                                   fg="white", command=guardar_edicion)
            btn_guardar.pack(pady=20)
    
    def ordenar_por_prioridad(self):
        """Ordena las tareas por prioridad"""
        prioridad_valor = {"Alta": 1, "Media": 2, "Baja": 3}
        self.tareas.sort(key=lambda x: prioridad_valor.get(x.prioridad, 2))
        self.actualizar_lista()
        self.guardar_tareas()
    
    def agregar_subtarea(self):
        """Agrega una subtarea a la tarea seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una tarea")
            return
        
        subtarea_texto = self.txt_subtarea.get().strip()
        if not subtarea_texto:
            messagebox.showwarning("Advertencia", "Ingresa una subtarea")
            return
        
        idx_texto = self.tree.item(seleccion[0])['text']
        tareas_filtradas = self.filtrar_tareas_data()
        
        if int(idx_texto) < len(tareas_filtradas):
            tarea = tareas_filtradas[int(idx_texto)]
            # Encontrar tarea original
            for t in self.tareas:
                if t.texto == tarea.texto and t.fecha_creacion == tarea.fecha_creacion:
                    t.subtareas.append({"texto": subtarea_texto, "completada": False})
                    break
            
            self.cargar_subtareas(tarea)
            self.txt_subtarea.delete(0, tk.END)
            self.guardar_tareas()
    
    def eliminar_subtarea(self):
        """Elimina la subtarea seleccionada"""
        seleccion = self.lista_subtareas.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una subtarea")
            return
        
        seleccion_tarea = self.tree.selection()
        if seleccion_tarea:
            idx_texto = self.tree.item(seleccion_tarea[0])['text']
            tareas_filtradas = self.filtrar_tareas_data()
            
            if int(idx_texto) < len(tareas_filtradas):
                tarea = tareas_filtradas[int(idx_texto)]
                for t in self.tareas:
                    if t.texto == tarea.texto and t.fecha_creacion == tarea.fecha_creacion:
                        t.subtareas.pop(seleccion[0])
                        break
                
                self.cargar_subtareas(tarea)
                self.guardar_tareas()
    
    def cargar_subtareas(self, tarea):
        """Carga las subtareas en el listbox"""
        self.lista_subtareas.delete(0, tk.END)
        for sub in tarea.subtareas:
            estado = "✓ " if sub["completada"] else "○ "
            self.lista_subtareas.insert(tk.END, estado + sub["texto"])
    
    def mostrar_menu_contextual(self, event):
        """Muestra menú contextual al hacer clic derecho"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Completar", command=self.marcar_completada)
            menu.add_command(label="Editar", command=lambda: self.editar_tarea_dialog())
            menu.add_separator()
            menu.add_command(label="Eliminar", command=self.eliminar_tarea)
            menu.post(event.x_root, event.y_root)
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas y barra de progreso"""
        total = len(self.tareas)
        completadas = sum(1 for t in self.tareas if t.completada)
        pendientes = total - completadas
        progreso = (completadas / total * 100) if total > 0 else 0
        
        self.lbl_total.config(text=f"Total: {total}")
        self.lbl_pendientes.config(text=f"Pendientes: {pendientes}")
        self.lbl_completadas.config(text=f"Completadas: {completadas}")
        self.lbl_progreso.config(text=f"Progreso: {progreso:.1f}%")
        self.progreso['value'] = progreso
    
    def cambiar_tema(self):
        """Cambia entre tema claro y oscuro"""
        self.tema_oscuro = not self.tema_oscuro
        self.btn_tema.config(text="☀️ TEMA CLARO" if self.tema_oscuro else "🌙 TEMA OSCURO")
        self.aplicar_tema()
        self.actualizar_lista()  # Refrescar colores de texto
    
    def exportar_csv(self):
        """Exporta las tareas a archivo CSV"""
        if not self.tareas:
            messagebox.showwarning("Advertencia", "No hay tareas para exportar")
            return
        
        filename = filedialog.asksaveasfilename(defaultextension=".csv", 
                                               filetypes=[("CSV files", "*.csv")])
        if filename:
            try:
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Tarea", "Categoría", "Prioridad", "Estado", "Fecha Vencimiento", "Fecha Creación"])
                    for t in self.tareas:
                        estado = "Completada" if t.completada else "Pendiente"
                        writer.writerow([t.texto, t.categoria, t.prioridad, estado, 
                                       t.fecha_vencimiento, t.fecha_creacion])
                
                messagebox.showinfo("Éxito", f"Exportado a {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar: {e}")
    
    def guardar_tareas(self):
        """Guarda las tareas en archivo JSON"""
        try:
            datos = [t.to_dict() for t in self.tareas]
            with open(self.archivo_json, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar: {e}")
    
    def cargar_tareas(self):
        """Carga las tareas desde archivo JSON"""
        if os.path.exists(self.archivo_json):
            try:
                with open(self.archivo_json, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self.tareas = [Tarea.from_dict(d) for d in datos]
            except Exception as e:
                print(f"Error al cargar: {e}")
                self.tareas = []
        else:
            # Tareas de ejemplo
            self.tareas = [
                Tarea("Completar proyecto Python", "Trabajo", "Alta", (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")),
                Tarea("Hacer ejercicio", "Salud", "Media", (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")),
                Tarea("Leer libro", "Personal", "Baja", ""),
            ]
    
    def programar_guardado_automatico(self):
        """Programa guardado automático cada 30 segundos"""
        self.guardar_tareas()
        self.root.after(30000, self.programar_guardado_automatico)
    
    def configurar_atajos(self):
        """Configura atajos de teclado"""
        self.root.bind('<Control-n>', lambda e: self.agregar_tarea())
        self.root.bind('<Delete>', lambda e: self.eliminar_tarea())
        self.root.bind('<Control-f>', lambda e: self.entry_busqueda.focus())
        self.root.bind('<Escape>', lambda e: self.limpiar_formulario())
        self.root.bind('<Control-s>', lambda e: self.guardar_tareas())

def main():
    """Función principal"""
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
