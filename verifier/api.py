from rest_framework import generics
from .models import Website
from .serializers import WebsiteListSerializer


class WebsiteList(generics.ListAPIView):

    model = Website
    serializer_class = WebsiteListSerializer
    queryset = Website.objects.all()
