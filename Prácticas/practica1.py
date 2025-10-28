trabajadores = input("Indica cantidad de trabajadores: ")
num_trabajadores = int(trabajadores)
print ("Hay " + trabajadores + " trabajadores.")

trabajadores_correctos = 0
trabajadores_incorrectos = 0
trabajador_mas_temprano_nombre = None
trabajador_mas_temprano_hora = None
trabajadores_entrada_temprana = 0
trabajador_salida_temprana = None
nombre_salida_temprana = None
trabajadores_madrugadores = 0

while num_trabajadores > 0:
    num_trabajadores -= 1
    
    nombre_empleado = input("Ingresa nombre del empleado: ")
    hora_entrada = input("Ingresa hora entrada del empleado: ")
    hora1 = int(hora_entrada)
    hora_salida = input("Ingresa hora salida del empleado: ")
    hora2 = int(hora_salida)

    if hora1 < hora2:
        print("Hora correcta!")
        trabajadores_correctos += 1
        
    else:
        print("Hora incorrecta!")
        trabajadores_incorrectos += 1
    
    if trabajador_mas_temprano_hora is None or trabajador_mas_temprano_hora > hora1:
        trabajador_mas_temprano_hora = hora1
        trabajador_mas_temprano_nombre = nombre_empleado
        

    if trabajador_salida_temprana is None or trabajador_salida_temprana > hora2:
        trabajador_salida_temprana = hora2
        nombre_salida_temprana = nombre_empleado

    if trabajador_mas_temprano_hora is not None and hora1 <= trabajador_mas_temprano_hora:
        trabajadores_madrugadores += 1
else:
    print("Hay " + str(trabajadores_correctos) + " que entran adecuadamente.") 
    print("Hay " + str(trabajadores_incorrectos) + " que entran inadecuadamente.") 

if trabajador_mas_temprano_hora is not None and trabajador_salida_temprana is not None:
    print("El trabajador que entra más temprano es " + trabajador_mas_temprano_nombre + " y entra a las " + str(trabajador_mas_temprano_hora) + ".")
    print("El trabajador que sale más temprano es " + nombre_salida_temprana + " y sale a las " + str(trabajador_salida_temprana) + ".")
    print("Hay " + str(trabajadores_madrugadores) + " que han entrado antes o a la hora de referencia")
