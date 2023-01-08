from rest_framework.serializers import ModelSerializer
from base.models import Fuel


class SerializeFuels(ModelSerializer):
    class Meta:
        model = Fuel
        fields = '__all__'