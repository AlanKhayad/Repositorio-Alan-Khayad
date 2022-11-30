import requests
import json

from equipos import Equipo
from estadios import Estadio
from restaurantes import Restaurante
from partidos import Partido
from boletos import Boleto
from productos import Producto, Bebida, Comida
from clientes1 import Cliente1

import emoji
from colorama import Fore, Back, Style
import random
from itertools import permutations

def importar_json_partidos(dict_partidos):
    archivo = "zproyecto/partidos.json" 
    with open(archivo, "r") as f:
        datos = f.read()
        dict_asientos_asist = json.loads(datos)
        f.close()
    return dict_asientos_asist

def importar_json_clientes(lista_clientes, lista_partidos, dict_clientes, lista_clientes_vip, codigos_usados, lista_clientes_1):
    archivo = "zproyecto/boletos.json"
    with open(archivo, "r") as f:
        datos = f.read()
        dict_clientes = json.loads(datos)
        f.close()
    
    for x,y in dict_clientes.items():
        for i in lista_partidos:
            if i.id == y["partido"]:
                partido = i
                break
        cliente = Boleto(y["nombre"], int(x), y["edad"], partido, y["tipo_entrada"], y["asiento"], y["id_entrada"], y["precio_ticket"], y["gasto_rest"], y["asistencia"])
        lista_clientes.append(cliente)

    for i in lista_clientes:
        if i.tipo_entrada == "VIP":
            lista_clientes_vip.append(i)

    #Importar codigos usados
    archivo = "zproyecto/codigos_usados.json"
    with open(archivo, "r") as f:
        datos = f.read()
        lista_cod = json.loads(datos)
        f.close()
    for i in lista_cod:
        codigos_usados.append(i)

    #Importar clientes1
    archivo = "zproyecto/clientes_1.json"
    with open(archivo, "r") as f:
        datos = f.read()
        dict_clientes1 = json.loads(datos)
        f.close()
    for x,y in dict_clientes1:
        cliente = Cliente1(y["nombre"], int(x), y["boletos"])
        lista_clientes_1.append(cliente)

    for i in lista_clientes_1:
        i.mostrar()

def crear_edd(lista_equipos, lista_estadios, lista_partidos, dict_partidos):
    url_equipos = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/teams.json"
    url_estadios = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/stadiums.json"
    url_partidos = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/matches.json"
    
    r1 = requests.get(url_equipos)
    r2 = requests.get(url_estadios)
    r3 = requests.get(url_partidos)

    edd_equipos = r1.json()
    edd_estadios = r2.json()
    edd_partidos = r3.json()

    for i in edd_equipos:
        equipo = Equipo(i["name"], i["flag"], i["fifa_code"], i["group"], i["id"])
        lista_equipos.append(equipo)
    
    for i in edd_estadios: 
        lista_rest = []
        for j in i["restaurants"]:
            lista_prod = []
            for k in j["products"]:
                if k["type"] == "beverages":
                    producto = Bebida(k["name"], k["price"], k["type"], 25, k["adicional"])
                    lista_prod.append(producto)
                if k["type"] == "food":
                    producto = Comida(k["name"], k["price"], k["type"], 25, k["adicional"])
                    lista_prod.append(producto)
            restaurante = Restaurante(j["name"], lista_prod)
            lista_rest.append(restaurante)
        estadio = Estadio(i["id"], i["name"], i["capacity"], i["location"], lista_rest)
        lista_estadios.append(estadio)

    for i in edd_partidos:
        for x in lista_equipos:
            if x.nombre == i["home_team"]:
                local = x
            elif x.nombre == i["away_team"]:
                visitante = x
        for x in lista_estadios:
            if x.id == i["stadium_id"]:
                estadio = x
        for x,y in dict_partidos.items():
            if x == i["id"]:
                asientos_ocup = y["asientos_ocup"]
                asistencia = y["asistencia"]
        partido = Partido(local, visitante, i["date"], estadio, i["id"], asientos_ocup, asistencia)
        lista_partidos.append(partido)

def partidos_por_pais(lista_partidos):
    pais = input("\nIngrese el país a buscar: ").title()
    lista = []
    for i in lista_partidos:
        if i.local.nombre == pais or i.visitante.nombre == pais:
            lista.append(i)   
    if len(lista) == 0:
        print("\n***No se ha encontrado el país***")
    else:
        print("\n-------------------------\n")
        for i in lista:
            i.mostrar_datos()
            print(" ")
        print("-------------------------\n")
