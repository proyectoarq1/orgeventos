
from flask import Flask, render_template, make_response,current_app, url_for, abort, flash
from flask_restful import Resource
from db.adapter_selected import adapter
from flask import session, request, redirect, json
from flask.ext.login import current_user, login_required
from formularios.requerimientoForm import RequerimientoForm


class AsignarRecursoController(Resource):

    def post(self):
        recurso_id = request.form["id_recurso"]
        cantidad = request.form["cantidad_llevar"]
        usuario_id = current_user.id

        asignado = adapter.obtener_asignacion_usuario(recurso_id, usuario_id)
        if asignado:
            print "ey estoy asignado puto"
            asignado = adapter.editar_asignacion_requerimiento(asignado, cantidad)
        else:
            print "no estaba asignado viejita"
            asignado = adapter.asignar_requerimiento(recurso_id,usuario_id,cantidad)

        requerimiento = adapter.obtener_requerimiento(recurso_id)
        asignaciones = adapter.obtener_asignaciones_requerimiento(recurso_id)
        faltan_reservar = requerimiento["cantidad"]
        asignacion_propia = asignado
        for a in asignaciones:
            faltan_reservar = faltan_reservar - a["cantidad"]

        print asignacion_propia["cantidad"]
        
        requerimiento_con_datos={"requerimiento":requerimiento,"faltan_reservar":(faltan_reservar+asignacion_propia["cantidad"]),"asignacion_propia":asignacion_propia}


        return requerimiento_con_datos