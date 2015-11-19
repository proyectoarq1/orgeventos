$(function() {

//$('#form-asistir').on('submit', function(event){
//    event.preventDefault();
//    contestando_asistencia();
//});

//$('#asistir').on('change', function(){
//    if(this.value != "0"){
//        contestando_asistencia();
//    }
//});

//$("#asistir1").val(eventos_invitados_y_asistencia[1].evento.id+","+eventos_invitados_y_asistencia[1].asistencia.value);


});
function contestando_asistencia(evento_id) {
    var opcionSeleccionada = $('#asistir'+evento_id).val()
    if (opcionSeleccionada !="0"){ 
        $.ajax({
            url : "perfil",
            type : "POST",
            data : { asistir : opcionSeleccionada},

        success : function(json) {
            $('#respuesta').hide(); 
            console.log(json);
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
};