def partidos_por_estadio(lista_partidos, lista_estadios):
    print("\n-----------IDs---------- ")
    for i in lista_estadios:
        print(f"{i.id}) {i.nombre}")
    while True:
        try:
            estadio = int(input("\nIngrese el código del estadio a buscar: "))
            break
        except ValueError:
            print("\n***Entrada inválida***")
            continue
    lista = []
    for i in lista_partidos:
        if i.estadio.id == estadio:
            lista.append(i)   
    if len(lista) == 0:
        print("\n***No se ha encontrado el estadio***")
    else:
        print("\n-------------------------\n")
        for i in lista:
            i.mostrar_datos()
            print(" ")
        print("-------------------------\n")
def partidos_por_fecha(lista_partidos):
    lista = []
    fecha = input("\nIngrese la fecha a buscar (mm/dd/aaaa): ")
    for i in lista_partidos:
        if i.fecha.split(sep=" ")[0] == fecha:
            lista.append(i)
    if len(lista) == 0:
        print("\n***En esta fecha no hay partidos***")
    else:
        print("\n-------------------------\n")
        for i in lista:
            i.mostrar_datos()
            print("")
        print("-------------------------\n")

def mostrar_partidos(lista_partidos, lista_estadios):
    pais = emoji.emojize(":world_map:")
    estadio = emoji.emojize(":stadium:")
    fecha = emoji.emojize(":calendar::")

    opcion = input(f"\nFiltrar partidos por:\n\n1) País {pais}\n2) Estadio {estadio}\n3) Fecha {fecha}\n\n-> ")
    if opcion == "1":
        partidos_por_pais(lista_partidos)
    elif opcion == "2":
        partidos_por_estadio(lista_partidos, lista_estadios)
    elif opcion == "3":
        partidos_por_fecha(lista_partidos)
    else:
        print("\n***Entrada inválida***\n")

def display_estadio(x, y, lista2, lista_letras, asiento_selec, lista_asientos_ocup): 

    #Puro display
    acum = 0
    acum1 = 0
    s = ""
    end1 = " "
    end2 = "|"
    end3 = ""
    if x == 40 or x == 60:
        s = "              "
        end3 = "------------------------------"
    if x == 60:
        end1 = ""
        end2 = ""
        print("\n"+ Back.RED + "***EL TAMAÑO DE ESTE ESTADIO NO CABE EN EL DISPLAY, SE OMITIRÁN LAS LÍNEAS QUE SEPARAN LOS NÚMEROS DE LAS COLUMNAS***" + Style.RESET_ALL)
    
    print("\n", emoji.emojize(":white_large_square:"), "Asientos disponibles  ", emoji.emojize(":red_square:"), "Asientos ocupados  ", emoji.emojize(":green_square:"), "Asiento seleccionado")

    print("")
    for i in range(1,x+1):
        if i < 10:
            print(f"0{i}",end=end2)
        else:
            print(i, end=end2)
    print("\n-----------------------------------------------------------------------------------------",end3)

    for i in lista2:
        acum1 += 1
        if acum1 <= len(lista2)/2:
            for j in i:
                if j in lista_asientos_ocup:
                    print(emoji.emojize(":red_square:"), end=end1)
                    continue
                elif j == asiento_selec:
                    print(emoji.emojize(":green_square:"), end=end1)
                else:
                    print(emoji.emojize(":white_large_square:"), end=end1)
            print("|",lista_letras[acum])
            acum += 1
        else:
            print(s,"------------------------------------------------------------------------------------------")
            print(s,"|                                           |                                            |")
            print(s,"|                                           |                                            |")
            print(s,"|                                           |                                            |")
            print(s,"|                                           |                                            |")
            print(s,"|¯¯¯¯¯¯¯¯¯¯¯¯|                              |                               |¯¯¯¯¯¯¯¯¯¯¯¯|")
            print(s,"|            |                              |                               |            |")
            print(s,"|¯¯¯¯|       |                          /¯¯¯|¯¯¯\                           |       |¯¯¯¯|")
            print(s,"|    |       |                         |    |    |                          |       |    |")
            print(s,"|    |       |                         |    |    |                          |       |    |")
            print(s,"|____|       |                          \___|___/                           |       |____|")
            print(s,"|            |                              |                               |            |")
            print(s,"|____________|                              |                               |____________|")
            print(s,"|                                           |                                            |")
            print(s,"|                                           |                                            |")
            print(s,"|                                           |                                            |")
            print(s,"|                                           |                                            |")
            print(s,"------------------------------------------------------------------------------------------")
            break
    acum1 = 0
    for i in lista2:
        acum1 += 1
        if acum1 > len(lista2)/2:
            for j in i:
                if j in lista_asientos_ocup:
                    print(emoji.emojize(":red_square:"), end=end1)
                    continue
                elif j == asiento_selec:
                    print(emoji.emojize(":green_square:"), end=end1)
                else:
                    print(emoji.emojize(":white_large_square:"), end=end1)
            print("|",lista_letras[acum])
            acum += 1
    print("-----------------------------------------------------------------------------------------",end3)

