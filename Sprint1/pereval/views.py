from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework import generics, viewsets, mixins
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from .serializers import *
from .models import *


class PerevalViewSet(viewsets.ModelViewSet):
    """Класс работы с БД """
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImagesSerializer


class PerevalList(ListAPIView):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer


class AuthEmailPerevalAPI(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Класс работы с БД для второго спринта: вывод всех записей по email"""
    queryset = Pereval.objects.all()
    serializer_class = AuthEmailPerevalSerializer


# отправка информации POST

@api_view(['POST'])
# декоратор, который принимает список HTTP-методов, на которые должно реагировать ваше представление
def submit_data(request):
    serializer = PerevalSerializer(data=request.image)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# извлечение информации GET

@api_view(['GET'])
# декоратор, который принимает список HTTP-методов, на которые должно реагировать ваше представление
def get_data(request, pk):
    try:
        pereval = Pereval.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(status=404)

    serializer = PerevalSerializer(pereval)
    return Response(serializer.data)


def get_email(self, request, *args, **kwargs):
    email = kwargs.get('email', None)
    if Pereval.objects.filter(user__email=email).is_exist == True:
        responseData = AuthEmailPerevalSerializer(Pereval.objects.filter(user__email=email), many=True).data

    else:
        responseData = {'message': f'Нет записей от email = {email}'}

    return Response(responseData, status=200)


# изменение информации

@api_view(['PATCH'])
def update_data(request, pk):
    try:
        pereval = Pereval.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response({'state': 0, 'message': 'Перевал не существует'}, status=status.HTTP_404_NOT_FOUND)

    if pereval.status != 'new':
        return Response({'state': 0, 'message': 'Статус перевала не является "новым"'},
                        status=status.HTTP_400_BAD_REQUEST)

    serializer = PerevalSerializer(pereval, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'state': 1}, status=status.HTTP_200_OK)
    return Response({'state': 0, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
