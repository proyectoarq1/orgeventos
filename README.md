
## Requisitos

+ Base de datos MySQL
+ Python 2.7.10
+ pip 
+ git

## Pasos

+ Clonar el proyecto mediante git (o bien descargar el código de la aplicación)  


```
git clone https://github.com/proyectoarq1/orgeventos.git
```

+ Posicionarse en la carpeta raiz del proyecto
+ Instalar dependencias del proyecto

```
pip install requirements.txt
```

+ Crear el esquema en la base de datos

```
python db/models.py
```

+ Levantar la aplicación

```
python routes.py
```

##Link a app en heroku:

https://glacial-scrubland-6807.herokuapp.com/