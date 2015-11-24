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