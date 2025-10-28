# practicaFinal.py - Mini CRM de eventos (con CSV, clases y datetime)

# Imports de librerías necesarias para la práctica
import csv
import re
from datetime import datetime, date
from typing import List, Dict, Set, Tuple, Optional
import os

# Definición de constantes de archivos utilizadoss
DATA_DIR = "data"
CLIENTES_CSV = f"{DATA_DIR}/clientes.csv"
EVENTOS_CSV = f"{DATA_DIR}/eventos.csv"
VENTAS_CSV = f"{DATA_DIR}/ventas.csv"
INFORME_CSV = f"{DATA_DIR}/informe_resumen.csv"


# ------------------------------
# CLASES
# ------------------------------

class Cliente:
    def __init__(self, id_: int, nombre: str, email: str, fecha_alta: date):
        self.id = id_
        self.nombre = nombre
        self.email = email
        self.fecha_alta = fecha_alta

    def antiguedad_dias(self) -> int:
        return (date.today() - self.fecha_alta).days

    def __repr__(self):
        return f"[{self.id}] {self.nombre} ({self.email}) - Alta: {self.fecha_alta}"


class Evento:
    def __init__(self, id_: int, titulo: str, categoria: str, fecha: date, precio: float):
        self.id = id_
        self.titulo = titulo
        self.categoria = categoria
        self.fecha = fecha
        self.precio = precio

    def dias_hasta_evento(self) -> int:
        return (self.fecha - date.today()).days

    def __repr__(self):
        return f"[{self.id}] {self.titulo} ({self.categoria}) - {self.fecha} - {self.precio}€"


class Venta:
    def __init__(self, id_: int, cliente_id: int, evento_id: int,
                 fecha: date, cantidad: int, precio_unitario: float):
        self.id = id_
        self.cliente_id = cliente_id
        self.evento_id = evento_id
        self.fecha = fecha
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    def total(self) -> float:
        return self.cantidad * self.precio_unitario

    def __repr__(self):
        return f"Venta[{self.id}] cliente={self.cliente_id}, evento={self.evento_id}, {self.fecha}, total={self.total()}€"


# ------------------------------
# FUNCIONES AUXILIARES
# ------------------------------

def validar_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def leer_fecha(texto: str) -> Optional[date]:
    try:
        return datetime.strptime(texto, "%Y-%m-%d").date()
    except ValueError:
        return None


def leer_csv_seguro(path: str):
    if not os.path.exists(path):
        print(f"Aviso: no se encontró {path}. Se usará una lista vacía.")
        return []
    with open(path, newline='', encoding='utf-8') as f:
        lector = csv.DictReader(f, delimiter=';')
        return list(lector)


# ------------------------------
# CARGA DE DATOS
# ------------------------------

clientes: Dict[int, Cliente] = {}
eventos: Dict[int, Evento] = {}
ventas: List[Venta] = []


def cargar_datos():
    global clientes, eventos, ventas
    clientes.clear()
    eventos.clear()
    ventas.clear()

    # CLIENTES
    for fila in leer_csv_seguro(CLIENTES_CSV):
        clientes[int(fila["id"])] = Cliente(
            int(fila["id"]),
            fila["nombre"],
            fila["email"],
            leer_fecha(fila["fecha_alta"])
        )

    # EVENTOS
    for fila in leer_csv_seguro(EVENTOS_CSV):
        eventos[int(fila["id"])] = Evento(
            int(fila["id"]),
            fila["titulo"],
            fila["categoria"],
            leer_fecha(fila["fecha"]),
            float(fila["precio"])
        )

    # VENTAS
    for fila in leer_csv_seguro(VENTAS_CSV):
        ventas.append(Venta(
            int(fila["id"]),
            int(fila["cliente_id"]),
            int(fila["evento_id"]),
            leer_fecha(fila["fecha"]),
            int(fila["cantidad"]),
            float(fila["precio_unitario"])
        ))

    print(f"Datos cargados: {len(clientes)} clientes, {len(eventos)} eventos, {len(ventas)} ventas.")


# ------------------------------
# LISTAR TABLAS
# ------------------------------

def listar(tabla: str):
    if tabla == "clientes":
        for c in clientes.values():
            print(c)
    elif tabla == "eventos":
        for e in eventos.values():
            print(e)
    elif tabla == "ventas":
        for v in ventas:
            print(v)
    else:
        print("Tabla no válida. Usa: clientes / eventos / ventas.")


# ------------------------------
# ALTA DE CLIENTE
# ------------------------------

