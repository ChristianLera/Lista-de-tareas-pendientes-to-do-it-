# 📋 To-Do List Profesional

Aplicación de gestión de tareas completa y moderna desarrollada en Python con Tkinter.

![Versión](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![Licencia](https://img.shields.io/badge/license-MIT-yellow)

## 👨‍💻 Autor

**Christian Lera**

## ✨ Características

- ✅ Crear, editar y eliminar tareas
- 🏷️ Categorización de tareas (Trabajo, Personal, Estudios, Hogar, Salud, Finanzas)
- 🔴 Prioridades (Alta, Media, Baja)
- 📅 Fechas de vencimiento
- 📝 Subtareas para cada tarea principal
- 🔍 Búsqueda y filtrado por estado (Todas/Pendientes/Completadas)
- 🌙 Tema oscuro / claro
- 📊 Estadísticas y barra de progreso
- 💾 Guardado automático en JSON
- 📤 Exportación a CSV
- ⌨️ Atajos de teclado
- 🖱️ Menú contextual (clic derecho)

## 🖥️ Capturas de pantalla

*(Añade aquí capturas de la aplicación)*

## 📋 Atajos de teclado

| Tecla | Acción |
|-------|--------|
| `Ctrl + N` | Nueva tarea |
| `Delete` | Eliminar tarea seleccionada |
| `Ctrl + F` | Enfocar búsqueda |
| `Ctrl + S` | Guardar manualmente |
| `Escape` | Limpiar formulario |

## 📁 Estructura del proyecto

```
ToDoIt/
├── ToDoIt.py           # Código principal de la aplicación
├── tareas.json         # Archivo de datos (se genera automáticamente)
├── ejecutar.bat        # Script para Windows (CMD)
├── ejecutar.ps1        # Script para Windows (PowerShell)
└── README.md           # Este archivo
```

## 🔧 Instalación

### Requisitos previos
- Python 3.7 o superior instalado en el sistema

### Pasos

1. **Clonar o descargar el repositorio**

## 🚀 Ejecución

### Windows (CMD)
```cmd
ejecutar.bat
```

### Windows (PowerShell)
```powershell
.\ejecutar.ps1
```

### Manual
```bash
python ToDoIt.py
```

## 📦 Dependencias

La aplicación solo utiliza módulos de la biblioteca estándar de Python:
- `tkinter` - Interfaz gráfica
- `json` - Almacenamiento de datos
- `datetime` - Manejo de fechas
- `os` - Operaciones del sistema
- `csv` - Exportación de datos

No requiere paquetes externos adicionales.

## 💾 Datos

Los datos se guardan automáticamente en `tareas.json` cada 30 segundos. También puedes guardar manualmente con `Ctrl + S`.

## 📤 Exportar datos

Puedes exportar tus tareas a CSV usando el botón "Exportar CSV" en la interfaz.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea tu rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📧 Contacto

**Christian Lera** - [Tu email o GitHub]

---

⭐ Si te gusta este proyecto, ¡no olvides darle una estrella!
