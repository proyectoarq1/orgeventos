function otros_12_eventos(ultimo_id, tipo, pre_post) {

    $.ajax({
        url : "/dealer_eventos",
        type : "POST",
        data : {"pivote_id":ultimo_id,"tipo":tipo,"pre_post":pre_post}, 

        success : function(json) {

            //{"eventos":eventos_publicos,"ultimo_id":ultimo_id, "primer_id":primer_id}

            if (json.hay_eventos==="true"){
                eventos = json.eventos
                a = ""
                $('#lista_publicos_eventos').replaceWith( '<div id="lista_publicos_eventos"></div>' );

                var tamanio = eventos.length;
                for (var i = 0; i < tamanio; i++) {
                    var e = eventos[i]

                    if (e.url_imagen !== "")
                        { var url_imagen = e.url_imagen }
                    else
                    { var url_imagen = "http://www.edsaugustablog.com/wp-content/uploads/2015/02/fiesta1.jpg" }

                    a = ''
                    a = a + '<div class="col-md-4" style=" margin-top:5px;">'
                    a = a + '<div class="row">'
                    a = a + '<div>'
                    a = a + '<img style="margin-left:25px; margin-top:5px;width:100px;height:100px;" align="left" class="img-circle"src="'+url_imagen+'"/>'
                    a = a + '</div>'
                    a = a + '<p style="margin-top:25px;font-size:20px" align="left">'
                    a = a + '<a href="/evento/'+e._id+'"> '+e.nombre+'</a>'
                    a = a + '</p>'
                    a = a + '</div>'
                    a = a + '</div>'

                    $('#lista_publicos_eventos' ).append( a );
                }
            }


            else{ $('#lista_publicos_eventos').replaceWith( '<div id="lista_publicos_eventos"><h3>No hay eventos que mostrar</h3></div>' ); }
            a = ''
            a = a + '<div id="navegador_eventos">'
            a = a + '<nav style=" margin-top:5px;">'
            a = a + '<ul class="pager">'
            a = a + '<li class="previous"><a onclick="otros_12_eventos('+json.primer_id+',&#39;publico&#39;,&#39;pre&#39;)"><span aria-hidden="true">&larr;</span> Anterior pagina</a></li>'
            a = a + '<li class="next"><a onclick="otros_12_eventos('+json.ultimo_id+',&#39;publico&#39;,&#39;post&#39;)">Proxima pagina <span aria-hidden="true">&rarr;</span></a></li>'
            a = a + '</ul>'
            a = a + '</nav>'
            a = a + '</div>'
            $('#navegador_eventos').replaceWith(a);
            

        },

        error : function(xhr,errmsg,err) {

            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); 
            console.log(xhr.status + ": " + xhr.responseText); 
        }
    });
};


