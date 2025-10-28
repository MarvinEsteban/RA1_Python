# 🐍 prácticaFinal.py - Mini CRM de Eventos

## 🌟 Resumen del Proyecto

Este proyecto es una **práctica final de programación en Python** que simula un **Mini CRM (Customer Relationship Management)** especializado en la gestión de **clientes, eventos y ventas** asociadas.

El objetivo principal es demostrar la comprensión y aplicación de conceptos fundamentales de Python como la **Programación Orientada a Objetos (POO)** mediante clases (`Cliente`, `Evento`, `Venta`), el manejo de **estructuras de datos complejas** (`Dict`, `List`, `Set`), la **gestión de archivos CSV** para la persistencia de datos, y el uso de la librería `datetime` para el manejo de fechas.

---

## ⚙️ Tecnologías y Características Clave

| Característica | Descripción | Librerías/Conceptos |
| :--- | :--- | :--- |
| **Persistencia de Datos** | Lectura y escritura de datos desde/hacia archivos CSV. | `csv`, `os` |
| **Modelado de Datos (POO)** | Clases para representar las entidades principales del sistema. | Clases `Cliente`, `Evento`, `Venta` |
| **Manejo de Fechas** | Cálculos de antigüedad de clientes, días hasta eventos y filtrado por rango. | `datetime`, `date` |
| **Validación de Datos** | Uso de expresiones regulares para validar el formato de email. | `re` |
| **Análisis de Datos** | Cálculo de estadísticas agregadas (ingresos totales, precios, etc.) y exportación de informes. | Funciones de agregación, diccionarios, sets |
| **Interfaz de Usuario** | Menú interactivo basado en consola. | Función `menu()` |

---

## 📂 Estructura de Archivos

La aplicación espera encontrar los datos iniciales y generará los archivos de informe dentro