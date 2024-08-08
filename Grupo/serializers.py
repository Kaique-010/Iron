
from rest_framework import serializers
from Grupo.models import Grupo


class GruposSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grupo
        fields = '__all__'
