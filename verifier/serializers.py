from rest_framework import serializers
from .models import Website


class WebsiteListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Website
        fields = '__all__'
