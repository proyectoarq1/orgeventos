
function asiganarse_requerimiento(id_form) {
    //console.log(id_form)
    //console.log($('form[id="form_asignarse'+id_form+'"]').serialize())

    $.ajax({
        url : "/asignar_recurso",
        type : "POST",
        data : $('form[id="form_asignarse'+id_form+'"]').serialize(),  

        success : function(json) {

            $('#'+json.requerimiento.id).modal('toggle');
            $('#contenedor'+id_form).attr('onclick', 'habilitar_edicion('+json.requerimiento.id+',"'+json.requerimiento.nombre+'","'+json.requerimiento.descripccion+'",'+json.requerimiento.cantidad+','+json.faltan_reservar+','+json.asignacion_propia.cantidad+')');

        },

        error : function(xhr,errmsg,err) {

            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); 
            console.log(xhr.status + ": " + xhr.responseText); 
        }
    });
};



function borrar_recurso(id) {
    console.log("delete post is working!")
    
    $.ajax({
        url : "/crear_recurso",
        type : "DELETE",
        data : {id_recurso:id}, 

        success : function(json) {

            console.log(json);
            $('#'+json).modal('toggle');
            $('#contenedor'+json).remove();

        },

        error : function(xhr,errmsg,err) {

            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); 
            console.log(xhr.status + ": " + xhr.responseText); 
        }
    });
};


function editar_recurso(id_form) {
    
    $.ajax({
        url : "/crear_recurso",
        type : "PUT",
        data : $('form[id="'+id_form+'"]').serialize(), 

        success : function(json) {

            console.log(json);
            $('#'+id_form).modal('toggle');

            $('#contenedor_nombre'+id_form).replaceWith( '<b id="contenedor_nombre'+id_form+'">'+json.nombre+'</b>' );
            $('#contenedor'+id_form).attr('onclick', 'habilitar_edicion('+json.id+',"'+json.nombre+'","'+json.descripccion+'",'+json.cantidad+')');

        },


        error : function(xhr,errmsg,err) {

            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); 
            console.log(xhr.status + ": " + xhr.responseText); 
        }
    });
};


$(function() {

$('#modalRequerimiento').on('submit', function(event){
    event.preventDefault();
    creando_requerimiento();
});

function creando_requerimiento() {
    $.ajax({
        url : "/crear_recurso",
        type : "POST", 
        data: $('form[id="modalRequerimiento"]').serialize(),

        success : function(json) {

            console.log(json);
            requerimiento = json.requerimiento
            console.log(requerimiento)


        a='<div>'
        a=a+'<div class="col-md-8" style="margin-top:1em;" id="contenedor_columna'+requerimiento.id+'">'
        a=a+'<a id="contenedor'+requerimiento.id+'" href="" data-toggle="modal" data-target=#'+requerimiento.id+' class="modal_req" onclick="habilitar_edicion('+requerimiento.id+',&#39;'+requerimiento.nombre+'&#39;,&#39;'+requerimiento.descripccion+'&#39;,'+requerimiento.cantidad+','+requerimiento.cantidad+')">'
        a=a+'<b>'+requerimiento.nombre+'</b></a>'
        a=a+'<div class="modal fade" id='+requerimiento.id+' role="dialog">'
        a=a+'<div class="modal-dialog">'
        a=a+'<div class="modal-content">'
        a=a+'<div class="modal-header">'
        a=a+'<button type="button" class="close" data-dismiss="modal">&times;</button>'
        a=a+'<h4 class="modal-title">Detalle del requerimiento</h4>'
        a=a+'</div>'
        a=a+'<div class="modal-body">'
        a=a+'<form id='+requerimiento.id+' style="margin-left:50px;" method="post">'
        a=a+'<input type="hidden" name="recurso_id" value='+requerimiento.id+' />'       
        a=a+'<input type="hidden" name="evento_id" value="1" />'
        a=a+'<label>Nombre del requerimiento</label>'
        a=a+'<input disabled="true" class="form-control" name="nombre" id="nombre" required="true" value="'+requerimiento.nombre+'"" />'
        a=a+'<label>Descripcion del requerimiento</label>'
        a=a+'<input disabled="true" class="form-control" name="descripccion" id="descripccion" required="true" value="'+requerimiento.descripccion+'"" />'
        a=a+'<label>Cantidad del requerimiento</label>'
        a=a+'<input disabled="true" type="number"  min="1" max="99" class="form-control" name="cantidad" id="cantidad" required="true" value='+requerimiento.cantidad+'>'
        a=a+'</form>'
        a=a+'<div class="modal-footer" >'
        a=a+'<button style="margin-left:50px;" class="btn btn-success" onclick="editar_recurso('+requerimiento.id+')">Guardar Cambios</button>'
        a=a+'<button type="button" class="btn btn-danger" onclick="borrar_recurso('+requerimiento.id+')">'
        a=a+'<span class="glyphicon glyphicon-trash" aria-hidden="true"></span>'
        a=a+'</button>'
        a=a+'<button type="button" class="btn btn-default" data-dismiss="modal">Cancelar</button>'
        a=a+'</div>'
        a=a+'</div>'
        a=a+'</div>'
        a=a+'</div>'
        a=a+'</div>'
        a=a+'</div>'
        a=a+'</div>'


        console.log(a)


            
            $('#modalRequerimiento').modal('toggle');
            $( "#requerimientos_lista" ).append( a );
        },
 
        error : function(xhr,errmsg,err) {

            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); 
            console.log(xhr.status + ": " + xhr.responseText); 
        }
    });
};

});




function habilitar_edicion(id_form, nombre,descripccion,cantidad,faltan_reservar,asignacion_propia) {

     var puede_editar = $('#puede_editar_evento').val();
     $('[name=nombre]').val(nombre);
     $('[name=descripccion]').val(descripccion);
     $('[name=cantidad]').val(cantidad);
     $('[name=cantidad_llevar]').attr("max",faltan_reservar);
     console.log(asignacion_propia)
     if (asignacion_propia) {
        $('[name=cantidad_llevar]').val(asignacion_propia); }
     else {
        $('[name=cantidad_llevar]').val(1); }



    if(puede_editar==="true") {
        //console.log("puede_editar")
        $("#"+id_form+" :input").attr("disabled",false);
    }

}

