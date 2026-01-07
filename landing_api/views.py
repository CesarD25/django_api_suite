from django.shortcuts import render

# DRF imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Firebase Admin SDK (Realtime Database) import
from firebase_admin import db

# Standard library
from datetime import datetime


# Create your views here.


class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "votes"

    # Placeholder methods for future CRUD operations can be added here.

    def get(self, request):
        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}')

        # get: Obtiene todos los elementos de la colección
        data = ref.get()

        # Devuelve un arreglo JSON
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):

      data = request.data

      # Referencia a la colección
      ref = db.reference(f'{self.collection_name}')

      current_time  = datetime.now()
      custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
      data.update({"timestamp": custom_format })

      # push: Guarda el objeto en la colección
      new_resource = ref.push(data)

      # Devuelve el id del objeto guardado
      return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)