def get_asiento(partido, lista_partidos):
    parametros = partido.estadio.capacidad
    x = parametros[0]
    y = parametros[1]

    lista2 = []

    lista_letras = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    #Creación de matriz
    acum_l = 0
    for j in range(y):
        acum_n = 1
        lista1 = []
        for i in range(x):
            lista1.append(lista_letras[acum_l] + str(acum_n))
            acum_n += 1
        lista2.append(lista1)
        acum_l +=1

    asiento = None

    for i in lista_partidos:
        if i == partido:
            lista_asientos_ocup = i.asientos_ocup

    display_estadio(x, y, lista2, lista_letras, asiento, lista_asientos_ocup)

    t1 = False
    while True: #Input y validación
        asiento = input("\nIngrese el asiento que desea comprar (ej: B7): " ).title()
        for i in lista2:
            for j in i:
                if j == asiento:
                    t1 = True
                if asiento in lista_asientos_ocup:
                    t1 = False
                    break
        if t1 == False:
            print(f"\n***El asiento {asiento} no se encuentra disponible***")
            continue
        else:
            break

    display_estadio(x, y, lista2, lista_letras, asiento, lista_asientos_ocup)

    while True:
        opcion1 = input("\n¿Este es el asiento que desea? (Si/No): ").title()
        if opcion1 == "Si":
            return asiento
            break
        elif opcion1 == "No":
            get_asiento(partido, lista_partidos)
        else:
            print("\n***Entrada inválida***")

def get_precio_ticket(tipo_entrada, cedula, asiento, partido, id_entrada):
    iva = 0
    if tipo_entrada == "General":
        subtotal = 50
    elif tipo_entrada == "VIP":
        subtotal = 120
    if es_vampiro(cedula) == True:
        descuento = subtotal * 0.5
    else:
        descuento = 0
    iva = (subtotal - descuento) * 0.16

    precio_ticket = subtotal - descuento + iva

    print(f"\n-----FACTURA", Back.WHITE + f" (ID: {id_entrada})",Style.RESET_ALL,"-----")
    print(f"{partido.local.nombre} VS {partido.visitante.nombre}")
    print(f"Fecha: {partido.fecha}")
    print(f"Asiento: {asiento}")
    print("---------------------------")
    print(f"Subtotal: {subtotal} $")
    print(f"Descuento: {descuento} $")
    print(f"IVA: {iva} $")
    print("---------------------------")
    print(f"Total: {precio_ticket} $")

    return precio_ticket

