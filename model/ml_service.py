# -*- coding: utf-8 -*-
import redis 
import json
import time 
from classifier import SentimentClassifier
########################################################################
# COMPLETAR AQUI: Crear conexion a redis y asignarla a la variable "db".
########################################################################
db = redis.Redis(host='redis', port=6379, db=0)
########################################################################

########################################################################
# COMPLETAR AQUI: Instanciar modelo de análisis de sentimientos.
# Use classifier.SentimentClassifier de la libreria
# spanish_sentiment_analysis ya instalada
########################################################################
model = SentimentClassifier()
########################################################################


def sentiment_from_score(score):
    if score > .55:
        sentiment='Positivo'
    elif score < .45: 
        sentiment='Negativo'
    else:
        sentiment='Neutral'
    return sentiment




def predict(text):
    score = model.predict(text)
    sentiment = sentiment_from_score(score)

    return sentiment, score
    

def classify_process():
    """
    Obtiene trabajos encolados por el cliente desde Redis. Los procesa
    y devuelve resultados.
    Toda la comunicación se realiza a travez de Redis, por ello esta
    función no posee atributos de entrada ni salida.
    """
    # Iteramos intentando obtener trabajos para procesar
    while True:
        ##################################################################
       
        # COMPLETAR AQUI: Obtenga un batch de trabajos encolados, use
        # lrange de Redis. Almacene los trabajos en la variable "queue".
        ##################################################################
        queue = db.lrange("service_queue",0,9) 
        ##################################################################

        # Iteramos por cada trabajo obtenido
        for q in queue:
            ##############################################################
            # COMPLETAR AQUI:
            #     - Utilice nuestra función "predict" para procesar la
            #       sentencia enviada en el trabajo.
            #     - Cree un diccionario con dos entradas: "prediction" y
            #       "score" donde almacenara los resultados obtenidos.
            #     - Utilice la funcion "set" de Redis para enviar la
            #       respuesta. Recuerde usar como "key" el "job_id".
            q=json.loads(q.decode('utf-8'))
            job_id=q['id']
            sentiment, score= predict(q['text'])

            response={'predicition':sentiment, 'score':score}
            db.set(job_id, json.dumps(response))
            ##############################################################

        ##################################################################
        # COMPLETAR AQUI: Use ltrim de Redis para borrar los trabajos ya
        # procesados. Luego duerma durante unos milisengundos antes de
        # pedir por mas trabajos.
        ##################################################################
        db.ltrim('service_queue',len(queue),-1)

        time.sleep=(2)
        ##################################################################


if __name__ == "__main__":
    print('Launching ML service...')
    classify_process()
