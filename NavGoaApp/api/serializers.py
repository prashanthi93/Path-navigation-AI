from rest_framework import serializers
from backend import models
class pathSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Paths
        fields = "__all__"