def datos_cliente(lista_clientes, lista_partidos, lista_estadios, lista_clientes_vip, lista_clientes_1):
    while True:
        nombre = input("\nIngrese el nombre del cliente: ").title()
        if not nombre.isalpha():
            print("\n***Entrada inválida***")
            continue
        try:
            cedula = int(input("Ingrese la cédula del cliente: "))
        except ValueError:
            print("\n***Entrada inválida***")
            continue
        try:
            edad = int(input("Ingrese la edad del cliente: "))
        except ValueError:
            print("\n***Entrada inválida***")
            continue   
        break            
    
    while True:
        opcion = input("\n1) Ver partidos disponibles\n2) Ingresar partido a comprar\n\n-> ")
        if opcion == "1":
            mostrar_partidos(lista_partidos, lista_estadios)
        elif opcion == "2":
            while True:
                id = input("\nIngrese el ID del partido que desea comprar: ")
                try:
                    int(id)
                except ValueError:
                    print("\n***Entrada inválida***")
                    continue
                if int(id) > 48 or int(id) < 0:
                    print("\n***Entrada inválida***")
                    continue
                break
            for i in lista_partidos:
                if i.id == id:
                    partido = i
                    break
            break
        else:
            print("\n***Entrada inválida***\n")
    while True:
        opcion = input("\nSeleccione el tipo de entrada que desea comprar:\n\n1) General\n2) VIP\n\n-> ")
        if opcion == "1":
            tipo_entrada = "General"
            break
        elif opcion == "2":
            tipo_entrada = "VIP"
            break
        else:
            print("***Entrada inválida***")

    asiento = get_asiento(partido, lista_partidos)

    lista_id = []
    for i in lista_clientes:
        lista_id.append(i.id_entrada)
    while True:
        id_entrada = random.randint(1,1000)
        if id_entrada in lista_id:
            continue
        else:
            break

    precio_ticket = get_precio_ticket(tipo_entrada, cedula, asiento, partido, id_entrada)

    while True:
        opcion2 = input("\n¿Desea proceder con la compra?:\n\n1) Sí\n2) No\n\n-> ").title()
        if opcion2 == "1" or opcion2 == "Si":
            cliente = Boleto(nombre, cedula, edad, partido, tipo_entrada, asiento, id_entrada, precio_ticket, 0, False)
            q = False
            for i in lista_clientes_1:
                if i.cedula == cedula:
                    i.append_boleto(cliente.asiento)
                    q = True
            if q == False:
                lista = []
                lista.append(cliente.asiento)
                cliente1 = Cliente1(nombre, cedula, lista)
                lista_clientes_1.append(cliente1)
            for i in lista_clientes_1:
                print(f"{i.nombre}: {len(i.boletos)}")
            lista_clientes.append(cliente)
            if cliente.tipo_entrada == "VIP":
                lista_clientes_vip.append(cliente)
            partido.asientos_ocup.append(asiento)
            print("\n***Pago Exitoso***")
            break
        elif opcion2 == "2" or opcion2 == "No":
            break
        else:
            print("\n***Entrada inválida***")
            continue

def asistencia_partidos(lista_clientes, codigos_usados):
    while True:
        try:
            codigo = int(input("\nIngrese el código de su boleto: "))
        except ValueError:
            print("\n***Entrada inválida***")
            continue
        break
    t = False
    for i in lista_clientes:
        if i.id_entrada == codigo:
            t = True
            i.asistencia = True
            if codigo in codigos_usados:
                t = False
                break
            i.partido.asistencia += 1
    if t == True:
        codigos_usados.append(codigo)
        print("\n***Entrada validada***")
    else:
        print("\n", emoji.emojize(":red_exclamation_mark:"),"BOLETO FALSO DETECTADO",emoji.emojize(":red_exclamation_mark:"))

def buscar_productos(lista_estadios):
    while True:
        q = False
        busqueda = input("\nBuscar productos por:\n\n1) Nombre\n2) Tipo\n3) Rango de precio\n\n-> ")
        if busqueda == "1":
            nombre_p = input("\nIngrese el nombre del producto: ").title()
            print("")
            for i in lista_estadios:
                for j in i.restaurantes:
                    for k in j.productos:
                        if k.nombre == nombre_p:
                            q = True
                            print("---------------------------------")
                            print(f"Estadio: {i.nombre}\nRestaurante: {j.nombre}")
                            k.mostrar()
            if q == True:
                print("---------------------------------\n")
            if q == False:
                print("***No se ha encontrado el producto***")
            break
        
        elif busqueda == "2":
            tipo_p = input("\nIngrese el tipo del producto: ").lower()
            print("")
            for i in lista_estadios:
                for j in i.restaurantes:
                    for k in j.productos:
                        if k.tipo == tipo_p:
                            q == True
                            print("---------------------------------")
                            print(f"Estadio: {i.nombre}\nRestaurante: {j.nombre}")
                            k.mostrar()
            if q == True:
                print("---------------------------------\n")
            if q == False:
                print("***No se ha encontrado el producto***")
            break

        elif busqueda == "3":
            while True:
                try:
                    rango = float(input("\nIngrese el precio máximo: "))
                    rango2 = float(input("\nIngrese el pracio mínimo: "))
                except ValueError:
                    print("\n***Entrada inválida***")
                    continue
                break
            print("")
            q = False
            for i in lista_estadios:
                for j in i.restaurantes:
                    for k in j.productos:
                        if k.precio_neto <= rango and k.precio_neto >= rango2:
                            q = True
                            print("---------------------------------")
                            print(f"Estadio: {i.nombre}\nRestaurante: {j.nombre}")
                            k.mostrar()
            if q == True:
                print("---------------------------------\n")
            if q == False:
                print("\n***No hay ningún producto comprendido en este rango de precio***")
            break

        else:
            print("\n***Entrada inválida***")

