import requests

from equipos import Equipo
from estadios import Estadio
from restaurantes import Restaurante
from partidos import Partido
from clientes import Cliente
from productos import Producto, Bebida, Comida

import emoji
from colorama import Fore, Back, Style
import random

def crear_edd(lista_equipos, lista_estadios, lista_partidos):
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
    
    for i in edd_estadios: #PENDIENTE PONER PRODUCTOS COMO OBJETOS PARA MODULO 4
        lista_rest = []
        for j in i["restaurants"]:
            lista_prod = []
            for k in j["products"]:
                if k["type"] == "beverages":
                    if k["name"] == "beer":
                        producto = Bebida(k["name"], k["price"], k["type"], 100, True)
                    else:
                        producto = Bebida(k["name"], k["price"], k["type"], 100, False)
                    lista_prod.append(producto)
                if k["type"] == "food":
                    producto = Comida(k["name"], k["price"], k["type"], 100)
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
        partido = Partido(local, visitante, i["date"], estadio, i["id"])
        lista_partidos.append(partido)

    print(lista_partidos[2].estadio.restaurantes[0].productos[3].precio_neto)

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
        print(f"{i.nombre}:  {i.id}")
    estadio = int(input("\nIngrese el código del estadio a buscar: "))
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
        print("***En esta fecha no hay partidos***")
    else:
        print("\n-------------------------\n")
        for i in lista:
            i.mostrar_datos()
            print("")
        print("-------------------------\n")

def mostrar_partidos(lista_partidos, lista_estadios):
    opcion = input("\nFiltrar partidos por:\n\n1) País\n2) Estadio\n3) Fecha\n\n-> ")
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
        asiento = input("\nIngrese el asiento que desea comprar (ej: B7): " )
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
        opcion1 = input("¿Este es el asiento que desea? (Si/No): ").title()
        if opcion1 == "Si":
            return asiento
            break
        elif opcion1 == "No":
            get_asiento(partido)
        else:
            print("***Entrada inválida***")

def es_vampiro(cedula):
    return False

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
    print(f"Subtotal: {subtotal}")
    print(f"Descuento: {descuento}")
    print(f"IVA: {iva}")
    print("---------------------------")
    print(f"Total: {precio_ticket}")

    return precio_ticket

def datos_cliente(lista_clientes, lista_partidos, lista_estadios, lista_clientes_vip):
    nombre = input("\nIngrese el nombre completo del cliente: ").title()
    cedula = int(input("Ingrese la cédula del cliente: "))
    edad = int(input("Ingrese la edad del cliente: "))
    while True:
        opcion = input("\n1) Ver partidos disponibles\n2) Ingresar partido a comprar\n\n-> ")
        if opcion == "1":
            mostrar_partidos(lista_partidos, lista_estadios)
        elif opcion == "2":
            id = input("\nIngrese el ID del partido que desea comprar: ")
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
            cliente = Cliente(nombre, cedula, edad, partido, tipo_entrada, asiento, id_entrada, precio_ticket, 0)
            lista_clientes.append(cliente)
            if cliente.tipo_entrada == "VIP":
                lista_clientes_vip.append(cliente)
            partido.asientos_ocup.append(asiento)
            print("\n***Pago Exitoso***")
            break
        elif opcion2 == "2" or opcion2 == "No":
            break
        else:
            print("***Entrada inválida***")
            continue

def asistencia_partidos(lista_clientes, codigos_usados):
    codigo = int(input("\nIngrese el código de su boleto: "))
    t = False
    for i in lista_clientes:
        if i.id_entrada == codigo:
            t = True
            i.asistencia = True
        if codigo in codigos_usados:
            t = False
    if t == True:
        codigos_usados.append(codigo)
        print("\n***Entrada validada***")
    else:
        print("\n", emoji.emojize(":red_exclamation_mark:"),"BOLETO FALSO DETECTADO",emoji.emojize(":red_exclamation_mark:"))

