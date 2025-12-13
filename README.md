# BizFlow - Sistema de Gestión de Ventas

Un sistema completo de gestión de ventas desarrollado en Django con MySQL.

## 🚀 Características

- **Dashboard** con métricas de ventas
- **Gestión de Productos** con categorías e imágenes
- **Gestión de Clientes** con información completa
- **Sistema de Ventas** con detalles y estados
- **Panel de Administración** completo
- **Interfaz responsive** con Bootstrap

## 📋 Requisitos

- Python 3.8+
- MySQL 5.7+
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd BizFlow
```

### 2. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
1. Crear base de datos MySQL:
```sql
CREATE DATABASE bizflow_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Configurar archivo `.env`:
```bash
cp .env.example .env
```

3. Editar `.env` con tus credenciales:
```
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
DB_NAME=bizflow_db
DB_USER=tu_usuario_mysql
DB_PASSWORD=tu_password_mysql
DB_HOST=localhost
DB_PORT=3306
```

### 5. Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario
```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor
```bash
python manage.py runserver
```

## 🎯 Uso

### Acceso a la aplicación
- **Aplicación principal**: http://127.0.0.1:8000
- **Panel de administración**: http://127.0.0.1:8000/admin

### Funcionalidades principales

#### Dashboard
- Métricas de ventas totales
- Contador de clientes activos
- Contador de productos disponibles
- Lista de ventas recientes

#### Gestión de Productos
- Crear, editar y eliminar productos
- Organizar por categorías
- Subir imágenes de productos
- Control de stock

#### Gestión de Clientes
- Registro completo de clientes
- Información de contacto
- Estado activo/inactivo

#### Sistema de Ventas
- Crear nuevas ventas
- Asociar múltiples productos
- Estados: Pendiente, Completada, Cancelada
- Cálculo automático de totales

## 📁 Estructura del Proyecto

```
BizFlow/
├── bizflow/                 # Configuración del proyecto
│   ├── settings.py         # Configuración principal
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # Configuración WSGI
├── ventas/                 # Aplicación de ventas
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Vistas
│   ├── admin.py           # Configuración admin
│   ├── urls.py            # URLs de la app
│   └── templates/         # Templates HTML
├── static/                 # Archivos estáticos
├── media/                  # Archivos subidos
├── requirements.txt        # Dependencias
├── .env.example           # Ejemplo de configuración
└── manage.py              # Script de Django
```

## 🗃️ Modelos de Datos

### Cliente
- Nombre, email, teléfono
- Dirección y fecha de registro
- Estado activo/inactivo

### Categoría
- Nombre y descripción

### Producto
- Nombre, descripción, precio
- Categoría asociada
- Stock e imagen
- Estado activo/inactivo

### Venta
- Cliente y vendedor
- Fecha y total
- Estado (pendiente/completada/cancelada)
- Notas adicionales

### DetalleVenta
- Producto y cantidad
- Precio unitario y subtotal

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
SECRET_KEY=clave-secreta-django
DEBUG=True/False
DB_NAME=nombre_base_datos
DB_USER=usuario_mysql
DB_PASSWORD=password_mysql
DB_HOST=localhost
DB_PORT=3306
```

### Configuración de MySQL
Asegúrate de que MySQL esté ejecutándose y que tengas los permisos necesarios.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🆘 Soporte

Si tienes problemas o preguntas:

1. Revisa la documentación
2. Busca en los issues existentes
3. Crea un nuevo issue con detalles del problema

## 🔄 Próximas Funcionalidades

- [ ] Reportes de ventas
- [ ] Gráficos y estadísticas
- [ ] Sistema de inventario avanzado
- [ ] Facturación automática
- [ ] API REST
- [ ] Notificaciones por email