def dividir_lista_en_dos(lista):
    return [lista[i:i + int(len(lista)/2)] for i in range(0, len(lista), int(len(lista)/2))]
def lista_a_int(lista):
    acum = ""
    for i in lista:
        acum += i
    return int(acum)
def es_vampiro(numero):
    lista = list(permutations(str(numero)))
    if len(str(numero)) % 2 != 0:
        return False
    for i in lista:
        lista1 = dividir_lista_en_dos(i)
        if lista_a_int(lista1[0]) * lista_a_int(lista1[1]) == numero:
            return True
    return False
def es_primo(numero):
    primo = True
    for i in range(2, numero):
        if numero % i == 0:
            primo = False
            break
        else:
            primo = True
    return primo
def es_perfecto(numero):
    lista = []
    for i in range(1,numero):
        if numero % i == 0:
            lista.append(i)
    if sum(lista) == numero:
        return True
    else:
        return False

def venta_en_restaurante(lista_clientes_vip):
    while True:
        try:
            cedula = int(input("\nIngrese su cédula: "))
        except ValueError:
            print("\n***Entrada inválida***")
            continue
        break
    t = False
    a = True
    for i in lista_clientes_vip:
        print(i.cedula)
        print(i.tipo_entrada)
        if i.cedula == cedula:
            cliente = i
            t = True
            if i.edad < 18:
                a = False
    if t == True:
        acum = 1
        lista_p = {}
        print("\n---------MENÚ---------")
        for j in i.partido.estadio.restaurantes:
            print(f"({j.nombre})")
            print("----------------------")
            for k in j.productos:
                print(f"{acum})", end=" ")
                k.mostrar2()
                lista_p[acum] = k
                acum += 1
                print("----------------------")

        canasta = []
        while True:
            t = False
            b = False
            opcion = input("\nSeleccione un producto del menú: ").title()
            for x,y in lista_p.items():
                if str(x) == opcion or y.nombre == opcion:
                    if y.nombre == "Beer":
                        if a == False:
                            print("\n***Menor de edad no puede consumir bebidas alcoholicas***")
                            b = True
                            break
                    if y.inventario > 0:
                        canasta.append(y)
                        p = y.nombre
                        t = True
                    else:
                        print(f"\n***Se han acabado las reservas de {y.nombre}")
            if t == True:
                print(f"\n***Producto {p} agregado***")
                opcion1 = input("\n¿Desea otro producto? (Si/No): ").title()
                if opcion1 == "Si":
                    continue
                elif opcion1 == "No":
                    break
            elif t == False and b == False:
                print(f"\n***El producto ({opcion}) no se encuentra disponible***")

        subtotal = 0
        for i in canasta:
            subtotal += i.precio
        descuento = 0
        if es_perfecto(cedula):
            descuento = subtotal * 0.15
        iva = (subtotal - descuento) * 0.16
        total = subtotal-descuento+iva
        print("\n--------FACTURA--------")
        for i in canasta:
            print(f"{i.nombre}  {i.precio} $")
        print("-----------------------")
        print(f"Subtotal: {subtotal} $")
        print(f"Descuento: {descuento} $")
        print(f"IVA: {iva}")
        print("-----------------------")
        print(f"Total: {total}")

        while True:
            opcion3 = input("\n¿Desea proceder con la compra? (Si/No): ").title()
            if opcion3 == "Si":
                cliente.act_gasto_rest(total)
                print("\n***Pago exitoso***")
                for i in canasta:
                    i.cambiar_inv()
                break
            elif opcion3 == "No":
                print("\n***Compra cancelada***")
                break
            else:
                print("\n***Entrada Inválida***")
                continue

    else:
        print("\n***La cédula no está asociada a una entrada VIP***")

