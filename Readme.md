<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p> 

# <h1 align=center> **Proyecto Individual MLOps** </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>
<p align="center">
<img src="./_src/images/img_1.png"  height=400>
</p>

# **Introducción**

En este proyecto, nuestro objetivo es llevar a cabo una serie de transformaciones con el fin de obtener información útil y desarrollar un modelo capaz de recomendar juegos similares a los seleccionados. Para lograr esto, llevaremos a cabo los procesos necesarios a lo largo del ciclo de vida de los datos, que incluyen la carga, el procesamiento y la selección de componentes o variables que se utilizarán en nuestro modelo de Machine Learning. Es importante destacar que el proyecto se llevó a cabo en un lapso de tres semanas y, por tanto, aunque se pueden realizar mejoras, nos enfocaremos en ofrecer un Producto Mínimo Viable que se entregará para su implementación.

Asumiendo el rol de un Data Scientist contratado por Steam, nos enfocaremos en crear un modelo de Machine Learning para abordar un problema de negocio específico: desarrollar un sistema de recomendación de videojuegos para usuarios, capaz de ofrecer sugerencias de juegos similares. Al iniciar el proyecto, observamos que la calidad de los datos no es óptima, ya que algunos están sin procesar y anidados, y además no contamos con un proceso automatizado para su identificación, lo que nos obligará a realizar una serie de transformaciones para obtener la información necesaria.

# **Objetivos**

Nuestros principales objetivos son la creación de una API (Interfaces de Programación de Aplicaciones) con un conjunto de funciones para su implementación, el despliegue de dicha API para su uso y la creación de un modelo de recomendación de juegos mediante Machine Learning.


### A continuación, enumeraremos de manera breve una serie de tareas relacionadas a las distintas Partes del trabajo que se puede ver en EDA.ipynb:

Aca el EDA,ETL y Funciones: [ETL](https://github.com/nicovid-ibarra/Proyecto-Individual-PI_ML_OPS/blob/master/EDA.ipynb)


## Parte 1: proceso de Análisis Exploratorio de Datos (EDA)


+ **Carga:** Como primer paso se cargan los datasets provistos como .json. Como resultado tenemos 3 dataframes, uno de reviews con las opiniones de los usuarios, otro con los juegos y sus características y por ultimo items que se compone por los usuarios de steam.

+ **Analisis:** Se observan las columnas de los dataframes, cantidad de datos, nulos (por ejemplo en el dataframe de juegos habia muchisimos nulos, mas de la mitad), duplicados, columnas anidadas(**'items'**,**'reviews'**,**'genres'**).

## Parte 2: proceso de extraccion, transformacion y carga (ETL)

+ **Eliminar valores nulos:**

  1- Se elimina valores nulos de las distintas columnas, examinando los dataframes resultantes y cantidad de datos
  
  2- Se reemplaza los valores vacios por Nan en casos puntuales como en **'funny'** o **'last_edited'**

  
+ **Eliminar los duplicados:**

  Se eliminan los duplicados de todas las columnas.

+ **Creación de la columna de analisis de sentimiento, reemplazando a la actual reviews:**

  Se ha creado una función llamada 'classify_sentiment' que clasifica una reseña con el valor 2 si es positiva, 1 si es neutra y 0 si es negativa. Este valor sustituye el texto en la columna de reseñas.

+ **Descarte de columnas no utilizadas:**

  Eliminaremos las columnas que no utilizaremos

+ **Desanidar datos:**

  Se desanida 'review' e 'items' y se incorpora las nuevas columnas al dataframe original

+ **Resetear indices:**

  Luego de las transformaciones se resetean los indices para facilitar el manejo de datos


## Parte 3: Tratamiento de outliers

+ **Histograma y boxplot**

 Para evitar sesgos en los analisis y debido a la importancia de la columna 'playtime_forever' se elimina los outliers, luego de graficar.

## Parte 4: Funciones

En esta etapa del proyecto, se propone montar y desplegar una API que responda a las peticiones del usuario disponibilizando la data de la empresa mediante el uso
del Framework FastAPI.

Para ello, como primer paso se construyen los dataframes necesarios y luego se monta la funcion, la cual se alimenta de ellos. 
En ciertos casos se vuelven a eliminar duplicados debido al merge, se realizan funciones auxiliares para obtener el año, etc.

Se han definido 5 funciones para los endpoints que serán consumidos en la API:

### A continuación, se detallan las funciones y las consultas que pueden realizarse a través de la API:

1. def **PlayTimeGenre( *`genero`* )**:
   + Esta función recibe como parámetro un genero y devuelve el año con mas horas jugadas para dicho género.
  

 2. def **UserForGenre( *`genero`* )**:
   + Se ingresa un genero. el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.


 3. def **UsersRecommend( *`año`* )**:
   + Se ingresa el año, retornando el top 3 de juegos MÁS recomendados por usuarios para el año dado.

 4. def **UsersNotRecommend( *`año`*)**:
   + Se ingresa el año, retornando el top 3 de juegos MENOS recomendados por usuarios para el año dado.

 5. def **sentiment_analysis( *`año`: str* )**:
   Se ingresa el año de posteo de reviews, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.

 

## Parte 5 Crear parquets y armar el main.py

Para evitar el uso de memoria en render, la cual es limitada en la version gratuita, procedo a armar dataframes con los posibles resultados de las 5 funciones y los exporto como parquets.

Luego se arma el archivo main.py con las funciones y los parquets, el cual alimenta a la Api Fastapi y se comprueba su funcionamiento. Se utiliza el decorador @app.get("/")

Luego de esto se procede a subir los archivos al repositorio y a hacer el deploy en render

Aca el archivo main.py: [main](https://github.com/nicovid-ibarra/Proyecto-Individual-PI_ML_OPS/blob/master/main.py)

## Parte 6: Modelo de Machine Learning

En esta ultima seccion, el objetivo es realizar un modelo de machine learning que al ingresar un item_id, nos devuelva 5 juegos recomendados similares al ingresado. En la teoria nos aconsejaron usar similitud del coseno, el cual mide la distancia entre vectores para ver su similitud. Aca tuve problemas para entender el uso de dicha funcion y con el deploy, por lo que opte por hacer un sistema de recomendacion en el cual fui filtrando progresivamente por genero, publisher y specs, para finalmente generar una columna de scores y tomar los 5 mejor posicionados.

# **Archivos de interés y fuentes:**

+ [Deployment](https://steam-deploy-ot9e.onrender.com/docs): El proyecto ha sido desplegado en un entorno en línea utilizando **Render**.

+ [Dataset original](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj)

+ [Diccionario de datos](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj): Diccionario con algunas descripciones de las columnas disponibles en el dataset.

+ [Video explicativo](https://www.youtube.com/watch?v=6X3lFgMQs54) Un video propio explicando algunos conceptos sobre el proyecto.

+ [Linkedin](https://www.linkedin.com/in/nicovid-ibarra/) Perfil oficial de Linkedin


Autor: Nicolás Agustín Ibarra
