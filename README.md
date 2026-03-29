# Tech Inventory API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009485?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.13+-3776ab?style=for-the-badge&logo=python)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791?style=for-the-badge&logo=postgresql)](https://www.postgresql.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-d52b1e?style=for-the-badge)](https://www.sqlalchemy.org)

RESTful API profesional para gestión integral de inventario y ventas de productos tecnológicos (teléfonos, computadoras, consolas). Construida con FastAPI, PostgreSQL y SQLAlchemy con autenticación JWT incluida.

## 🚀 Características Principales

### ✅ Autenticación y Autorización
- Registro y login de usuarios con JWT
- Contraseñas hasheadas con bcrypt
- Endpoints protegidos con Bearer tokens
- Profiler de usuario autenticado

### ✅ Gestión de Productos
- CRUD completo de productos
- Atributos: nombre, categoría, marca, SKU único, precio, stock
- Validación de SKU duplicado
- Filtrado y búsqueda de productos

### ✅ Gestión de Inventario
- Registro de movimientos de entrada/salida (kardex)
- Actualización automática de stock
- Validación de stock disponible antes de salida
- Historial trazable de movimientos por producto

### ✅ Gestión de Ventas
- Creación de ventas con múltiples ítems
- Descuento aplicable a nivel de venta
- Cálculo automático de subtotal y total
- Actualización automática de stock al vender
- Registro automático de movimiento de salida de inventario
- Detalle completo de cada venta

## 📋 Requisitos Previos

- **Python**: 3.11+
- **PostgreSQL**: 12+
- **pip**: Gestor de paquetes Python
- **Virtualenv** (recomendado)

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Steeven24/tech-inventory-api.git
cd tech-inventory-api
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\Activate.ps1
```

**Linux/MacOS:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

### 1. Crear base de datos en PostgreSQL

```sql
CREATE DATABASE tech_inventory;
```

### 2. Configurar variables de entorno

Copiar archivo de ejemplo:
```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:

```env
# Base de datos
DATABASE_URL=postgresql+psycopg2://postgres:tu_contraseña@localhost:5432/tech_inventory

# Seguridad JWT
SECRET_KEY=tu_clave_secreta_super_segura_cambiar_en_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**Importante**: En producción, cambiar `SECRET_KEY` a una cadena aleatoria segura.

## ▶️ Ejecutar la Aplicación

### Desarrollo (con hot-reload)

```bash
uvicorn main:app --reload
```

### Producción

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

La API estará disponible en: **http://localhost:8000**

## 📚 Documentación Interactiva

Una vez ejecutada la API, acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Estructura del Proyecto

```
tech-inventory-api/
├── main.py                           # Punto de entrada de la aplicación
├── requirements.txt                  # Dependencias del proyecto
├── .env.example                      # Plantilla de variables de entorno
├── .gitignore
├── README.md                         # Este archivo
│
├── core/                            # Módulo de configuración base
│   ├── __init__.py
│   ├── database.py                  # Configuración SQLAlchemy y conexión BD
│   └── security.py                  # Utilidades JWT para autenticación
│
├── models/                          # Modelos de base de datos (SQLAlchemy)
│   ├── __init__.py
│   ├── user_model.py                # Modelo de usuarios
│   ├── product_model.py             # Modelo de productos
│   ├── inventory_movement_model.py  # Modelo de movimientos de inventario
│   └── sale_model.py                # Modelos de ventas y detalles
│
├── schemas/                         # Esquemas Pydantic (validación/respuesta)
│   ├── __init__.py
│   ├── user_schema.py               # Esquemas de usuarios
│   ├── product_schema.py            # Esquemas de productos
│   ├── inventory_movement_schema.py # Esquemas de movimientos
│   └── sale_schema.py               # Esquemas de ventas
│
├── services/                        # Lógica de negocio
│   ├── __init__.py
│   ├── user_service.py              # Servicios de usuarios
│   ├── product_service.py           # Servicios de productos
│   ├── inventory_movement_service.py # Servicios de movimientos
│   └── sale_service.py              # Servicios de ventas
│
├── routes/                          # Rutas API (endpoints)
│   ├── __init__.py
│   ├── auth_routes.py               # Endpoints autenticación
│   ├── user_routes.py               # Endpoints gestión usuarios
│   ├── product_routes.py            # Endpoints gestión productos
│   ├── inventory_movement_routes.py # Endpoints movimientos inventario
│   └── sale_routes.py               # Endpoints gestión ventas
│
└── venv/                            # Entorno virtual (no subir a git)
```

## 📡 Endpoints API

### 🔐 Autenticación (Pública)

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/auth/login` | Login y obtener JWT token |
| `GET` | `/auth/me` | Perfil del usuario autenticado |

### 👥 Usuarios (Pública/Protegida)

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| `POST` | `/users` | Crear nuevo usuario | No |
| `GET` | `/users` | Listar todos usuarios | Sí |
| `GET` | `/users/{user_id}` | Obtener usuario por ID | Sí |
| `PUT` | `/users/{user_id}` | Actualizar usuario | Sí |
| `DELETE` | `/users/{user_id}` | Eliminar usuario | Sí |

