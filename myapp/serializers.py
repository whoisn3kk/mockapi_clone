import io
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import *

# class EndpointModel:
#     def __init__(self, key, value) -> None:
#         self.key = key
#         self.value = value



class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = ['user', 'key', 'value']

class EndpointCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = ['key', 'value']


class EndpointValueUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = ['value']

# def encode():
#     model = EndpointModel("sneakers", {"test": 1})
#     model_sr = EndpointSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep="\n")
#     json = JSONRenderer().render(model_sr.data)
#     print(json)

# def decode():
#     stream = io.BytesIO(b'{"key":"sneakers","value":{"test":1}}')
#     data = JSONParser().parse(stream)
#     serializer = EndpointSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)