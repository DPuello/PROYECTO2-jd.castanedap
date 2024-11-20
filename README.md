# 🍦 Proyecto 2 - La Heladería Web

Un sistema web robusto desarrollado con Flask para administrar heladerías, gestionar inventario de productos e ingredientes.

El proyecto incluye una función en app.py que permite crear y configurar la base de datos. Para reiniciar la base de datos a su estado inicial, simplemente descomenta la línea 16 del archivo app.py.

Adicionalmente, se proporciona un archivo SQL de respaldo en la carpeta database que contiene la estructura completa de la base de datos.

## 🌐 Navegación
La página principal muestra un listado completo de heladerías y sus productos disponibles. Cada producto cuenta con un botón de venta que, al ser presionado, actualiza automáticamente tanto el registro de ventas de la heladería como el inventario de ingredientes.

En la parte superior encontrarás una barra de navegación que te permite acceder fácilmente a las secciones de ingredientes, productos e inicio. Para agregar nuevos productos o ingredientes, primero debes seleccionar una heladería específica desde la tabla principal.

## 📊 Diagrama Entidad Relación

![Diagrama Entidad Relación](./Diagrama%20Entidad%20Relación.png)


## 🧪 Ejecutar los test
Para ejecutar los test:

```
python -m unittest .\tests\test_products.py
```
```
python -m unittest .\tests\test_ingredients.py
```
```
python -m unittest .\tests\test_icecreamshop.py
```	

