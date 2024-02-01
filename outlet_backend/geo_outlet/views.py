from rest_framework import serializers, generics
from .models import Outlet

class OutletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outlet
        fields = '__all__'

class OutletList(generics.ListAPIView):
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer

