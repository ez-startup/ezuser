from rest_framework import serializers
from .models import *

class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        models = License
        fields = "__all__"

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        models = Device
        fields = "__all__"
        
        