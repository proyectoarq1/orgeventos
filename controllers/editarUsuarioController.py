from flask import render_template, make_response, request, redirect, url_for, current_app
from formularios.usuario_form import UserForm
from flask_restful import Resource
from db.adapter_selected import adapter
from flask.ext.login import current_user, login_required



class EditarUsuarioController(Resource):
    @login_required
    def get(self):

        form = UserForm(obj=current_user)

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("register.html", editar=True, form=form),200,headers)


    def post(self):
    	
        form = UserForm(request.form)
        
        if form.password.data=="" and form.confirm.data=="":
            current_app.logger.info('No se cambio la contrasenia, sigue la misma que la anterior')
            form.password.data = current_user.password
            form.confirm.data = current_user.password
        else:
            current_app.logger.info('Las contrasenias ingresadas para cambiarla no concuerdan.')

    	if form.validate():
            usuario = adapter.guardar_edicion_a_usuario(current_user.get_id(),form)
            current_app.logger.info('Se guardo con exito la edicion del usuario ' + usuario["nombre"])
            return redirect(url_for('perfil'))
    	else :
            current_app.logger.info('No se pudo guardar la edicion del usuario ya que el form no esta validado')
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template("register.html", editar=True, form=form),200,headers)