$(function() {
  $('#fecha')
      .datepicker({
          format: 'mm/dd/yyyy',
          startDate: '01/01/2015',
          endDate: '12/30/2030'
      });
 
});


function borrar_evento(id) {
    console.log("delete is working!") // sanity check
    
    $.ajax({
        url : "/editar/"+id,
        type : "DELETE",
        data : {id_evento:id}, 

        success : function() {

            window.location.replace("https://glacial-scrubland-6807.herokuapp.com/perfil");
        },

        error : function(xhr,errmsg,err) {

            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};