def buscar_productos(lista_estadios):
    while True:
        busqueda = input("\nBuscar productos por:\n\n1) Nombre\n2) Tipo\n3) Rango de precio\n\n-> ")
        if busqueda == "1":
            nombre_p = input("\nIngrese el nombre del producto: ").title()
            print("")
            for i in lista_estadios:
                for j in i.restaurantes:
                    for k in j.productos:
                        if k.nombre == nombre_p:
                            print("---------------------------------")
                            print(f"Estadio: {i.nombre}\nRestaurante: {j.nombre}")
                            k.mostrar()
            print("---------------------------------\n")
            break
        
        elif busqueda == "2":
            tipo_p = input("\nIngrese el tipo del producto: ").lower()
            print("")
            for i in lista_estadios:
                for j in i.restaurantes:
                    for k in j.productos:
                        if k.tipo == tipo_p:
                            print("---------------------------------")
                            print(f"Estadio: {i.nombre}\nRestaurante: {j.nombre}")
                            k.mostrar()
            print("---------------------------------\n")
            break

        elif busqueda == "3":
            rango = float(input("\nIngrese el precio máximo: "))
            print("")
            for i in lista_estadios:
                for j in i.restaurantes:
                    for k in j.productos:
                        if k.precio_neto <= rango:
                            print("---------------------------------")
                            print(f"Estadio: {i.nombre}\nRestaurante: {j.nombre}")
                            k.mostrar()
            print("---------------------------------\n")
            break

def es_primo(numero):
    primo = True
    for i in range(2, numero):
        if numero % i == 0:
            primo = False
            break
        else:
            primo = True
    return primo

def venta_en_restaurante(lista_clientes_vip):
    cedula = int(input("Ingrese su cédula: "))
    t = False
    for i in lista_clientes_vip:
        if i.cedula == cedula:
            cliente = i
            t = True
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
            opcion = input("\nSeleccione un producto del menú: ").title()
            for x,y in lista_p.items():
                if str(x) == opcion or y.nombre == opcion:
                    if y.inventario > 0:
                        y.cambiar_inv()
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
            elif t == False:
                print(f"\n***El producto {opcion} no se encuentra disponible***")

        subtotal = 0
        for i in canasta:
            subtotal += i.precio
        descuento = 0
        if es_primo(cedula):
            descuento = subtotal * 0.15
        iva = (subtotal - descuento) * 0.16
        print("--------FACTURA--------")
        for i in canasta:
            print(f"{i.nombre}  {i.precio} $")
        print("-----------------------")
        print(f"Subtotal: {subtotal} $")
        print(f"Descuento: {descuento} $")
        print(f"IVA: {iva}")
        print("-----------------------")
        print(f"Total: {subtotal-descuento+iva}")

    else:
        print("\n***La cédula no está asociada a una entrada VIP***")

def main():

    lista_equipos = []
    lista_estadios = []
    lista_partidos = []

    lista_clientes = []
    
    codigos_usados = []

    lista_clientes_vip = []

    crear_edd(lista_equipos, lista_estadios, lista_partidos)

    while True:
        menu = input("\nSeleccione un módulo:\n\n1) Gestión de partidos y estadios\n2) Gestión de venta de entradas\n3) Gestion de asistencia a partidos\n4) Gestión de restaurantes\n5) Gestión de venta de restaurantes\n6) Indicadores de gestión\n\n-> ")
        if menu == "1":
            mostrar_partidos(lista_partidos, lista_estadios)
        
        elif menu == "2":
            datos_cliente(lista_clientes, lista_partidos, lista_estadios, lista_clientes_vip)

        elif menu == "3":
            asistencia_partidos(lista_clientes, codigos_usados)
        
        elif menu == "4":
            buscar_productos(lista_estadios)

        elif menu == "5":
            venta_en_restaurante(lista_clientes_vip)






main()

#print(lista_partidos[0].estadio.restaurantes[0].productos)