def orden_por_asistencia(e):
    return e.asistencia
def orden_por_inventario_producto(e):
    return e.inventario
def orden_por_len(e):
    return len(e.boletos)

def ordenar_dict_por_key(dict):
    claves = dict.keys()
    claves_ord = sorted(claves)
    dict_ord = {}
    for i in claves_ord:
        dict_ord[i] = dict[i]
    return dict_ord

def get_estadisticas(lista_partidos, lista_clientes_vip, lista_estadios, lista_clientes_1): #PENDIENTE GRÁFICOS
    
    opcion = input("\nSeleccione una opción:\n\n1) Gasto promedio de cliente VIP\n2) Asistencia a partidos\n3) Partido con mayor asistencia\n4) Partido con más boletos vendidos\n5) Productos más vendidos en cada restaurante\n6) Clientes que más compraron boletos\n\n-> ")
    if opcion == "1":
        count = 0
        acum = 0
        for i in lista_clientes_vip:
            acum += i.precio_ticket + i.gasto_rest
            count +=1
        print(f"\nGasto promedio de cliente VIP: {round(acum/count,2)} $")

    elif opcion == "2":
        lista_ord = lista_partidos
        lista_ord.sort(reverse=True,key=orden_por_asistencia) 
        print("\n--------------------\n")
        for i in lista_ord:
            i.mostrar_datos_2()
            print("")
        print("\n--------------------")

    elif opcion == "3": 
        mayor = 0
        for i in lista_partidos:
            if i.asistencia > mayor:
                mayor = i.asistencia
                partido = i
        print("\n--------------------\n")
        if mayor != 0:
            partido.mostrar_datos_2()
        else:
            print("***No se ha registrado ninguna asistencia***")
        print("\n--------------------")

    elif opcion == "4":
        mayor = 0
        for i in lista_partidos:
            if len(i.asientos_ocup) > mayor:
                mayor = len(i.asientos_ocup)
                partido = i
        print("\n--------------------\n")
        if mayor != 0:
            partido.mostrar_datos_2()
        else:
            print("***No se ha registrado ninguna entrada***")
        print("\n--------------------")

    elif opcion == "5":
        acum = 1
        dict_rest = {}
        print("\n--------------------\n")
        for i in lista_estadios:
            for j in i.restaurantes:
                print(f"{acum}) {j.nombre}")
                dict_rest[acum] = j
                acum += 1
        print("\n--------------------")
        opcion2 = int(input("Seleccione el restaurante: "))
        for x,y in dict_rest.items():
            if opcion2 == x:
                lista_ord_prod = y.productos
                lista_ord_prod.sort(key=orden_por_inventario_producto)
                acum = 1
                for i in lista_ord_prod:
                    print(f"\nProductos más vendidos:\n\n{acum}) {i.nombre}: {100 - i.inventario} vendidos")
                    acum += 1
                    if lista_ord_prod.index(i) == 2:
                        break
                    
    elif opcion == "6":
        mayor = 0
        lista_ord = lista_clientes_1
        lista_ord.sort(reverse=True,key=orden_por_len)
        acum = 1
        print("\nClientes que más compraron boletos:\n")
        for i in lista_ord:
            print(f"\n{acum}) {i.nombre} (CI: {i.cedula}): {len(i.boletos)} boletos")
            acum += 1
            if lista_ord.index(i) == 2:
                break

    else: 
        print("***Entrada Inválida***")

