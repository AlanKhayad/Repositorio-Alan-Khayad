import json
from equipos import Equipo

#equipo = Equipo("a", "b", "c", "d", "e")
equipo = "hola"

print(equipo)

nombre_arc = "zproyecto/prueba.json"

with open(nombre_arc, "r") as f:
    my_data = f.read()

    print(my_data)

    my = json.loads(
      my_data
    ) 

    my.append(equipo)

    print(my)

    c = json.dumps(my)

with open(nombre_arc, "w") as f:
    f.write(c)
    f.close()