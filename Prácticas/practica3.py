import csv

class RegistroHorario: 
    def __init__(self, empleado: str, dia: str, entrada: int, salida: int):
        self.empleado = empleado
        self.dia = dia
        self.entrada = entrada
        self.salida = salida

    def duracion(self) -> int:
        """Devuelve la cantidad de horas trabajadas en este registro"""
        return self.salida - self.entrada
        
registros = []
with open('prácticas/horarios.csv', newline='', encoding='utf-8') as f:
    lector = csv.reader(f, delimiter=';', quotechar='"')
    for fila in lector:
        # Cada fila es una lista de cadenas: [nombre, dia, entrada, salida]
        nombre, dia, h_entrada, h_salida = fila
        # Convertimos las horas a enteros
        entrada = int(h_entrada)
        salida = int(h_salida)
        registro = RegistroHorario(nombre, dia, entrada, salida)
        registros.append(registro)

print(f"Se han leído {len(registros)} registros")

empleados_por_dia = {}
for registro in registros:
    # Creamos el conjunto para el día si no existe
    if registro.dia not in empleados_por_dia:
        empleados_por_dia[registro.dia] = set()
    # Añadimos el empleado al conjunto del día
    empleados_por_dia[registro.dia].add(registro.empleado)

# Mostrar empleados por día
for dia, empleados in empleados_por_dia.items():
    print(f"{dia}: {empleados}")

# Calcular horas totales por empleado
horas_totales = {}
for registro in registros:
    horas_totales.setdefault(registro.empleado, 0)
    horas_totales[registro.empleado] += registro.duracion()

# Escribir un resumen en un nuevo CSV
with open('prácticas/resumen_horarios.csv', 'w', newline='', encoding='utf-8') as f:
    escritor = csv.writer(f, delimiter=';', quotechar='"')
    # Cabecera
    escritor.writerow(['Empleado', 'Horas totales'])
    # Filas con los datos acumulados
    for empleado, total in horas_totales.items():
        escritor.writerow([empleado, total])

print("Se ha generado el fichero resumen_horarios.csv")

#------------------------
# EMPLEADOS MADRUGADORES
#------------------------

hora_referencia = 9 #hora de referencia escogida

# Usamos un conjunto para evitar duplicados
madrugadores = set()

# Recorremos los registros para ver quién entra antes de la hora de referencia
for registro in registros:
    if registro.entrada < hora_referencia:
        madrugadores.add((registro.empleado, registro.entrada))

# Guardar los resultados en el csv
with open('prácticas/madrugadores.csv', 'w', newline='', encoding='utf-8') as f:
    escritor = csv.writer(f, delimiter=';', quotechar='"')
    escritor.writerow(['Empleado', 'Hora_entrada'])
    for empleado, hora in madrugadores:
        escritor.writerow([empleado, hora])

print("Se ha generado el fichero madrugadores.csv")

# -------------------------------------------------------
# Empleados que trabajaron tanto el lunes como el viernes
# -------------------------------------------------------

# Comprobamos que existan los dos días en el diccionario
if 'Lunes' in empleados_por_dia and 'Viernes' in empleados_por_dia:
    ambos_dias = empleados_por_dia['Lunes'] & empleados_por_dia['Viernes']

    print("\nEmpleados que trabajaron tanto el lunes como el viernes:")
    for empleado in ambos_dias:
        print(empleado)

    # Guardamos el resultado en un nuevo CSV
    with open('prácticas/en_dos_dias.csv', 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f, delimiter=';', quotechar='"')
        escritor.writerow(['Empleado'])
        for empleado in ambos_dias:
            escritor.writerow([empleado])

    print("Se ha generado el fichero en_dos_dias.csv")
else:
    print("No se han encontrado datos para Lunes o Viernes.")

#-----------------------------------------
# EMPLEADOS SÁBADO PERO NO DOMINGO
#-----------------------------------------

# Comprobamos que existan los días en el diccionario
if 'Sábado' in empleados_por_dia and 'Domingo' in empleados_por_dia:
    exclusivos = empleados_por_dia['Sábado'] - empleados_por_dia['Domingo']

    print("Empleados que trabajaron el sábado pero no el domingo:")
    for empleado in exclusivos:
        print(empleado)

    # Guardamos el resultado en CSV
    with open('prácticas/exclusivos_sabado.csv', 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f, delimiter=';', quotechar='"')
        escritor.writerow(['Empleado'])
        for empleado in exclusivos:
            escritor.writerow([empleado])

    print("Se ha generado el fichero exclusivos_sabado.csv")
