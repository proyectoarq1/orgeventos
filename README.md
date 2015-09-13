
## Requisitos

+ MySQL o MongoDB local
+ Si la opccion es MySQL, crear base de datos 'prueba' con usurio root y password root
+ Python 2.7.10
+ pip 
+ git

## Pasos

+ Clonar el proyecto mediante git (o bien descargar el código de la aplicación)  


```
git clone https://github.com/proyectoarq1/orgeventos.git
```

+ Posicionarse en la carpeta raiz del proyecto

```
cd orgeventos/
```

+ Instalar dependencias del proyecto

```
pip install requirements.txt
```

+ Seleccionar MySQL o MongoDB: Exportar la variable de entorno 'TIPO_BASE_DE_DATOS' desde la consola con el valor 'MySQL' o bien 'MongoDB' (Por default si la variable no existe la base de datos utilizada sera MySQL) 

```
export TIPO_BASE_DE_DATOS='MongoDB'
```

+Si la base elegida es MySQL, crear el esquema en la base de datos

```
python db/models.py
```

+ Levantar la aplicación

```
python routes.py
```

##Link a app en heroku:

https://glacial-scrubland-6807.herokuapp.com/