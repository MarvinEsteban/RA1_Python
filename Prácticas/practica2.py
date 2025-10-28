horarios = {
    'María':  ('08', '16'),
    'Juan':   ('09', '17'),
    'Lucía':  ('07', '15'),
    'Diego':  ('10', '18'),
    # Ampliación (Actividad sugerida: añade más y verifica que todo sigue funcionando)
    'Ana':    ('08', '14'),
    'Raúl':   ('12', '20'),
    'Mariete':   ('13', '25'),
    'Rodrigo':   ('20', '30'),
    'Motis':   ('22', '45'),
    'Albert':   ('17', '17'),
    'Sofía':    ('06', '14'),
    'Andrés':   ('14', '22'),
    'Clara':    ('15', '23'),
    'Pedro':    ('05', '13'),
    'Valeria':  ('11', '19'),
    'Héctor':   ('00', '08'),  
    'Elena':    ('16', '00'), 
    'Manuel':   ('18', '02'),
    'Paula':    ('04', '12'),
}
 
def mostrar_registros():

    print("\n=== REGISTROS ===")
    for i, (persona, (entrada, salida)) in enumerate(horarios.items(), start=1):
        print(f"{i}. {persona} -> {entrada}:00h - {salida}:00h")
    print()

def contar_entradas():
    
    try:
        hora_usuario = int(input("Introduce una hora (0–23): "))

        if hora_usuario < 0 or hora_usuario > 23:
            print("Hora incorrecta, por favor introduce un número entero entre 0-23.")
            return

        contador = 0

        for persona, (entrada, _) in horarios.items():

            try:
                if int(entrada) == hora_usuario:
                    contador += 1

                print(f"\nPersonas que entran a las {hora_usuario:02d}:00 -> {contador}")
            except ValueError:
                continue

    except ValueError:
        print("Debes introducir un número entero (0–23).")

def menu():
    """
    Menú principal repetitivo (bucle while) para elegir acciones:
      1) Mostrar registros
      2) Contar entradas
      3) Salir
    """
    while True:
        print("========== MENÚ ==========")
        print("1) Mostrar registros")
        print("2) Contar entradas")
        print("3) Salir")
        opcion = input("Elige una opción (1-3): ").strip()
 
        if opcion == '1':
            mostrar_registros()
        elif opcion == '2':
            contar_entradas()
        elif opcion == '3':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.\n")
 
 
# ---------------------------------------------------------------------------
# 4) Punto de entrada
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    # Consejo de depuración: descomenta las dos líneas siguientes para pausar en este punto
    # import debugpy
    # debugpy.breakpoint()
 
    menu()

  