$(function() {

    if (asistencia_actual == "2"){ //"2" value del enum Asisto
        $("#requerimientos_lista").show();
    }else{
        $("#requerimientos_lista").hide();
    }

});
function borrar_evento(id) {
    console.log("delete is working!") // sanity check
    
    $.ajax({
        url : "/editar/"+id,
        type : "DELETE",
        data : {id_evento:id}, 

        success : function() {

            window.location.replace("http://localhost:5000/perfil");
        },

        error : function(xhr,errmsg,err) {

            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

function invitar(evento_id){
    var opcionSeleccionada_id = $( "#invitado option:selected" ).val();
    var opcionSeleccionada_text = $( "#invitado option:selected" ).text();
    $.ajax({
        url : "/evento/"+evento_id,
        type : "POST",
        data : { invitado : opcionSeleccionada_id},

    success : function(json) {
        //$('#respuesta').hide(); 
        console.log(opcionSeleccionada_text);
        var nueva_invitacion = '<h5 id="' + opcionSeleccionada_text + '" style="margin-left:7em;">' + opcionSeleccionada_text + ' - Pendiente </h5>'
        $( "#usuarios_invitados").append( nueva_invitacion );
        $("#invitado option[value='"+opcionSeleccionada_id+"']").remove();
        console.log("success");
      },

    error : function(xhr,errmsg,err) {
        //$('#results').html("<div class='alert-box alert radius' data-alert>Oops! error: "+errmsg+
        //    " <a href='#' class='close'>&times;</a></div>");
        console.log("error");
     //       console.log(xhr.status + ": " + xhr.responseText);
      }
    });
}

function contestando_asistencia_a_evento(evento_id) {
    var opcionSeleccionada = $('#asistir').val()
    if (opcionSeleccionada !="0"){ 
        $.ajax({
            url : "/evento_asistencia",
            type : "POST",
            data : { id_evento: evento_id, asistir : opcionSeleccionada},

        success : function(json) {
            console.log(json);
            console.log(json.asistencia_actual);
            if (json['asistencia_actual'] == "Asisto"){
                $("#requerimientos_lista").show();
            }else{
                $("#requerimientos_lista").hide();
            }
            var estado_asistencia = '<h5 id="' + json.usuario + '" style="margin-left:7em;">' + json.usuario + ' - ' + json.asistencia_actual + '</h5>'
            $( "#"+json.usuario ).replaceWith( estado_asistencia );

            console.log("success");
          },

        error : function(xhr,errmsg,err) {
            console.log("error");
          }
        });
    }
};