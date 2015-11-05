from flask import render_template, make_response, request, redirect, url_for
from formularios.usuario_form import UserForm
from flask_restful import Resource
from db.adapter_selected import adapter
from flask.ext.login import current_user



class EditarUsuarioController(Resource):
    def get(self):

        form = UserForm(obj=current_user)

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("register.html", editar=True, form=form),200,headers)


    def post(self):
    	
        form = UserForm(request.form)
        
        if form.password.data=="" and form.confirm.data=="":
            form.password.data = current_user.password
            form.confirm.data = current_user.password

    	if form.validate():
    		usuario = adapter.guardar_edicion_a_usuario(current_user.get_id(),form)
    		return redirect(url_for('perfil'))
    	else :
    		headers = {'Content-Type': 'text/html'}
	    	return make_response(render_template("register.html", editar=True, form=form),200,headers)