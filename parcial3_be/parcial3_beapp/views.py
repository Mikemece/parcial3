from django.http import HttpResponse
from parcial3_beapp.serializers import EventoSerializer, TokenSerializer
import pymongo
import requests
import json

from google.oauth2 import id_token
from google.auth.transport import requests

import cloudinary
import cloudinary.uploader

from datetime import datetime
from dateutil import parser

from bson import ObjectId
from rest_framework.response import Response

from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status

from pymongo import ReturnDocument

from django.shortcuts import render, get_object_or_404


# Conexión a la base de datos MongoDB
my_client = pymongo.MongoClient('mongodb+srv://parcial:parcial@1parcial23.zzs3aop.mongodb.net/')

# Nombre de la base de datos
dbname = my_client['parcial3']

# Colecciones
collection_evento = dbname["evento"]

# ---------------- EL CRUD DE LAS TABLAS ---------------------- 

@api_view(['GET', 'POST'])
def eventos(request):
    if request.method == 'GET':
        evento = list(collection_evento.find({}))        
        for p in evento:
            p['_id'] = str(ObjectId(p.get('_id',[])))

        evento_serializer = EventoSerializer(data=evento, many= True)
        if evento_serializer.is_valid():
            json_data = evento_serializer.data
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(evento_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    elif request.method == 'POST':
        serializer = EventoSerializer(data=request.data)
        if serializer.is_valid():
            evento = serializer.validated_data
            evento['_id'] = ObjectId()
            result = collection_evento.insert_one(evento)
            if result.acknowledged:
                return Response({"message": "Evento creado con éxito."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Algo salió mal. Evento no creado."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT', 'DELETE'])
def evento(request, idp):
    if request.method == 'PUT':
        serializer = EventoSerializer(data=request.data)
        if serializer.is_valid():
            evento = serializer.validated_data
            evento['_id'] = ObjectId(idp)
            result = collection_evento.replace_one({'_id': ObjectId(idp)}, evento)
            if result.acknowledged:
                return Response({"message": "Evento actualizado con éxito",},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": "Algo salió mal. Evento no actualizado."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    elif request.method == 'GET':
            p = collection_evento.find_one({'_id': ObjectId(idp)})
            p['_id'] = str(ObjectId(p.get('_id', [])))

            serializer = EventoSerializer(data=p)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    elif request.method == 'DELETE' :
        delete_data = collection_evento.delete_one({'_id': ObjectId(idp)})
        if delete_data.deleted_count == 1:
            return Response({"mensaje": "Evento eliminado con éxito"}, status=status.HTTP_200_OK)
        else:
            return Response({"ERROR": "Evento no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['GET'])
def eventoPostal(request, postal):
    if request.method =='GET':
        evento = collection_evento.find_one({'lugar':postal })        
        evento['_id'] = str(ObjectId(evento.get('_id',[])))

        evento_serializer = EventoSerializer(data=evento)
        if evento_serializer.is_valid():
            json_data = evento_serializer.data
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(evento_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ---------------- IMÁGENES ----------------------
        
@api_view(['POST'])
def upload_image(request):
    if request.method == 'POST' and request.FILES.getlist('images'):
        uploaded_files = request.FILES.getlist('images')
        uploaded_urls = []

        # Upload each image to Cloudinary
        cloudinary.config(
                cloud_name="dsr356a9z",
                api_key="216828456522265",
                api_secret="OWVoBppOphupt67TZSHyDHogmQ4"
            )

        for file in uploaded_files:
            upload_result = cloudinary.uploader.upload(
                file,
                folder='examen'
            )
            uploaded_urls.append(upload_result['secure_url'])
        return JsonResponse({'urls': uploaded_urls})
    return HttpResponse(status=400)


# ---------------- TOKEN OAUTH ----------------------

CLIENT_ID = '97897189905-91u0q02ni37ctgtgege5uidl9cefa6gt.apps.googleusercontent.com'

@api_view(['POST'])
def oauth(request):
    if request.method == 'POST':
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            tokenData = serializer.validated_data
            try:
                token = tokenData['idtoken']
                idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
                userid = idinfo['sub']
                if userid:
                    return Response({"userid": userid,},
                                    status=status.HTTP_200_OK)
            except ValueError:
                # Invalid token
                
                return Response({"error": "Token no valido: "+token,},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)