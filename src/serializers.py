from rest_framework import serializers
from .models import Category,Book



class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="cat_api-detail",)  