def alta_cliente():
    nombre = input("Nombre: ").strip()
    email = input("Email: ").strip()
    if not validar_email(email):
        print("Email no válido.")
        return
    fecha_texto = input("Fecha de alta (YYYY-MM-DD): ").strip()
    fecha = leer_fecha(fecha_texto)
    if not fecha:
        print("Fecha inválida.")
        return

    nuevo_id = max(clientes.keys(), default=0) + 1
    nuevo = Cliente(nuevo_id, nombre, email, fecha)
    clientes[nuevo_id] = nuevo

    # Guardar incrementalmente
    existe = os.path.exists(CLIENTES_CSV)
    with open(CLIENTES_CSV, "a", newline='', encoding='utf-8') as f:
        escritor = csv.writer(f, delimiter=';')
        if not existe:
            escritor.writerow(["id", "nombre", "email", "fecha_alta"])
        escritor.writerow([nuevo.id, nuevo.nombre, nuevo.email, nuevo.fecha_alta])
    print("Cliente agregado correctamente.")


# ------------------------------
# FILTRAR VENTAS POR RANGO
# ------------------------------

def filtrar_ventas_por_rango():
    inicio = leer_fecha(input("Fecha inicio (YYYY-MM-DD): "))
    fin = leer_fecha(input("Fecha fin (YYYY-MM-DD): "))
    if not inicio or not fin:
        print("Fechas inválidas.")
        return
    print(f"\nVentas entre {inicio} y {fin}:\n")
    for v in ventas:
        if inicio <= v.fecha <= fin:
            print(v)


# ------------------------------
# ESTADÍSTICAS
# ------------------------------

def estadisticas():
    if not ventas:
        print("No hay ventas cargadas.")
        return

    ingresos_totales = sum(v.total() for v in ventas)
    ingresos_por_evento: Dict[str, float] = {}
    for v in ventas:
        evento = eventos.get(v.evento_id)
        if evento:
            ingresos_por_evento[evento.titulo] = ingresos_por_evento.get(evento.titulo, 0) + v.total()

    categorias: Set[str] = {e.categoria for e in eventos.values()}

    dias_hasta_evento_mas_prox = min(e.dias_hasta_evento() for e in eventos.values())

    precios = [e.precio for e in eventos.values()]
    tupla_precios = (min(precios), max(precios), round(sum(precios) / len(precios), 2))

    print(f"\nESTADÍSTICAS:")
    print(f"Ingresos totales: {ingresos_totales:.2f} €")
    print(f"Ingresos por evento: {ingresos_por_evento}")
    print(f"Categorías existentes: {categorias}")
    print(f"Días hasta el evento más próximo: {dias_hasta_evento_mas_prox}")
    print(f"(min, max, media) precios eventos: {tupla_precios}")


# ------------------------------
# EXPORTAR INFORME
# ------------------------------

def exportar_informe():
    if not ventas:
        print("No hay ventas cargadas.")
        return
    resumen: Dict[int, float] = {}
    for v in ventas:
        resumen[v.evento_id] = resumen.get(v.evento_id, 0) + v.total()

    with open(INFORME_CSV, "w", newline='', encoding='utf-8') as f:
        escritor = csv.writer(f, delimiter=';')
        escritor.writerow(["Evento", "Total_ingresos"])
        for evento_id, total in resumen.items():
            nombre_evento = eventos[evento_id].titulo if evento_id in eventos else f"Evento {evento_id}"
            escritor.writerow([nombre_evento, round(total, 2)])
    print(f"Informe exportado en {INFORME_CSV}")


# ------------------------------
# MENÚ PRINCIPAL
# ------------------------------

def menu():
    while True:
        print("\n=== MINI CRM DE EVENTOS ===")
        print("1) Cargar datos")
        print("2) Listar tabla")
        print("3) Alta de cliente")
        print("4) Filtrar ventas por rango de fechas")
        print("5) Estadísticas")
        print("6) Exportar informe resumen")
        print("7) Salir")

        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            cargar_datos()
        elif opcion == "2":
            tabla = input("¿Qué tabla quieres listar? (clientes/eventos/ventas): ").strip()
            listar(tabla)
        elif opcion == "3":
            alta_cliente()
        elif opcion == "4":
            filtrar_ventas_por_rango()
        elif opcion == "5":
            estadisticas()
        elif opcion == "6":
            exportar_informe()
        elif opcion == "7":
            print("Cerrando programa...")
            break
        else:
            print("Opción no válida.")


# ------------------------------
# PUNTO DE ENTRADA
# ------------------------------

# NOTA: Ya que el código se va a ejecutar en un portátil que no es el mío,
# para asegurar de que exista el directorio data antes de ejecutarse se 
# realiza el os.makedirs para crearlo en caso de que no exista en el sistema
# operativo.

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    menu()
