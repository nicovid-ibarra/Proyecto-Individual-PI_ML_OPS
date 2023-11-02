from fastapi import FastAPI
import pandas as pd

app = FastAPI()

f1=pd.read_parquet('src/datas/datasf1.parquet')
f2=pd.read_parquet('src/datas/datasf2.parquet')
f3=pd.read_parquet('src/datas/datasf3.parquet')
f4=pd.read_parquet('src/datas/datasf4.parquet')
f5=pd.read_parquet('src/datas/datasf5.parquet')
data_final=pd.read_parquet('src/datas/ml1.parquet')
datb=pd.read_parquet('src/datas/ml2.parquet')


@app.get('/PlayTimeGenre/{genero}', name= 'Año con mas horas jugadas para el genero')
async def PlayTimeGenre(genero):
    año=f1[f1['Género'] == genero]['Año resultado']
    if año.empty:
        return {'mensaje': f'No se encontraron resultados para el género {genero}'}
    else:
        return {'Año con mas hs jugadadas para el genero ':genero,'es: ': año}

@app.get('/UserForGenre/{genero}', name='Usuario con mas hs jugadas para el genero y horas jugadas por año')
def UserForGenre(genero):
    usuario = f2[f2['Género'] == genero]['usuario']
    horas = f2[f2['Género'] == genero]['hs por año']
    
    if usuario.empty or horas.empty:
        return {'mensaje': f'No se encontraron resultados para el género {genero}'}
    else:
        usuario_resultado = usuario.iloc[0]
        horas_resultado = horas.iloc[0]
        return {'Usuario con más horas jugadas para el género': genero, 'es': usuario_resultado, 'habiendo jugado por año': horas_resultado.tolist()}
    

    
@app.get('/UsersRecommend/{year}', name='Top 3 juegos recomendados para el año')   
def UsersRecommend(year:int):
    juego = f3[f3['Año'] == year]['app_name'].tolist()
    score = f3[f3['Año'] == year]['score'].tolist()
    juegos_scores = [{'juego recomendado': juego[i], 'con un score': score[i]} for i in range(len(juego))]
    return juegos_scores

@app.get('/UsersNotRecommend/{year}', name='NoTop 3 juegos recomendados para el año')   
def UsersNotRecommend(year:int):
    juego = f4[f4['Año'] == year]['app_name'].tolist()
    score = f4[f4['Año'] == year]['score'].tolist()
    juegos_scores = [{'juego recomendado': juego[i], 'con un score': score[i]} for i in range(len(juego))]
    return juegos_scores

@app.get('/sentiment_analysis/{year}',name='Cantidad de reseñas positivas, negativas y neutras para dicho año')
async def sentiment_analysis(year: int):
    data = f5[f5['Año'] == year]
    if data.empty:
        return {'mensaje': f'No se encontraron resultados para el año {year}'}
    else:
        positivo = data['Positivos'].values[0]
        negativo = data['Negativos'].values[0]
        neutro = data['Neutros'].values[0]
        return {'Reviews positivas': int(positivo), 'Reviews negativas': int(negativo), 'Reviews Neutras': int(neutro)}


@app.get('/extract_genres_by_item_id/{year}',name='Devuelve 5 juegos similares')
async def extract_genres_by_item_id(item_id):
    #Primero se realiza una serie de filtros para achicar el df
    #Se extrae el o los generos asociados al juego usando datb
    genres = datb[datb['item_id'] == item_id]['genres'].tolist()
    #Se extraen los item_id relacionados con los genereos del juego en cuestion
    related_items1 = datb[datb['genres'].apply(lambda x: any(item in x for item in genres))]['item_id'].unique().tolist()
    #Se extrae el o los specs asociados al juego usando datb
    genres = datb[datb['item_id'] == item_id]['specs'].tolist()
    #Se extraen los item_id relacionados con los specs del juego en cuestion
    related_items2 = datb[datb['specs'].apply(lambda x: any(item in x for item in genres))]['item_id'].unique().tolist()
    #Finalmente se sacan los item_id que aparecen en los 3
    common_items = set(related_items1).intersection(related_items2)

    #Se extrae de data final solo los item_id identificados anteriormente, se toma aquellas filas que son recomendadas 
    #y se eliminan las columnas recommend y review por ser irrelevantes luego del filtro
    filtered_data_final = data_final[data_final['item_id'].isin(common_items)]
    filtered_data_final = filtered_data_final[(filtered_data_final['recommend'] == True) & (filtered_data_final['review'] == 2)]
    filtered_data_final = filtered_data_final.drop(columns=['recommend', 'review'])

    # Ordenar el DataFrame por 'score' en orden descendente
    filtered_data_final.sort_values('score', ascending=False, inplace=True)
    # Obtener los 5 item_id con la puntuación más alta
    top_5_items = filtered_data_final['item_id'].unique()[:5]
    app_names = list(set(datb[datb['item_id'].isin(top_5_items)]['app_name']))
    
    return app_names