def guardar_datos_json(lista_partidos, lista_clientes, codigos_usados, lista_clientes_vip, lista_clientes_1, dict_partidos, dict_clientes):
    
    #Lista de partidos
    archivo = "zproyecto/partidos.json"

    for i in lista_partidos:
        sub_dict = {}
        sub_dict.update({"asientos_ocup":i.asientos_ocup})
        sub_dict.update({"asistencia":i.asistencia})
        dict_partidos.update({i.id:sub_dict})

    d = json.dumps(dict_partidos, indent=4)
    with open(archivo, "w") as f:
        f.write(d)
        f.close()
    
    #Lista de clientes
    archivo = "zproyecto/boletos.json"

    dict_clientes = {} #REVISAR SI DA ERRORES
    for i in lista_clientes:
        sub_dict = {}
        sub_dict.update({"nombre":i.nombre})
        sub_dict.update({"edad":i.edad})
        sub_dict.update({"partido":i.partido.id})
        sub_dict.update({"tipo_entrada":i.tipo_entrada})
        sub_dict.update({"asiento":i.asiento})
        sub_dict.update({"id_entrada":i.id_entrada})
        sub_dict.update({"precio_ticket":i.precio_ticket})
        sub_dict.update({"gasto_rest":i.gasto_rest})
        sub_dict.update({"asistencia":i.asistencia})
        dict_clientes.update({i.cedula:sub_dict})

    d = json.dumps(dict_clientes,indent=4)
    with open(archivo, "w") as f:
        f.write(d)
        f.close()

    #Códigos usados
    archivo = "zproyecto/codigos_usados.json"

    lista = []
    for i in codigos_usados:
        lista.append(i)

    d = json.dumps(lista, indent=4)
    with open(archivo, "w") as f:
        f.write(d)
        f.close()

    #Lista Clientes1
    archivo = "zproyecto/clientes_1.json"

    dict_clientes_1 = {}
    for i in lista_clientes_1:
        sub_dict = {}
        sub_dict.update({"nombre":i.nombre})
        sub_dict.update({"boletos":i.boletos})
        dict_clientes_1.update({i.cedula:sub_dict})

    d = json.dumps(dict_clientes_1, indent=4)
    with open(archivo, "w") as f:
        f.write(d)
        f.close()

    #Lista inventario


def main():

    lista_equipos = []
    lista_estadios = []
    lista_partidos = [] #edd - LISTO

    lista_clientes = [] #edd - LISTO (REVISAR)
    
    codigos_usados = [] #edd - LISTO

    lista_clientes_vip = [] #edd - LISTO

    lista_clientes_1 = [] #edd

    dict_partidos = {}
    dict_partidos = importar_json_partidos(dict_partidos)

    crear_edd(lista_equipos, lista_estadios, lista_partidos, dict_partidos)

    dict_clientes = {} #Esta siendo agarrado como None - REVISAR
    dict_clientes = importar_json_clientes(lista_clientes, lista_partidos, dict_clientes, lista_clientes_vip, codigos_usados, lista_clientes_1)

    pelota = emoji.emojize(":soccer_ball:")
    ticket = emoji.emojize(":admission_tickets:")
    assist = emoji.emojize(":pen:")
    rest = emoji.emojize(":hamburger:")
    venta = emoji.emojize(":shopping_cart:")
    estadistica = emoji.emojize(":bookmark_tabs:")

    while True:
        menu = input(f"\nSeleccione un módulo:\n\n1) Gestión de partidos y estadios {pelota} \n2) Gestión de venta de entradas {ticket}\n3) Gestion de asistencia a partidos {assist}\n4) Gestión de restaurantes {rest}\n5) Gestión de venta de restaurantes {venta}\n6) Indicadores de gestión {estadistica}\n\n-> ")
        if menu == "1":
            mostrar_partidos(lista_partidos, lista_estadios)
        
        elif menu == "2":
            datos_cliente(lista_clientes, lista_partidos, lista_estadios, lista_clientes_vip, lista_clientes_1)

        elif menu == "3":
            asistencia_partidos(lista_clientes, codigos_usados)
        
        elif menu == "4":
            buscar_productos(lista_estadios)

        elif menu == "5":
            venta_en_restaurante(lista_clientes_vip)

        elif menu == "6":
            get_estadisticas(lista_partidos, lista_clientes_vip, lista_estadios, lista_clientes_1)

        elif menu == "7":
            guardar_datos_json(lista_partidos, lista_clientes, codigos_usados, lista_clientes_vip, lista_clientes_1, dict_partidos, dict_clientes)
            print("\n***Datos guardados***")

            #JSON lista_clientes_1 se hace con un len(boletos)

        #elif menu == "8":
            #dict_partidos = importar_json_partidos(dict_partidos)

        else:
            print("\n***Entrada inválida***")
            for i in lista_partidos:
                i.mostrar_datos_2()






main()