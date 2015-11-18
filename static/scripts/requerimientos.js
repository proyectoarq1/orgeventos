

function borrar_recurso(id) {
    console.log("delete post is working!") // sanity check
    
    $.ajax({
        url : "/crear_recurso",
        type : "DELETE",
        data : {id_recurso:id}, 

        success : function(json) {

            console.log(json);
            $('#'+json).modal('toggle');
            $('#contenedor'+json).remove();

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {

            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
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

        // handle a non-successful response
        error : function(xhr,errmsg,err) {

            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
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


        a='<div>'
        a=a+'<div class="col-md-8" style="margin-top:1em;" id="contenedor_columna'+json.id+'">'
        a=a+'<a id="contenedor'+json.id+'" href="" data-toggle="modal" data-target=#'+json.id+' class="modal_req" onclick="habilitar_edicion('+json.id+',&#39;'+json.nombre+'&#39;,&#39;'+json.descripccion+'&#39;,'+json.cantidad+')">'
        a=a+'<b>'+json.nombre+'</b></a>'
        a=a+'<div class="modal fade" id='+json.id+' role="dialog">'
        a=a+'<div class="modal-dialog">'
        a=a+'<div class="modal-content">'
        a=a+'<div class="modal-header">'
        a=a+'<button type="button" class="close" data-dismiss="modal">&times;</button>'
        a=a+'<h4 class="modal-title">Crear un requerimiento</h4>'
        a=a+'</div>'
        a=a+'<div class="modal-body">'
        a=a+'<form id='+json.id+' style="margin-left:50px;" method="post">'
        a=a+'<input type="hidden" name="recurso_id" value='+json.id+' />'       
        a=a+'<input type="hidden" name="evento_id" value="1" />'
        a=a+'<label>Nombre del requerimiento</label>'
        a=a+'<input disabled="true" class="form-control" name="nombre" id="nombre" required="true" value="'+json.nombre+'"" />'
        a=a+'<label>Descripcion del requerimiento</label>'
        a=a+'<input disabled="true" class="form-control" name="descripccion" id="descripccion" required="true" value="'+json.descripccion+'"" />'
        a=a+'<label>Cantidad del requerimiento</label>'
        a=a+'<input disabled="true" type="number"  min="1" max="99" class="form-control" name="cantidad" id="cantidad" required="true" value='+json.cantidad+'>'
        a=a+'</form>'
        a=a+'<button style="margin-left:50px;" class="btn btn-success" onclick="editar_recurso('+json.id+')">Guardar Cambios</button>'
        a=a+'<button type="button" class="btn btn-danger" onclick="borrar_recurso('+json.id+')">'
        a=a+'<span class="glyphicon glyphicon-trash" aria-hidden="true"></span>'
        a=a+'</button>'
        a=a+'</div>'
        a=a+'<div class="modal-footer">'
        a=a+'<button type="button" class="btn btn-default" data-dismiss="modal">Cancelar</button>'
        a=a+'</div>'
        a=a+'</div>'
        a=a+'</div>'
        a=a+'</div>'
        a=a+'</div>'
        a=a+'</div>'


        console.log(a)


            
            $('#modalRequerimiento').modal('toggle');
            $( "#requerimientos_lista" ).append( a );
            //$("#modalRequerimiento").removeData("modal");
        },
 
        error : function(xhr,errmsg,err) {

            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

});




function habilitar_edicion(id_form, nombre,descripccion,cantidad) {

     var puede_editar = $('#puede_editar_evento').val();
     $('[name=nombre]').val(nombre);
     $('[name=descripccion]').val(descripccion);
     $('[name=cantidad]').val(cantidad);


    if(puede_editar==="true") {
        //console.log("puede_editar");
        $("#"+id_form+" :input").attr("disabled",false);
    }

}

