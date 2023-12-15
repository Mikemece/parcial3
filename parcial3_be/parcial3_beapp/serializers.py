from rest_framework import serializers

class EventoSerializer(serializers.Serializer):

    _id = serializers.CharField(max_length = 24, required=False)
    nombre = serializers.CharField(max_length = 20)
    timestam = serializers.DateTimeField(required=False)
    lugar = serializers.CharField(max_length = 7)
    lat = serializers.FloatField()
    long = serializers.FloatField()
    organizador = serializers.CharField()
    imagen = serializers.CharField()

class TokenSerializer(serializers.Serializer):
    idtoken = serializers.CharField()