else:
    print("No se han encontrado empleados que trabajen el sabado y no el domingo.")

# -------------------------------------------------
# Resumen semanal
# -------------------------------------------------

# Diccionario donde guardaremos horas totales y días trabajados
resumen_semanal = {}

for registro in registros:
    # Inicializamos si no existe
    if registro.empleado not in resumen_semanal:
        resumen_semanal[registro.empleado] = {'horas_totales': 0, 'dias': set()}
    
    # Sumamos horas y añadimos día al set
    resumen_semanal[registro.empleado]['horas_totales'] += registro.duracion()
    resumen_semanal[registro.empleado]['dias'].add(registro.dia)

# Escribimos resumen_semanal.csv
with open('prácticas/resumen_semanal.csv', 'w', newline='', encoding='utf-8') as f:
    escritor = csv.writer(f, delimiter=';', quotechar='"')
    escritor.writerow(['Empleado', 'Dias_trabajados', 'Horas_totales'])
    for empleado, info in resumen_semanal.items():
        escritor.writerow([empleado, len(info['dias']), info['horas_totales']])

print("Se ha generado el fichero resumen_semanal.csv")

# -------------------------------------------------
# Filtrado por duración: empleados con al menos 6 horas en todas sus jornadas
# -------------------------------------------------

empleados_min6h = {empleado for empleado in resumen_semanal
                    if all(reg.duracion() >= 6 and reg.empleado == empleado for reg in registros)}

print("\nEmpleados que trabajaron al menos 6 horas en todas sus jornadas:")
for e in empleados_min6h:
    print(e)

# Guardamos el resultado en CSV
with open('prácticas/empleados_6h.csv', 'w', newline='', encoding='utf-8') as f:
    escritor = csv.writer(f, delimiter=';', quotechar='"')
    escritor.writerow(['Empleado'])
    for empleado in empleados_min6h:
        escritor.writerow([empleado])

print("Se ha generado el fichero empleados_6h.csv")

# -------------------
# CREACIÓN DE CLASES
# -------------------

# Clase RegistroHorario para crear los gorarios de cada empleado y luego almacenarlos
class RegistroHorario:
    def __init__(self, empleado, dia, entrada, salida):
        self.empleado = empleado
        self.dia = dia
        self.entrada = entrada
        self.salida = salida

    def duracion(self):
        return self.salida - self.entrada
    
# Clase empleado
class Empleado:

    def __init__ (self, nombre):
        self.nombre = nombre
        self.registros = []

    def agregarRegistro(self, registro):
        self.registros.append(registro)

    def horasTotales(self):
        return sum(r.duracion() for r in self.registros)

    def diasTrabajados(self):
        return len(set(r.dia for r in self.registros))
    
    def filaCsv(self):
        return [self.nombre, self.diasTrabajados(), self.horasTotales()]

 # Clase GestorHorarios

class GestorHorarios:
    def __init__(self, archivo_entrada):
        self.archivo_entrada = archivo_entrada
        self.empleados = {}

    def leerCsv(self):
        with open(self.archivo_entrada, newline='', encoding='utf-8') as f:
            lector = csv.reader(f, delimiter=';', quotechar='"')
            for fila in lector:
                nombre, dia, h_entrada, h_salida = fila
                registro = RegistroHorario(nombre, dia, int(h_entrada), int(h_salida))
                if nombre not in self.empleados:
                    self.empleados[nombre] = Empleado(nombre)
                self.empleados[nombre].agregarRegistro(registro)

    def generarResumen(self, archivo_salida):
        with open(archivo_salida, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f, delimiter=';', quotechar='"')
            escritor.writerow(['Empleado', 'Dias_trabajados', 'Horas_totales'])
            for empleado in self.empleados.values():
                escritor.writerow(empleado.filaCsv())

# Código principal
gestor = GestorHorarios('prácticas/horarios.csv')
gestor.leerCsv()
gestor.generarResumen('prácticas/resumen_clases.csv')
print("Se ha generado resumen_clases.csv")