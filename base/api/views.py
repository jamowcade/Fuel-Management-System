from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Fuel
from .serializers import SerializeFuels


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET',
        'GET/api/fuels',
        'GET/api/fuels/:id'
    ]

    return Response(routes)

@api_view(['GET'])
def getFuels(request):
    fuels = Fuel.objects.all()
    serializer = SerializeFuels(fuels, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getFuel(request, pk):
    fuel = Fuel.objects.get(id=pk)
    serializer = SerializeFuels(fuel, many=False)
    return Response(serializer.data)