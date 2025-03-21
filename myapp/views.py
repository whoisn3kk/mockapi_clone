from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from myapp.serializers import *
from .models import *

# Create your views here.

class NewEndpointLCApiView(generics.ListCreateAPIView):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointCreateUpdateSerializer

    def get_queryset(self):
        queryset = Endpoint.objects.filter(user__uuid=self.kwargs.get("uuid"))
        return queryset

    def create(self, request, *args, **kwargs):
        user = kwargs.get("uuid")
        user = Users.objects.filter(uuid=user).first()
        if not user:
            return Response({"error": "User matching query does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        dct = {
            "key": request.data.get("key"),
            "value": request.data.get("value"),
            "user": user.id
        }

        try:
            dct["value"] = json.loads(dct["value"])
        except:
            return Response({"error": "Provided data is not valid json"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EndpointSerializer(data=dct)
        serializer.is_valid()
        if Endpoint.objects.filter(key=serializer.data.get("key")):
            return Response({"error": "This key already exists. Use PUT(PATCH) to modify it."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.create(serializer.validated_data)
        serializer = EndpointCreateUpdateSerializer(data=dct)
        serializer.is_valid()

        return Response(serializer.data)

class NewEndpointRUDApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointValueUpdateSerializer
    lookup_field = "key"

    def get(self, request, *args, **kwargs):
        ep = Endpoint.objects.filter(key=kwargs.get("key")).first()
        if not ep:
            return Response({"error": "Endpoint matching query does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(ep.value)
    
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        ep = Endpoint.objects.filter(key=kwargs.get("key")).first()
        return Response(ep.value)

class UserView(APIView):
    @swagger_auto_schema(
        operation_description="Get list of all endpoints for a user",
        responses={200: EndpointSerializer(many=True)} 
    )
    def get(self, request):
        return Response({"users": list(Users.objects.all().values())})


class EndpointDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointValueUpdateSerializer
    lookup_field = 'key'

    def get_object(self):
        user_uuid = self.kwargs['uuid']
        endpoint_key = self.kwargs['endpoint']
        user = get_object_or_404(Users, uuid=user_uuid)
        return get_object_or_404(Endpoint, user=user, key=endpoint_key)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('uuid', openapi.IN_PATH,
                              description="User UUID", type=openapi.TYPE_STRING),
            openapi.Parameter('endpoint', openapi.IN_PATH,
                              description="Endpoint string", type=openapi.TYPE_STRING)
        ],
        operation_description="Get details of a specific endpoint",
        responses={200: EndpointCreateUpdateSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update the value of a specific endpoint",
        request_body=EndpointValueUpdateSerializer,
        responses={
            200: openapi.Response(
                description="A JSON object containing the value of the endpoint",
                examples={
                    "application/json": {
                        "value": [
                            {"key1": "value1"},
                            {"key2": "value2"}
                        ]
                    }
                },
                schema=EndpointValueUpdateSerializer
            )
        }
    )
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific endpoint",
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)




class EndpointView(generics.ListCreateAPIView):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointCreateUpdateSerializer

    def get_object(self):
        user_uuid = self.kwargs['uuid']
        user = get_object_or_404(Users, uuid=user_uuid)
        return get_object_or_404(Endpoint, user=user)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('uuid', openapi.IN_PATH,
                              description="User UUID", type=openapi.TYPE_STRING),
        ],
        operation_description="Get list of all endpoints for a user",
        responses={200: EndpointSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_description="Create a new endpoint",
        request_body=EndpointCreateUpdateSerializer,
        responses={201: EndpointSerializer}
    )
    def create(self, request, *args, **kwargs):
        user_uuid = self.kwargs['uuid']
        user = get_object_or_404(Users, uuid=user_uuid)
        request.data["user"] = user.id

        if Endpoint.objects.filter(user=user, key=request.data["key"]).exists():
            return Response({"error": f"Endpoint {request.data['key']} already exists. Use PUT method to modify it."}, status=400)

        return super().create(request, *args, **kwargs)