from django.shortcuts import render, redirect
import json

# Create your views here.

# Funcion para Listar el contenido de la vista
def home(request, element=None):
    cadena_json = json.load(open('bancarios/BD.json',encoding="utf8"))
    contexto = {'productos': cadena_json, "cantidadTitulos":len(cadena_json), "response":element}
    template_name = "bancarios/base.html"
    return render(request, template_name, contexto)

def listar(action=None, status=None, idTitulo=None):
    if idTitulo != None:
        cadena_json          = json.load(open('bancarios/BD.json',encoding="utf8"))
        output_dict          = [x for x in cadena_json if x['idTitulo'] == idTitulo.upper()]
        if len(output_dict) > 0:
            return 200
        else:
            return 404
    else:
        cadena_json = json.load(open('bancarios/BD.json',encoding="utf8"))
        template_name = "bancarios/base.html"
        contexto = {"productos": cadena_json, 
                    "cantidadTitulos":len(cadena_json), 
                    "action":action, 
                    "status":status}
        return [contexto, template_name]

#Funcion que resive los parametros para realizar un nuevo registro
def create(request):
    if request.method == 'POST':
        cadena_json = json.load(open('bancarios/BD.json',encoding="utf8"))
        response = listar("crear_user", '',idTitulo=request.POST["id_titulo"])
        if(response == 404):
            data = {
                    "idTitulo": request.POST["id_titulo"],
                    "titulo":request.POST["titulo"],
                    "clasificacion":request.POST["clasificacion"],
                    "valor":request.POST["valor"],
                    "fecha_creacion":request.POST["fecha_creacion"],
                    "fecha_vencimiento":request.POST["fecha_vencimiento"],
                    "pagocuota":"n"
                    }
            output_dict_diferent = [x for x in cadena_json if x['idTitulo'] != request.POST["id_titulo"]]
            output_dict_diferent.append(data)
            f = open("bancarios/BD.json", "w")
            f.write(json.dumps(output_dict_diferent))
            f.close()
            contexto, template_name = listar("crear_user",404)
            return render(request, template_name, contexto)
        else:
            contexto, template_name = listar("crear_user", 200)
            return render(request, template_name, contexto)
    else:
        contexto, template_name = listar("crear_user")
        return render(request, template_name, contexto)

#Funcion para realizar el pago de la cuota (y/n)
def cuotaPagar(request):
    if request.method == 'POST':
        response_data = buscarRegistro(request.POST["id_titulo"].upper())
        contexto, template_name = listar("pago_cuota", response_data)
        return render(request, template_name, contexto)
    else:
        contexto, template_name = listar("pago_cuota")
        return render(request, template_name, contexto)

#Buscar registro por iTitulo 
def buscarRegistro(id_titulo=None):
    cadena_json          = json.load(open('bancarios/BD.json',encoding="utf8"))
    output_dict_diferent = [x for x in cadena_json if x['idTitulo'] != id_titulo.upper()]
    output_dict          = [x for x in cadena_json if x['idTitulo'] == id_titulo.upper()]
    if len(output_dict) > 0:
        output_dict[0]["pagocuota"] = "y"
        output_dict_diferent.append(output_dict[0])
        f = open("bancarios/BD.json", "w")
        f.write(json.dumps(output_dict_diferent))
        f.close()
        return 200
    else:
        return 404

#Eliminar Registro
def cuotaEliminar(request):
    if request.method == 'POST':
        id_titulo            = request.POST["id_titulo"]
        cadena_json_eliminar = json.load(open('bancarios/BD.json',encoding="utf8"))
        output_dict          = [x for x in cadena_json_eliminar if x['idTitulo'] == id_titulo.upper()]
        if len(output_dict) > 0:
            output_dict_diferent = [x for x in cadena_json_eliminar if x['idTitulo'] != id_titulo.upper()]
            f = open("bancarios/BD.json", "w")
            f.write(json.dumps(output_dict_diferent))
            f.close()
            contexto, template_name = listar("Eliminar", 200)
            return render(request, template_name, contexto)
        else:
            contexto, template_name = listar("Eliminar", 404)
            return render(request, template_name, contexto)
    else:
        contexto, template_name = listar("Eliminar")
        return render(request, template_name, contexto)

#ACTUALIZAR FECHA
def actualizarFecha(request):
    if request.method == 'POST':
        fecha_creacion       = request.POST["fecha_creacion"]
        nueva_fecha          = request.POST["nueva_fecha"]
        cadena_json          = json.load(open('bancarios/BD.json',encoding="utf8"))
        output_dict_diferent = [x for x in cadena_json if x['fecha_creacion'] != fecha_creacion]
        output_dict          = [x for x in cadena_json if x['fecha_creacion'] == fecha_creacion]
        
        if len(output_dict) > 0:
            for data_fecha in output_dict:
                data_fecha["fecha_creacion"] = nueva_fecha
                output_dict_diferent.append(data_fecha)
            f = open("bancarios/BD.json", "w")
            f.write(json.dumps(output_dict_diferent))
            f.close()
            contexto, template_name = listar("fechas_actualizar", 200)
            return render(request, template_name, contexto)
        else:
            contexto, template_name = listar("fechas_actualizar", 404)
            return render(request, template_name, contexto)
    else:
        contexto, template_name = listar("fechas_actualizar")
        return render(request, template_name, contexto)