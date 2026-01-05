from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):

      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
      data = request.data

      # Validación mínima
      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)

class DemoRestApiItem(APIView):
      """Operaciones sobre un item identificado por su `id`.

      - PUT: Reemplaza completamente el recurso (el cuerpo debe incluir `id` igual al id de la URL).
      - PATCH: Actualiza parcialmente los campos del recurso (no permite cambiar `id`).
      - DELETE: Eliminación lógica (marca `is_active` = False).
      """

      def get_item_index(self, item_id):
        for idx, item in enumerate(data_list):
          if item.get('id') == item_id:
            return idx
        return None

      def put(self, request, id):
        body = request.data

        if 'id' not in body:
          return Response({'error': 'El campo "id" es obligatorio en el cuerpo.'}, status=status.HTTP_400_BAD_REQUEST)

        if str(body.get('id')) != str(id):
          return Response({'error': 'El id del cuerpo debe coincidir con el id de la URL.'}, status=status.HTTP_400_BAD_REQUEST)

        idx = self.get_item_index(id)
        if idx is None:
          return Response({'error': 'Recurso no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Construir nuevo item manteniendo el id
        new_item = {'id': str(id)}
        # Copiar campos del body excepto id
        for k, v in body.items():
          if k == 'id':
            continue
          new_item[k] = v

        # Si no se proporciona is_active, mantener True por defecto
        if 'is_active' not in new_item:
          new_item['is_active'] = True

        data_list[idx] = new_item
        return Response({'message': 'Recurso reemplazado exitosamente.', 'data': new_item}, status=status.HTTP_200_OK)

      def patch(self, request, id):
        body = request.data

        if 'id' in body and str(body.get('id')) != str(id):
          return Response({'error': 'No se permite cambiar el id del recurso.'}, status=status.HTTP_400_BAD_REQUEST)

        idx = self.get_item_index(id)
        if idx is None:
          return Response({'error': 'Recurso no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        item = data_list[idx]
        # Actualizar solo los campos provistos (excepto id)
        for k, v in body.items():
          if k == 'id':
            continue
          item[k] = v

        data_list[idx] = item
        return Response({'message': 'Recurso actualizado exitosamente.', 'data': item}, status=status.HTTP_200_OK)

      def delete(self, request, id):
        idx = self.get_item_index(id)
        if idx is None:
          return Response({'error': 'Recurso no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        item = data_list[idx]
        # Eliminación lógica
        item['is_active'] = False
        data_list[idx] = item
        return Response({'message': 'Recurso eliminado lógicamente.'}, status=status.HTTP_200_OK)

    