### 📦 Productos (Protegida)

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| `POST` | `/products` | Crear producto | Sí |
| `GET` | `/products` | Listar productos | Sí |
| `GET` | `/products/{product_id}` | Obtener producto | Sí |
| `PUT` | `/products/{product_id}` | Actualizar producto | Sí |
| `DELETE` | `/products/{product_id}` | Eliminar producto | Sí |

### 📊 Movimientos de Inventario (Protegida)

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| `POST` | `/inventory-movements` | Registrar movimiento | Sí |
| `GET` | `/inventory-movements` | Listar movimientos | Sí |
| `GET` | `/inventory-movements/{movement_id}` | Obtener movimiento | Sí |
| `GET` | `/inventory-movements/product/{product_id}` | Movimientos por producto | Sí |

### 🛒 Ventas (Protegida)

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| `POST` | `/sales` | Crear venta | Sí |
| `GET` | `/sales` | Listar ventas | Sí |
| `GET` | `/sales/{sale_id}` | Obtener venta | Sí |

## 🔐 Autenticación

### 1. Registrarse (Crear Usuario)

```bash
POST /users
Content-Type: application/json

{
  "name": "Steven Loor",
  "email": "steven@example.com",
  "password": "SecurePassword123!"
}
```

### 2. Login

```bash
POST /auth/login
Content-Type: application/json

{
  "email": "steven@example.com",
  "password": "SecurePassword123!"
}
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Usar Token en Endpoints Protegidos

Incluir en header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 📖 Ejemplos de Uso

### Crear Producto

```bash
curl -X POST http://localhost:8000/products \
  -H "Authorization: Bearer TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15 Pro",
    "category": "Smartphones",
    "brand": "Apple",
    "sku": "IPHONE15PRO001",
    "price": 999.99,
    "stock": 50
  }'
```

### Registrar Movimiento de Entrada

```bash
curl -X POST http://localhost:8000/inventory-movements \
  -H "Authorization: Bearer TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "movement_type": "in",
    "quantity": 20,
    "note": "Compra a proveedor ABC"
  }'
```

### Crear Venta

```bash
curl -X POST http://localhost:8000/sales \
  -H "Authorization: Bearer TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "discount": 50.00,
    "items": [
      {
        "product_id": 1,
        "quantity": 2
      },
      {
        "product_id": 2,
        "quantity": 1
      }
    ]
  }'
```

## 🔄 Flujo de Ventas

1. **Crear venta** con ítems
2. **Sistema valida**:
   - Productos existen
   - Stock disponible por producto
   - Descuento no excede subtotal
3. **Sistema actualiza**:
   - Stock de cada producto (resta)
   - Crea registro de venta
   - Registra detalle de cada ítem
   - Crea movimientos de inventario tipo "out"
4. **Respuesta** incluye venta completa con detalles

## 🛠️ Stack Tecnológico

| Tecnología | Versión | Propósito |
|------------|---------|----------|
| FastAPI | 0.104+ | Framework web |
| Python | 3.13+ | Lenguaje |
| PostgreSQL | 14+ | Base de datos |
| SQLAlchemy | 2.0+ | ORM |
| Pydantic | 2.0+ | Validación datos |
| python-jose | 3.3+ | JWT tokens |
| passlib | 1.7+ | Hash contraseñas |
| uvicorn | 0.24+ | Servidor ASGI |
| python-dotenv | 1.0+ | Variables entorno |

## 📦 Dependencias

Ver `requirements.txt` para lista completa:

```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
passlib[bcrypt]
pydantic[email]
python-dotenv
python-jose[cryptography]
```

## 🚦 Próximas Features (Roadmap)

- [ ] Refresh tokens y logout
- [ ] Roles y permisos (admin, vendedor, bodeguero)
- [ ] Reportes de ventas
- [ ] Dashboard con métricas
- [ ] Categorías dinámicas
- [ ] Proveedores y órdenes de compra
- [ ] Devoluciones de ventas
- [ ] Alertas de stock bajo
- [ ] Búsqueda y filtros avanzados
- [ ] Rate limiting
- [ ] Tests automatizados
- [ ] CI/CD pipeline

## 🧪 Testing

(En desarrollo) Para ejecutar tests:

```bash
pytest
```

## 🐛 Troubleshooting

### Error: "DATABASE_URL is not configured"

Asegurar que `.env` existe y tiene `DATABASE_URL` definida.

### Error: "connection refused" en PostgreSQL

Verificar que PostgreSQL está corriendo:
- Windows: Services → PostgreSQL → Iniciar
- Linux: `sudo systemctl start postgresql`

### Error: "port 8000 already in use"

Cambiar puerto:
```bash
uvicorn main:app --port 8001 --reload
```

## 📝 Convenciones de Código

- **Nombres**: snake_case para variables/funciones, PascalCase para clases
- **Docstrings**: Documentar funciones importantes
- **Type hints**: Usados en parámetros y retornos
- **Commits**: Semantic versioning (feat: ..., fix: ..., etc)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear rama feature: `git checkout -b feature/nueva-feature`
3. Commit cambios: `git commit -m "feat: descripción"`
4. Push rama: `git push origin feature/nueva-feature`
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver `LICENSE` para más detalles.

## 👤 Autor

**Steven Loor** - [@Steeven24](https://github.com/Steeven24)

---

## 📞 Soporte

Para problemas o sugerencias, abrir un issue en el repositorio.

**Last Updated**: Marzo 29, 2026
